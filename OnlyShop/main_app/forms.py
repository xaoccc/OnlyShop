from django import forms

from OnlyShop.main_app.models import Item
from OnlyShop.utils.mixins import ReadOnlyFieldsMixin


class ItemDeleteForm(forms.ModelForm, ReadOnlyFieldsMixin):
    class Meta:
        model = Item
        fields = ["name", "type", "new_price", "description"]
        labels = {field.name: field.verbose_name for field in Item._meta.fields}

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance
