from googleapiclient.discovery import build
from translate_service import translate_text
from drive_service import get_creds, upload_image_to_drive, get_image_link
from font_service import filterFonts
from PIL import Image, ImageDraw, ImageFont
import requests
import os
import easyocr
import cv2
import numpy as np
import uuid
import json

def generate_id():
    return str(uuid.uuid4())

def process_presentation(original_file_name, original_file_id, new_file_id, selected_language, language_name):
    creds = get_creds()
    slide_service = build("slides", "v1", credentials=creds)
    presentation = slide_service.presentations().get(presentationId=original_file_id).execute()
    presentation_to_translate = slide_service.presentations().get(presentationId=new_file_id).execute()
    presentation_to_translate_slides = presentation_to_translate.get("slides")
    slides = presentation.get("slides")

    '''
    for slide in presentation_to_translate_slides:
        for element in slide.get("pageElements", []):
            if 'shape' in element and 'text' in element['shape']:
                delete_request = [{
                    "deleteText" : {
                        "objectId": element["objectId"]
                    }
                }]
                slide_service.presentations().batchUpdate(presentationId=new_file_id, body={"requests": delete_request}).execute()
            else:
                delete_request = [{
                    "deleteObject" : {
                        "objectId": element["objectId"]
                    }
                }]
                slide_service.presentations().batchUpdate(presentationId=new_file_id, body={"requests": delete_request}).execute()

        '''        
    slide_count = 0
    for slide in slides:
        slide_count = slide_count+1
        print("slide count", slide_count)
        # Create a new slide in the new presentation

        # Process each element in the slide
        for element in slide.get("pageElements", []):
            
            if 'shape' in element and 'text' in element['shape']:
                delete_request = [{
                            "deleteText" : {
                                "objectId": element["objectId"],
                                "textRange": {
                                    "type": "ALL"
                                }
                            }
                        }]
                slide_service.presentations().batchUpdate(presentationId=new_file_id, body={"requests": delete_request}).execute()
                
            elif 'shape' not in element and 'elementGroup' not in element:
                delete_request = [{
                    "deleteObject" : {
                        "objectId": element["objectId"]
                    }
                }]
                slide_service.presentations().batchUpdate(presentationId=new_file_id, body={"requests": delete_request}).execute()
            process_element(slide_service, new_file_id, slide["objectId"],element, element["objectId"], selected_language, language_name)


    '''
    original_slide_masters = presentation.get("masters")
 
    original_slide_layouts = presentation.get("layouts")
 
    

    original_slide_page_size = presentation.get("pageSize")

    new_presentation_object = {
        "pageSize": original_slide_page_size,
        "title": original_file_name +"_"+ language_name,
        "masters": original_slide_masters,
        "layouts": original_slide_layouts,
        
    }

    new_slide = slide_service.presentations().create(body=new_presentation_object).execute()
    json_object = json.dumps(new_slide, indent=4)
    with open("newslide.json", "w") as outfile:
        outfile.write(json_object)
    
    new_presentation = slide_service.presentations().get(presentationId=new_slide["presentationId"]).execute() 
    new_presentation_id = new_presentation["presentationId"]
    

def create_new_slide(slide_service, presentation_id):
    slide_id = generate_id()
    requests = [{
        "createSlide": {
            "objectId": slide_id,
            "slideLayoutReference": {
                "predefinedLayout": "BLANK"
            }
        }
    }]
    slide_service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
    return slide_id
'''
def process_element(slide_service, presentation_id, slide_id, element, element_id, target_language, name_of_language):

    if 'shape' in element and 'text' in element['shape']:
        process_shape(slide_service, presentation_id, slide_id, element, element_id, target_language)
    elif 'image' in element:
        process_image_element(slide_service, presentation_id, slide_id, element, element_id, target_language, name_of_language)
    elif 'video' in element:
        process_video(slide_service, presentation_id, slide_id, element, element_id)
    elif 'line' in element:
        process_line(slide_service, presentation_id, slide_id, element, element_id)
    elif 'table' in element:
        process_table(slide_service, presentation_id, slide_id, element, element_id, target_language)
    elif 'wordArt' in element:
        process_word_art(slide_service, presentation_id, slide_id, element, element_id, target_language)
    elif 'sheetsChart' in element:
        process_sheets_chart(slide_service, presentation_id, slide_id, element, element_id)
    elif 'group' in element:
        process_group(slide_service, presentation_id, slide_id, element, target_language, name_of_language)

def process_shape(slide_service, presentation_id, slide_id, element, element_id, target_language):
    shape_type = element['shape']['shapeType']
    shape_size = element['size']
    shape_transform = element['transform']
    '''
    slide_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={
            "requests": [{
                "createShape": {
                    "objectId": element_id,
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": shape_size,
                        "transform": shape_transform
                    },
                    "shapeType": shape_type
                }
            }]
        }
    ).execute()
    '''
    for text_element in element['shape']['text']['textElements']:
        if 'textRun' in text_element:
            text = text_element['textRun']['content']
            text_style = text_element['textRun']['style']

            if text.strip():
                translated_text = translate_text(text, target_language)
                slide_service.presentations().batchUpdate(
                    presentationId=presentation_id,
                    body={
                        "requests": [{
                            "insertText": {
                                "objectId": element_id,
                                "text": translated_text
                            }},
                            {"updateTextStyle": {
                                "objectId": element_id,
                                "style": text_style,
                                "fields": "*"
                            }
                        }
                    ]}
                ).execute()

