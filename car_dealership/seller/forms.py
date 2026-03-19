# forms.py
from django import forms
from cars.models import Car, CarVideo

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand',
            'car_model',
            'image',
            'prod_year',
            'price',
            'levy',
            'mileage',
            'fuel_type',
            'gear_box_type',
            'description',
            'color',
            'leather_interior',
            'drive_wheels',
            'doors',
            'wheel',
            'engine_volume',
            'cylinders',
            'airbags',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CarVideoForm(forms.ModelForm):
    class Meta:
        model = CarVideo
        fields = ['video']