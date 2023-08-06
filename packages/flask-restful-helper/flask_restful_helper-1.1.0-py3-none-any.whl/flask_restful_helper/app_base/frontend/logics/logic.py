from flask_restful_helper import Logic

from apps.frontend.managers import manager
from apps.frontend.schemas import schema


class Menu(Logic):
    _manager = manager.Menu
    _schema = schema.Menu
