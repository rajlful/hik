import sqlite3

class Hikdb:

    def __init__(self, db_name):

        self.db_connect = sqlite3.connect(db_name)
        self.cursor = self.db_connect.cursor()

    def __del__(self):
        self.cursor.close()

    def create_new_db(self):
        
        self.cursor.execute("""CREATE TABLE Cameras_events(
                        model_name text,
                        event text);""")
        self.db_connect.commit()
        

    def add_events(self, model, event):
        
        self.cursor.execute(f"""INSERT INTO Cameras_events
                  VALUES ('{model}', '{event}')""")
        self.db_connect.commit()

    def show_events(self, ):
        
        self.cursor.execute(f"SELECT * FROM Cameras_events")
        return self.cursor.fetchall()
