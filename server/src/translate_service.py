from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language)
    return result['translatedText']

def list_languages():
    translate_client = translate.Client()

    results = translate_client.get_languages()
    
    return results
