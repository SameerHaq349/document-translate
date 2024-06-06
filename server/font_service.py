import requests
from dotenv import load_dotenv
import os

load_dotenv()

font_api_key = os.getenv("FONT_API_KEY")

def filterFonts(language):
    font_service = requests.get("https://www.googleapis.com/webfonts/v1/webfonts?key="+font_api_key)

    font_array = font_service.json()
    items = font_array.get("items")

    def filterFunction(x):
        font_object = x
        print("font object", font_object["family"])
        if language in font_object["family"]:
            return True
        else: 
            return False

    filtered_fonts = list(filter(filterFunction, items))
    link_key = next(iter(filtered_fonts[0].get("files")))
    link = filtered_fonts[0].get("files").get(link_key)
    return link



filterFonts("Arabic")