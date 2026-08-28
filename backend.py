import sqlite3
import pandas as pd
import skyfield
from skyfield.api import load
from skyfield.api import Star, load
from skyfield.data import hipparcos
from skyfield.api import wgs84
from timezonefinder import TimezoneFinder
from datetime import datetime
from zoneinfo import ZoneInfo
import asyncio
import location

status,lat,lon= asyncio.run(location.get_windows_location())#[lat,lon]

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)

planets = load('de421.bsp')
earth = planets['earth']

ts = load.timescale()
t = ts.now()

#22.36504286515413,88.43000192857329
#idx_time ON observation(utc_start_time)
#idx_location ON observation(latitude, longitude)

'''observation table structure
            Observation_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time_from TEXT,
            time_to TEXT,
            latitude REAL,
            longitude REAL,
            light_pollution integer,
            weather TEXT,
            azimuth float,
            altitude float,
            direction TEXT,
            brightness TEXT,
            utc_start_time TEXT,
            hip_id INTEGER
'''

'''stars=pd.read_csv("stars.csv")
name_stars=stars[stars['proper'].notna()]
#db=sqlite3.connect('stellar diary.db')
print(name_stars.shape)
name_stars.to_csv('name stars.csv',index=False)
#db.close()
print("Fuck")

db=sqlite3.connect('stellar diary.db')
mc=db.cursor()
mc.execute("PRAGMA table_info(Observation);")'''

logs=[]
catch=[]
db = sqlite3.connect('stellar diary.db')
mc = db.cursor()

tf = TimezoneFinder()

def add(hip_id,date,timef,timet,latitude,longitude,light_pollution,weather,direction,brightness,time_zone):
    # correcting the format and telling its zone
    dt=datetime.strptime(f"{date} {timef}", "%d-%m-%Y %H:%M").replace(tzinfo=ZoneInfo(time_zone))

    #az,alt finding
    a = Star.from_dataframe(df.loc[hip_id])
    loc = earth + wgs84.latlon(latitude, longitude, elevation_m=43)
    astro = loc.at(ts.from_datetime(dt)).observe(a)
    app = astro.apparent()
    alt, az, distance = app.altaz()

    #finalizing data
    alt_deg,az_deg=round(alt.degrees,4),round(az.degrees,4)
    latitude,longitude=round(latitude,3),round(longitude,3)
    dt=dt.astimezone(ZoneInfo("UTC")) #UTC time
    dt = dt.strftime("%Y-%m-%d %H:%M:%S")

    if [date,alt_deg,az_deg] in catch:
        return False

    '''mc = db.cursor()
    mc.execute(f"SELECT * FROM star_info WHERE hip={hip_id}")
    n=mc.fetchone()
    print(n)
    n=n[7]'''

    catch.append([date,alt_deg,az_deg])
    logs.append([hip_id,date,timef,timet,latitude,longitude,light_pollution,weather,az_deg,alt_deg,direction,brightness,dt])
    print(hip_id,date,timef,timet,latitude,longitude,light_pollution,weather,az,alt,direction,brightness,dt)

    return True

def save():
    insert_query = """
                   INSERT INTO observation (hip_id,date, time_from, time_to, latitude, longitude, 
                                            light_pollution, weather, azimuth, altitude, 
                                            direction, brightness, utc_start_time) 
                   VALUES (? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   """

    for log in logs:
        mc.execute(insert_query, log)
    db.commit()

def get_location():
    if status:
        return lat, lon, tf.timezone_at(lat=lat, lng=lon)
    else:
        return "--","--","--"

def star_name():
    mc.execute("SELECT proper FROM star_info WHERE proper not NUll order by proper")
    n = mc.fetchall()
    return [i[0] for i in n]

def find_hip(x):
    i= "SELECT hip FROM star_info WHERE proper = ? "
    mc.execute(i,(x,))
    r= mc.fetchone()
    return str(r[0])[0:-2] if r else None

def sname(hip):
    i = "SELECT proper FROM star_info WHERE hip = ? "
    mc.execute(i, (hip,))
    r = mc.fetchone()
    if r is None:
        return ""

    pname= r[0]
    if pname is None:
        return ""
    else:
        return pname
