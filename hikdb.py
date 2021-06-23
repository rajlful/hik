import sqlite3

class Hikdb:

    def __init__(self, db_name):

        self.db_connect = sqlite3.connect(db_name)
        self.cursor = self.db_connect.cursor()


    def create_new_db(self, db_name):
        
        self.cursor.execute("""CREATE TABLE Cameras_events(
                        model_name text,
                        event text);""")
        self.db_connect.commit()
        #self.cursor.close()

    def add_events(self, db_name, model, event):
        
        self.cursor.execute(f"""INSERT INTO Cameras_events
                  VALUES ('{model}', '{event}')""")
        self.db_connect.commit()
        #self.cursor.close()

    def show_events(self, db_name):
        
        self.cursor.execute(f"""SELECT * FROM Cameras_events""")
        return self.cursor.fetchall()

#a = Hikdb('hik.db')
#print(a.show_events('hik.db'))