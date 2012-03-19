from mmedia.models import Video, Audio, Image
from django.contrib import admin

"""
Arquivo de configuração e customização da interface administrativa do Django.
"""

admin.site.register(Audio)
admin.site.register(Video)
admin.site.register(Image)
