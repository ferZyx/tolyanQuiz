import json
import os
import random

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import UploadedFile, Tests
from googleDocsApi import upload_with_conversion, export_as_html_zip, make_single_html_file, get_questions_count
from django.conf import settings
from bs4 import BeautifulSoup as BS
from django.core.cache import cache
from django.utils import timezone
from django.urls import reverse

base_dir = settings.BASE_DIR
abcde_array = ['a', 'b', 'c', 'd', 'e']


def main_page(request):
    return render(request, 'mainQuizApp/index.html')


def mytests_view(request):
    # if request.method == 'POST':
    #     file = request.FILES['file']
    #     content = file.read()
    #     with open(f'{base_dir}\\mainQuizApp\\temp\\{request.user.username}.docx', 'wb') as f:
    #         f.write(content)
    #     file_id = upload_with_conversion(f'{base_dir}\\mainQuizApp\\temp\\{request.user.username}.docx')
    #     if file_id:
    #         messages.success(request, 'Congratulations by brother! Uploaded successful!!!')
    #         new_file = UploadedFile(user=request.user, file_id=file_id, name=file.name)
    #         new_file.save()
    #         os.remove(f'{base_dir}\\mainQuizApp\\temp\\{request.user.username}.docx')
    #         return redirect('tests')
    #     else:
    #         messages.error(request, 'Something was wrong. Talk with admin about it! Dont be shy, poops :3')
    # files = UploadedFile.objects.filter(user=request.user)
    started_tests = Tests.objects.filter(user=request.user, is_finished=False).values('file__name', 'question_count',
                                                                                      'started_at', 'pk')
    finished_tests = Tests.objects.filter(user=request.user, is_finished=True).values('file__name', 'question_count',
                                                                                      'finished_at', 'pk', 'result')
    files = UploadedFile.objects.filter(user=request.user).values('name', 'file_id', 'uploaded_at', 'questions_count',
                                                                  'pk')
    context_data = {'title': ' Мои тесты',
                    'started_tests': started_tests,
                    'finished_tests': finished_tests,
                    'files': files,
                    }
    return render(request, 'mainQuizApp/mytests.html', context=context_data)


def upload_docx(request):
    if request.method == 'POST':
        file = None
        if 'file' in request.FILES:
            file = request.FILES['file']
        if not file:
            messages.error(request, 'Вы не указали файл!')
            return redirect('mytests')
        content = file.read()
        with open(f'{base_dir}\\mainQuizApp\\temp\\{request.user.username}.docx', 'wb') as f:
            f.write(content)
        file_id = upload_with_conversion(f'{base_dir}\\mainQuizApp\\temp\\{request.user.username}.docx')
        questions_count = get_questions_count(file_id)
        if file_id and questions_count:
            messages.success(request, 'Congratulations by brother! Uploaded successful!!!')
            new_file = UploadedFile(user=request.user, file_id=file_id, name=file.name, questions_count=questions_count)
            new_file.save()
            os.remove(f'{base_dir}\\mainQuizApp\\temp\\{request.user.username}.docx')
            return redirect('mytests')
        else:
            messages.error(request, 'Something was wrong. Talk with admin about it! Dont be shy, poops :3')

    # started_tests = Tests.objects.filter(user=request.user, is_finished=False).values('file__name', 'question_count',
    #                                                                                   'started_at', 'pk')
    # finished_tests = Tests.objects.filter(user=request.user, is_finished=True).values('file__name', 'question_count',
    #                                                                                   'finished_at', 'pk')
    # files = UploadedFile.objects.filter(user=request.user).values('name', 'file_id')
    # context_data = {'title': ' Мои тесты',
    #                 'started_tests': started_tests,
    #                 'finished_tests': finished_tests,
    #                 'files': files,
    #                 }
    # return render(request, 'mainQuizApp/mytests.html', context=context_data)


