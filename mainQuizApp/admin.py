from django.contrib import admin
from .models import UploadedFile, Tests
from django import forms


class UploadedFileAdminForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = '__all__'


class UploadedFileAdmin(admin.ModelAdmin):
    form = UploadedFileAdminForm
    save_on_top = True
    list_display = ('pk', 'user', 'name', 'uploaded_at', 'questions_count')
    list_display_links = ('pk', 'user', 'name', 'uploaded_at', 'questions_count')
    search_fields = ('user__username', 'name',)
    list_filter = ('user',)
    readonly_fields = ('uploaded_at', )
    fields = ('user', 'file_id', 'name', 'uploaded_at', 'questions_count')


class TestsAdminForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = '__all__'


class TestsAdmin(admin.ModelAdmin):
    form = TestsAdminForm
    save_on_top = True
    list_display = ('pk', 'user', 'file', 'started_at', 'is_finished', 'finished_at', 'question_count', 'result')
    list_display_links = ('pk', 'user', 'file', 'started_at', 'is_finished', 'finished_at', 'question_count', 'result')
    search_fields = ('user__username', 'file__name',)
    list_filter = ('user', 'is_finished')
    readonly_fields = ('user', 'started_at', 'finished_at', 'file', 'question_count')
    fields = ('user', 'file', 'started_at', 'is_finished', 'finished_at', 'question_count', 'result', 'test_array')


# Register your models here.
admin.site.register(UploadedFile, UploadedFileAdmin)
admin.site.register(Tests, TestsAdmin)
