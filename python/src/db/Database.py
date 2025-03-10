from typing import List
import psycopg
import pandas as pd
from psycopg.errors import IoError

class Database:
    def __init__(self, name: str, user: str, host: str = "127.0.0.1", port: int 
                 = 5432):
        self.name: str = name
        self.user: str = user
        self.host: str = host 
        self.port: int = port  

    def table_init(self, tablename: str = "movies")->None: 
        """
                                    tablename
        +--------+---------+--------------+--------+---------+-------------+
        |   id   | movieid |    title     | genres | ratings | users_rated |
        +--------+---------+--------------+--------+---------+-------------+
        | SERIAL | SERIAL  | VARCHAR(128) | TEXT[] | REAL    | SERIAL      |
        +--------+---------+--------------+--------+---------+-------------+
              ^---- PRIMARY KEY
            Furthermore, your dataset should be csv, with the following
            structure:
                --> links.csv: movieid, imdbid, tmdbid (up to two sources of
                movie ids)
                --> movies.csv: movieid, title, genres
                --> ratings.csv: userid, movieid, rating, timestamp
                --> tags.csv: userid, movieid, tag, timestamp
            Preferably the user, should pass with those names and shouldn't be
            changed.
            We can calculate rating easily.
        """
        if not self.exists(tablename):
            print("[INFO]: table_init(): Table doesn't exist. Creating one")
            try:
                # --- TODO: probably should make construct_query to handle some bad
                # injections etc --- # 
                create_table_query = """CREATE TABLE {tablename} ( 
                    id SERIAL PRIMARY KEY,
                    movieid SERIAL,
                    title VARCHAR(128),
                    genres TEXT[],
                    ratings REAL,
                    users_rated SERIAL
                    )""".format(tablename=tablename) 
                self.make_query(query=create_table_query)
            except IOError as e:
                print(f"[ERROR] table_init(): Couldn't create given table.\n{e}")
                exit(1) 

            # --- Load movies into the database --- #
            for from_link in pd.read_csv("resource/links.csv", sep=',',
                                         skiprows=1).itertuples(index=False,
                                                                name=None): 
                print(from_link)

        return

    def exists(self, tablename: str) -> bool:
        try:
            with psycopg.connect(dbname=self.name, 
                                 user=self.user, 
                                 host=self.host,
                                 port=self.port) as conn:

                with conn.cursor() as cur:
                    query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)"
                    cur.execute(query, (tablename,))
                    return cur.fetchone()[0] 
        except IoError as e: 
            print(f"[ERROR] exists(): Failed to execute the query.\n{e}")
            exit(1)


    def make_query(self, query: str ="", *args)-> None:
        """
            Parameters:
                query: what should this function execute
                args: arguments for query
        """

        if len(query) == 0:
            print("[WARNING] Query is length of 0, query omitted.")
            return

        try:

            with psycopg.connect(dbname=self.name, 
                                 user=self.user, 
                                 host=self.host,
                                 port=self.port) as conn:

                with conn.cursor() as cur:
                    # --- Sample query, not final --- #
                    cur.execute(query, args)
                    
        except IoError as e: 
            print(f"[ERROR] make_query(): Failed to execute the query.\n{e}")


    def fill_database(self, batch: List): 
        try:
            with psycopg.connect(dbname=self.name, 
                                 user=self.user, 
                                 host=self.host,
                                 port=self.port) as conn:

                with conn.cursor() as cur:
                    query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)"
                    cur.execute(query, (tablename,))
                    return cur.fetchone()[0] 
        except IoError as e: 
            print(f"[ERROR] exists(): Failed to execute the query.\n{e}")
            exit(1)


    def transaction(self):
        assert 1 != 1, "TODO: Not initialized"
        return

