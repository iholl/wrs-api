import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from decouple import config

# connection = psycopg2.connect(
#   user="fnrysdbbvtpjwi", 
#   password="9282012800a9ba7b9a33a9f47db1240e4b66a549afcbb1cd0cb38a5fea37ff20",
#   host="ec2-23-23-141-171.compute-1.amazonaws.com",
#   port="5432",
#   database="dmq87c8s22tvn"
# )

connection = psycopg2.connect(
  user=config("DATABASE_USER"), 
  password=config("DATABASE_PASSWORD"),
  host=config("DATABASE_HOST_URL"),
  port=config("DATABASE_PORT"),
  database=config("DATABASE_NAME")
)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
  db_cursor = connection.cursor(cursor_factory=RealDictCursor)
  db_cursor.execute("SELECT * FROM surveys;")
  return db_cursor.fetchall()

@app.get("/sightings/")
async def root():
  db_cursor = connection.cursor(cursor_factory=RealDictCursor)
  db_cursor.execute("SELECT * FROM sightings;")
  return db_cursor.fetchall()

@app.get("/sightings/{id}")
async def read_item(id):
  db_cursor = connection.cursor(cursor_factory=RealDictCursor)
  db_cursor.execute("SELECT * FROM sightings WHERE ndow_id='{}';".format(id))
  return db_cursor.fetchall()