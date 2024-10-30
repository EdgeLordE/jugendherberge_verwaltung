from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
 
 
class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.drop_down_City.items = anvil.server.call("get_jugendherbergen", "name, JID")
    self.drop_down_User.items = anvil.server.call('get_Gast')
    self.drop_down_PriceCategorie.items = anvil.server.call('get_Preiskategorie')
    self.current_user = [self.drop_down_User.items[self.drop_down_User.selected_value - 1][0], self.drop_down_User.selected_value]
    self.current_pricecategorie = [self.drop_down_PriceCategorie.items[self.drop_down_PriceCategorie.selected_value - 1][0], self.drop_down_PriceCategorie.selected_value]
    self.current_City = [self.drop_down_City.items[self.drop_down_City.selected_value - 1][0], self.drop_down_City.selected_value]

    self.drop_down_MoreUser.items = anvil.server.call('get_More_user', self.current_user[0])
    #self.drop_down_Room.items = anvil.server.call('get_zimmer_for_jugendherberge', self.current_City[1]+1)

    self.start_date_check = False
    self.end_date_check = False

  
  def drop_down_City_change(self, **event_args):
    """This method is called when an item is selected"""
    self.current_City = [self.drop_down_City.items[self.drop_down_City.selected_value - 1][0], self.drop_down_City.selected_value]
    self.drop_down_Room.items = anvil.server.call('get_zimmer_for_jugendherberge', self.current_City[1]+1)
    print(self.current_City)
  
  def drop_down_User_change(self, **event_args):
    """This method is called when an item is selected"""
    self.current_user = [self.drop_down_User.items[self.drop_down_User.selected_value - 1][0], self.drop_down_User.selected_value]
    self.drop_down_MoreUser.items = anvil.server.call('get_More_user', self.current_user[0])
    print(self.current_user)

  def drop_down_PriceCategorie_change(self, **event_args):
    """This method is called when an item is selected"""
    self.current_pricecategorie = [self.drop_down_PriceCategorie.items[self.drop_down_PriceCategorie.selected_value - 1][0], self.drop_down_PriceCategorie.selected_value]
    print(self.current_pricecategorie)

  def date_picker_StartDate_change(self, **event_args):
    """This method is called when the selected date changes"""
    if len(str(self.date_picker_StartDate.date)) == 10:
      self.start_date_check = True
    else:
      self.end_date_check = False
    print(self.start_date_check)

  def date_picker_EndDate_change(self, **event_args):
    """This method is called when the selected date changes"""
    if len(str(self.date_picker_EndDate.date)) == 10:
      self.end_date_check = True
    else:
      self.end_date_check = False
    print(self.end_date_check)

    


    
    
    
