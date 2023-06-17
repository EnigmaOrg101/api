import pandas as pd
import numpy as np
import json
from sklearn.neighbors import NearestNeighbors

df_popular = pd.read_csv('./output_popular.csv')

df_copy_popular = df_popular.drop_duplicates()
df_copy_popular  = df_copy_popular[df_copy_popular['ratings'].notna()]
df_copy_popular = df_copy_popular[df_copy_popular['ratings'].apply(lambda x: x>4)]

# mean_rating = sum(df_copy_popular['no_of_reviews']) / len(df_copy_popular['no_of_reviews'])
df_copy_popular = df_copy_popular[df_copy_popular['ratings']>=4]
df_copy_popular = df_copy_popular.sort_values('ratings', ascending=False)
df_copy_popular=df_copy_popular.drop_duplicates()

df_copy_popular['location'] = list(zip(df_copy_popular.latitude, df_copy_popular.longitude))

def recommend_places(coordinates, hotels, k):
    X = hotels

    # Create a NearestNeighbors instance
    nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(X)

    # # Find the k nearest neighbors to the given coordinates
    distances, indices = nbrs.kneighbors([coordinates])
    # print(distances)
    # # Get the indices of the k nearest hotels
    nearest_hotel_indices = indices[0]
    # print(nearest_hotel_indices)
    
    # distances, indices = nbrs.kneighbors([coordinates], n_neighbors=k+1)

    # Get the indices of the k nearest hotels with different distances
    # unique_distances, unique_indices = np.unique(distances[0], return_index=True)
    # nearest_hotel_indices = indices[0][unique_indices[1:k+1]]  # Exclude the first index since it corresponds to the given coordinates

    # Retrieve the corresponding hotels
    nearest_hotels = [hotels[index] for index in nearest_hotel_indices]
    # nearest_hotels = [hotels[803], hotels[1045], hotels[971]]
    # print(nearest_hotels)
    # print(hotels[803])
    # nearest_hotels_name = 
    return nearest_hotels

# Example usage
given_coordinates = (27.69968054367523,85.32814110662525 )  # Replace with your given coordinates
# coordinates_list = [(45.189, -63.170), (48.696, -68.167), (45.200, -63.161), (44.200, -60.160),(42.00, -62.150)]  # Replace with your list of hotel coordinates
# print(type(coordinates_list[0]))
coordinates_column = df_copy_popular['location'].values
# print(type(coordinates_column[0]),type(eval(coordinates_column[0])) )
hotel_list = [coord for coord in coordinates_column]
# coordinates_list = [tuple(map(float, coord.strip('()').split(','))) for coord in coordinates_column]

# hotel_list = [(coord) for coord in coordinates_list]
# print(hotel_list)
# print(hotel_list)
k = 5 # Number of nearest hotels to recommend

nearest_hotels = recommend_places(given_coordinates, hotel_list, k)

# print(nearest_hotels)

# #   for hotel in nearest_hotels:
# #     print(hotel,type(hotel))

# nearest_hotels_json = []
# for hotel in nearest_hotels:
#     hotel_json = {
#         "latitude": hotel[0],
#         "longitude": hotel[1]
#     }
#     nearest_hotels_json.append(hotel_json)

# # Specify the file path to save the JSON data
# json_file_path = 'nearest_hotels.json'

# # Write the JSON data to the file
# with open(json_file_path, 'w') as json_file:
#     json.dump(nearest_hotels_json, json_file)

# print("Nearest hotels saved to", json_file_path)

# hotels = []
# i = 0
# for hotel in nearest_hotels:
#     match = df_copy_popular[(df_copy_popular['latitude'] == hotel[0]) & (df_copy_popular['longitude'] == hotel[1])]
#     if not match.empty:
#         hotel_info = {
#             "latitude": hotel[0],
#             "longitude": hotel[1],
#             "name": match['name'].values[0],  # Assuming the DataFrame has a column named 'hotel_name'
#             "rating": match['ratings'].values[0],  # Assuming the DataFrame has a column named 'ratings'
#             # Add more hotel information as needed
#         }
#         hotels.append(hotel_info)
#     i += 1

# print(hotels)