def process_image_element(slide_service, presentation_id, slide_id, element, element_id, target_language, name_of_language):
    image_url = element['image']['contentUrl']
    image_path = download_image(image_url)
    if image_path:
        img_array = process_image(image_path, target_language)
        print("img_array", img_array)

     

        if img_array:
            edited_image_path = edit_image(image_path, img_array, name_of_language)

            photo_id = upload_image_to_drive(edited_image_path)

            web_content_link = get_image_link(photo_id)

            slide_service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={
                    "requests": [{
                        "createImage": {
                            "objectId": element_id,
                            "elementProperties": {
                                "pageObjectId": slide_id,
                                "size": element['size'],
                                "transform": element['transform']
                            },
                            "url": web_content_link
                        }
                    }]
                }
            ).execute()
        else:
            photo_id = upload_image_to_drive(image_path)

            web_content_link = get_image_link(photo_id)

            slide_service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={
                    "requests": [{
                        "createImage": {
                            "objectId": element_id,
                            "elementProperties": {
                                "pageObjectId": slide_id,
                                "size": element['size'],
                                "transform": element['transform']
                            },
                            "url": web_content_link
                        }
                    }]
                }
            ).execute()


def process_video(slide_service, presentation_id, slide_id, element, element_id):
    video = element['video']
    slide_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={
            "requests": [{
                "createVideo": {
                    "objectId": element_id,
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": element['size'],
                        "transform": element['transform']
                    },
                    "source": {
                        "url": video['sourceUrl']
                    }
                }
            }]
        }
    ).execute()

def process_line(slide_service, presentation_id, slide_id, element, element_id):
    slide_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={
            "requests": [{
                "createLine": {
                    "objectId": element_id,
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": element['size'],
                        "transform": element['transform']
                    },
                    "lineCategory": element['line']['lineCategory']
                }
            }]
        }
    ).execute()

def process_table(slide_service, presentation_id, slide_id, element, element_id, target_language):
    table = element['table']
    slide_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={
            "requests": [{
                "createTable": {
                    "objectId": element_id,
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": element['size'],
                        "transform": element['transform']
                    },
                    "rows": table['rows'],
                    "columns": table['columns']
                }
            }]
        }
    ).execute()

    for row_index, row in enumerate(table['tableRows']):
        for cell_index, cell in enumerate(row['tableCells']):
            text = cell['text']['textElements'][0]['textRun']['content']
            translated_text = translate_text(text, target_language)
            slide_service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={
                    "requests": [{
                        "insertText": {
                            "objectId": element_id,
                            "cellLocation": {"rowIndex": row_index, "columnIndex": cell_index},
                            "text": translated_text
                        }
                    }]
                }
            ).execute()

def process_word_art(slide_service, presentation_id, slide_id, element, element_id, target_language):
    text = element['wordArt']['renderedText']
    translated_text = translate_text(text, target_language)
    slide_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={
            "requests": [{
                "createWordArt": {
                    "objectId": element_id,
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": element['size'],
                        "transform": element['transform']
                    },
                    "renderedText": translated_text
                }
            }]
        }
    ).execute()

def process_sheets_chart(slide_service, presentation_id, slide_id, element, element_id):
    slide_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={
            "requests": [{
                "createSheetsChart": {
                    "objectId": element_id,
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": element['size'],
                        "transform": element['transform']
                    },
                    "spreadsheetId": element['sheetsChart']['spreadsheetId'],
                    "chartId": element['sheetsChart']['chartId']
                }
            }]
        }
    ).execute()

def process_group(slide_service, presentation_id, slide_id, element, target_language, language_name):
    for el in element["group"]["children"]:
        process_element(slide_service, presentation_id, slide_id, el, target_language, language_name)

def download_image(url):
    image_path = os.path.join(os.getcwd(), 'downloaded_image.jpg')

    if os.path.exists(image_path):
        with open(image_path, 'wb') as f:
            f.write(requests.get(url).content)
        return image_path if os.path.exists(image_path) else None
    else:
        image_path = os.path.join(os.getcwd(), 'downloaded_image.png')
        with open(image_path, 'wb') as f:
            f.write(requests.get(url).content)
        return image_path if os.path.exists(image_path) else None



def process_image(image_path, target_language):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)

   

    img_array = []

    for (bbox, text, prob) in result:
        if text.strip():
            translated_text = translate_text(text, target_language)
            if (prob < 0.7):
                continue
            else:
                img_array.append({'bbox': bbox, 'translated_text': translated_text, 'text': text, 'prob': prob})
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
        #print("top_left_pixel", top_left_pixel)
        #print("background", background)

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
        #print("font_link",font_link)
        fnt = ImageFont.truetype(font_link,text_size)
        draw.text((0,0), i['translated_text'] , font=fnt, fill=text_color)
        try: 
            Image.Image.paste(im, translated_segment, (int(i['bbox'][0][0]),int(i['bbox'][0][1]), int(i['bbox'][2][0]), int(i['bbox'][2][1])))
        except ValueError: 
            continue
    if(im.mode =='RGBA'):
        edited_image_path = "edited_image.png"
    else:
        edited_image_path = "edited_image.jpg"
    im.save(edited_image_path)
    return edited_image_path



    '''
   1. print out the confidence thresholds to see what the threshold should be
   2. write a conditional that says if the confidence is less than the determined threshold from above, it shhould skip the current iteration of the loop and move on to the next one
    '''