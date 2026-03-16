from django.contrib.auth.models import AbstractUser
from django.db import models

# Department
class Department(models.model):
    name = models.CharField(max_length=30)
    faculty = models.CharField(max_length=100)
    def _str_(self):
        return f"{self.name} ({self.faculty})"
    
#CustomUser
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("student","Student"),
        ("lecturer","Lecturer"),
        ("registrar","Academic Registrar"),
    ]
    role = models.CharField(max_length=30), choices=ROLE_CHOICES, default = "student" 
    department = models.Foreignkey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lecturers",
    )
    def _str_(self):
        return f"{self.username} ({self.get_role_display()})"
    
    #Issue
    class Issue(models.model):
        CATEGORY_CHOICES = [
            ("missing_marks","Missing Marks"),
            ("course_registration","Course Registration"),
            ("exam_card","Exam Card"),
            ("transcript","Transcript"),
            ("other","Other"),
        ]

        STATUS_CHOICES = [
            ("open","Open"),
            ("assigned","Assigned"),
            ("in_review","In Review"),
            ("resolved","Resolved"),
            ("closed","Closed"),
        ]
        #Who submitted the issue
        student = models.ForeignKey(
            CustomUser,
            on_delete=models.CASCADE,
            related_name ="submitted_issues",
            limit_choices_to={"role":"student"},
        )
        #Which lecurer was assigned
        assigned_to = models.ForeignKeys(
            CustomUser,
            on_delete=models.SET_NULL,
            null=True,
            related_name="assigned_issues",
            limit_choices_to={"role": "lecturer"},
        )

        category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
        description = models.TextField()
        supporting_document = models.FileField(
            upload_to="issue_docs/" , null=True, blank=True
        )
        status = models.CharField(max_length=20, choices=STATUS_CHOICES,default="open")
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_noew=True)
        #Auto generated tracking number
        tracking_number = models.CharField(max_length=20, unique=True, blank=True)

        def save(self, *args, **kwargs):
            #Generate tracking number on first save
            if not self.traking_number:
                super().save(*args, **kwargs)  #get a PK first
                self.tracking+number = f"AITS-{self.pk:05d}"
            super().save(*args, **kwargs)    
        def _str_(self):
            return f"{self.tracking_number} | {self.get_category_display() | {self.get_status_display()}}"    




