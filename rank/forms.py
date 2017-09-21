from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Fieldset, Div, Submit, HTML, Button, Row, Field
from .models import Ranking


class RankingForm(forms.ModelForm):
    class Meta:
        model = Ranking
        fields = '__all__'

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))