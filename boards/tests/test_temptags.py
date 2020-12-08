from django import forms
from django.test import TestCase
from ..templatetags.form_tags import field_type, input_class

# Create your tests here.
class ExampleForm(forms.Form):
    name = forms.CharField()
    pwd = forms.CharField(widget=forms.PasswordInput())

    class Meta:
         fields=('name','pwd')

class FieldTypeTests(TestCase):
    def test_field_widget_type(self):
        form = ExampleForm()
        self.assertEquals('TextInput',field_type(form['name']))
        self.assertEquals('PasswordInput', field_type(form['pwd']))

class InputClassTests(TestCase):
    def test_unbound_field_initial_state(self):
        form = ExampleForm()
        self.assertEquals('form-control ',input_class(form['name']))
        self.assertEquals('form-control ',input_class(form['pwd']))

    def test_valid_bound_field(self):
        form = ExampleForm({'name':'user','pwd':'123'})
        self.assertEquals('form-control is-valid',input_class(form['name']))
        self.assertEquals('form-control ',input_class(form['pwd']))
    
    def test_invalid_bound_field(self):
        form = ExampleForm({'name':'','pwd':'123'})
        self.assertEquals('form-control is-invalid',input_class(form['name']))
        self.assertEquals('form-control ',input_class(form['pwd']))



       