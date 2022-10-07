from datetime import datetime

class Item: 
    def __init__(self, id, name,list, dateLastActivity = datetime.today(),due = None): 
        self.id = id 
        self.name = name
        self.list = list
        self.dateLastActivity = dateLastActivity
        
        self.due = due
       
            
        
    @classmethod 
    def from_trello_card(cls, card): 
        return cls(card['_id'], card['name'],card['status'],card['dateLastActivity'], card['due'] ) 