import tempfile

from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _

from gtts import gTTS

from flashcards.apps.core.models import UrlBase

WORD_LANGUAGES = [
    ('Arabic', 'ar'),
    ('Simplified Chinese', 'zh'),
    ('Traditional Chinese', 'zh-tw'),
    ('Czech', 'cs'),
    ('Danish', 'da'),
    ('Dutc', 'nl'),
    ('English', 'en'),
    ('French', 'fr'),
    ('German', 'de'),
    ('Greek', 'el'),
    ('Hebrew', 'iw'),
    ('Hindi', 'hi'),
    ('Italian', 'it'),
    ('Japanese', 'ja'),
    ('Korean', 'ko'),
    ('Latin', 'la'),
    ('Norwegian', 'no'),
    ('Polish', 'pl'),
    ('Portuguese', 'pt'),
    ('Portuguese Brazilian', 'pt-br'),
    ('Russian', 'ru'),
    ('Spanish', 'es'),
    ('Swedish', 'sv'),
    ('Thai', 'th'),
    ('Turkish', 'tr'),
]

DIFERENT_OPTIONS = {
    'tw': 'zh-tw',
    'dk': 'da',
    'he': 'iw',
    'br': 'pt-br'
}


class Word(UrlBase):
    word = models.CharField(_('Word'), max_length=100)
    language = models.CharField(_('Language'), max_length=2)
    audio_phonetic = models.FileField(_('Audio'), upload_to='phonetics/', null=True)

    def save(self, *args, **kwargs):
        if not self.audio_phonetic:
            audio = gTTS(text=self.word, lang=self.language, slow=True)

            with tempfile.TemporaryFile(mode='w') as file:
                audio.write_to_fp(file)
                file_name = f'{self.word}.mp3'
                self.audio_phonetic.save(file_name, File(file=file))

            super().save(*args, **kwargs)


class Meaning(models.Model):
    word = models.ForeignKey(
        Word,
        related_name='meanings',
        on_ddelete=models.CASCADE
    )
    headword = models.CharField(_('Headword'), max_length=100)
    definitions = models.TextField(_('Definitions'))

    def get_definitions(self):
        return [definition for definition in self.definitions.split('|')]
