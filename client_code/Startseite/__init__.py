from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, timedelta

class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    today = datetime.now().date()
    self.date_picker_StartDate.min_date = today
    self.date_picker_EndDate.min_date = today

    self.drop_down_Room.enabled = True
    self.outlined_button_2.enabled = False  
    self.label_result.text = "Bitte wählen Sie ein Zimmer und Start- und Enddatum für die Buchung aus.\nWählen Sie einen anderen Benutzer aus um die Mitbucherliste zurückzusetzen."

    self.drop_down_City.items = anvil.server.call("get_jugendherbergen", "name, JID")
    self.drop_down_User.items = anvil.server.call('get_Gast')
    self.drop_down_PriceCategorie.items = anvil.server.call('get_Preiskategorie')
    
    self.current_user = [self.drop_down_User.items[self.drop_down_User.selected_value - 1][0], self.drop_down_User.selected_value]
    self.current_pricecategorie = [self.drop_down_PriceCategorie.items[self.drop_down_PriceCategorie.selected_value - 1][0], self.drop_down_PriceCategorie.selected_value]
    self.current_City = [self.drop_down_City.items[self.drop_down_City.selected_value - 1][0], self.drop_down_City.selected_value]
    
    self.current_book_dates = []
    self.current_more_user = []
    
    self.drop_down_MoreUser.items = anvil.server.call('get_More_user', self.current_user[0])
    self.drop_down_Room.items = anvil.server.call('get_zimmer_for_jugendherberge', self.current_City[1], self.current_pricecategorie[1])

    self.start_date_check = False
    self.end_date_check = False

  def drop_down_City_change(self, **event_args):
    """This method is called when a city is selected."""
    self.current_City = [self.drop_down_City.items[self.drop_down_City.selected_value - 1][0], self.drop_down_City.selected_value]
    self.drop_down_Room.items = anvil.server.call('get_zimmer_for_jugendherberge', self.current_City[1], self.current_pricecategorie[1])
    
  
  def drop_down_User_change(self, **event_args):
    """This method is called when a user is selected."""
    self.current_user = [self.drop_down_User.items[self.drop_down_User.selected_value - 1][0], self.drop_down_User.selected_value]
    self.drop_down_MoreUser.items = anvil.server.call('get_More_user', self.current_user[0])
    self.current_more_user = []
   

  def drop_down_PriceCategorie_change(self, **event_args):
    """This method is called when a price category is selected."""
    self.current_pricecategorie = [self.drop_down_PriceCategorie.items[self.drop_down_PriceCategorie.selected_value - 1][0], self.drop_down_PriceCategorie.selected_value]
    self.drop_down_Room.items = anvil.server.call('get_zimmer_for_jugendherberge', self.current_City[1], self.current_pricecategorie[1])

  def date_picker_StartDate_change(self, **event_args):
    """This method is called when the start date changes."""
    start_date = self.date_picker_StartDate.date
    
    if start_date:
      self.start_date_check = True
      self.date_picker_EndDate.min_date = start_date
    else:
      self.start_date_check = False
    self.check_enable_booking_button()
    

  def date_picker_EndDate_change(self, **event_args):
    """This method is called when the end date changes."""
    start_date = self.date_picker_StartDate.date
    end_date = self.date_picker_EndDate.date
    
    if end_date and start_date and end_date < start_date:
      alert("Das Enddatum darf nicht vor dem Startdatum liegen. Bitte wählen Sie ein gültiges Enddatum.")
      self.date_picker_EndDate.date = None  
      self.end_date_check = False
    else:
      self.end_date_check = bool(end_date)
    self.check_enable_booking_button()
    

  def check_enable_booking_button(self):
    """Enable 'Jetzt Buchen' button only if both dates and a room are selected."""
    if self.start_date_check and self.end_date_check and self.drop_down_Room.selected_value:
      self.outlined_button_2.enabled = True
    else:
      self.outlined_button_2.enabled = False

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      max_persons = anvil.server.call('get_room_sleep_Place', self.drop_down_Room.selected_value)[0][0]
      if len(set(self.current_more_user)) + 1 >= max_persons:
        alert("Die maximale Anzahl an Leuten in dem Zimmer wurde erreicht.")
        
      else:
        self.current_more_user.append(self.drop_down_MoreUser.selected_value)
    except:
      pass
  def outlined_button_2_click(self, **event_args):
    """This method is called when the booking button is clicked."""
    
    gid = self.current_user[1]  
    zid = self.drop_down_Room.selected_value  
    start_date = self.date_picker_StartDate.date.strftime('%Y-%m-%d')  
    end_date = self.date_picker_EndDate.date.strftime('%Y-%m-%d')  
    
    anvil.server.call('write_booking', gid, zid, start_date, end_date)

    latest_bid = anvil.server.call('get_latest_bid')  

    for guest_gid in set(self.current_more_user):
        anvil.server.call('write_more_user', latest_bid, guest_gid)

    anvil.server.call('update_room_book', zid, 1)

    self.label_result.text = "Buchung erfolgreich abgeschlossen!"
    
    self.drop_down_Room.items = anvil.server.call('get_zimmer_for_jugendherberge', self.current_City[1], self.current_pricecategorie[1])

  def outlined_button_input_check_click(self, **event_args):
    """This method is called when the input check button is clicked."""
    
    user = self.current_user[0]  
    jugendherberge = self.current_City[0]  
    zimmer =  anvil.server.call('get_room_number', self.drop_down_Room.selected_value)[0][0]
    start_datum = self.date_picker_StartDate.date.strftime('%d.%m.%Y') if self.date_picker_StartDate.date else "Nicht festgelegt"
    end_datum = self.date_picker_EndDate.date.strftime('%d.%m.%Y') if self.date_picker_EndDate.date else "Nicht festgelegt"
    
    try:
        more_user = anvil.server.call('get_username', list(set(self.current_more_user)))
        
        string_more_user = ", ".join(more_user) if more_user else "Nicht festgelegt"
    except Exception as e:
        string_more_user = f"Fehler beim Abrufen der Mitbucher: {str(e)}"

    result_message = (f"Benutzer: {user}\n"
                      f"Jugendherberge: {jugendherberge}\n"
                      f"Zimmer: {zimmer}\n"
                      f"Von: {start_datum}\n"
                      f"Bis: {end_datum}\n"
                      f"Mitbucher: {string_more_user}"
                     )

    self.label_result.text = result_message

