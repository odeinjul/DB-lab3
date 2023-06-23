from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from reportlab.pdfgen import canvas

from .models import Teacher, Paper, Project, Class, Authorship, Leading, Teaching
from .forms import TeacherForm, PaperUpdateForm, PaperCreateForm, ProjectCreateForm, AuthorshipCreateForm, \
    ProjectUpdateForm, AuthorshipUpdateForm, LeadingCreateForm, LeadingUpdateForm, TeachingCreateForm, TeachingUpdateForm
from .templatetags.custom_filters import *

class IndexView(generic.ListView):
    template_name = "teachers/index.html"
    context_object_name = "latest_list"

    def get_queryset(self):
        """Return the last five teachers."""
        tea = Teacher.objects.order_by("tea_id")[:5]
        paper = Paper.objects.order_by("paper_id")[:5]
        proj = Project.objects.order_by("proj_id")[:5]
        classes = Class.objects.order_by("class_id")[:5]
        return {"tea": tea, "paper": paper, "proj": proj, "class": classes}


def about(request):
    return render(request, "teachers/about.html")


def teacher_search(request):
    if request.method == 'POST':
        tea_id = request.POST.get('tea_id')
        try:
            teacher = Teacher.objects.filter(tea_id__contains=tea_id)
        except Teacher.DoesNotExist:
            teacher = 0
        return render(request, 'teachers/teacher_search.html', {'teacher': teacher})

    return render(request, 'teachers/teacher_search.html')


