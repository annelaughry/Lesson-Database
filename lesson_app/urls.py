from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.search, name='search'),
    path('search/', views.search, name='search'),
    path('add/', views.add_document, name='add_document'),
    path('manual-activity/', views.manual_activity, name='manual_activity'),
    path('preview/<int:activity_id>/', views.preview_activity, name='preview_activity'),
    path('activity-saved/', views.activity_saved, name='activity_saved'),
    path('search-lesson-standards/', views.search_lesson_standards, name='search_lesson_standards'),
    path('get-standards/', views.get_standards, name='get_standards'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)