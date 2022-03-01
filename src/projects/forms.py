from django import forms
from django.forms import ModelForm, widgets
from .models import Project


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, value in self.fields.items():
            value.widget.attrs.update({'class': 'input'})

    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link',
                  'source_link', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }
