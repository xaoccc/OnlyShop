from django import forms

from OnlyShop.main_app.models import Item
from OnlyShop.utils.mixins import ReadOnlyFieldsMixin

# Here we create a fake form, used only to display the model fields in the view
class ItemDeleteForm(forms.ModelForm, ReadOnlyFieldsMixin):
    class Meta:
        model = Item
        fields = ["name", "type", "new_price", "description"]
        labels = {field.name: field.verbose_name for field in Item._meta.fields}
