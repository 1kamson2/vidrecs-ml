import argparse
from db.Database import Database
parser = argparse.ArgumentParser(
    prog='videorecs-main',
    description=f"Show user the best recommendations of movies, " 
        "using Reinforcement Learning method.",
    epilog='Use wisely (>,<)')

parser.add_argument("dbname")
parser.add_argument('username')
args = parser.parse_args()
db = Database(args.dbname, args.username)
db.table_init() 


