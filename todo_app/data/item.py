class Item: 
    def __init__(self, id, name,list, dateLastActivity = None,due = None): 
        self.id = id 
        self.name = name
        self.list = list
        self.dayLastActivity = dateLastActivity
        self.due = due
        
            
        
    @classmethod 
    def from_trello_card(cls, card,list): 
        return cls(card['id'], card['name'],list['name'], card['dateLastActivity'],card['due'] ) 