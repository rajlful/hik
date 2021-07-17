import sqlite3
import datetime

class Hikdb:

    def __init__(self, db_name):

        self.db_connect = sqlite3.connect(db_name)
        self.cursor = self.db_connect.cursor()

    def __del__(self):
        self.cursor.close()

    def create_new_db(self):
        
        self.cursor.execute("""CREATE TABLE Cameras_events(
                        time text,
                        model_name text,
                        event text);""")
        self.db_connect.commit()
        

    def add_events(self, dateandatime, model, event):
        
        self.cursor.execute(f"""INSERT INTO Cameras_events
                  VALUES ('{dateandatime}', '{model}', '{event}')""")
        self.db_connect.commit()

    def show_events(self ):
        
        self.cursor.execute(f"SELECT * FROM Cameras_events LIMIT 10")
        return self.cursor.fetchall()

if __name__ == "__main__":
    a = Hikdb('hik.db')
    event_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    e = a.show_events()
    print(e)
    
