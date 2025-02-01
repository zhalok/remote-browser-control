sessionsStore = {}


def add(session_id, playwright, browser, page):
    sessionsStore[session_id] = {
        "playwright": playwright,
        "browser": browser,
        "page": page,
    }


def get(session_id):
    return sessionsStore.get(session_id)


def remove(session_id):
    del sessionsStore[session_id]
