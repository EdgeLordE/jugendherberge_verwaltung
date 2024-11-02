from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, timedelta
 
class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    today = datetime.now().date()
    
    # Zimmer-Auswahl deaktivieren und Hinweistext im Label anzeigen
    self.drop_down_Room.enabled = False
    self.outlined_button_2.enabled = False  # "Jetzt Buchen" button initially disabled
    self.label_result.text = "Bitte wählen Sie zuerst das Start- und Enddatum aus, um ein Zimmer auszuwählen."

    # Initialize dropdown values and other variables
    self.drop_down_City.items = anvil.server.call("get_jugendherbergen", "name, JID")
    self.drop_down_User.items = anvil.server.call('get_Gast')
    self.drop_down_PriceCategorie.items = anvil.server.call('get_Preiskategorie')
    
    # Selected user, price, and city data
    self.current_user = [self.drop_down_User.items[self.drop_down_User.selected_value - 1][0], self.drop_down_User.selected_value]
    self.current_pricecategorie = [self.drop_down_PriceCategorie.items[self.drop_down_PriceCategorie.selected_value - 1][0], self.drop_down_PriceCategorie.selected_value]
    self.current_City = [self.drop_down_City.items[self.drop_down_City.selected_value - 1][0], self.drop_down_City.selected_value]
    
    self.current_book_dates = []
    self.current_more_user = []
    
    # Update lists
    self.drop_down_MoreUser.items = anvil.server.call('get_More_user', self.current_user[0])
    self.drop_down_Room.items = anvil.server.call('get_zimmer_for_jugendherberge', self.current_City[1], self.current_pricecategorie[1])

    # Flags for date selection check
    self.start_date_check = False
    self.end_date_check = False

  def check_enable_room_dropdown(self):
    """Enables the room dropdown only if both start and end dates are valid and updates label_result."""
    if self.start_date_check and self.end_date_check:
      self.drop_down_Room.enabled = True
      self.outlined_button_2.enabled = False  # Disable "Jetzt Buchen" button when room dropdown is enabled
      self.label_result.text = ""  # Remove hint text
    else:
      self.drop_down_Room.enabled = False
      self.outlined_button_2.enabled = True  # Enable "Jetzt Buchen" button when room dropdown is disabled
      self.label_result.text = "Bitte wählen Sie zuerst das Start- und Enddatum aus, um ein Zimmer auszuwählen."

  def drop_down_City_change(self, **event_args):
    """This method is called when a city is selected."""
    self.current_City = [self.drop_down_City.items[self.drop_down_City.selected_value - 1][0], self.drop_down_City.selected_value]
    self.drop_down_Room.items = anvil.server.call('get_zimmer_for_jugendherberge', self.current_City[1], self.current_pricecategorie[1])
    print(self.current_City)
  
  def drop_down_User_change(self, **event_args):
    """This method is called when a user is selected."""
    self.current_user = [self.drop_down_User.items[self.drop_down_User.selected_value - 1][0], self.drop_down_User.selected_value]
    self.drop_down_MoreUser.items = anvil.server.call('get_More_user', self.current_user[0])
    print(self.current_user)

  def drop_down_PriceCategorie_change(self, **event_args):
    """This method is called when a price category is selected."""
    self.current_pricecategorie = [self.drop_down_PriceCategorie.items[self.drop_down_PriceCategorie.selected_value - 1][0], self.drop_down_PriceCategorie.selected_value]
    print(self.current_pricecategorie)

  def date_picker_StartDate_change(self, **event_args):
    """This method is called when the start date changes."""
    if self.date_picker_StartDate.date:
      self.start_date_check = True
    else:
      self.start_date_check = False
    self.check_enable_room_dropdown()  # Überprüfen, ob das Zimmer-Dropdown aktiviert und das Label aktualisiert werden soll
    print("Start date check:", self.start_date_check)

  def date_picker_EndDate_change(self, **event_args):
    """This method is called when the end date changes."""
    if self.date_picker_EndDate.date:
      self.end_date_check = True
    else:
      self.end_date_check = False
    self.check_enable_room_dropdown()  # Überprüfen, ob das Zimmer-Dropdown aktiviert und das Label aktualisiert werden soll
    print("End date check:", self.end_date_check)

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    max_persons = anvil.server.call('get_room_sleep_Place', self.drop_down_Room.selected_value)[0][0]
    if len(set(self.current_more_user)) + 1 >= max_persons:
      alert("Die maximale Anzahl an Leuten in dem Zimmer wurde erreicht.")
      print("Aktuelle zusätzliche Benutzer:", set(self.current_more_user))
    else:
      self.current_more_user.append(self.drop_down_MoreUser.selected_value)
    
  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

