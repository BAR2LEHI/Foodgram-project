import io
import csv
from rest_framework import renderers

RECIPE_SHOP_LIST_DATA = ['id', 'name', 'description']


class TxtREnder(renderers.BaseRenderer):

    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        text_buffer = io.StringIO()
        text_buffer.write(' '.join(header for header in RECIPE_SHOP_LIST_DATA) + '\n')
        for recipe in data:
            text_buffer.write(' '.join(str(sd) for sd in list(recipe.values())) + '\n')
        return text_buffer.getvalue()
