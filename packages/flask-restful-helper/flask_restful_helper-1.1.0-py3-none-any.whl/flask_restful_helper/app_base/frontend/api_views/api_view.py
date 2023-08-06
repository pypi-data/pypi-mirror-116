from flask_restful_helper import ApiView

from apps.frontend.logics import logic


class Menu(ApiView):
    _logic = logic.Menu
