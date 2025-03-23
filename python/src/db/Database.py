from typing import Dict, Any, List, Tuple
import psycopg
import pandas as pd
import numpy as np
import math
import tomllib
from pathlib import Path
from psycopg.abc import Query
from utils.enums import Actions
from psycopg.rows import TupleRow


class Database:
    cls_name = "MovieDB"
    # TODO: Add logging

    def __init__(self, **db_config):
        """
        TODO: Titles appear to be very long.
        """

        with open(Path("resource/queries.toml"), "rb") as toml:
            queries = tomllib.load(toml)

        self._db_config: Dict[str, Any] = db_config
        self.name: str = db_config["name"]
        self.user: str = db_config["user"]
        self.host: str = db_config["host"]
        self.port: int = db_config["port"]
        self.queries: Dict = queries["POSTGRES_QUERIES"]
        self.bounds = np.array([1, -(1 << 31)], dtype=np.int32)

    def table_init(self) -> None:
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
                self.set_tablename()
            except ValueError | psycopg.DatabaseError as e:
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

                link_df = pd.read_csv(self._db_config["links"], sep=",", skiprows=0)
                for idx, relation in enumerate(
                    link_df.itertuples(index=False, name=None)
                ):
                    """
                        IDs provided in the csv seems to be incorrect.
                    """
                    _, imdbid, *_ = relation
                    entry = [0 for _ in range(6)]
                    entry[0] = idx
                    entry[1] = imdbid
                    movies_data[idx] = entry
                    self.bounds[1] = max(self.bounds[1], idx)
                # --- Drop the reference --- #
                del link_df

                if self._db_config["movies"] not in csv_files:
                    print("[ERROR] movies.csv wasn't found.")
                    exit(1)

                movies_df = pd.read_csv(self._db_config["movies"], sep=",", skiprows=0)
                for idx, relation in enumerate(
                    movies_df.itertuples(index=False, name=None)
                ):
                    """
                    From now on, thanks to the previous loop, the IDs are
                    correct.
                    """
                    _, title, genres = relation
                    # --- Get entry info --- #
                    entry = movies_data[idx]
                    entry[2] = title.rstrip()
                    entry[3] = sorted(genres.split("|"))
                    # --- Replace with new entry --- #
                    movies_data[idx] = entry

                del movies_df
                """
                For now there is no real reason to use this, because csv, with
                ratings is pretty bugged. we will render random ratings.
                """
                for idx in range(self.bounds[1]):
                    nratings = np.random.randint(0, 100, size=1)
                    ratings_sum = sum(
                        float(math.ceil(6 * np.random.random()))
                        for _ in range(*nratings)
                    )
                    entry = movies_data[idx]
                    entry[4] = ratings_sum
                    entry[5] = int(nratings[0])
                    movies_data[idx] = tuple(entry)

                #
                # if self._db_config["ratings"] not in csv_files:
                #     print("[ERROR] ratings.csv wasn't found.")
                #     exit(1)
                #
                #
                #
                # ratings_df = pd.read_csv(
                #     self._db_config["ratings"], sep=",", skiprows=0
                # )
                # print(ratings_df)
                # for idx, relation in enumerate(
                #     ratings_df.itertuples(index=False, name=None)
                # ):
                #     *_, rating, _ = relation
                #     # --- Get entry info --- #
                #     entry = movies_data[idx]
                #     entry[4] += rating
                #     entry[5] += 1
                #     # --- Replace with new entry --- #
                #     movies_data[idx] = entry

                # del ratings_df
                # TODO: For now skipping the tags.csv

            except ValueError | IndexError as e:
                print(e)
                exit(1)

            try:
                with self.get_connection() as conn:
                    with conn.cursor() as cur:
                        for relation in movies_data.values():
                            cur.execute(self.queries["INSERT_INTO"], relation)
            except IOError as e:
                print(e)
                exit(1)
            print("[INFO] table_init(): Movies loaded successfully.")
            return

        # For more readibility, could be else
        if self.check_if_exists():
            try:
                with self.get_connection() as conn:
                    with conn.cursor() as cur:
                        CHECK_ROWS = self.queries["CHECK_NUMBER_OF_ROWS"].format(
                            tablename=self._db_config["tablename"]
                        )
                        cur.execute(CHECK_ROWS)
                        fetched = cur.fetchone()
                        assert fetched is not None, (
                            "[ERROR] table_init(): Fetched row is None"
                        )
                        assert fetched[0] > 0, (
                            "[ERROR] table_init(): Your database is not initialized"
                        )
                        self.bounds[1] = fetched[0]
                        CHECK_COLS = self.queries["CHECK_NUMBER_OF_COLS"].format(
                            tablename=self._db_config["tablename"]
                        )
                        cur.execute(CHECK_COLS)
                        fetched = cur.fetchone()
                        assert fetched is not None, (
                            "[ERROR] table_init(): Fetched column is None"
                        )
                        assert fetched[0] > 0, (
                            "[ERROR] table_init(): Your database is not initialized"
                        )
                print("[INFO} table_init(): Your database passed light test.")
                return
            except psycopg.DatabaseError | psycopg.ProgrammingError | ValueError as e:
                print(e)
                exit(1)

    def make_query(
        self, info: str, query: Query, **kwargs
    ) -> TupleRow | List[TupleRow]:
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
        if key not in ALLOWED_QUERIES:
            print(f"[ERROR] make_query(): '{kwargs}' is not handled by this function.")
            exit(1)

        if len(info) == 0:
            print("[WARNING] make_query(): No info provided.")
        else:
            print(f"[INFO] make_query(): {info}")

        if len(query) == 0:
            print("[ERROR] make_query(): No query provided.")
            return (None,)

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    match key:
                        case "tablename":
                            tablename, *_ = kwargs[key]
                            query = query.format(tablename=tablename)
                            cur.execute(query)
                            return (None,)
                        case "exists":
                            cur.execute(query, kwargs[key])
                            fetched = cur.fetchone()
                            return (False,) if fetched is None else fetched
                        case "batch_size":
                            genres, *_ = extra
                            cur.execute(query, (list(kwargs[genres]),))
                            cands: List[TupleRow] = cur.fetchall()
                            np.random.shuffle(cands)
                            sz = min(kwargs[key], len(cands) - 1)
                            cands = cands[:sz]
                            fetched_final = tuple(
                                tuple(
                                    tuple(item) if isinstance(item, List) else item
                                    for item in cand
                                )
                                for cand in cands
                            )
                            return fetched_final
                        case "id":
                            cur.execute(query, (kwargs["id"],))
                            fetched = cur.fetchone()
                            if fetched is None:
                                return (None,)
                            fetched_final = tuple(
                                tuple(item) if isinstance(item, List) else item
                                for item in fetched
                            )

                            return fetched_final
                        case _:
                            raise ValueError("[ERROR] make_query(): Unhandled query.")
        except ValueError | psycopg.InternalError as e:
            print(f"[ERROR] make_query(): Failed to execute the query.\n{e}")

    def check_if_exists(self) -> TupleRow:
        """
        Function:
        Wrapper around query for checking if given table name exists.
        """
        return self.make_query(
            "", self.queries["SELECT_EXISTS"], exists=(self._db_config["tablename"],)
        )[0]

    def set_tablename(self) -> None:
        """
        Function:
        Wrapper around query for setting a tablename.
        """
        self.make_query(
            "Table doesn't exist, making one.",
            query=self.queries["CREATE_TABLE"],
            tablename=(self._db_config["tablename"],),
        )

    def get_batch(
        self, genres: Tuple | List, action: Actions
    ) -> TupleRow | List[TupleRow]:
        """
        Function:
        Wrapper around query for getting a batch of {batch_size}.
        """
        query = (
            self.queries["SELECT_IF_UPVOTE"]
            if action == Actions.UPVOTE
            else self.queries["SELECT_IF_DOWNVOTE"]
            if action == Actions.DOWNVOTE
            else None
        )

        if query is None:
            return (None,)

        query = query.format(tablename=self._db_config["tablename"])
        return self.make_query(
            f"Getting random elements. [{self._db_config['batch_size']}]",
            query,
            batch_size=self._db_config["batch_size"],
            genres=genres,
        )

    def get_by_id(self, id: int) -> TupleRow | List[TupleRow]:
        """
        Function:
        Wrapper around query for getting a random element.
        """
        return self.make_query(
            f"Getting an element with id={id}.", self.queries["GET_BY_ID"], id=id
        )

    def get_random_entry(self) -> TupleRow | List[TupleRow]:
        lo, hi = self.bounds
        id = int(*np.random.randint(low=lo, high=hi, size=1))
        query = self.queries["GET_BY_ID"].format(tablename=self._db_config["tablename"])
        return self.make_query(
            "Getting a random element.",
            query,
            id=id,
        )

    def get_connection(self):
        try:
            conn = psycopg.connect(
                dbname=self.name, user=self.user, host=self.host, port=self.port
            )
            return conn
        except psycopg.errors.ConnectionTimeout as e:
            print(e)
            exit(1)

    def __repr__(self):
        rows = {
            "name": self.name,
            "user": self.user,
            "host": self.host,
            "port": str(self.port),
        }

        max_length = max(len(f"{key}: {value}") for key, value in rows.items())

        title = f" {self.cls_name} "
        half_padding = (max_length - len(title)) // 2
        header = f"{'=' * half_padding}{title}{'=' * half_padding}"
        header = header.ljust(max_length, "=")

        formatted_rows = [
            f"{key}: {str(value).rjust(max_length - len(key) - 2)}"
            for key, value in rows.items()
        ]
        return f"{header}\n" + "\n".join(formatted_rows) + f"\n{'=' * len(header)}"
