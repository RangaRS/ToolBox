from django import forms


class uploadicon(forms.Form):
    CHOICES = [('icon', 'icon'),
               ('illustration', 'illustration')]

    category = forms.ChoiceField(label='Category', label_suffix=' : ', choices=CHOICES, widget=forms.Select)
    iconimg = forms.FileField(label='Upload Image', label_suffix=' : ', widget=forms.FileInput(attrs={'accept': '.svg,.png,.jpg,.jpeg'}))
    tags = forms.CharField(label='Tags', label_suffix=' : ', widget=forms.Textarea)