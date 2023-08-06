from plover.system.english_stenotype import *

SUFFIX_KEYS = ()

ORTHOGRAPHY_RULES = [
    (r'^(.*(?:[bcdfghjklmnprstvwxyz]|qu)[aeiou])([bcdfgklmnprtvz]) \^ (([aeiouy]|[aei]e|[eo]i)(?:[bcdfghjklmnpqrstvwxyz].?)?)$', r'\1\2\2\3'),
    (r'^(.*(?:[bcdfghjklmnprstvwxyz]|qu)[aeiou])([bcdfgklmnprtvz]) \^ ([ei]?ous)$', r'\1\2\2\3'),
    (r'^(.*(?:[bcdfghjklmnprstvwxyz]|qu)[aeiou])([bcdfgklmnprtvz]) \^ ([ai]ble)$', r'\1\2\2\3'),
    (r'^(.*(?:[bcdfghjklmnprstvwxyz]|qu)[aeiou])([bcdfgklmnprtvz]) \^ ([ae]nce)$', r'\1\2\2\3'),
    (r'^(.*(?:[bcdfghjklmnprstvwxyz]|qu)[aeiou])([bcdfgklmnprtvz]) \^ (e[rn]ing)$', r'\1\2\2\3'),
    (r'^(.*(?:[bcdfghjklmnprstvwxyz]|qu)[aeiou])([bcdfgklmnprtvz]) \^ (ation)$', r'\1\2\2\3'),
    (r'^(.*(?:[bcdfghjklmnprstvwxyz]|qu)[aeiou])([bcdfgklmnprtvz]) \^ (iness)$', r'\1\2\2\3'),
    (r'^(.*(?:[bcdfghjklmnprstvwxyz]|qu)[aeiou])([bcdfgklmnprtvz]) \^ (ably)$', r'\1\2\2\3'),
    (r'^(.*(?:[bcdfghjklmnprstvwxyz]|qu)[aeiou])([bcdfgklmnprtvz]) \^ (ened)$', r'\1\2\2\3'),
    (r'^(.*(?:[bcdfghjklmnprstvwxyz]|qu)[aeiou])([bcdfgklmnprtvz]) \^ (ings)$', r'\1\2\2\3'),
]

ORTHOGRAPHY_RULES_ALIASES = {}

ORTHOGRAPHY_WORDLIST = 'american_english_words.txt'