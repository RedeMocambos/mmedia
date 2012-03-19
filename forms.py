form django import forms
from mmedia.models import MMedia

"""
Arquivo com as definições dos forms da aplicação Django.
"""

class MMediaForm(forms.Form):
    def __init__(self, author, *args, **kwargs):
        super(MMediaForm, self).__init__(*args, **kwargs):
        self.author = author
