from django import forms


class IconTypeChoiceForm(forms.ModelForm):
    ICON_TYPE_CHOICES = (
        ('default', '대표 아이콘'),
    )

    icon_type = forms.ChoiceField(choices=ICON_TYPE_CHOICES)
