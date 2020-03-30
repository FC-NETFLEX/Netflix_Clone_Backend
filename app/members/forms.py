from django import forms


class IconTypeChoiceForm(forms.ModelForm):
    ICON_TYPE_CHOICES = (
        ('기본 아이콘', '기본 아이콘'),
        ('', '')
    )

    icon_category = forms.ChoiceField(choices=ICON_TYPE_CHOICES)
