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
def get_zimmer_for_jugendherberge(jid):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
        f"""
        SELECT  'Zimmernummer: ' || zimmernummer || ', ' || 'Bettenanzahl: ' || bettenanzahl || ', ' || 'Preis/Nacht: ' || preis_pro_nacht as deteils, 
        ZID 
        FROM zimmer 
        WHERE JID = {int(jid)}
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



  