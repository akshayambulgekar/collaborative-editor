# app/routes/document.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from ..models.document import Document
from ..models.version import Version
from ..models import db
from ..services.ai_suggestions import get_grammar_suggestions
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

doc_bp = Blueprint('doc', __name__)

class DocumentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Create Document')

class EditorForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save')

class RestoreForm(FlaskForm):
    submit = SubmitField('Restore')

@doc_bp.route('/documents')
@login_required
def documents():
    user_documents = Document.query.filter_by(owner_id=current_user.id).all()
    form = DocumentForm()
    return render_template('documents.html', documents=user_documents, form=form)

@doc_bp.route('/create_document', methods=['POST'])
@login_required
def create_document():
    form = DocumentForm()
    if form.validate_on_submit():
        title = form.title.data
        document = Document(title=title, content='', owner_id=current_user.id)
        db.session.add(document)
        db.session.commit()
        logger.info(f"Created document with ID {document.id} for user {current_user.id}")
        return redirect(url_for('doc.editor', doc_id=document.id))
    flash('Invalid title.')
    return redirect(url_for('doc.documents'))

@doc_bp.route('/editor/<int:doc_id>', methods=['GET', 'POST'])
@login_required
def editor(doc_id):
    document = Document.query.get_or_404(doc_id)
    if document.owner_id != current_user.id:
        flash('You do not have permission to edit this document.')
        return redirect(url_for('doc.documents'))
    form = EditorForm()
    if form.validate_on_submit():
        content = form.content.data
        if content != document.content:
            version = Version(document_id=doc_id, content=document.content)
            db.session.add(version)
            document.content = content
            try:
                db.session.commit()
                logger.info(f"Saved content and version for document ID {doc_id}")
                flash('Document saved successfully.')
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to save content for document ID {doc_id}: {e}")
                flash('Error saving document. Please try again.')
        return redirect(url_for('doc.editor', doc_id=doc_id))
    form.content.data = document.content
    return render_template('editor.html', document=document, form=form)

@doc_bp.route('/versions/<int:doc_id>')
@login_required
def versions(doc_id):
    document = Document.query.get_or_404(doc_id)
    if document.owner_id != current_user.id:
        flash('You do not have permission to view this document.')
        return redirect(url_for('doc.documents'))
    versions = Version.query.filter_by(document_id=doc_id).order_by(Version.timestamp.desc()).all()
    form = RestoreForm()
    return render_template('versions.html', document=document, versions=versions, form=form)

@doc_bp.route('/restore_version/<int:doc_id>/<int:version_id>', methods=['POST'])
@login_required
def restore_version(doc_id, version_id):
    document = Document.query.get_or_404(doc_id)
    if document.owner_id != current_user.id:
        flash('You do not have permission to modify this document.')
        return redirect(url_for('doc.documents'))
    form = RestoreForm()
    if form.validate_on_submit():
        version = Version.query.get_or_404(version_id)
        if version.document_id == doc_id:
            version_new = Version(document_id=doc_id, content=document.content)
            db.session.add(version_new)
            document.content = version.content
            try:
                db.session.commit()
                flash('Version restored successfully.')
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to restore version for document ID {doc_id}: {e}")
                flash('Error restoring version. Please try again.')
        else:
            flash('Invalid version for this document.')
    return redirect(url_for('doc.editor', doc_id=doc_id))

@doc_bp.route('/api/suggestions', methods=['POST'])
@login_required
def suggestions():
    text = request.json.get('text')
    if text:
        suggestions = get_grammar_suggestions(text)
        return {'suggestions': suggestions}
    return {'suggestions': []}
