import gettext

AVAILABLE_LANGUAGES = ["en", "vi"]

translators = {}
for locale in AVAILABLE_LANGUAGES:
    translator = gettext.translation("base", localedir="locales", languages=[locale])
    translator.install()
    translators[locale] = translator

DEFAULT_TRANSLATOR = translators["en"]


def T(message, locale="en", **kargs):
    translator = translators.get(locale, DEFAULT_TRANSLATOR)
    return translator.gettext(message.format(**kargs))


def _(message):
    return message
