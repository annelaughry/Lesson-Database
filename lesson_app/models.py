from django.db import models

class LessonStandard(models.Model):
    COUNTRY_CHOICES = [
        ('us', 'United States'),
        ('moldova', 'Moldova'),
    ]

    GRADE_CHOICES = [
        ('4', '4th Grade'),
        ('5', '5th Grade'),
        ('6', '6th Grade'),
        ('7', '7th Grade'),
        ('8', '8th Grade'),
        ('9', '9th Grade'), 
    ]

    SUBJECT_CHOICES = [
        ('bio', 'Biology'),
        ('chem', 'Chemistry'),
        ('phys', 'Physics'),
        ('ps', 'Physical Science (US)'),
        ('ls', 'Life Science (US)'),
        ('ess', 'Earth and Space Science (US)'), 
    ]

    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    grade_level = models.CharField(max_length=10, choices=GRADE_CHOICES)
    code = models.CharField(max_length=50, unique=True)  # Unique standard code
    description = models.TextField()  # Detailed description of the standards

    def __str__(self):
        return f"{self.code} - {self.subject} - {self.grade_level}"


class Document(models.Model):
    LESSON_TYPE_CHOICES = [
        ('lesson', 'Lesson'),
        ('challenge', 'Challenge'),
        ('project', 'Project'),
        ('module', 'Module'),
    ]

    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=10, choices=LESSON_TYPE_CHOICES, default='Choose an option')  # Dropdown for type
    description = models.TextField(blank=True, null=True)
    upload_file = models.FileField(upload_to='documents/pdfs/', blank=True, null=True)

    standards = models.ManyToManyField(LessonStandard, blank=True, related_name='documents')

    
    def __str__(self):
        return self.title

class Activity(models.Model):
    activity_name = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50)
    grade_level = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    entered_by = models.CharField(max_length=50)
    materials = models.TextField()  
    observation = models.TextField(blank=True, null=True)
    question_idea = models.TextField(blank=True, null=True)
    hypothesis = models.TextField(blank=True, null=True)
    experiemnt_test = models.TextField(blank=True, null=True)
    results_analysis = models.TextField(blank=True, null=True)
    communication = models.TextField(blank=True, null=True)
    

    def save(self, *args, **kwargs):
        # Process materials list into a comma-separated string before saving
        if isinstance(self.materials, list):
            self.materials = ','.join(self.materials)
        super(Activity, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
