from django import forms


class FormForms(forms.Form):
    name = forms.CharField(required=False)
    instrumentWorks = forms.CharField()
    whatAmount = forms.CharField()
    whatTradingStrategy = forms.CharField()
    optimalInvestmentPeriod = forms.JSONField()
    howToReach = forms.CharField()

# class MyForm(forms.Form):
#     QUESTION_CHOICES = (
#         ('option1', 'Option 1'),
#         ('option2', 'Option 2'),
#     )
#     question = forms.ChoiceField(choices=QUESTION_CHOICES, widget=forms.RadioSelect())
