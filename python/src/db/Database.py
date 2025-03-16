from typing import Dict, Any, List, Tuple
import psycopg
import pandas as pd
import numpy as np
from psycopg.errors import IoError
from psycopg.rows import TupleRow

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
    table_select_query = "SELECT * FROM %s WHERE id=%s"
    def __init__(self, **db_config):
        """
            TODO: Titles appear to be very long.
            TODO: Make better errors.
            TODO: get rid of unnecessary parameters and functions, e.g.:
            update_db etc. For example you could do *args, the first one would
            be query, the rest is batch or some other data, that should be
            passed to execute. Keep in mind to check if injection occurrs.
        """
        self._db_config: Dict[str, Any] = db_config
        self.name: str = db_config["name"] 
        self.user: str = db_config["user"] 
        self.host: str = db_config["host"] 
        self.port: int = db_config["port"]  
        self.bounds = np.array([1, -(1 << 31)], dtype=np.int32) 

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
         
        if not self.check_if_exists():
            try:
                # --- TODO: probably should make construct_query to handle some bad
                # injections etc --- # 
                self.set_tablename()
            except IOError as e:
                print(f"[ERROR] table_init(): Couldn't create given table.\n{e}")
                exit(1) 

            try:
                # --- Load movies into the database --- #
                print("[INFO] table_init(): Loading all movies.")
                csv_files = list(self._db_config["resource"].glob("*.csv")) 
                movies_data = dict() 

                if self._db_config["links"] not in csv_files:
                    print("[ERROR] links.csv wasn't found.")
                    exit(1)

                link_df = pd.read_csv(self._db_config["links"], sep=',', skiprows=0)
                for relation in link_df.itertuples(index=False, name=None):
                    movieid, imdbid, *_ = relation
                    entry = [0 for _ in range(6)]
                    entry[0] = movieid
                    entry[1] = imdbid
                    movies_data[movieid] = entry
                # --- Drop the reference --- #
                del link_df

                if self._db_config["movies"] not in csv_files:
                    print("[ERROR] movies.csv wasn't found.")
                    exit(1)

                movies_df = pd.read_csv(self._db_config["movies"], sep=',', skiprows=0)
                for relation in movies_df.itertuples(index=False, name=None):
                    movieid, title, genres = relation
                    # --- Get entry info --- #
                    entry = movies_data[movieid]
                    entry[2] = title.rstrip() 
                    entry[3] = genres.split('|') 
                    # --- Replace with new entry --- #
                    movies_data[movieid] = entry

                del movies_df

                if self._db_config["ratings"] not in csv_files:
                    print("[ERROR] ratings.csv wasn't found.")
                    exit(1)

                ratings_df = pd.read_csv(self._db_config["ratings"], sep=',', skiprows=0)
                for relation in ratings_df.itertuples(index=False, name=None):
                    _, movieid, rating, _ = relation
                    # --- Get entry info --- #
                    entry = movies_data[movieid]
                    entry[4] += rating 
                    entry[5] += 1 
                    self.bounds[1] = max(self.bounds[1], movieid)
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

    def make_query(self, info: str, query: str, **kwargs)->(TupleRow | List[TupleRow]):
        """
            Parameters:
                info: Specifies what this function does, it is used only 
                for logging to know what query is executed. 
                query: Specifies what the program will execute.
                **kwargs: Dictionary type like parameter, that should contain
                all variables that will be executed in the query. The following
                arguments are allowed (all should be in a tuple):
                'exists': str: Check if table name exists. 
                'tablename': str: Create a table.
                'batch_size': int: Get the elements with size of the batch size. 
                Those elements will be selected randomly. 
                'id': int: Get the element with given id. 
            This function connects to specified database, then executes queries
            defined in the function.
        """
        ALLOWED_QUERIES: set = {"exists", "tablename", "batch_size", "id"} 
        key, *extra = kwargs.keys()
        if key not in ALLOWED_QUERIES or len(extra) > 1:
            print(f"[ERROR] make_query(): '{kwargs}' is not handled by this function.") 
            exit(1)
        del extra

        if len(info) == 0:
            print("[WARNING] make_query(): No info provided.") 
        else:
            print(f"[INFO] make_query(): {info}")

        if len(query) == 0:
            print("[ERROR] make_query(): No query provided.")
            exit(1)

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    # TODO: For now it might work, but what if I would like to
                    # update the database? 
                    if key=="tablename":
                        tablename, *_ = kwargs[key]
                        query = query.format(tablename=tablename) 
                        cur.execute(query)
                        return (None,) 
                    elif key=="exists":
                        cur.execute(query, kwargs[key])
                        return cur.fetchone() 
                    elif key=="batch_size":
                        ret = []
                        generator = np.random.default_rng()
                        lo, hi = self.bounds
                        for _ in range(kwargs[key]):
                            id = generator.integers(low=lo, high=hi, size=1) 
                            cur.execute(query,(self._db_config["tablename"], id)) 
                            ret.append(cur.fetchone)
                        return tuple(ret)
                    elif key=="id":
                        cur.execute(query,(self._db_config["tablename"], key)) 
                        return (cur.fetchone(),) 
                    else:
                        cur.execute(query, kwargs[key])
                        return (cur.fetchone(),) 
                    
        except IoError as e: 
            print(f"[ERROR] make_query(): Failed to execute the query.\n{e}")

    def check_if_exists(self)->TupleRow:
        """
            Function:
            Wrapper around query for checking if given table name exists.
        """
        return self.make_query("", 
                self.table_exists_query, 
                exists=(self._db_config["tablename"],))[0]
        

    def set_tablename(self)->None:
        """
            Function:
            Wrapper around query for setting a tablename.
        """
        self.make_query("Table doesn't exist, making one.",
                                query=self.table_init_query,
                                tablename=(self._db_config["tablename"],))


    def get_batch(self, batch_size)->(TupleRow | List[TupleRow]):
        """
            Function:
            Wrapper around query for getting a batch of {batch_size}.
        """
        return self.make_query(f"Getting random elements. [{batch_size}]", self.table_select_query,
                        batch_size=batch_size) 
        
    def get_by_id(self, id: int)->(TupleRow | List[TupleRow]):
        """
            Function:
            Wrapper around query for getting a random element.
        """
        return self.make_query(f"Getting a random element.", self.table_select_query,
                        id=id) 

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
