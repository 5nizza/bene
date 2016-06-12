import re

from peewee import IntegerField
from field_desc import FieldDesc


"""
This to be defined by you.
It expresses the often changing stats you want to log.
"""


adhoc_fields = (
    FieldDesc('real_atm_convert_sec',
              int,
              IntegerField(null=True),
              re.compile('\(real\) automaton translation took \(sec\): ([0-9]+)')),
    FieldDesc('real_atm_size',
              int,
              IntegerField(null=True),
              re.compile('\(real\) automaton size is: ([0-9]+)')),
    FieldDesc('real_model_search_sec',
              int,
              IntegerField(null=True),
              re.compile('\(real\) model_searcher\.search took \(sec\): ([0-9]+)')),

    FieldDesc('unreal_atm_convert_sec',
              int,
              IntegerField(null=True),
              re.compile('\(unreal\) automaton translation took \(sec\): ([0-9]+)')),
    FieldDesc('unreal_atm_size',
              int,
              IntegerField(null=True),
              re.compile('\(unreal\) automaton size is: ([0-9]+)')),
    FieldDesc('unreal_model_search_sec',
              int,
              IntegerField(null=True),
              re.compile('\(unreal\) model_searcher\.search took \(sec\): ([0-9]+)'))
)
