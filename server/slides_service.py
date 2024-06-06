from googleapiclient.discovery import build
from translate_service import translate_text
import requests
from PIL import Image, ImageDraw, ImageFont
import easyocr
import cv2
import os
from drive_service import get_creds, upload_image_to_drive, get_image_link
from font_service import filterFonts
import math
import numpy as np

def process_presentation(file_id, selected_language, language_name):
    creds = get_creds()
    slide_service = build("slides", "v1", credentials=creds)
    presentation = slide_service.presentations().get(presentationId=file_id).execute()
    slides = presentation.get("slides")

    slide_requests = []
    target_language = selected_language

    for slide in slides:
        for element in slide.get("pageElements", []):
            if 'shape' in element and 'text' in element['shape']:
                objectID = element['objectId']
                for text_element in element['shape']['text']['textElements']:
                    if 'textRun' in text_element:
                        text = text_element['textRun']['content']
                        translated_text = translate_text(text, target_language)
                        slide_requests.append({
                            "replaceAllText": {
                                "replaceText": translated_text,
                                "containsText": {
                                    "text": text,
                                    "matchCase": False
                                }
                            }
                        })

            if 'image' in element:
                objectID = element['objectId']
                image_url = element['image']['contentUrl']
                image_path = download_image(image_url)

                img_check = Image.open(image_path)
                
                if(img_check.format =='GIF'):
                    continue


                if image_path:
                    img_array = process_image(image_path, target_language)
                    if img_array:
                        edited_image_path = edit_image(image_path, img_array, language_name)
                        photo_id = upload_image_to_drive(edited_image_path)
                        web_content_link = get_image_link(photo_id)
                        slide_requests.append({
                            "replaceImage": {
                                "imageObjectId": objectID,
                                "imageReplaceMethod": "CENTER_INSIDE",
                                "url": web_content_link
                            }
                        })

    if slide_requests:
        body = {"requests": slide_requests}
        slide_service.presentations().batchUpdate(presentationId=file_id, body=body).execute()

def download_image(url):
    image_path = os.path.join(os.getcwd(), 'downloaded_image.jpg')
    with open(image_path, 'wb') as f:
        f.write(requests.get(url).content)
    return image_path if os.path.exists(image_path) else None

def process_image(image_path, target_language):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    img_array = []

    for (bbox, text, prob) in result:
        translated_text = translate_text(text, target_language)
        img_array.append({'bbox': bbox, 'translated_text': translated_text, 'text': text, 'prob': prob})
        print({'bbox': bbox, 'translated_text': translated_text, 'text': text, 'prob': prob})
    return img_array

def edit_image(image_path, array, language_name):
    im = Image.open(image_path)
    for i in array:
        if (i['translated_text'] == i['text']):
            continue
        if ((i['bbox'][2][0] < i['bbox'][0][0]) or (i['bbox'][2][1] < i['bbox'][0][1])):
            break
        else:
            crop_img = im.crop((i['bbox'][0][0],i['bbox'][0][1], i['bbox'][2][0], i['bbox'][2][1]))
        top_left_pixel = crop_img.getpixel((0, 0))
        
        
        
        if(len(top_left_pixel) >3):
            background = top_left_pixel
        else:
            background = top_left_pixel + (255,) 
        print("top_left_pixel", top_left_pixel)
        print("background", background)

        height = i['bbox'][2][1] - i['bbox'][0][1]
        width = i['bbox'][2][0] - i['bbox'][0][0]

        if (height < 0):
            break
        if (width < 0):
            break

        translated_segment = Image.new('RGBA',(int(width), int(height)), background )
        draw = ImageDraw.Draw(translated_segment)

        gray_background = cv2.cvtColor(np.uint8([[background]]), cv2.COLOR_BGR2GRAY)[0][0]

        if gray_background < 128:
            text_color = (255,255,255, 255)
        else:
            text_color = ( 0,0 ,0 ,255)
        
        text_size = int(height * (1/1.7))

        font_link = filterFonts(language_name)
        fnt = ImageFont.truetype(font_link,text_size)
        draw.text((0,0), i['translated_text'] , font=fnt, fill=text_color)

        Image.Image.paste(im, translated_segment, (int(i['bbox'][0][0]),int(i['bbox'][0][1]), int(i['bbox'][2][0]), int(i['bbox'][2][1])))
    if(im.mode =='RGBA'):
        edited_image_path = "edited_image.png"
    else:
        edited_image_path = "edited_image.jpg"
    im.save(edited_image_path)
    return edited_image_path


