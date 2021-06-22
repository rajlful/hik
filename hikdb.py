import sqlite3

def create_new_db(db_name):
    new_db = sqlite3.connect(db_name)
    cursor = new_db.cursor()
    cursor.execute("""CREATE TABLE Cameras_events(
                        model_name text,
                        event text);""")
    new_db.commit()
    cursor.close()

def add_events(db_name, model, event):
    new_db = sqlite3.connect(db_name)
    cursor = new_db.cursor()
    cursor.execute(f"""INSERT INTO Cameras_events
                  VALUES ('{model}', '{event}')""")
    new_db.commit()
    cursor.close()

def show_events(db_name):
    new_db = sqlite3.connect(db_name)
    cursor = new_db.cursor()
    cursor.execute(f"""SELECT * FROM Cameras_events""")
    return cursor.fetchall()

