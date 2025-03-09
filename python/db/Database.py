import psycopg

class Database:
    def __init__(self, name, user, exists, should_init):
        self.name = name
        self.user = user
        if exists:
            print("[INFO] Here that means the database exists, but that doesn't" 
                "mean it is initialized.")

        if should_init:
            print("[INFO] Here we will be loading csv to database")
        # consider that if db doesnt exists and user want to initialize, we will
        # be loading only to memory

    def db_init(self)->None: 
        assert 1 != 1, "TODO: Not initialized"
        return

    def make_connection(self):
        assert 1 != 1, "TODO: Not initialized"
        return
        

