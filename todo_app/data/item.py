class Item: 
    def __init__(self, id, name,list, dateLastActivity = None,due = None): 
        self.id = id 
        self.name = name
        self.list = list
        self.yearLastActivity = dateLastActivity and dateLastActivity[0:4]
        self.monthLastActivity = dateLastActivity and dateLastActivity[5:7]
        self.dayLastActivity = dateLastActivity and dateLastActivity[8:10]
        self.timeLastActivity = dateLastActivity and dateLastActivity[11:16]
        if due != None:
            self.due= due[8:10]+'-'+due[5:7]+'-'+due[0:4]
            
        if due == None:    
            self.due = due
            
        
    @classmethod 
    def from_trello_card(cls, card,list): 
        return cls(card['id'], card['name'],list['name'], card['dateLastActivity'],card['due'] ) 