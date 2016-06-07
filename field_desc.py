from peewee import Field


class FieldDesc:
    def __init__(self, name: str, python_type: type, db_field: Field, compiled_reg_exp):
        self.name = name
        self.python_type = python_type
        self.db_field = db_field
        self.compiled_reg_exp = compiled_reg_exp
