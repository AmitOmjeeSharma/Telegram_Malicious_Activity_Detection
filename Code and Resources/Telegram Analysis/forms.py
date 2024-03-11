from django import forms

class MessageForm(forms.Form):
    group_link = forms.CharField(max_length=255)
    # category = forms.ChoiceField(choices=[('Normal', 'Normal'), ('Terrorism', 'Terrorism'), ('Cyber_Space', 'Cyber_Space'),
    #            ('Data_Leak', 'Data_Leak')])

