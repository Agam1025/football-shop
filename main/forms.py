from django.forms import ModelForm
from main.models import Shop
from django.utils.html import strip_tags

class ShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = ["name", "price", "description", "category", "thumbnail", "is_featured"]

    def clean_title(self):
        title = self.cleaned_data["title"]
        return strip_tags(title)

    def clean_content(self):
        content = self.cleaned_data["content"]
        return strip_tags(content)