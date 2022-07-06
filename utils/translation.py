import requests
import os

from googletrans import Translator

from utils.language import fix_language_to_lexicala, fix_language_to_google

headers = {
    "X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
    "X-RapidAPI-Host": "lexicala1.p.rapidapi.com"
}

translator = Translator()


def get_lexical_definitions(word, word_language, language):
    word_language = fix_language_to_lexicala(word_language)
    language = fix_language_to_google(language)

    url = f'https://lexicala1.p.rapidapi.com/search?source=global&language={word_language}&text={word}&analyzed=true'

    response_json = requests.request('GET', url, headers=headers).json()

    if not response_json['results']:
        return None

    definitions = []

    for result in response_json['results']:
        result_definitions = []

        for sense in result['senses']:
            sense = sense.get('definition')
            if sense:
                sense_translated = translator.translate(text=sense, dest=language).text
                result_definitions.append(sense_translated)

        headword = result['headword']['pos']
        headword_translated = translator.translate(headword, dest=language).text
        result_dict = {headword_translated: result_definitions}

        definitions.append(result_dict)

    return definitions


def get_word_meanigs(word, language_to, language):
    language_to = fix_language_to_google(language_to)
    language = fix_language_to_google(language)

    word_translated = translator.translate(text=word, dest=language_to, src=language)

    meanings = set()

    if word_translated.extra_data['possible-translations']:
        for a in word_translated.extra_data['possible-translations']:
            for c in a[2]:
                if c[0]:
                    meanings.add(c[0].capitalize())

    if word_translated.extra_data['all-translations']:
        for translations in word_translated.extra_data['all-translations']:
            for translation in translations[1]:
                meanings.add(translation.capitalize())

    return meanings


if __name__ == '__main__':
    headers = {
        "X-RapidAPI-Key": "e2d1cb271bmsh5756db474c5f250p1e8bbbjsn30ed473e7697",
        "X-RapidAPI-Host": "lexicala1.p.rapidapi.com"
    }
    # print(get_lexical_definitions('Teasdat', 'en', 'pt-br'))
    # print(get_word_meanigs('Train', 'pt-br', 'en'))
