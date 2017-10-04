from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Fieldset, Div, Submit, HTML, Button, Row, Field
from .models import Ranking, SystemMessage
from django.core.urlresolvers import reverse

class RankingForm(forms.ModelForm):
    class Meta:
        model = Ranking
        fields = '__all__'

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = 'dataentry'
    helper.layout = Layout(
        Field('sprint', css_class='input-xlarge'),
        Field('team', css_class='input-xlarge'),
        Field('criteria', rows="3", css_class='input-xlarge'),
        Field('points', style="background: #FAFAFA; padding: 10px;"),
        Field('dataDate', id="dataDate",
              template='rank/datepicker.html')
    )
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))

class SystemMessageForm(forms.ModelForm):
    class Meta:
        model = SystemMessage
        fields = '__all__'

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = 'systemmessages'
    helper.layout = Layout(
        Field('content', css_class='input-xlarge'),
        Field('isActive'),

    )
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
