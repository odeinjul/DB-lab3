from django.db import models


class Teacher(models.Model):
    def __str__(self):
        return self.name

    tea_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

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

    gender = models.PositiveIntegerField(choices=GENDER_CHOICES)
    title = models.PositiveIntegerField(choices=TITLE_CHOICES)

    papers = models.ManyToManyField('Paper', through='Authorship')
    classes = models.ManyToManyField('Class', through='Teaching')
    projects = models.ManyToManyField('Project', through='Leading')


class Paper(models.Model):
    def __str__(self):
        return self.name

    paper_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    pub_year = models.PositiveIntegerField("publication year")

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
    type = models.PositiveIntegerField(choices=TYPE_CHOICES)
    level = models.PositiveIntegerField(choices=LEVEL_CHOICES)

    authors = models.ManyToManyField('Teacher', through='Authorship')


class Class(models.Model):
    def __str__(self):
        return self.name

    class_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    time = models.PositiveIntegerField(default=0)

    TYPE_CHOICES = (
        (1, '本科生课程'),
        (2, '研究生课程'),
    )
    type = models.PositiveIntegerField(choices=TYPE_CHOICES)

    teachers = models.ManyToManyField('Teacher', through='Teaching')


class Project(models.Model):
    def __str__(self):
        return self.name

    proj_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)

    TYPE_CHOICES = (
        (1, '国家级项目'),
        (2, '省部级项目'),
        (3, '市厅级项目'),
        (4, '企业合作项目'),
        (5, '其他类型项目'),
    )
    type = models.PositiveIntegerField(choices=TYPE_CHOICES)
    funds = models.FloatField(default=0.)
    startYear = models.PositiveIntegerField(default=0)
    endYear = models.PositiveIntegerField(default=0)

    leaders = models.ManyToManyField('Teacher', through='Leading')


class Authorship(models.Model):
    def __str__(self):
        return self.author.name + " - " + self.paper.name + " 的论文关系"

    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)

    rank = models.PositiveIntegerField(default=0)
    is_corresponding_author = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'paper'], name='unique_authorship'),
            models.UniqueConstraint(fields=['paper', 'rank'], name='unique_authorship_rank')
        ]


class Teaching(models.Model):
    def __str__(self):
        return self.teacher.name + " - " + self.class_obj.name + " 的教学关系"
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)

    year = models.PositiveIntegerField(default=0)
    SEME_CHOICES = (
        (1, '春季学期'),
        (2, '夏季学期'),
        (3, '秋季学期'),
    )
    semester = models.PositiveIntegerField(choices=SEME_CHOICES)
    hours = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['teacher', 'class_obj', 'year', 'semester'], name="unique_teaching"),
        ]


class Leading(models.Model):
    def __str__(self):
        return self.leader.name + " - " + self.project.name + " 的项目关系"

    leader = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    rank = models.PositiveIntegerField(default=0)
    fund = models.FloatField(default=0.)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['leader', 'project'], name='unique_leading'),
            models.UniqueConstraint(fields=['project', 'rank'], name='unique_leading_rank')
        ]
