import tempfile

from django.conf import settings
from django.utils.text import slugify
from django.core.files.storage import default_storage

from gtts import gTTS


def get_word_phonetic(word):
    audio = gTTS(text=word, lang='en', slow=True)

    with tempfile.TemporaryFile(mode='wb+') as file:
        audio.write_to_fp(file)
        file_path = 'phonetics/' + f'{slugify(word)}.mp3'
        default_storage.save(file_path, file)

    return settings.WEBSITE_URL + 'media/' + file_path
