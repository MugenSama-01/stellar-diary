import asyncio
import winrt.windows.devices.geolocation as geolocation

async def get_windows_location():
    # 1. Request permission from Windows
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