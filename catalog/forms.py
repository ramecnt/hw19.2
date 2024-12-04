from django import forms
from django.forms import BooleanField

from catalog.models import Product, Version, Blog

# List of restricted words that cannot be used in certain fields.
restricted_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]


class StyleFormMixin:
    """
    A mixin to apply consistent styling to form fields.

    Boolean fields are styled as 'form-check-input', and all other fields
    are styled as 'form-control'.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and apply the styles to all fields.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                # Style for Boolean fields.
                field.widget.attrs['class'] = 'form-check-input'
            else:
                # Style for other fields.
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    """
    A form for creating and editing Product instances.

    Includes validation to prevent restricted words in the name and description fields.
    """
    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        """
        Validates the 'name' field to ensure it does not contain restricted words.

        Raises:
            forms.ValidationError: If a restricted word is found in the name.
        """
        name = self.cleaned_data.get('name')
        for i in name.split():
            if i.lower() in restricted_words:
                raise forms.ValidationError("Название содержит запрещенные слова")
        return name

    def clean_description(self):
        """
        Validates the 'description' field to ensure it does not contain restricted words.

        Raises:
            forms.ValidationError: If a restricted word is found in the description.
        """
        description = self.cleaned_data.get('description')
        for i in description.split():
            if i.lower() in restricted_words:
                raise forms.ValidationError("Описание содержит запрещенные слова")
        return description


class VersionForm(StyleFormMixin, forms.ModelForm):
    """
    A form for creating and editing Version instances.
    """
    class Meta:
        model = Version
        fields = '__all__'


class BlogForm(StyleFormMixin, forms.ModelForm):
    """
    A form for creating and editing Blog instances.

    The 'is_accepted' field is excluded from the form.
    """
    class Meta:
        model = Blog
        exclude = ['is_accepted']