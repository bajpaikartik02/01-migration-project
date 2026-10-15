import mysql.connector as database
import xml.etree.ElementTree as ET

db=database.connect(host = "localhost",user = "root",password = "kartik15")
cursor=db.cursor()

temp="create database if not exists itune"
temp2="use itune"

#Creating tracks table 
temp3="DROP TABLE IF EXISTS tracks"
temp4="create table tracks (trackID integer primary key auto_increment, name varchar(1000), artist_id integer default 0, genre_id integer, album_id integer, size integer, total_time integer, rating integer default 0, kind_id integer )"
cursor.execute(temp)
cursor.execute(temp2)
cursor.execute(temp3)
cursor.execute(temp4)
db.commit()

#Craeating dependent foreign tables(artist, genre, album, kind) for tracks table.
cmd1="DROP TABLE IF EXISTS artist"
cmd2="DROP TABLE IF EXISTS genre"
cmd3="DROP TABLE IF EXISTS album"
cmd4="DROP TABLE IF EXISTS kind"

cursor.execute(cmd1)
cursor.execute(cmd2)
cursor.execute(cmd3)
cursor.execute(cmd4)

temp5="create table artist (artist_id integer primary key auto_increment, name varchar(100))"
temp6="create table genre (genre_id integer primary key auto_increment, name varchar(100))"
temp7="create table album (album_id integer primary key auto_increment, name varchar(100))"
temp8="create table kind (kind_id integer primary key auto_increment, type varchar(100))"
cursor.execute(temp5)
cursor.execute(temp6)
cursor.execute(temp7)
cursor.execute(temp8)
db.commit()

#opening and extracting Tracks data from given xml file.
xmltree=ET.parse("Library.xml")
data=xmltree.findall("dict/dict/dict") #Extract the given pattern sub-tree from the main tree structure of xml-tree.


#Queries to check that given value is exist or not in a given table(artist, genre, album, kind) and insert it into the table if not exist.
cmd5="select name from artist where name=%s"
cmd6="insert into artist(name) values(%s)"

cmd7="select name from genre where name=%s"
cmd8="insert into genre(name) values(%s)"

cmd9="select name from album where name=%s"
cmd10="insert into album(name) values(%s)"

cmd11="select type from kind where type=%s"
cmd12="insert into kind(type) values(%s)"


#Queries to 'fetch the id' of the given value from the related tables.
cmd13="select artist_id from artist where name=%s"
cmd14="select genre_id from genre where name=%s"
cmd15="select album_id from album where name=%s"
cmd16="select kind_id from kind where type=%s"

#This function will take a dictionary three and covert it's key-value children into python dictionary, then return the dictionary.
def createTrackDict(tracks):
    track={}
    key=None
    value=None
    for child in tracks:
        if child.tag=="key":
            key=child.text
        else:
            value=child.text
            track[key]=value
    return track

#This loop will iterate over all the tracks-dict.
for tracks in data:
    track=createTrackDict(tracks)

    #Populating Artist table
    try:
        cursor.execute(cmd5,(track["Artist"],))
        value=cursor.fetchone()
        if value is None:
            cursor.execute(cmd6,(track["Artist"],))
            db.commit()   
    except Exception as e:
        print(e)

    #Populating Genre table
    try:
        cursor.execute(cmd7,(track["Genre"],))
        value=cursor.fetchone()
        print(value)
        if value is None:
            cursor.execute(cmd8,(track["Genre"],))
            db.commit()
    except Exception as e:
        print(e)

    #Populating Album table
    try:
        cursor.execute(cmd9,(track["Album"],))
        value=cursor.fetchone()
        print(value)
        if value is None:
            cursor.execute(cmd10,(track["Album"],))
            db.commit()
    except Exception as e:
        print(e)

    #Populating Kind table
    try:
        cursor.execute(cmd11,(track["Kind"],))
        value=cursor.fetchone()
        print(value)
        if value is None:
            cursor.execute(cmd12,(track["Kind"],))
            db.commit()
    except Exception as e:
        print(e)

    ######################Populating Tracks table######################    
    """Extacting the column-values of each track which is available, then save it into row tupple.
        If not exist then save default value in the row tupple."""
    row=()
    try:
        row+=(track["Name"],)
    except Exception as e:
        row+=("",)
        print(e)
    try:
        row+=(track["Total Time"],)
    except Exception as e:
        row+=(0,)
        print(e)
    try:
         row+=(track["Size"],)
    except Exception as e:
            row+=(0,)
            print(e)
    try:
        row+=(track["Rating"],)
    except Exception as e:
        row+=(0,)
        print(e)
    print(row)
        

    """ Extacting the id of the related columns from thr related tables and save them into a all_id-tupple if exist,
        If not exist then save the some default value for the  column. """
    temp=("Artist","Genre","Album","Kind")
    all_id=()
    print(all_id)
    for i in temp:
        columnVal=None
        try:
            columnVal=track[i]
        except:
            columnVal=0

        if i=="Artist" and columnVal!=0:
            cursor.execute(cmd13,(columnVal,))
            artist_id=cursor.fetchone()
            all_id+=artist_id

        elif i=="Genre"and columnVal!=0:
            cursor.execute(cmd14,(columnVal,))
            genre_id=cursor.fetchone()
            all_id+=genre_id

        elif i=="Album" and columnVal!=0:
            cursor.execute(cmd15,(columnVal,))
            album_id=cursor.fetchone()
            all_id+=album_id

        elif i=="Kind" and columnVal!=0:
            cursor.execute(cmd16,(columnVal,))
            kind_id=cursor.fetchone()
            all_id+=kind_id
        else:
            all_id+=(0,)
    print(all_id)

    #Inserting all the values of a row(track) extracted above in row and all_id variaibles, into the tracks table in single insert querry.
    cursor.execute("insert into tracks(name, total_time, size, rating, artist_id,genre_id,album_id,kind_id) values(%s,%s,%s,%s,%s,%s,%s,%s)",row+all_id)
    db.commit()
            
     #himanshu       
        

        

    



    






