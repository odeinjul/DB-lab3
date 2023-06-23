from django.contrib import admin

from .models import Teacher, Class, Project, Paper, Teaching, Leading, Authorship

admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Project)
admin.site.register(Paper)
admin.site.register(Teaching)
admin.site.register(Leading)
admin.site.register(Authorship)