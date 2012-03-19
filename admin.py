from mmedia.models import Video, Audio, Image
from django.contrib import admin

"""
Arquivo de configuracao e customizacao da interface administrativa do Django.
"""

admin.site.register(Audio)
admin.site.register(Video)
admin.site.register(Image)
