import re

from peewee import IntegerField
from field_desc import FieldDesc


"""
This to be defined by you.
It expresses the often changing stats you want to log.
"""


adhoc_fields = (
    FieldDesc('automata_translation_sec',
              int,
              IntegerField(null=True),
              re.compile('automata translation took \(sec\): ([0-9]+)')),
    FieldDesc('parsing_building_expr',
              int,
              IntegerField(null=True),
              re.compile('parsing and building expr took \(sec\): ([0-9]+)')),
    FieldDesc('model_search_sec',
              int,
              IntegerField(null=True),
              re.compile('model_searcher\.search took \(sec\): ([0-9]+)'))
)
