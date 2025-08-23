from datetime import datetime

class DB():
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    async def clean_db(self):
        self.cursor.execute("""
            DELETE FROM Links
            WHERE created_at < datetime('now', '-7 days')
        """)
        deleted = self.cursor.rowcount
        self.connection.commit()
        print("Deleted  " + len(deleted) + " rows ")

    def create_link_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS Links (
            sketchy TEXT NOT NULL PRIMARY KEY,
            real TEXT NOT NULL,
            created_at INTEGER
        );
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print("Table 'Links' created successfully!")

    def add_link_to_db(self, sketchy_url, real_url):
        try:
            self.cursor.execute('INSERT INTO Links VALUES (?, ?, ?);', (sketchy_url, real_url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            print("[+] Added link to DB: " + sketchy_url + " | " + real_url)
            return "ok"
        except Exception as e:
            print("[!] Error trying to add link to DB: " + str(e))
            return "error"

    def fetch_real_url_from_db(self, sketchy_url):
        self.cursor.execute('SELECT real FROM Links WHERE sketchy=?;', (sketchy_url,))
        output = self.cursor.fetchone()
        if output:
            return output[0]
        return None