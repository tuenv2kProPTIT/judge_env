__all__ = [
    "LANGUAGES",
    "HEADER_EXTS", "SOURCE_EXTS", "OBJECT_EXTS",
    "get_language", "filename_to_language"
]


LANGUAGES = list()
_BY_NAME = dict()
HEADER_EXTS = set()
OBJECT_EXTS = set()
SOURCE_EXTS = set()


def get_language(name):
    """Return the language object corresponding to the given name.

    name (unicode): name of the requested language.
    return (Language): language object.

    raise (KeyError): if the name does not correspond to a language.

    """
    if name not in _BY_NAME:
        raise KeyError("Language `%s' not supported." % name)
    return _BY_NAME[name]


def filename_to_language(filename):
    """Return one of the languages inferred from the given filename.

    filename (string): the file to test.

    return (Language|None): one (arbitrary, but deterministic)
        language matching the given filename, or None if none
        match.

    """
    ext_index = filename.rfind(".")
    if ext_index == -1:
        return None
    ext = filename[ext_index:]
    names = sorted(language.name
                   for language in LANGUAGES
                   if ext in language.source_extensions)
    return None if len(names) == 0 else get_language(names[0])


def _load_languages():
    """Load the available languages and fills all other data structures."""
    if len(LANGUAGES) > 0:
        return

    for cls in plugin_list("cms.grading.languages"):
        language = cls()
        LANGUAGES.append(language)
        _BY_NAME[language.name] = language
        HEADER_EXTS.update(language.header_extensions)
        OBJECT_EXTS.update(language.object_extensions)
        SOURCE_EXTS.update(language.source_extensions)


# Initialize!
_load_languages()