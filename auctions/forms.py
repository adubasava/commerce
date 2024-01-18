from django.forms import ModelForm
from .models import Listing


class NewListingForm(ModelForm):
    class Meta:
        model = Listing        
        exclude = ["watchlist", "user", "active", "time"]
