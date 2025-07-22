# app/sockets/document_socket.py
from flask_socketio import SocketIO, join_room, emit
from ..models.document import Document
from ..models.version import Version
from ..models import db
import logging
from flask_socketio import emit
from flask_login import current_user

logger = logging.getLogger(__name__)

def init_sockets(socketio: SocketIO):
    @socketio.on('join')
    def on_join(data):
        doc_id = data['doc_id']
        join_room(str(doc_id))
        logger.info(f"User joined document room: {doc_id}")

    @socketio.on('edit')
    def on_edit(data):
        doc_id = data['doc_id']
        content = data['content']
        document = Document.query.get(doc_id)
        if document and content != document.content:
            version = Version(document_id=doc_id, content=document.content)
            db.session.add(version)
            document.content = content
            try:
                db.session.commit()
                logger.info(f"Saved WebSocket edit and version for document ID {doc_id}")
                emit('update', {'content': content}, room=str(doc_id))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to save WebSocket edit for document ID {doc_id}: {e}")
        else:
            logger.warning(f"Document ID {doc_id} not found or no content change")


def register_socket_handlers(socketio):
    @socketio.on('connect')
    def handle_connect():
        if current_user.is_authenticated:
            emit('connection_status', {'status': 'connected', 'user': current_user.username})
        else:
            emit('connection_status', {'status': 'anonymous'})

    @socketio.on('edit_document')
    def handle_edit(data):
        document_id = data.get('document_id')
        content = data.get('content')
        emit('document_update', {'document_id': document_id, 'content': content}, broadcast=True)

    @socketio.on('disconnect')
    def handle_disconnect():
        emit('connection_status', {'status': 'disconnected', 'user': current_user.username if current_user.is_authenticated else 'anonymous'})