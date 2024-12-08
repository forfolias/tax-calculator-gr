import os
import gettext


def setup_translations(domain='messages'):
    lang = os.getenv("LANG", "en").split("_")[0]
    locales_dir = os.path.join(os.path.dirname(__file__), "locales")
    translation = gettext.translation(domain, localedir=locales_dir, languages=[lang], fallback=True)

    translation.install()

    return translation.gettext


_ = setup_translations()
