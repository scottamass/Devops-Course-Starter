from pydoc import visiblename
import pytest

from todo_app.data.views import ViewModel
from todo_app.data.item import Item


    
def test_doing_items_methord_on_view_model_class():
    #arrange
    items = [
        Item("123","doing todo","Doing")
    ]
    View_mode = ViewModel(items)

    #act
    doing_items = View_mode.doing_items
    #assert
    assert len(doing_items) == 1
   
def test_todo_items_methord_on_view_model_class():
    #arrange
    items = [
        Item("123","doing todo","To-do")
    ]
    View_mode = ViewModel(items)

    #act
    todo_items = View_mode.todo_items
    #assert
    assert len(todo_items) == 1    

def test_done_items_methord_on_view_model_class():
    #arrange
    items = [
        Item("123","doing todo","Done")
    ]
    View_mode = ViewModel(items)

    #act
    done_items = View_mode.done_items
    #assert
    assert len(done_items) == 1       