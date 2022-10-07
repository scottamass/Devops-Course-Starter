from datetime import date, datetime

#today = date.today().strftime('%d-%m-%Y')
#print (today)
class ViewModel:
        def __init__(self,items):
            self._items =items    
        @property
        def items(self):
            return self._items    
        @property
        def doing_items(self):
            doing_items =[]
            for item in self._items:
                if item.list == "Doing":
                    doing_items.append(item) 
            return doing_items

        @property
        def todo_items(self):
            todo_items =[]
            for item in self._items:
                if item.list == "To Do":
                    todo_items.append(item) 
            return todo_items

        @property
        def done_items(self):
            done_items =[]
            for item in self._items:
                if item.list == "Done":
                    done_items.append(item) 
            
            return done_items       

       
        @property
        def recently_done_items(self):
            recently_done_items = []
            today = date.today().strftime('%d-%m-%Y')
            print(today)
            for item in self._items:
                if item.list == "Done" and item.dateLastActivity[0:10] == today :
                    recently_done_items.append(item)
            return recently_done_items
        
        @property
        def old_done_items(self):
            old_done_items=[]
            today = date.today().strftime('%d-%m-%Y')
            for item in self._items:
                if item.list =="Done" and item.dateLastActivity[0:10] != today:
                    old_done_items.append(item)
            return old_done_items  

