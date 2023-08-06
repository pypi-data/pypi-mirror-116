from flask_restful_helper import Manager

from apps.frontend.models import model


class Menu(Manager):
    _model = model.Menu
