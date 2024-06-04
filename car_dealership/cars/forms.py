from django.forms.widgets import ClearableFileInput
from django import forms
from .models import Manufacturer, BrandModel, Car, CarImages
from django.forms.widgets import ClearableFileInput, TextInput, NumberInput, Textarea, Select


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_file_clean = super(MultipleFileField, self).clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        else:
            return single_file_clean(data, initial)


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name']


class BrandModelForm(forms.ModelForm):
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all())

    class Meta:
        model = BrandModel
        fields = ['manufacturer', 'name']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model_name', 'year', 'price', 'description',
                  'petrol_type', 'car_type', 'gear_type']


class CarImagesForm(forms.ModelForm):
    image = MultipleFileField(required=False)

    class Meta:
        model = CarImages
        fields = ['car', 'image', 'featured']

    def __init__(self, *args, **kwargs):
        car = kwargs.pop('car', None)
        super().__init__(*args, **kwargs)
        if car:
            self.fields['car'].initial = car
        # Hide the car field in the form
        self.fields['car'].widget = forms.HiddenInput()
        self.fields['featured'].required = False

    def save(self, commit=True):
        images = self.cleaned_data.get('images', [])
        featured = self.cleaned_data.get('featured', False)
        car = self.cleaned_data.get('car')
        instances = []

        for image in images:
            instance = CarImages(car=car, image=image, featured=featured)
            if commit:
                instance.save()
            instances.append(instance)
            # Reset featured to False for subsequent images
            featured = False

        return instances


class EditCarForm(forms.ModelForm):
    images = MultipleFileField(required=False)
    class Meta:
        model = Car
        fields = ['model_name', 'year', 'price', 'milage', 'description',
                  'petrol_type', 'car_type', 'gear_type', 'images']
        widgets = {
            'model_name': Select(attrs={'class': 'form-control'}),
            'year': NumberInput(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'milage': NumberInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'petrol_type': Select(attrs={'class': 'form-control'}),
            'car_type': Select(attrs={'class': 'form-control'}),
            'gear_type': Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'].widget.attrs.update(
            {'multiple': True, 'class': 'form-control'})
        self.fields['milage'].label = "Milage (km)"
        
class AddCarForm(forms.ModelForm):

    brand_model_name = forms.ModelChoiceField(
        queryset=BrandModel.objects.all(),
        label="Brand Model Name",
        widget=Select(attrs={'class': 'form-control',
                         'placeholder': 'Enter brand model name'})
    )
    images = MultipleFileField(
        required=False,
        widget=MultipleFileInput(
            attrs={'class': 'form-control', 'multiple': True})
    )

    class Meta:
        model = Car
        fields = [
            'brand_model_name', 'year', 'price', 'milage', 'description',
            'petrol_type', 'car_type', 'gear_type', 'images'
        ]
        widgets = {
            'year': NumberInput(attrs={'class': 'form-control', 'placeholder': 'YYYY'}),
            'price': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Specify your price'}),
            'milage': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Specify your milage'}),
            'description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your description here.'}),
            'petrol_type': Select(attrs={'class': 'form-control'}),
            'car_type': Select(attrs={'class': 'form-control'}),
            'gear_type': Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'].widget.attrs.update({'multiple': True})
        self.fields['milage'].label = "Milage (km)"
