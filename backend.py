import sqlite3
import pandas as pd
import skyfield
from skyfield.api import load
from skyfield.api import Star, load
from skyfield.data import hipparcos
from skyfield.api import wgs84
from timezonefinder import TimezoneFinder
import asyncio
import location

status,lat,lon= asyncio.run(location.get_windows_location())#[lat,lon]

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)

planets = load('de421.bsp')
earth = planets['earth']

ts = load.timescale()
t = ts.now()


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
            brightness TEXT
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
db = sqlite3.connect('stellar diary.db')
mc = db.cursor()

tf = TimezoneFinder()

def add(hip_id,date,timef,timet,latitude,longitude,light_pollution,weather,direction,brightness):

    a = Star.from_dataframe(df.loc[hip_id])
    loc = earth + wgs84.latlon(latitude, longitude, elevation_m=43)
    astro = loc.at(ts.utc(2025, 1, 1, 20, 30, 00)).observe(a)
    app = astro.apparent()
    alt, az, distance = app.altaz()

    mc = db.cursor()
    mc.execute(f"SELECT * FROM star_info WHERE hip={hip_id}")
    n=mc.fetchone()
    print(n)
    n=n[7]

    logs.append([hip_id,date,timef,timet,latitude,longitude,light_pollution,weather,az,alt,direction,brightness])
    print(hip_id,date,timef,timet,latitude,longitude,light_pollution,weather,az,alt,direction,brightness)
    return n

def location():
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




