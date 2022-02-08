from django import forms
from ChatbotApp.models import corona_xray


class corona_xray_form(forms.ModelForm):

    class Meta:
        model = corona_xray
        fields = '__all__'