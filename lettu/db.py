from lettu import credentials
import mariadb

def connect():
    try:
        db = mariadb.connect(
            user=credentials.USER,
            password=credentials.PASSWORD,
            host=credentials.HOST,
            port=credentials.PORT,
            database=credentials.DBNAME
        )
        print("Connection to mariadb succesful")
        db.autocommit = True
        cur = db.cursor()
        return cur

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")