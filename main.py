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

@app.get("/geojson")
async def root():
  db_cursor = connection.cursor(cursor_factory=RealDictCursor)
  sql = """
    SELECT ST_AsText(ST_Transform(geom, 4326)) As wgs_geom FROM sightings;

    SELECT json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(
            json_build_object(
                'type',       'Feature',
                'id',         id, 
                'geometry',   ST_AsGeoJSON(ST_Transform(geom, 4326))::json,
                'properties', json_build_object(
                  'ndow_id', ndow_id,
                  'sight_time', sight_time,
                  'species', species,
                  'id', id
                )
            )
        )
    )
    FROM sightings;
  """
  db_cursor.execute(sql)

  return db_cursor.fetchall()