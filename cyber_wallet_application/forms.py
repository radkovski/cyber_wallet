from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tempus_dominus.widgets import DateTimePicker

from cyber_wallet_application.models import Operation, Report, Note, LocalConfiguration


# klasa bazowa dla formatek
class BaseForm(forms.ModelForm):
    # konstruktor ustawia wszystkim polom klasę bootstrapa: form-control
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# klasa formatki dla dodawania / edycji operacji
class OperationForm(BaseForm):
    class Meta:
        model = Operation
        exclude = ["user", "accounting_moment"]

    execution_moment = forms.DateTimeField(label="Data", required=True, initial=datetime.now(),
                                           widget=DateTimePicker(
                                               options={
                                                   'useCurrent': True,
                                                   'collapse': False,
                                               },
                                               attrs={
                                                   'append': 'fa fa-calendar',
                                                   'icon_toggle': True,
                                               }))
    description = forms.CharField(label="Opis", required=True)
    amount = forms.DecimalField(label="Kwota", required=True, decimal_places=2)

    def __init__(self, *args, **kwargs):
        BaseForm.__init__(self, *args, **kwargs)


# klasa formatki dla dodawania / edycji raportów
class ReportForm(BaseForm):
    class Meta:
        model = Report
        exclude = ["user"]

    from_moment = forms.DateTimeField(label="Od", required=True, initial=datetime.now(),
                                      widget=DateTimePicker(
                                          options={
                                              'useCurrent': True,
                                              'collapse': False,
                                          },
                                          attrs={
                                              'append': 'fa fa-calendar',
                                              'icon_toggle': True,
                                          }))
    to_moment = forms.DateTimeField(label="Do", required=True, initial=datetime.now() + timedelta(30),
                                    widget=DateTimePicker(
                                        options={
                                            'useCurrent': True,
                                            'collapse': False,
                                        },
                                        attrs={
                                            'append': 'fa fa-calendar',
                                            'icon_toggle': True,
                                        }))

    def __init__(self, *args, **kwargs):
        BaseForm.__init__(self, *args, **kwargs)


# klasa formatki dla dodawania / edycji notatek
class NoteForm(BaseForm):
    class Meta:
        model = Note
        exclude = ["user"]

    from_moment = forms.DateTimeField(label="Ważna od", required=True, initial=datetime.now(),
                                      widget=DateTimePicker(
                                          options={
                                              'useCurrent': True,
                                              'collapse': False,
                                          },
                                          attrs={
                                              'append': 'fa fa-calendar',
                                              'icon_toggle': True,
                                          }))
    to_moment = forms.DateTimeField(label="Ważna do", required=True, initial=datetime.now() + timedelta(7),
                                    widget=DateTimePicker(
                                        options={
                                            'useCurrent': True,
                                            'collapse': False,
                                        },
                                        attrs={
                                            'append': 'fa fa-calendar',
                                            'icon_toggle': True,
                                        }))
    text = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        BaseForm.__init__(self, *args, **kwargs)


# klasa formatki dla dodawania / edycji ustawień
class LocalConfigurationForm(BaseForm):
    class Meta:
        model = LocalConfiguration
        exclude = ["user", "key"]

    value = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        BaseForm.__init__(self, *args, **kwargs)


# klasa formatki dla rejestracji

class NewUserForm(BaseForm, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        BaseForm.__init__(self, *args, **kwargs)
