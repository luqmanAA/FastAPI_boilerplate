from datetime import datetime
from json import JSONEncoder
from ..accounts.models import Role


class RoleEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Role):
            return obj.__dict__
        return super().default(obj)
    
from sqlalchemy.ext.declarative import DeclarativeMeta

class TicketJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # If the object is an SQLAlchemy model, extract its dictionary representation
            return obj.__dict__
        elif isinstance(obj, datetime):
            # If the object is a datetime, convert it to a string
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)

# Use the custom encoder when converting to JSON
# json_data = json.dumps(your_data, cls=RoleEncoder)
