from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Layout, ButtonHolder, Fieldset, Div, Submit, HTML, Button, Row, Field
from .models import Ranking, SystemMessage, Sprint
from django.core.urlresolvers import reverse,reverse_lazy
from datetime import date

class RankingForm(forms.ModelForm):
    class Meta:
        model = Ranking
        fields = '__all__'

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = 'dataentry'
    helper.layout = Layout(

    )
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.layout = Layout(
        Field('sprint'),
        Field('team'),
        Field('criteria'),
        Field('points'),
        AppendedText('dataDate', '<span class="glyphicon glyphicon-calendar"></span>', active=True)
    )
class SystemMessageForm(forms.ModelForm):
    class Meta:
        model = SystemMessage
        fields = '__all__'

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = 'systemmessages'
    helper.layout = Layout(
        Field('name'),
        Field('content', css_class='input-xlarge'),
        Field('isActive'),

    )
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.add_input(
    Button('shpreview', "Show Preview", css_class='btn', onclick="showPreview()"))
    helper.add_input(
    Button('rmpreview', "Remove Preview", css_class='btn hidden', onclick="removePreview()"))

class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['id','name','isActive']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = 'sprints'
    helper.form_tag = False

    helper.layout = Layout(

        Field('name'),
        Field('isActive'),

    )
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))


