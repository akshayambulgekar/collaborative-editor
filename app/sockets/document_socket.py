# app/sockets/document_socket.py
from flask_socketio import SocketIO, join_room, emit
from ..models.document import Document
from ..models.version import Version
from ..models import db
import logging

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