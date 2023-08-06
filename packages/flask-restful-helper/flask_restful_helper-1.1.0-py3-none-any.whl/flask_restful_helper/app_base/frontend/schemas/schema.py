from apps.frontend.models import model
from main.extension import ma


class Menu(ma.Schema):
    class Meta:
        model = model.Menu
