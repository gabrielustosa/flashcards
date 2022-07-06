DIFERENT_OPTIONS_TO_LEXICALA = {
    'zh-tw': 'tw',
    'da': 'dk',
    'iw': 'he',
    'pt-br': 'br',
}

DIFERENT_OPTIONS_TO_GOOGLE = {
    'zh': 'zh-nc',
    'pt-br': 'pt_br',
}


def fix_language_to_google(language):
    if language in DIFERENT_OPTIONS_TO_GOOGLE.keys():
        return DIFERENT_OPTIONS_TO_GOOGLE[language]
    return language


def fix_language_to_lexicala(language):
    if language in DIFERENT_OPTIONS_TO_LEXICALA.keys():
        return DIFERENT_OPTIONS_TO_LEXICALA[language]
    return language
