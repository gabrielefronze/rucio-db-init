from sqlalchemy.ext.declarative import declarative_base
BASE = declarative_base()

SCOPE_LENGTH = 25
NAME_LENGTH = 250

from uuid import uuid4 as uuid
def generate_uuid():
    return str(uuid()).replace('-', '').lower()