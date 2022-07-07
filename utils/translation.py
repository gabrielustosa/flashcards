import requests
import os
import uuid

lexicala_headers = {
    "X-RapidAPI-Key": os.environ.get('LEXICALA_API_KEY'),
    "X-RapidAPI-Host": "lexicala1.p.rapidapi.com"
}

microsoft_headers = {
    'Ocp-Apim-Subscription-Key': os.environ.get('MICROSOFT_API_KEY'),
    'Ocp-Apim-Subscription-Region': 'brazilsouth',
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

microsoft_endpoint = 'https://api.cognitive.microsofttranslator.com'


def get_lexical_definitions(word, to_language):
    url = f'https://lexicala1.p.rapidapi.com/search?source=global&language=en&text={word}&analyzed=true'

    response_json = requests.request('GET', url, headers=lexicala_headers).json()

    if not response_json['results']:
        return None

    definitions = []

    for result in response_json['results']:
        result_definitions = []

        for sense in result['senses']:
            sense = sense.get('definition')
            if sense:
                sense_translated = get_text_translated(sense, to_language)
                result_definitions.append(sense_translated)

            if isinstance(result['headword'], dict):

                try:
                    headword_pos = result['headword']['pos']
                except KeyError:
                    headword_pos = 'NOUN'

                headword_text = result['headword']['text']

                headword = headword_pos.upper() + '-' + headword_text

                headword_translated = headword
                result_dict = {headword_translated: result_definitions}

                definitions.append(result_dict)

    return definitions


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
    similar = set()

    for translation in response[0]['translations']:
        for back_translation in translation['backTranslations']:
            if back_translation['normalizedText'] != word:
                similar.add(back_translation['normalizedText'])
        meanings.add(f'{translation["normalizedTarget"]}')

    return meanings, '|'.join(similar)


if __name__ == '__main__':
    print(get_lexical_definitions('Think', 'pt-br'))
    print(get_word_meanigs('Think', 'pt-br'))
