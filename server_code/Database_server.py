import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3



# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def say_hello(name):
   print("Hello, " + name + "!")
   return 42


@anvil.server.callable
def get_jugendherbergen(row="*"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {row} FROM jugendherbergen"))
  return res
  
@anvil.server.callable
def get_zimmer_for_jugendherberge(jid, pid):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
        f"""
        SELECT  'Zimmernummer: ' || zimmernummer || ', ' || 'Bettenanzahl: ' || bettenanzahl || ', ' || 'Preis/Nacht: ' || preis_pro_nacht as deteils, 
        ZID 
        FROM zimmer 
        WHERE JID = {int(jid)} AND PID = {int(pid)} AND gebucht=0
        """
    ))
  print(res)
  return res

@anvil.server.callable
def get_Gast():
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute("Select Benutzername,GID from Gast"))
  return res

@anvil.server.callable
def get_Preiskategorie():
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute("Select PreisVon, PreisBis, PID from Preiskategorie"))
  price_ranges = [(f"{row[0]} - {row[1]}", row[2]) for row in res]
  return price_ranges

@anvil.server.callable
def get_More_user(Username):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"Select Benutzername, GID from Gast where Benutzername <> '{Username}'"))
  return res

@anvil.server.callable
def get_room_sleep_Place(zid):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"Select bettenanzahl from zimmer where ZID={int(zid)}"))
  return res

@anvil.server.callable
def get_username(gid_list):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  
  gid_str = ', '.join(map(str, gid_list))
  res = list(cursor.execute(f"SELECT Benutzername FROM Gast WHERE GID IN ({gid_str})"))
  
  usernames = [row[0] for row in res]
  return usernames

@anvil.server.callable
def write_booking(gid, zid, start_date, end_date):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  cursor.execute(f"insert into Buchung (GID, ZID, StartDatum, EndDatum) values ({int(gid)}, {int(zid)}, {str(start_date)}, {str(end_date)})")
  conn.commit()

@anvil.server.callable
def write_more_user(bid, gid):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  cursor.execute(f"insert into MitBuchung (BID, GID) values ({int(bid)}, {int(gid)})")
  conn.commit()
  
@anvil.server.callable
def update_room_book(zid, number):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  cursor.execute(f"update zimmer set gebucht={int(number)} where ZID={int(zid)}")
  conn.commit()

@anvil.server.callable
def get_latest_bid():
    conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(BID) FROM Buchung")  
    latest_bid = cursor.fetchone()[0]
    return latest_bid

@anvil.server.callable
def get_room_number(zid):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"select zimmernummer from zimmer where ZID={int(zid)}"))
  return res
  