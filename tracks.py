import xml.etree.ElementTree as ET
import sqlite3 as sql

con=sql.connect("tracksDB.sqlite")
cur=con.cursor()

#Making the database schema.
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;

CREATE TABLE Artist (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE );

CREATE TABLE Genre (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE );

CREATE TABLE Album (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE );

CREATE TABLE Track (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    album_id INTEGER,
    genre_id INTEGER,
    title TEXT UNIQUE,
    len INTEGER,
    rating INTEGER,
    count INTEGER );
''')

#opening an i-Tune library XML file to form database.
fname=input("Enter the XML file name:")
if len(fname)<1: fname="Library.xml"

xml= ET.parse(fname)
data=xml.findall("dict/dict/dict")
print("Dict count:",len(data))

#Function to get data from XML easily.
def check(d,value):
    iterator=False
    for child in d:
        if iterator: return child.text
        if child.tag=="key" and child.text==value:
            iterator=True
    return 0

for entry in data:
    if check(entry,"Track ID")==0:
        continue
    name=check(entry,'Name')
    artist=check(entry,'Artist')
    album=check(entry,'Album')
    count=check(entry,'Play Count')
    genre=check(entry,'Genre')
    rating=check(entry,'Rating')
    length=check(entry,"Total Time")
    #print(name,artist,album,count,genre,rating,length)
    cur.execute('INSERT OR IGNORE INTO Genre(name) VALUES(?)',
        (genre,)
        )
    cur.execute("SELECT id FROM Genre WHERE name=?",
        (genre,)
        )
    #print(cur.fetchall())
    genre_id=cur.fetchall()[0][0]
    print(genre_id)
    cur.execute('INSERT OR IGNORE INTO Artist(name) VALUES(?)',
        (artist,)
        )
    cur.execute('SELECT id FROM Artist WHERE name=?',
        (artist,)
        )
    artist_id=cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Album(artist_id,title) VALUES (?,?)',
        (artist_id,album)
        )
    cur.execute('SELECT id FROM Album WHERE title=?',
        (album,)
        )
    album_id=cur.fetchone()[0]
    #print(album,artist,genre,name,length,rating,count)
    cur.execute('''INSERT OR REPLACE INTO Track
        (album_id,genre_id,title,len,rating,count) VALUES
        (?,?,?,?,?,?)''',
        (album_id,genre_id,name,length,rating,count))
con.commit()

#Yaiiii... code run very well
