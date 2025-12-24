from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from google.transit import gtfs_realtime_pb2

app = FastAPI()

# Allow requests from your React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # change later to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




    







@app.get("/api/buses")
def get_buses():
    try:
        response = requests.get(BC_TRANSIT_FEED)
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        buses = []
        for entity in feed.entity:
            if entity.HasField("vehicle"):
                bus = {
                    "id": entity.id,
                    "routeId": entity.vehicle.trip.route_id,
                    "latitude": entity.vehicle.position.latitude,
                    "longitude": entity.vehicle.position.longitude,
                    "bearing": entity.vehicle.position.bearing
                }
                buses.append(bus)
        return {"buses": buses}

    except Exception as e:
        return {"error": str(e)}