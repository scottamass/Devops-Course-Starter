from todo_app.data.trello_items import get_trello_items

def tasks (req):
    items = get_trello_items()
    c=0
    for Item in items:
        if Item.listID == req:
            c= c+1
    return c        