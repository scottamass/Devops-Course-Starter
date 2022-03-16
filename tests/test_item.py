import pytest

from todo_app.data.trello_items import Item, ViewModel

@pytest.fixture
def item() -> Item:
    return Item
    
def test_doing(Item):
    #arrange
    
    #act

    #assert
    assert len(ViewModel.items) == 0
   
    