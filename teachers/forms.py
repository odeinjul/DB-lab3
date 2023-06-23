from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum

from .models import Teacher, Paper, Project, Class, Authorship, Teaching, Leading


class TeacherForm(forms.ModelForm):
    GENDER_CHOICES = (
        (1, '男'),
        (2, '女'),
    )
    TITLE_CHOICES = (
        (1, '博士后'),
        (2, '助教'),
        (3, '讲师'),
        (4, '副教授'),
        (5, '特任教授'),
        (6, '教授'),
        (7, '助理研究员'),
        (8, '特任副研究员'),
        (9, '副研究员'),
        (10, '特任研究员'),
        (11, '研究员'),
    )
    # tea_id = forms.IntegerField(label='工号')
    name = forms.CharField(label='姓名')
    gender = forms.ChoiceField(choices=GENDER_CHOICES,  label='性别')
    title = forms.ChoiceField(choices=TITLE_CHOICES,  label='职称')

    class Meta:
        model = Teacher
        fields = ['name', 'gender', 'title']


class PaperCreateForm(forms.ModelForm):
    TYPE_CHOICES = (
        (1, 'Full paper'),
        (2, 'Short paper'),
        (3, 'Poster paper'),
        (4, 'Demo paper'),
    )
    LEVEL_CHOICES = (
        (1, 'CCF-A'),
        (2, 'CCF-B'),
        (3, 'CCF-C'),
        (4, '中文 CCF-A'),
        (5, '中文 CCF-B'),
        (6, '无级别'),
    )
    paper_id = forms.IntegerField(label='论文号')
    name = forms.CharField(label='论文名称')
    source = forms.CharField(label='发表源')
    pub_year = forms.IntegerField(label='发表年份')
    type = forms.ChoiceField(choices=TYPE_CHOICES,  label='类型')
    level= forms.ChoiceField(choices=LEVEL_CHOICES,  label='级别')

    class Meta:
        model = Paper
        fields = ['paper_id', 'name', 'source', 'pub_year', 'type', 'level']


class ProjectCreateForm(forms.ModelForm):
    TYPE_CHOICES = (
        (1, '国家级项目'),
        (2, '省部级项目'),
        (3, '市厅级项目'),
        (4, '企业合作项目'),
        (5, '其他类型项目'),
    )
    proj_id = forms.IntegerField(label='项目号')
    name = forms.CharField(label='项目名称')
    source = forms.CharField(label='项目来源')
    type = forms.ChoiceField(choices=TYPE_CHOICES, label='项目类型')
    funds = forms.FloatField(label='总经费')
    startYear = forms.IntegerField(label='开始年份')
    endYear = forms.IntegerField(label='结束年份')

    class Meta:
        model = Project
        fields = ['proj_id', 'name', 'source', 'type', 'funds', 'startYear', 'endYear']


class ProjectUpdateForm(forms.ModelForm):
    TYPE_CHOICES = (
        (1, '国家级项目'),
        (2, '省部级项目'),
        (3, '市厅级项目'),
        (4, '企业合作项目'),
        (5, '其他类型项目'),
    )
    name = forms.CharField(label='项目名称')
    source = forms.CharField(label='项目来源')
    type = forms.ChoiceField(choices=TYPE_CHOICES, label='项目类型')
    funds = forms.FloatField(label='总经费')
    startYear = forms.IntegerField(label='开始年份')
    endYear = forms.IntegerField(label='结束年份')

    class Meta:
        model = Project
        fields = ['name', 'source', 'type', 'funds', 'startYear', 'endYear']


class AuthorshipCreateForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='作者')
    paper = forms.ModelChoiceField(queryset=Paper.objects.all(), label='论文')
    rank = forms.IntegerField(label='排名')
    is_corresponding_author = forms.BooleanField(widget=forms.CheckboxInput(), label='是否是通讯作者', required=False)

    class Meta:
        model = Authorship
        fields = ['author', 'paper', 'rank', 'is_corresponding_author']

    def clean(self):
        cleaned_data = super().clean()
        paper = cleaned_data.get('paper')
        is_corresponding_author = cleaned_data.get('is_corresponding_author')
        corresponding_author_count = Authorship.objects.filter(paper=paper,
                                                               is_corresponding_author=True).count()
        if corresponding_author_count > 0 and is_corresponding_author:
            e = ValidationError('每个作者和论文组合下最多只能有一个通讯作者')
            raise e
        return cleaned_data


class AuthorshipUpdateForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='作者', disabled=True)
    paper = forms.ModelChoiceField(queryset=Paper.objects.all(), label='论文', disabled=True)
    rank = forms.IntegerField(label='排名')
    is_corresponding_author = forms.BooleanField(widget=forms.CheckboxInput(), label='是否是通讯作者', required=False)

    class Meta:
        model = Authorship
        fields = ['author', 'paper', 'rank', 'is_corresponding_author']

    def clean(self):
        cleaned_data = super().clean()
        paper = cleaned_data.get('paper')
        author = cleaned_data.get('author')
        is_corresponding_author = cleaned_data.get('is_corresponding_author')
        corresponding_author_count = Authorship.objects.filter(paper=paper,
                                                               is_corresponding_author=True).exclude(author=author).count()
        if corresponding_author_count > 0 and is_corresponding_author:
            e = ValidationError('每个作者和论文组合下最多只能有一个通讯作者')
            raise e
        return cleaned_data


