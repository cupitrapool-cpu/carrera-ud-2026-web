"""Public demo data layer. No private SQLite data or administrator access.
This deployment is NOT synchronized with the local race timing database.
"""
import sqlite3
import pandas as pd

_CONNECTION = sqlite3.connect(":memory:", check_same_thread=False)
_CONNECTION.row_factory = sqlite3.Row
_CONNECTION.executescript("""
CREATE TABLE settings(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE categories(name TEXT PRIMARY KEY, laps INTEGER, lap_km REAL);
CREATE TABLE athletes(id INTEGER PRIMARY KEY, document TEXT, name TEXT, category TEXT, dorsal TEXT, status TEXT, source TEXT);
CREATE TABLE races(id INTEGER PRIMARY KEY, category TEXT, start_epoch REAL, active INTEGER);
CREATE TABLE marks(id INTEGER PRIMARY KEY, race_id INTEGER, seconds REAL, created REAL, paired INTEGER);
CREATE TABLE arrivals(id INTEGER PRIMARY KEY, race_id INTEGER, dorsal TEXT, created REAL, paired INTEGER);
CREATE TABLE laps(id INTEGER PRIMARY KEY, race_id INTEGER, dorsal TEXT, lap INTEGER, seconds REAL, split REAL);
CREATE TABLE penalties(id INTEGER PRIMARY KEY, race_id INTEGER, dorsal TEXT, reason TEXT, note TEXT, created REAL);
""")
_CONNECTION.executemany('INSERT INTO categories VALUES (?,?,?)', [
 ('5K Femenina Estudiantes Elite',5,1.0),
 ('5K Masculina Estudiantes Elite',5,1.0),
 ('3K Femenina Estudiantes Recreativa',3,1.0),
 ('3K Masculina Estudiantes Recreativa',3,1.0),
 ('3K Masculina Docentes y Administrativos',3,1.0),
 ('3K Femenina Docentes y Administrativos',3,1.0),
 ('Relevo Mixto 4x1K',4,1.0),
])
_CONNECTION.commit()

def con():
    return _CONNECTION

def setting(key):
    return {"registrations_open":"0", "form_url":"https://docs.google.com/forms/d/e/1FAIpQLSdRk26E_Pj1ptysbfPwKPnBWxch2cPBCD-jj8RxtEMg2Ec5eQ/viewform"}.get(key, "")

def categories():
    return pd.read_sql_query('SELECT name,laps,lap_km FROM categories ORDER BY name',_CONNECTION)

def athletes():
    return pd.read_sql_query('SELECT id,document,name,category,dorsal,status,source FROM athletes ORDER BY name',_CONNECTION)

def live_results():
    return pd.DataFrame(columns=['Salida','Prueba','Dorsal','Corredor','Vueltas','Meta','Segundos','Estado'])
