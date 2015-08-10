from django import forms
from django.db import models

class URLForm(forms.Form):
    urls=forms.CharField(required=False,widget=forms.Textarea(attrs={"class":"form-control"}),label="Urls List")
    file=forms.FileField(required=False,label='Select a file',help_text='max. 5 megabytes')
    email=forms.EmailField(required=False,label="Enter your email")
    
    def clean(self):
        if hasattr(self, 'cleaned_data'):
            cleaned_data=self.cleaned_data
            if cleaned_data['urls'] or cleaned_data['file']:
                if cleaned_data['urls']:
                    if len(cleaned_data['urls'])<5:
                        raise forms.ValidationError("Please fill url filed with proper url")
                elif cleaned_data['file']:
                    filename = cleaned_data['file'].name
                    if not filename.endswith('.txt'):
                        raise forms.ValidationError("Invalid file format. Please upload only txt files")
                    elif not cleaned_data['email']:
                        raise forms.ValidationError("Please fill up the email field")
                return cleaned_data
            else:
                raise forms.ValidationError("Please fill the any one of the inputs")
        else:
            raise forms.ValidationError("Please fill the any one of the inputs")
    
    