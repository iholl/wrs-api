import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

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
  data = db_cursor.execute("SELECT * FROM sightings WHERE ndow_id='{}';".format(id))
  if not data:
    raise HTTPException(status_code=404, detail="sighting not found")
  else:
    return db_cursor.fetchall()
    