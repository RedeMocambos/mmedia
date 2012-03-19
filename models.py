from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core import serializers

import os
import logging

"""
Modelos da aplicacao Django. 

Neste arquivo sao definidos os modelos de dados da aplicacao *mmedia*.
"""


logger = logging.getLogger(__name__)

def _path(instance):
    """Constroe o caminho (path) do arquivo relativo a um objeto *mmedia*, retorna o caminho (path) do arquivo."""
    return os.path.join(settings.MEDIA_ROOT, instance.user.username, \
                            instance.filename)

def _path_to_upload(instance, filename):
    """Constroe o caminho (path) para armazenar o arquivo relativo a um objeto *mmedia*, retorna o caminho (path) para armazenar o arquivo."""
    # TODO: Next release should manage gin annex directory dynamically
    return os.path.join(settings.GITANNEX_DIR, settings.PORTAL_NAME, instance.author.username, instance.mediatype, filename)

def createObjectFromFiles():
    """Recria os objetos em Django a partir dos objetos serializados"""
    pass


class MMedia(models.Model):
    """Classe abstrata com o modelo geral dos objetos multimediais.
    
    Atributos:
        title: nome do conteudo multimedial
        description: descricao do conteudo multimedial
        author: chave externa (agregacao) para objeto *User*
        date: data de publicacao
        fileref: apontador para o arquivo no disco (objeto FileField)
        mediatype: etiqueta para definir o tipo de conteudo
    """

    def __init__(self, *args, **kwargs):
        super(MMedia, self).__init__(*args, **kwargs)

    title = models.CharField(_('title'), max_length=120)
    description = models.TextField(_('description'), blank=True)
    author = models.ForeignKey(User)
    date = models.DateTimeField(_('release date'), blank=True, null=True)
    fileref = models.FileField(upload_to=_path_to_upload)
    mediatype = "mmedia"
#    tags = TagField(verbose_name=_('tags'), help_text=tagfield_help_text)

    def path(self):
        """Constroe o caminho (path) absoluto do arquivo do objeto, retorna o caminho (path) absoluto do arquivo em disco do objeto."""
        return os.path.join(settings.MEDIA_ROOT, settings.GITANNEX_DIR, settings.PORTAL_NAME, self.author.username, self.mediatype, \
                                self.fileref.path)

    def path_relative(self):
        """Constroe o caminho (path) relativo do arquivo do objeto, retorna o caminho (path) relativo do arquivem disco do objeto."""
        return os.path.join(settings.GITANNEX_DIR, settings.PORTAL_NAME, self.author.username, self.mediatype, \
                                self.fileref.path)

    def __unicode__(self):
        return self.title
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Sobrescreve (override) a funcao generica *save()* incluindo a serializacao do objeto.
        
        Serializa o objeto em XML na pasta /MEDIA_ROOT/GITANNEX_DIR/PORTAL_NAME/SERIALIZED_DIR/
        """
        logger.debug(type(self))
        serializeTo = os.path.join(settings.MEDIA_ROOT, settings.GITANNEX_DIR,\
                                       settings.PORTAL_NAME, settings.SERIALIZED_DIR,\
                                       os.path.basename(self.fileref.path) + '.xml')
        logger.info('>>>> Serialize to: ' + serializeTo)
        out = open(serializeTo, "w")
        XMLSerializer = serializers.get_serializer("xml")
        xml_serializer = XMLSerializer()
        xml_serializer.serialize((self, ), stream=out)
        super(MMedia, self).save(*args, **kwargs)
        
class Audio(MMedia):
    """Implementa o modelo de dados de um arquivo de audio.

    Implementa e especializa a classe abstrata *MMedia* para conteudos de tipo audio.
    
    Atributos:
        mediatype: etiqueta para definir o tipo de conteudo
    """
    mediatype = "audio"
    
class Image(MMedia):
    """Implementa o modelo de dados de um arquivo de imagem.

    Implementa e especializa a classe abstrata *MMedia* para conteudos de tipo imagem.
    
    Atributos:
        mediatype: etiqueta para definir o tipo de conteudo
        height: altura da imagem
        width: largura da imagem
    """

    mediatype = "image"
    height = models.IntegerField(max_length=4)
    width = models.IntegerField(max_length=4)

    def get_tiny_object(self):
        return self.mediatype

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

class Video(MMedia):
    """Implementa o modelo de dados de um arquivo de video.

    Implementa e especializa a classe abstrata *MMedia* para conteudos de tipo video.
    
    Atributos:
        mediatype: etiqueta para definir o tipo de conteudo
        preview: apontador para uma imagem de anteprima (objeto ImageField)
    """

    mediatype = "video"
    preview = models.ImageField(upload_to="video_thumbnails")

    def get_tiny_object(self):
        return self.mediatype

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')