def class_search(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        try:
            class_obj = Class.objects.filter(class_id__contains=class_id)
            print(class_obj)
        except Class.DoesNotExist:
            class_obj = 0
        return render(request, 'teachers/class_search.html', {'class_obj': class_obj})

    return render(request, 'teachers/class_search.html')


def paper_search(request):
    if request.method == 'POST':
        paper_name = request.POST.get('paper_name')
        try:
            papers = Paper.objects.filter(name__contains=paper_name)
            print(papers)
        except Paper.DoesNotExist:
            papers = 0
        return render(request, 'teachers/paper_search.html', {'papers': papers})

    return render(request, 'teachers/paper_search.html')


class PaperDeleteView(generic.DeleteView):
    model = Paper
    success_url = reverse_lazy("teachers:paper_search")
    template_name = "teachers/paper_delete.html"


class PaperUpdateView(generic.UpdateView):
    model = Paper
    form_class = PaperUpdateForm
    template_name = 'teachers/paper_update.html'

    def get_success_url(self):
        id = self.object.paper_id
        return f"/paper/{id}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paper_id'] = self.object.paper_id
        return context


def project_search(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            projects = Project.objects.filter(name__contains=name)
        except Project.DoesNotExist:
            projects = 0
        return render(request, 'teachers/project_search.html', {'projects': projects})

    return render(request, 'teachers/project_search.html')


class TeacherView(generic.DetailView):
    model = Teacher
    template_name = "teachers/teacher_detail.html"


class PaperView(generic.DetailView):
    model = Paper
    template_name = "teachers/paper_detail.html"


class PaperCreateView(generic.CreateView):
    model = Paper
    form_class = PaperCreateForm
    template_name = 'teachers/paper_create.html'
    success_url = '/paper'  # 添加成功后的重定向URL


class ProjectView(generic.DetailView):
    model = Project
    template_name = "teachers/proj_detail.html"


class ProjectCreateView(generic.CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'teachers/project_create.html'
    success_url = '/proj'  # 添加成功后的重定向URL


class ProjectUpdateView(generic.UpdateView):
    model = Project
    form_class = ProjectUpdateForm
    template_name = 'teachers/project_update.html'

    def get_success_url(self):
        proj_id = self.object.proj_id
        return f"/proj/{proj_id}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proj_id'] = self.object.proj_id
        return context


class ProjectDeleteView(generic.DeleteView):
    model = Project
    success_url = reverse_lazy("teachers:project_search")
    template_name = "teachers/project_delete.html"


class ClassView(generic.DetailView):
    model = Class
    template_name = "teachers/class_detail.html"


class TeacherUpdateView(generic.UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/teacher_update.html'

    def get_success_url(self):
        tea_id = self.object.tea_id
        return f"/tea/{tea_id}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tea_id'] = self.object.tea_id
        return context


class AuthorshipCreateView(generic.CreateView):
    model = Authorship
    form_class = AuthorshipCreateForm
    template_name = 'teachers/authorship_create.html'
    success_url = "/"

    def form_valid(self, form):
        form.instance.clean()
        return super().form_valid(form)


class AuthorshipDeleteView(generic.DeleteView):
    model = Authorship
    success_url = "/"
    template_name = "teachers/authorship_delete.html"

    def get_object(self, queryset=None):
        tea_id = self.kwargs['tea_id']
        paper_id = self.kwargs['paper_id']
        return get_object_or_404(Authorship, author_id=tea_id, paper_id=paper_id)


class AuthorshipUpdateView(generic.UpdateView):
    model = Authorship
    form_class = AuthorshipUpdateForm
    template_name = 'teachers/authorship_update.html'

    def get_success_url(self):
        tea_id = self.object.author.tea_id
        return f"/tea/{tea_id}"

    def get_object(self, queryset=None):
        tea_id = self.kwargs['tea_id']
        paper_id = self.kwargs['paper_id']
        return get_object_or_404(Authorship, author_id=tea_id, paper_id=paper_id)


class LeadingDeleteView(generic.DeleteView):
    model = Leading
    success_url = "/"
    template_name = "teachers/leading_delete.html"

    def get_object(self, queryset=None):
        tea_id = self.kwargs['tea_id']
        proj_id = self.kwargs['proj_id']
        return get_object_or_404(Leading, leader_id=tea_id, project_id=proj_id)


class LeadingCreateView(generic.CreateView):
    model = Leading
    form_class = LeadingCreateForm
    template_name = 'teachers/leading_create.html'
    success_url = "/"

    def form_valid(self, form):
        form.instance.clean()
        return super().form_valid(form)


class LeadingUpdateView(generic.UpdateView):
    model = Leading
    form_class = LeadingUpdateForm
    template_name = 'teachers/leading_update.html'

    def get_success_url(self):
        tea_id = self.object.leader.tea_id
        return f"/tea/{tea_id}"

    def get_object(self, queryset=None):
        tea_id = self.kwargs['tea_id']
        proj_id = self.kwargs['proj_id']
        return get_object_or_404(Leading, leader_id=tea_id, project_id=proj_id)


class TeachingDeleteView(generic.DeleteView):
    model = Leading
    success_url = "/"
    template_name = "teachers/teaching_delete.html"

    def get_object(self, queryset=None):
        tea_id = self.kwargs['tea_id']
        class_id = self.kwargs['class_id']
        year = self.kwargs['year']
        semester = self.kwargs['semester']
        return get_object_or_404(Teaching, teacher_id=tea_id, class_obj_id=class_id, year=year, semester=semester)


class TeachingCreateView(generic.CreateView):
    model = Teaching
    form_class = TeachingCreateForm
    template_name = 'teachers/teaching_create.html'
    success_url = "/"

    def form_valid(self, form):
        form.instance.clean()
        return super().form_valid(form)


class TeachingUpdateView(generic.UpdateView):
    model = Teaching
    form_class = TeachingUpdateForm
    template_name = 'teachers/teaching_Update.html'

    def get_success_url(self):
        tea_id = self.object.teacher.tea_id
        return f"/tea/{tea_id}"

    def get_object(self, queryset=None):
        tea_id = self.kwargs['tea_id']
        class_id = self.kwargs['class_id']
        year = self.kwargs['year']
        semester = self.kwargs['semester']
        return get_object_or_404(Teaching, teacher_id=tea_id, class_obj_id=class_id, year=year, semester=semester)


def teaching_research_summary(request):
    if request.method == 'POST':
        tea_id = request.POST.get('tea_id')
        start_year = request.POST.get('startYear')
        end_year = request.POST.get('endYear')

        teacher = Teacher.objects.get(
            tea_id=tea_id,
        )
        papers = Authorship.objects.filter(author_id=tea_id, paper__pub_year__gte=start_year, paper__pub_year__lte=end_year)
        projects = Leading.objects.filter(leader_id=tea_id, project__startYear__gte=start_year, project__endYear__lte=end_year)
        classes = Teaching.objects.filter(teacher_id=tea_id, year__gte=start_year, year__lte=end_year)
        return render(request, 'teachers/teaching_research_summary.html', {
            'teacher': teacher,
            'papers': papers,
            'projects': projects,
            'classes': classes,
            'tea_id': tea_id,
            'start_year': start_year,
            'end_year': end_year
        })

    return render(request, 'teachers/teaching_research_summary.html')


from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('PingFang', 'simhei.ttf'))
pdfmetrics.registerFont(TTFont('PingFang-bold', 'STHeitiBold.ttf'))


def generate_pdf_report(request):
    if request.method == 'POST':
        tea_id = request.POST.get('tea_id')
        start_year = request.POST.get('startYear')
        end_year = request.POST.get('endYear')

        teacher = Teacher.objects.get(tea_id=tea_id)
        papers = Authorship.objects.filter(author_id=tea_id, paper__pub_year__gte=start_year, paper__pub_year__lte=end_year)
        projects = Leading.objects.filter(leader_id=tea_id, project__startYear__gte=start_year, project__endYear__lte=end_year)
        classes = Teaching.objects.filter(teacher_id=tea_id, year__gte=start_year, year__lte=end_year)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="teaching_research_report.pdf"'

        p = canvas.Canvas(response)
        p.setFont("PingFang-bold", 20)
        p.drawString(200, 790, "教师教学科研情况统计".format(tea_id))
        x1, y1 = 50, 770
        x2, y2 = 550, 770
        p.line(x1, y1, x2, y2)

        p.setFont("PingFang", 12)
        p.setFont("PingFang-bold", 12)
        p.drawString(50, 750, "查询信息:")
        p.setFont("PingFang", 12)
        p.drawString(120, 750, "教师工号: {}".format(tea_id))
        p.drawString(120, 735, "查询起始年份: {}".format(start_year))
        p.drawString(120, 720, "查询结束年份: {}".format(end_year))
        x1, y1 = 50, 700
        x2, y2 = 550, 700
        p.line(x1, y1, x2, y2)

        y = 680
        p.setFont("PingFang-bold", 12)
        p.drawString(50, y, "教师信息:")
        p.setFont("PingFang-bold", 12)
        p.drawString(120, y, "姓名:")
        p.setFont("PingFang", 12)
        p.drawString(180, y, teacher.name)
        y -= 15

        p.setFont("PingFang-bold", 12)
        p.drawString(120, y, "工号:")
        p.setFont("PingFang", 12)
        p.drawString(180, y, f"{teacher.tea_id}")
        y -= 15

        p.setFont("PingFang-bold", 12)
        p.drawString(120, y, "性别:")
        p.setFont("PingFang", 12)
        p.drawString(180, y, teacher_gender_to_string(teacher.gender))
        y -= 15

        p.setFont("PingFang-bold", 12)
        p.drawString(120, y, "职称:")
        p.setFont("PingFang", 12)
        p.drawString(180, y, teacher_title_to_string(teacher.title))
        y -= 15

        x1, y1 = 50, y
        x2, y2 = 550, y
        p.line(x1, y1, x2, y2)
        y -= 20

        p.setFont("PingFang-bold", 12)
        p.drawString(50, y, "论文信息:")
        p.setFont("PingFang", 11)

        for paper in papers:
            p.drawString(120, y, paper.paper.name)
            y -= 20
            p.setFont("PingFang-bold", 11)
            p.drawString(120, y, '[' + paper.paper.source + ',' + f"{paper.paper.pub_year}" + '], ' + paper_level_to_string(paper.paper.level))
            p.setFont("PingFang", 11)
            y -= 20

        x1, y1 = 50, y
        x2, y2 = 550, y
        p.line(x1, y1, x2, y2)
        y -= 20

        p.setFont("PingFang-bold", 12)
        p.drawString(50, y, "项目信息:")
        p.setFont("PingFang", 11)
        for project in projects:
            p.drawString(120, y, project.project.name)
            y -= 20
            p.setFont("PingFang-bold", 11)
            p.drawString(120, y,
                         '[' + project.project.source + ',' + f"{project.project.startYear} - {project.project.endYear}" + '], ' + project_type_to_string(
                             project.project.type) + ', ' + f"经费：{project.fund}")
            p.setFont("PingFang", 11)
            y -= 20

        x1, y1 = 50, y
        x2, y2 = 550, y
        p.line(x1, y1, x2, y2)
        y -= 20
        p.setFont("PingFang-bold", 12)
        p.drawString(50, y, "课程信息:")
        p.setFont("PingFang", 11)
        for class_info in classes:
            p.drawString(120, y, class_info.class_obj.name)
            y -= 20
            p.setFont("PingFang-bold", 11)
            p.drawString(120, y,
                         '[' + class_type_to_string(class_info.class_obj.type) + '], ' + class_semester_to_string(class_info.semester) + ',' + f"{class_info.year}"
                         + ', ' + f"学时：{class_info.hours}")
            p.setFont("PingFang", 11)
            y -= 20

        p.showPage()
        p.save()

        return response

    return render(request, 'teachers/teaching_research_summary.html')
