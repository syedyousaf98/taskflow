from django.contrib import admin
from .models import Task, Category, Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