def test_config_view(request, file_pk):
    if request.method == 'POST':
        lower_diapason = int(request.POST['lower_diapason'])
        upper_diapason = int(request.POST['upper_diapason'])
        if 'is_random' in request.POST:
            is_random = True
        else:
            is_random = False

        file_data = UploadedFile.objects.filter(pk=file_pk).values('file_id')
        file_id = file_data[0]['file_id']
        export_as_html_zip(file_id, f'{base_dir}/mainQuizApp/temp/{request.user.username}.zip')
        make_single_html_file(f"{base_dir}/mainQuizApp/temp/{request.user.username}.zip", base_dir,
                              request.user.username)

        with open(f'{base_dir}/mainQuizApp/temp/{request.user.username}/index.html', 'r') as html:
            html = html.read().replace('\n            ', ' ')
            bs_object = BS(html, 'html.parser')
            p_list = bs_object.find_all('p')
            question_dict_list = []
            question = ''
            answers_array = []
            for i in range(len(p_list)):
                if 'question' in str(p_list[i].contents[0]):
                    while 'variant' not in str(p_list[i].contents[0]):
                        question += str(p_list[i]) + '<br>'
                        i += 1
                    answers_array.append(str(p_list[i]).replace('&lt;variant&gt;', ''))
                    answers_array.append(str(p_list[i + 1]).replace('&lt;variant&gt;', ''))
                    answers_array.append(str(p_list[i + 2]).replace('&lt;variant&gt;', ''))
                    answers_array.append(str(p_list[i + 3]).replace('&lt;variant&gt;', ''))
                    answers_array.append(str(p_list[i + 4]).replace('&lt;variant&gt;', ''))
                    correct_answer = answers_array[0]
                    random.shuffle(answers_array)

                    question_dict = {
                        'question': question.replace('&lt;question&gt;', ''),
                        'answer1': answers_array[0],
                        'answer2': answers_array[1],
                        'answer3': answers_array[2],
                        'answer4': answers_array[3],
                        'answer5': answers_array[4],
                        'correct_answer': abcde_array[answers_array.index(correct_answer)]
                    }
                    question_dict_list.append(question_dict)
                    question = ''
                    answers_array = []
        question_dict_list = question_dict_list[lower_diapason:upper_diapason]
        if is_random:
            random.shuffle(question_dict_list)

        file = UploadedFile.objects.get(pk=file_pk)
        new_test = Tests(user=request.user, file=file, test_array=question_dict_list,
                         question_count=len(question_dict_list))
        new_test.save()

        cache_key = f"user_data_{request.user.id}|{new_test.pk}"
        cache.set(cache_key, new_test, 300)

        return redirect('test_view', new_test.pk)
    else:
        file = UploadedFile.objects.get(pk=file_pk)
        context = {
            'title': 'Настройка тестирования',
            'file': file,
        }
        return render(request, 'mainQuizApp/test_config.html', context)


def testing_view(request, test_pk):
    cache_key = f"user_data_{request.user.id}|{test_pk}"

    test = cache.get(cache_key)
    if not test:
        test = Tests.objects.get(pk=test_pk)
        print('no test')
    if test.user != request.user:
        return redirect('mytests')
    if test.is_finished:
        return redirect('test_result_view', test_pk)
    context = {
        "title": "Тестирование! Юхуу",
        "test_array": test.test_array,
    }
    return render(request, 'mainQuizApp/quiz_tester.html', context)


def finish_test(request):
    if request.method == "POST":
        answers = json.loads(request.body)
        answers.pop('csrfmiddlewaretoken', None)  # удаление ключа 'csrfmiddlewaretoken' из словаря
        test_pk = int(answers.pop("test_pk"))

        test = Tests.objects.get(pk=test_pk)

        if test.is_finished:
            return redirect('mytests')

        question_dict_list = test.test_array

        result = 0

        for i in range(len(question_dict_list)):
            if answers.get(str(i)) == question_dict_list[i]['correct_answer']:
                result += 1

        test.result = result
        test.is_finished = True
        test.finished_at = timezone.now()

        test.save()
        return JsonResponse({'redirect': reverse('test_result_view', args=[test_pk])})


def test_result_view(request, test_pk):
    print(test_pk)
    return render(request, 'mainQuizApp/test_result.html')


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, 'Вы успешно зарегистрированы!')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('home')

        else:
            messages.error(request, 'Ошибка регистрации, перепроверьте данные!')
    else:
        form = UserRegisterForm()
    return render(request, 'mainQuizApp/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно авторизованы!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка авторизации, перепроверьте данные!')
    else:
        form = UserLoginForm(auto_id=True)
    return render(request, 'mainQuizApp/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
