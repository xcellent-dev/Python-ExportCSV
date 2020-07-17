from django import forms


class UserInputData(forms.Form):
    stringLength = forms.IntegerField()
    density = forms.FloatField()
    total_words = forms.IntegerField()
    main_keyword = forms.CharField(widget=forms.Textarea)
    supporting_words = forms.CharField(widget=forms.Textarea)
    supporting_density = forms.FloatField()
    p_tags = forms.IntegerField()
