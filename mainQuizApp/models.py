from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    questions_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('test', kwargs={"file_id": self.file_id})

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Загруженный файл'
        verbose_name_plural = 'Загруженные файлы'


class Tests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)
    finished_at = models.DateTimeField(blank=True, null=True)
    test_array = models.JSONField(default=list, blank=True)
    question_count = models.IntegerField()
    result = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.user) + ' | ' + self.file.name

    @property
    def get_test_name(self):
        return self.file.name if self.file else 'Какие то траблы с названием теста брат('

    def get_test_url(self):
        return reverse('test-view', args=[str(self.pk)])

    class Meta:
        ordering = ['started_at']
        verbose_name = 'Лог тестов'
        verbose_name_plural = 'Логи тестов'
