from typing import List
import psycopg
import pandas as pd
from psycopg.errors import IoError

class Database:
    cls_name = "Database"
    table_init_query = """CREATE TABLE {tablename} ( 
                    id SERIAL PRIMARY KEY,
                    imdbid SERIAL,
                    title VARCHAR,
                    genres TEXT[],
                    ratings REAL,
                    users_rated SERIAL
                    )"""
    insert_into_query = """INSERT INTO movies(id, imdbid, title, genres,
     ratings, users_rated) VALUES(%s, %s, %s, %s, %s, %s)"""
    table_exists_query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)"

    def __init__(self, **config):
        """
            TODO: Titles appear to be very long.
            TODO: Make better errors.
            TODO: get rid of unnecessary parameters and functions, e.g.:
            update_db etc. For example you could do *args, the first one would
            be query, the rest is batch or some other data, that should be
            passed to execute. Keep in mind to check if injection occurrs.
        """
        self.config = config
        self.name: str = config["name"] 
        self.user: str = config["user"] 
        self.host: str = config["host"] 
        self.port: int = config["port"]  

    def table_init(self)->None: 
        """
                                    tablename
        +--------+---------+--------------+--------+---------+-------------+
        |   id   | imdbid  |    title     | genres | ratings | users_rated |
        +--------+---------+--------------+--------+---------+-------------+
        | SERIAL | SERIAL  |   VARCHAR    | TEXT[] | REAL    | SERIAL      |
        +--------+---------+--------------+--------+---------+-------------+
              ^---- PRIMARY KEY
            Furthermore, your dataset should be csv, with the following
            structure:
                - links.csv: movieid, imdbid, tmdbid (up to two sources of
                movie ids)
                - movies.csv: movieid, title, genres
                - ratings.csv: userid, movieid, rating, timestamp
                - tags.csv: userid, movieid, tag, timestamp
            Preferably the user, should pass with those names and shouldn't be
            changed.
            We can calculate rating easily.
        """
        if not self.exists(self.config["tablename"]):
            print("[INFO] table_init(): Table doesn't exist, making one.")
            try:
                # --- TODO: probably should make construct_query to handle some bad
                # injections etc --- # 
                self.make_query(query=self.table_init_query.format(tablename=self.config["tablename"]))
            except IOError as e:
                print(f"[ERROR] table_init(): Couldn't create given table.\n{e}")
                exit(1) 

            try:
                # --- Load movies into the database --- #
                print("[INFO] table_init(): Loading all movies.")
                csv_files = list(self.config["resource"].glob("*.csv")) 
                movies_data = dict() 

                if self.config["links"] not in csv_files:
                    print("[ERROR] links.csv wasn't found.")
                    exit(1)

                link_df = pd.read_csv(self.config["links"], sep=',', skiprows=0)
                for relation in link_df.itertuples(index=False, name=None):
                    movieid, imdbid, *_ = relation
                    entry = [0 for _ in range(6)]
                    entry[0] = movieid
                    entry[1] = imdbid
                    movies_data[movieid] = entry
                # --- Drop the reference --- #
                del link_df

                if self.config["movies"] not in csv_files:
                    print("[ERROR] movies.csv wasn't found.")
                    exit(1)

                movies_df = pd.read_csv(self.config["movies"], sep=',', skiprows=0)
                for relation in movies_df.itertuples(index=False, name=None):
                    movieid, title, genres = relation
                    # --- Get entry info --- #
                    entry = movies_data[movieid]
                    entry[2] = title.rstrip() 
                    entry[3] = genres.split('|') 
                    # --- Replace with new entry --- #
                    movies_data[movieid] = entry

                del movies_df

                if self.config["ratings"] not in csv_files:
                    print("[ERROR] ratings.csv wasn't found.")
                    exit(1)

                ratings_df = pd.read_csv(self.config["ratings"], sep=',', skiprows=0)
                for relation in ratings_df.itertuples(index=False, name=None):
                    _, movieid, rating, _ = relation
                    # --- Get entry info --- #
                    entry = movies_data[movieid]
                    entry[4] += rating 
                    entry[5] += 1 
                    # --- Replace with new entry --- #
                    movies_data[movieid] = entry
                del ratings_df
                # TODO: For now skipping the tags.csv
                
            except IOError as e:
                print(e)
                exit(1)

            try:
                with self.get_connection() as conn:
                    with conn.cursor() as cur:
                        for relation in movies_data.values():
                            cur.execute(self.insert_into_query, relation)
            except IOError as e:
                print(e)
                exit(1)


        return

    def exists(self, tablename: str) -> bool:
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(self.table_exists_query, (tablename,))
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
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    # --- Sample query, not final --- #
                    cur.execute(query, args)
            
                    
        except IoError as e: 
            print(f"[ERROR] make_query(): Failed to execute the query.\n{e}")

    def get_connection(self):
        try:
            conn = psycopg.connect(dbname=self.name, 
                                 user=self.user, 
                                 host=self.host,
                                 port=self.port)
            return conn
        except IOError as e:
            print(e)
            exit(1)


    def update_db(self, *batch: List): 
        assert 1 == 1, "TODO: fill_database() not implemented"
        try:
            with self.get_connection() as conn:
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

    def __repr__(self):
        rows = {
            "name": self.name,
            "user": self.user,
            "host": self.host,
            "port": str(self.port)  
        }

        max_length = max(len(f"{key}: {value}") for key, value in rows.items())

        title = f" {self.cls_name} "
        half_padding = (max_length - len(title)) // 2
        header = f"{'=' * half_padding}{title}{'=' * half_padding}"
        header = header.ljust(max_length, "=")

        formatted_rows = [f"{key}: {str(value).rjust(max_length - len(key) - 2)}" for key, value in rows.items()]
        return f"{header}\n" + "\n".join(formatted_rows) + f"\n{'=' * len(header)}"