class LeadingCreateForm(forms.ModelForm):
    leader = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='承担人')
    project = forms.ModelChoiceField(queryset=Project.objects.all(), label='项目')
    rank = forms.IntegerField(label='排名')
    fund = forms.FloatField(label='经费')

    class Meta:
        model = Leading
        fields = ['leader', 'project', 'rank', 'fund']

    def clean(self):
        cleaned_data = super().clean()
        leader = cleaned_data.get('leader')
        project = cleaned_data.get('project')
        fund = cleaned_data.get('fund')
        if fund < 0:
            e = ValidationError('经费不能是负数')
            raise e
        total_funds = Leading.objects.filter(project=project).exclude(leader=leader).aggregate(Sum('fund'))[
                              'fund__sum'] or 0

        if total_funds + fund > project.funds:
            raise ValidationError('项目经费已超过预算')

        return cleaned_data


class LeadingUpdateForm(forms.ModelForm):
    leader = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='承担人', disabled=True)
    project = forms.ModelChoiceField(queryset=Project.objects.all(), label='项目', disabled=True)
    rank = forms.IntegerField(label='排名')
    fund = forms.FloatField(label='经费')

    class Meta:
        model = Leading
        fields = ['leader', 'project', 'rank', 'fund']

    def clean(self):
        cleaned_data = super().clean()
        leader = cleaned_data.get('leader')
        project = cleaned_data.get('project')
        fund = cleaned_data.get('fund')
        if fund < 0:
            e = ValidationError('经费不能是负数')
            raise e
        total_funds = Leading.objects.filter(project=project).exclude(leader=leader).aggregate(Sum('fund'))[
                              'fund__sum'] or 0

        if total_funds + fund > project.funds:
            raise ValidationError('项目经费已超过预算')

        return cleaned_data


class PaperUpdateForm(forms.ModelForm):
    TYPE_CHOICES = (
        (1, 'Full paper'),
        (2, 'Short paper'),
        (3, 'Poster paper'),
        (4, 'Demo paper'),
    )
    LEVEL_CHOICES = (
        (1, 'CCF-A'),
        (2, 'CCF-B'),
        (3, 'CCF-C'),
        (4, '中文 CCF-A'),
        (5, '中文 CCF-B'),
        (6, '无级别'),
    )
    name = forms.CharField(label='论文名称')
    source = forms.CharField(label='发表源')
    pub_year = forms.IntegerField(label='发表日期')
    type = forms.ChoiceField(choices=TYPE_CHOICES,  label='类型')
    level= forms.ChoiceField(choices=LEVEL_CHOICES,  label='级别')

    class Meta:
        model = Paper
        fields = ['name', 'source', 'pub_year', 'type', 'level']


class TeachingCreateForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='教师')
    class_obj = forms.ModelChoiceField(queryset=Class.objects.all(), label='课程')
    year = forms.IntegerField(label='年份')
    SEME_CHOICES = (
        (1, '春季学期'),
        (2, '夏季学期'),
        (3, '秋季学期'),
    )
    semester = forms.ChoiceField(choices=SEME_CHOICES,  label='学期')
    hours = forms.IntegerField(label='学时')

    class Meta:
        model = Teaching
        fields = ['teacher', 'class_obj', 'year', 'semester', 'hours']

    def clean(self):
        cleaned_data = super().clean()
        teacher = cleaned_data.get('teacher')
        class_obj = cleaned_data.get('class_obj')
        year = cleaned_data.get('year')
        semester = cleaned_data.get('semester')
        hours = cleaned_data.get('hours')
        if hours < 0:
            e = ValidationError('学时不能是负数')
            raise e
        total_time = Teaching.objects.filter(class_obj=class_obj, year=year, semester=semester).exclude(teacher=teacher).aggregate(Sum('hours'))[
                              'hours__sum'] or 0

        if total_time + hours > class_obj.time:
            raise ValidationError('总学时超过预定学时')

        return cleaned_data


class TeachingUpdateForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='教师', disabled=True)
    class_obj = forms.ModelChoiceField(queryset=Class.objects.all(), label='课程', disabled=True)
    year = forms.IntegerField(label='年份', disabled=True)
    SEME_CHOICES = (
        (1, '春季学期'),
        (2, '夏季学期'),
        (3, '秋季学期'),
    )
    semester = forms.ChoiceField(choices=SEME_CHOICES,  label='学期', disabled=True)
    hours = forms.IntegerField(label='学时')

    class Meta:
        model = Teaching
        fields = ['teacher', 'class_obj', 'year', 'semester', 'hours']

    def clean(self):
        cleaned_data = super().clean()
        teacher = cleaned_data.get('teacher')
        class_obj = cleaned_data.get('class_obj')
        year = cleaned_data.get('year')
        semester = cleaned_data.get('semester')
        hours = cleaned_data.get('hours')
        if hours < 0:
            e = ValidationError('学时不能是负数')
            raise e
        total_time = Teaching.objects.filter(class_obj=class_obj, year=year, semester=semester).exclude(teacher=teacher).aggregate(Sum('hours'))[
                              'hours__sum'] or 0

        if total_time + hours > class_obj.time:
            raise ValidationError('总学时超过预定学时')

        return cleaned_data
