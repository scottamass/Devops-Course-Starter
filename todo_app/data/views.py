

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

         