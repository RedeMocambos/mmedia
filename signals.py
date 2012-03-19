from django.dispatch import receiver
from django.core import serializers
from django.conf import settings

from gitannex.signals import filesync_done
from gitannex.models import GitAnnexRepository

import os

"""
Arquivo de definicao dos sinais.

Os sinais sao usados para interligar diferentes *apps* do Django. 
"""


@receiver(filesync_done, sender=GitAnnexRepository)
def syncGitAnnexRepository(sender, **kwargs):
    """Inicia a sincronizacao do repositorio git annex."""
    createObjectsFromFiles(os.path.join(settings.MEDIA_ROOT, settings.GITANNEX_DIR, sender.repositoryURLOrPath))

def createObjectsFromFiles(pathToFiles):
    """Recria os objetos no Django a partir dos objetos serializados em XML."""
    print ">>> DESERIALIZING"
    for root, dirs, files in os.walk(pathToFiles):
        for file in files:
            if file.endswith('.xml'):
                xmlIn = open(os.path.join(root, file), "r")

                for obj in serializers.deserialize("xml", xmlIn):
                    obj.id = None
                    obj.pk = None
                    obj.save()
                os.remove(os.path.join(root, file))
