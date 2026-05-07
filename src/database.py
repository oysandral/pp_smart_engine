import psycopg2
import json 

class DatabaseManager:

    @staticmethod
    def load_settings(settings_path : str) -> dict:
        with open(settings_path, 'r', encoding="utf-8") as file:
            return json.load(file)


    def __init__ (self, localhost : str, user : str, password : str, database : str):
        self.localhost = localhost
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self):
        try:
            conn = psycopg2.connect(
                host = self.localhost,
                user = self.user,
                password = self.password,
                database = self.database
            )
            return conn 
        
        except Exception as e:
            print(f"You have problems with connection: {e}")
            return None