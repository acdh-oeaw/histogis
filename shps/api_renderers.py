from rest_framework import renderers


class LinkedPastsRenderer(renderers.BaseRenderer):

    media_type = "application/json+linkedpasts"
    format = 'json+lp'

    def render(self, data, media_type=None, renderer_context=None):
        return data
