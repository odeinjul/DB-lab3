from django.urls import path

from . import views

app_name = "teachers"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.about, name="about"),
    path("tea/", views.teacher_search, name="teacher_search"),
    path("class/", views.class_search, name="class_search"),
    path("summary/", views.teaching_research_summary, name="teacher_summary"),
    path('summary/generate-pdf-report/', views.generate_pdf_report, name='generate_pdf_report'),

    path("paper/", views.paper_search, name="paper_search"),
    path("paper/create", views.PaperCreateView.as_view(), name="paper_create"),
    path("paper/<int:pk>/delete", views.PaperDeleteView.as_view(), name="paper_delete"),
    path("paper/<int:pk>/update", views.PaperUpdateView.as_view(), name="paper_update"),

    path("as/create/", views.AuthorshipCreateView.as_view(), name="authorship_create"),
    path("as/<int:tea_id>/<int:paper_id>/delete/", views.AuthorshipDeleteView.as_view(), name="authorship_delete"),
    path("as/<int:tea_id>/<int:paper_id>/update/", views.AuthorshipUpdateView.as_view(), name="authorship_update"),

    path("ld/create/", views.LeadingCreateView.as_view(), name="leading_create"),
    path("ld/<int:tea_id>/<str:proj_id>/delete/", views.LeadingDeleteView.as_view(), name="leading_delete"),
    path("ld/<int:tea_id>/<str:proj_id>/update/", views.LeadingUpdateView.as_view(), name="leading_update"),

    path("tc/create/", views.TeachingCreateView.as_view(), name="teaching_create"),
    path("tc/<int:tea_id>/<str:class_id>/<int:year>/<int:semester>/delete/", views.TeachingDeleteView.as_view(), name="teaching_delete"),
    path("tc/<int:tea_id>/<str:class_id>/<int:year>/<int:semester>/update/", views.TeachingUpdateView.as_view(), name="teaching_update"),

    path("proj/", views.project_search, name="project_search"),
    path("proj/create", views.ProjectCreateView.as_view(), name="project_create"),
    path("proj/<str:pk>/delete", views.ProjectDeleteView.as_view(), name="project_delete"),
    path("proj/<str:pk>/update", views.ProjectUpdateView.as_view(), name="project_update"),

    path("tea/<int:pk>/", views.TeacherView.as_view(), name="teacher_detail"),
    path("paper/<int:pk>/", views.PaperView.as_view(), name="paper_detail"),
    path("proj/<str:pk>/", views.ProjectView.as_view(), name="project_detail"),
    path("class/<str:pk>/", views.ClassView.as_view(), name="class_detail"),
    path("tea/<int:pk>/update", views.TeacherUpdateView.as_view(), name="teacher_update"),
]