import asyncio
import sys

async def get_windows_location():
    import winrt.windows.devices.geolocation as geolocation
    access_status = await geolocation.Geolocator.request_access_async()

    # 2. Check if Windows allows Python to access location
    if access_status != geolocation.GeolocationAccessStatus.ALLOWED:
        print("Access denied! You need to allow location access in Windows settings.")
        return

    # 3. Initialize the geolocator
    locator = geolocation.Geolocator()

    try:
        print("Fetching exact coordinates... (this might take a few seconds)")

        # 4. Wait for Windows to pinpoint the location
        pos = await locator.get_geoposition_async()

        # 5. Extract the data
        lat = pos.coordinate.point.position.latitude
        lon = pos.coordinate.point.position.longitude
        accuracy = pos.coordinate.accuracy  # Tells you how precise the reading is

        print("\n--- Location Found ---")
        print(f"Latitude: {lat}")
        print(f"Longitude: {lon}")
        print(f"Accuracy: within {accuracy} meters")

        return True,lat, lon

    except Exception as e:
        print(f"Failed to get location: {e}")
        return False,"-","-"

def _fetch_geoclue_sync():
    import gi
    gi.require_version('Geoclue', '2.0')
    from gi.repository import Geoclue

    simple = Geoclue.Simple.new_sync(
                "python-geo-app",
                Geoclue.AccuracyLevel.EXACT,
                None)
    
    location = simple.get_location()
    return location.get_property("latitude"), location.get_property("longitude")


async def get_linux_location():
    
    try:
        lat,lon = await asyncio.to_thread(_fetch_geoclue_sync)
        print(f"Location Found: {lat}, {lon}")
        return True, lat, lon
    
    except Exception as e:
        print(f"Failed to get location: {e}")
        return False,"-","-"

async def get_location():
    if sys.platform == "win32":
        return await get_windows_location()
    elif sys.platform.startswith("linux"):
        return await get_linux_location()
    else:
        print(f"Unsupported OS: {sys.platform}")
        return False, "-", "-"