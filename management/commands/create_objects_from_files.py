from django.core.management.base import BaseCommand, CommandError

from mmedia.signals import createObjectsFromFiles

"""
Definicoes do comando para recriar objetos no Django a partir de objetos serializados em XML.
"""

class Command(BaseCommand):
    """Recria os objetos no Django a partir dos objetos serializados em XML."""
    help = 'Create mmedia objects from serialized objects in given path.'

    def handle(self, *args, **options):
        createObjectsFromFiles(args[0])
        
