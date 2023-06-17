import numpy as np
import pandas as pd
from fastapi import FastAPI
from typing import List, Dict, Union
from popularityBased import recommend_places, given_coordinates, hotel_list, df_copy_popular
from contentBased import content_recommend
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/recommend_hotels", response_model=List[Dict[str, Union[str, str]]])
def recommend_hotels_endpoint() -> List[Dict[str, Union[str, str]]]:
    all_hotels_json = []
    for hotel in df.values:
        hotel_info = {
            "latitude": f"{hotel[1]:.20f}",
            "longitude": f"{hotel[2]:.20f}",
            "name": str(hotel[0]),
            "rating": f"{hotel[3]:.2f}",
            "hotel type": str(hotel[5]),
            "small_photo": str(hotel[6]),
            "price": str(hotel[7]),
            "category": str(hotel[12]),
            # Add more hotel information as needed
        }
        all_hotels_json.append(hotel_info)
    return all_hotels_json

@app.get("/recommend_popular/{k}", response_model=List[Dict])
def recommend_hotels_endpoint(k: int) -> List[Dict]:

    # Call the existing recommend_hotels function
    popular_place = recommend_places(given_coordinates, hotel_list, k)

    place_json = []
    for hotel in popular_place:
        match = df_copy_popular[(df_copy_popular['latitude'] == hotel[0]) & (df_copy_popular['longitude'] == hotel[1])]
        if not match.empty:
            hotel_info = {
                "latitude": hotel[0],
                "longitude": hotel[1],
                "name": match['name'].values[0],  # Assuming the DataFrame has a column named 'hotel_name'
                "rating": match['ratings'].values[0],  # Assuming the DataFrame has a column named 'ratings'
                # Add more hotel information as needed
            }
            place_json.append(hotel_info)
    # print(nearest_hotels_json)
    # Return the recommendations as the API response
    return place_json

@app.get("/recommend_content", response_model=List[Dict])
def recommend_hotels_endpoint() -> List[Dict]:

    content_places = content_recommend().values

    content_place_json = []
    for place in content_places:
        place_info = {
            "latitude": place[2],
            "longitude": place[3],
            "name": place[1],  # Assuming the DataFrame has a column named 'hotel_name'
            "rating": place[4],
            "type": place[5],
            "small_photo": place[6],
            "category": place[7],
            # Add more hotel information as needed
        }
        content_place_json.append(place_info)

    return content_place_json

if __name__ == "__main__":
    port = int(getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=8000)