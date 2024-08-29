from google.cloud import translate_v2 as translate
import deepl
from dotenv import load_dotenv
import os

load_dotenv()
'''
translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))

def first_translation(first_iteration, target_language):
    result = translator.translate_text(first_iteration, target_lang=target_language)

    return result.text

def translate_text(text, target_language):
    print("text", text)
    print("target", target_language)
    result = translator.translate_text(text, target_lang=target_language)

    final_result = first_translation(result.text, target_language)

    return final_result
    '''
'''
load_dotenv()

def translate_text(text, target_language):

    client = OpenAI()
    text_to_translate = text
    language_to = target_language

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a language translator. If there's nothing to translate, don't respond with anything, only respond with a translation."},
            {"role": "user", "content": "translate '" + text_to_translate + "' to " + language_to + " without quotation marks"}
        ]
    )

    print("respons: ", response.choices[0].message.content)
    return response.choices[0].message.content

def list_languages():
    translate_client = translate.Client()

    results = translate_client.get_languages()
    
    return results

'''


def translate_text(text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language)
    return result['translatedText']

def list_languages():
    translate_client = translate.Client()

    results = translate_client.get_languages()
    
    return results
