from django import forms
from .widgets import BootstrapDateTimePickerInput
from datetime import datetime, timedelta


class main_form(forms.Form):
    options = {
        'input_formats': ['%d.%m.%Y'],
        'widget': BootstrapDateTimePickerInput(),
        'initial': datetime.today().strftime('%d.%m.%Y'),
    }
    behaviour = forms.ChoiceField(choices=(
        ("1", "Display"),
        ("2", "Fetch"),
    ), help_text="Display - to get data from the DB; Fetch - to upload new data into the DB.")
    date = forms.DateField(**options)
    date_to = forms.DateField(**options)
    secret_command = forms.CharField(initial='Fire!')
