from django.shortcuts import render, redirect, get_object_or_404
from .models import Document, LessonStandard, Activity
from .forms import SearchForm, DocumentForm, ActivityForm, LessonStandardSearchForm
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import os


def search(request):
    query = None
    activity_type = None
    results = []
    
    if request.method == 'GET':
        form = SearchForm(request.GET)
        
        if form.is_valid():
            query = form.cleaned_data['query']
            activity_type = form.cleaned_data['activity_type']
            
            # Start building the query with AND logic for multiple keywords
            q_objects = Q()
            
            # Handle keyword search
            if query:
                search_terms = query.split()  # Split query into individual words
                for term in search_terms:
                    # AND condition: All words must be in title or content
                    q_objects &= Q(title__icontains=term) | Q(description__icontains=term)

            # Filter by activity type if specified
            if activity_type:
                q_objects &= Q(document_type=activity_type)

            # Perform the search
            results = Document.objects.filter(q_objects).distinct()
    
    else:
        form = SearchForm()

    return render(request, 'lesson_app/search.html', {'form': form, 'results': results, 'query': query, 'activity_type': activity_type})

def add_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('search')  # Redirect to search page after saving
    else:
        form = DocumentForm()

    return render(request, 'lesson_app/add_document.html', {'form': form})

def manual_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            # Redirect to the preview page with form data
            return render(request, 'lesson_app/activity_saved.html', {'form': form.cleaned_data})
    else:
        form = ActivityForm()

    return render(request, 'lesson_app/manual_activity.html', {'form': form})

def preview_activity(request, activity_id):
    # Retrieve the activity using the ID
    activity = get_object_or_404(Activity, id=activity_id)

    # Render the preview template with the activity details
    return render(request, 'lesson_app/activity_preview.html', {'activity': activity})

def save_activity_as_document(request):
    if request.method == 'POST':
        # Get the form data from the POST request
        materials_list = request.POST.getlist('materials')
        materials_string = ','.join(materials_list)  # Convert list to comma-separated string
        
        # Extract values from the POST request
        activity_name = request.POST.get('activity_name')
        document_type = request.POST.get('document_type')
        activity_description = request.POST.get('activity_description')
        curriculum_standards = request.POST.get('standards')
        observation = request.POST.get('observation')
        question_idea = request.POST.get('question_idea')
        hypothesis = request.POST.get('hypothesis')
        experiment_test = request.POST.get('experiment_test')
        results_analysis = request.POST.get('results_analysis')
        communication = request.POST.get('communication')
        
        # Save activity to the database
        activity = Activity.objects.create(
            activity_name=activity_name,
            document_type=document_type,
            activity_description=activity_description,
            curriculum_standards=curriculum_standards,
            materials=materials_string,
            observation=observation,
            question_idea=question_idea,
            hypothesis=hypothesis,
            experiment_test=experiment_test,
            results_analysis=results_analysis,
            communication=communication
        )

        # If the standards field is a ManyToManyField, set the relationship after saving the activity
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity.standards.set(form.cleaned_data['standards'])

         # Generate the PDF file (ensure that generate_pdf is a valid function)
        pdf_file_name = generate_pdf(
            activity_name=activity_name,
            activity_description=activity_description,
            curriculum_standards=curriculum_standards,
            materials_list=materials_list,
            observation=observation,
            question_idea=question_idea,
            hypothesis=hypothesis,
            experiment_test=experiment_test,
            results_analysis=results_analysis,
            communication=communication
        )

        # Save the content as a document in the database, with a reference to the PDF file
        if pdf_file_name:
            document = Document.objects.create(
                title=activity_name,
                description=activity_description,
                upload_file=pdf_file_name,
                document_type=document_type
            )

        # Redirect to the preview page after saving
        return render(request, 'lesson_app/activity_saved.html', {'document': document})

    return redirect('manual_activity')
            
def activity_saved(request):
    return render(request, 'lesson_app/activity_saved.html')

def generate_pdf(activity_name, activity_description, curriculum_standards, materials, observation, question_idea, 
                 hypothesis, experiment_test, results_analysis, communication):
    # Create the context for rendering the PDF template
    context = {
        'activity_name': activity_name,
        'activity_description': activity_description,
        'curriculum_standards': curriculum_standards,
        'materials': materials,
        'observation': observation,
        'question_idea': question_idea,
        'hypothesis': hypothesis,
        'experiment_test': experiment_test,
        'results_analysis': results_analysis,
        'communication': communication,
    }
    
    # Render the HTML content for the PDF
    html = render_to_string('lesson_app/pdf_template.html', context)

    # Path to save the PDF
    pdf_file_name = f"{activity_name}.pdf"
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'documents/pdfs', pdf_file_name)

    # Generate PDF and save it to the file path
    with open(pdf_file_path, "w+b") as pdf_file:
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)

    # Check if there was an error generating the PDF
    if pisa_status.err:
        return None  # Handle the error if needed

    return os.path.join('documents/pdfs', pdf_file_name)

def search_lesson_standards(request):
    form = LessonStandardSearchForm(request.GET or None)
    results = []

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        country = form.cleaned_data.get('country')
        subject = form.cleaned_data.get('subject')
        grade_level = form.cleaned_data.get('grade_level')

        # Build query based on the form inputs
        query = Q()
        
        if keyword:
            query &= Q(code__icontains=keyword) | Q(description__icontains=keyword)

        if country:
            query &= Q(country=country)
        
        if subject:
            query &= Q(subject=subject)
        
        if grade_level:
            query &= Q(grade_level=grade_level)

        results = LessonStandard.objects.filter(query)

    return render(request, 'lesson_app/search_lesson_standards.html', {'form': form, 'results': results})

def get_standards(request):
    country = request.GET.get('country')
    grade = request.GET.get('grade')
    subject = request.GET.get('subject')

    print(f"Country: {country}, Grade: {grade}, Subject: {subject}")  # Log values

    # Filter LessonStandard based on the selected criteria
    standards = LessonStandard.objects.filter(country=country, grade_level=grade, subject=subject).values('id', 'code', 'description')
    
    # Return the filtered standards as JSON response
    return JsonResponse(list(standards), safe=False)


