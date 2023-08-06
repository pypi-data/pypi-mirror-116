from plover.system.english_stenotype import *

SUFFIX_KEYS = ()
ORTHOGRAPHY_RULES_ALIASES = {}
ORTHOGRAPHY_WORDLIST = None

ORTHOGRAPHY_RULES = [
    (r'^(.*(?:[bcdfghjklmnprstvwxyz]|qu)[aeiou])([bcdfgklmnprtvz]) \^ ([aeiouy].*)$', r'\1\2\2\3'),
]