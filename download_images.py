"""
    This file downloads the player pictures
    By: Tito Henry Joseph Phillip Lokuku Minga
"""
import os
import requests
import json
import asyncio


async def download_images(data):
    for item in data:
        player_name = item['player_name']

        # Create folder for player if it doesn't exist
        player_folder = os.path.join("euro_images", player_name)
        os.makedirs(player_folder, exist_ok=True)
        # if os.path.exists(player_folder):
        #     continue

        # Download club image
        club_image_url = item["club_image"]
        path_image = os.path.join(player_folder, f"{player_name}_club_image.png")
        if not os.path.exists(path_image):
            await download_image(club_image_url, path_image, player_name)
        else:
            print("File exists")

        # Download player image
        player_image_url = item["player_image"]
        path_player = os.path.join(player_folder, f"{player_name}.png")
        if not os.path.exists(path_player):
            await download_image(player_image_url, path_player, player_name)
        else:
            print("File Exists")


async def download_image(url, save_path, name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image successfully downloaded: {save_path}")
        else:
            print(f"Failed to download image. HTTP Status Code: {response.status_code}")
    except:
        print(f"Error occured - {name}")


# Load JSON data from file with UTF-8 encoding
with open('euro_images.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Download images
asyncio.run(download_images(data))

# # Return the number of players got
# items = os.listdir('euro_images')
# print(len(items))
