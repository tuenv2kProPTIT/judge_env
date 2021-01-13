# from ..language import base

# from ..language.base import *
# from .test import *
try:
    from ..language.base import  CompiledLanguage
    from ..language.cpp11_gpp import *
    from ..language.python3_cpython import *
    from ..languageall import get_language,filename_to_language
except:
    from language.base import  CompiledLanguage
    from language.cpp11_gpp import *
    from language.python3_cpython import *
    from languageall import get_language,filename_to_language
# from language import Cpp11Gpp


print("test language is here")

print("test class cpp11_gpp", Cpp11Gpp())
print("test class python3",  Python3CPython())
print(filename_to_language("a.cpp"))
print(filename_to_language("a.py"))
print(filename_to_language("a.java"))
# print(get_language(filename_to_language("a.cpp")))
print("test done")
