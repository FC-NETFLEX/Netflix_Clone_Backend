from model_bakery.recipe import Recipe

from members.models import Profile

profile_kids = Recipe(
    Profile,
    is_kids=True
)

profile = Recipe(
    Profile,
    is_kids=False
)
