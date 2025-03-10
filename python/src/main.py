import argparse
from db.Database import Database
parser = argparse.ArgumentParser(
    prog='videorecs-main',
    description=f"Show user the best recommendations of movies, " 
        "using Reinforcement Learning method.",
    epilog='Use wisely (>,<)')

parser.add_argument("dbname")
parser.add_argument('username')
parser.add_argument('db_exists')
parser.add_argument('db_should_init')
args = parser.parse_args()
print(args.dbname, args.username, args.db_exists, args.db_should_init)
print("Hello world!")
db = Database(args.dbname, args.username)
db.table_init() 


