class Item: 
    def __init__(self, id, name,list, dateLastActivity = None,due = None): 
        self.id = id 
        self.name = name
        self.list = list
        self.dayLastActivity = dateLastActivity
        if due == None:
            self.due = due
        else:
            self.due= due[8:10]+"-"+due[5:7]+"-"+due[0:4]    
        
            
        
    @classmethod 
    def from_trello_card(cls, card,list): 
        return cls(card['id'], card['name'],list['name'], card['dateLastActivity'],card['due'] ) 