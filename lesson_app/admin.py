from django.contrib import admin
from .models import Document, LessonStandard

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type','description', 'upload_file')  # Fields to display in the admin list view
    search_fields = ('title', 'decription')  # Add a search bar for title and content
    list_filter = ('document_type',)  # Add a filter for document_type

@admin.register(LessonStandard)
class LessonStandardAdmin(admin.ModelAdmin):
    list_display = ('code', 'country', 'subject', 'grade_level', 'description')
    search_fields = ('code', 'description')
    list_filter = ('country', 'subject', 'grade_level')