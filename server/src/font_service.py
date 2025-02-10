import requests
from dotenv import load_dotenv
import os
from urllib.request import urlopen

load_dotenv()

font_api_key = os.getenv("FONT_API_KEY")

def filterFonts(language):
    font_service = requests.get("https://www.googleapis.com/webfonts/v1/webfonts?key="+font_api_key)

    font_array = font_service.json()
    items = font_array.get("items")

    def filterFunction(x):
        font_object = x
        if language in font_object["family"]:
            return True
        else: 
            return False

    def notoSansFilterFunction(x):
        noto_font_object = x
        if language in noto_font_object["family"] and "Noto Sans" in noto_font_object["family"]:
            return True
        else:
            return False
    noto_sans_filtered_font = list(filter(notoSansFilterFunction, items))
    filtered_fonts = list(filter(filterFunction, items))

    if (len(noto_sans_filtered_font)>0):
        link = noto_sans_filtered_font[0].get("files").get("regular")
    else:
        link = filtered_fonts[0].get("files").get("regular")

    font_request = urlopen(link)
    print("font_request", font_request)

    
    return font_request

