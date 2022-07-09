import requests
import os
import uuid


microsoft_headers = {
    'Ocp-Apim-Subscription-Key': os.environ.get('MICROSOFT_API_KEY'),
    'Ocp-Apim-Subscription-Region': 'brazilsouth',
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

microsoft_endpoint = 'https://api.cognitive.microsofttranslator.com'


def get_word_definitions(word):
    response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')

    if response.status_code == 404:
        return None

    json = response.json()[0]

    result = {}

    for json_result in json.items():
        key, value = json_result
        if key == 'phonetics':
            for phonetics in value:
                if phonetics['audio']:
                    result['audio'] = phonetics['audio']
        if key == 'meanings':
            result_meaning = []
            synonyms = []
            for meaning in value:
                result_meaning.append(meaning)
                if meaning.get('synonyms'):
                    synonyms.extend(meaning.get('synonyms'))
            result['meaning'] = result_meaning
            result['synonyms'] = synonyms
    return result


def get_text_translated(sentence, to_language):
    sentence = sentence.strip().lower()

    path = '/translate'
    constructed_url = microsoft_endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': to_language,
    }

    request = requests.post(constructed_url, params=params, headers=microsoft_headers, json=[{'text': sentence}])

    response = request.json()

    sentence_translated = response[0]['translations'][0]['text']

    return sentence_translated


def get_word_meanigs(word, to_language):
    word = word.strip().lower()

    path = '/dictionary/lookup'

    constructed_url = microsoft_endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': to_language,
    }

    request = requests.post(constructed_url, params=params, headers=microsoft_headers, json=[{'text': word}])

    response = request.json()

    meanings = set()

    for translation in response[0]['translations']:
        meanings.add(f'{translation["normalizedTarget"]}')

    return '|'.join(meanings)


if __name__ == '__main__':
    teste = get_word_definitions('for')
    print(teste)
