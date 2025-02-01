websocket_client_store = {}


def set(session_id, websocket_data):
    websocket_client_store[session_id] = websocket_data


def get(session_id):
    return websocket_client_store.get(session_id)


def delete(session_id):
    del websocket_client_store[session_id]
