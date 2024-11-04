from django import forms
from .models import Document, LessonStandard

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)
    
    # Use the same choices defined in the Document model for activity type
    ACTIVITY_TYPE_CHOICES = [
        ('', 'Any Type'),  # Empty choice for selecting all types
        ('lesson', 'Lesson'),
        ('challenge', 'Challenge'),
        ('project', 'Project'),
        ('module', 'Module'),
    ]
    
    activity_type = forms.ChoiceField(
        choices=ACTIVITY_TYPE_CHOICES,
        required=False,
        label='Activity Type'
    )

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'upload_file', 'document_type']  # Include document_type


class ActivityForm(forms.ModelForm):
    # Using choices directly from the LessonStandard model
    activity_name = forms.CharField(
        max_length=100, required=False
    )
    country = forms.ChoiceField(
        choices=LessonStandard.COUNTRY_CHOICES,
        widget=forms.Select(attrs={'id': 'country'})
    )
    grade_level = forms.ChoiceField(
        choices=LessonStandard.GRADE_CHOICES,
        widget=forms.Select(attrs={'id': 'grade'})
    )
    subject = forms.ChoiceField(
        choices=LessonStandard.SUBJECT_CHOICES,
        widget=forms.Select(attrs={'id': 'subject'})
    )
    entered_by = forms.CharField(
        max_length=100, required=False
    )
    materials = forms.CharField(
        max_length=100, required=False
    )
    observation = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),  
        required=False
    )
    question_idea = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),  
        required=False
    )
    hypothesis = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), 
        required=False
    )
    experiment_test = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),  
        required=False
    )
    results_analysis = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), 
        required=False
    )
    communication = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),  
        required=False
    )

class LessonStandardSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False, label="Keyword")
    country = forms.ChoiceField(choices=[('', 'Any')] + LessonStandard.COUNTRY_CHOICES, required=False, label="Country")
    subject = forms.ChoiceField(choices=[('', 'Any')] + LessonStandard.SUBJECT_CHOICES, required=False, label="Subject")
    grade_level = forms.ChoiceField(choices=[('', 'Any')] + LessonStandard.GRADE_CHOICES, required=False, label="Grade Level")