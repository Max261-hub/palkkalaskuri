import sqlite3
import hashlib
from datetime import datetime

DB_NAME = "kevytyrittaja_v1.db"

def luo_tietokanta():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS kayttajat 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, tunnus TEXT UNIQUE, 
                      salasana TEXT, nimi TEXT, vero REAL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS palkat 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, kayttaja_id INTEGER,
                      brutto REAL, vero_p REAL, palvelu REAL, vakuutus REAL, 
                      tyel REAL, vero_euro REAL, netto REAL, pvm DATETIME)''')
        conn.commit()

def rekisteroi(t, s, n, v):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            h = hashlib.sha256(s.encode()).hexdigest()
            conn.execute("INSERT INTO kayttajat (tunnus, salasana, nimi, vero) VALUES (?, ?, ?, ?)", (t, h, n, v))
            return True
    except: return False

def kirjaudu(t, s):
    with sqlite3.connect(DB_NAME) as conn:
        h = hashlib.sha256(s.encode()).hexdigest()
        c = conn.execute("SELECT id, nimi, vero FROM kayttajat WHERE tunnus = ? AND salasana = ?", (t, h))
        return c.fetchone()

def tallenna_laskelma(k_id, brutto, vero_p, palvelu, vakuutus, tyel, vero_e, netto):
    with sqlite3.connect(DB_NAME) as conn:
        nyt = datetime.now().strftime("%d.%m.%Y %H:%M")
        conn.execute("INSERT INTO palkat (kayttaja_id, brutto, vero_p, palvelu, vakuutus, tyel, vero_euro, netto, pvm) VALUES (?,?,?,?,?,?,?,?,?)", 
                     (k_id, brutto, vero_p, palvelu, vakuutus, tyel, vero_e, netto, nyt))
        conn.commit()

def hae_historia(k_id):
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT * FROM palkat WHERE kayttaja_id = ? ORDER BY id DESC", (k_id,)).fetchall()