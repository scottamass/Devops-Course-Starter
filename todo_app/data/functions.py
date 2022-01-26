from todo_app.data.session_items import get_items

def tasks (req):
    items = get_items()
    c=0
    for item in items:
        if item['status'] == req:
            c= c+1
    return c        