from app.models import db

def resolve_conflict(document, new_content, user_id):
    # Save new version before updating
    version = Version(document_id=document.id, content=new_content)
    db.session.add(version)
    document.content = new_content
    db.session.commit()
    return document