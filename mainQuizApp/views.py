import os

from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import UploadedFile, Tests
from googleDocsApi import upload_with_conversion, export_as_html_zip, make_single_html_file
from django.conf import settings
from bs4 import BeautifulSoup as BS

base_dir = settings.BASE_DIR


def main_page(request):
    return render(request, 'mainQuizApp/index.html')


def files_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        content = file.read()
        with open(f'{base_dir}\\mainQuizApp\\temp\\{request.user.username}.docx', 'wb') as f:
            f.write(content)
        file_id = upload_with_conversion(f'{base_dir}\\mainQuizApp\\temp\\{request.user.username}.docx')
        if file_id:
            messages.success(request, 'Congratulations by brother! Uploaded successful!!!')
            new_file = UploadedFile(user=request.user, file_id=file_id, name=file.name)
            new_file.save()
            os.remove(f'{base_dir}\\mainQuizApp\\temp\\{request.user.username}.docx')
            return redirect('tests')
        else:
            messages.error(request, 'Something was wrong. Talk with admin about it! Dont be shy, poops :3')
    files = UploadedFile.objects.filter(user=request.user)

    context_data = {'files': files}
    return render(request, 'mainQuizApp/tests.html', context=context_data)


def test_view(request):
    if request.method == 'POST':
        file_id = request.POST['file_id']
        lower_diapason = int(request.POST['lower_diapason'])
        upper_diapason = int(request.POST['upper_diapason'])
        if 'is_random' in request.POST:
            is_random = True
        else:
            is_random = False

        export_as_html_zip(file_id, f'{base_dir}\\mainQuizApp\\temp\\{request.user.username}.zip')
        make_single_html_file(f"{base_dir}/mainQuizApp/temp/{request.user.username}.zip", base_dir,
                              request.user.username)

        with open(f'{base_dir}\\mainQuizApp\\temp\\{request.user.username}\\index.html', 'r') as html:
            html = html.read().replace('\n            ', ' ')
            bs_object = BS(html, 'html.parser')
            p_list = bs_object.find_all('p')
            question_list = []
            question = ''
            question_array = []
            for i in range(len(p_list)):
                if 'question' in str(p_list[i].contents[0]):
                    while 'variant' not in str(p_list[i].contents[0]):
                        question += str(p_list[i]) + '<br>'
                        i += 1
                    question_array.append(question.replace('&lt;question&gt;', ''))
                    question_array.append(str(p_list[i]).replace('&lt;variant&gt;', ''))
                    question_array.append(str(p_list[i + 1]).replace('&lt;variant&gt;', ''))
                    question_array.append(str(p_list[i + 2]).replace('&lt;variant&gt;', ''))
                    question_array.append(str(p_list[i + 3]).replace('&lt;variant&gt;', ''))
                    question_array.append(str(p_list[i + 4]).replace('&lt;variant&gt;', ''))

                    question_list.append(question_array)
                    question = ''
                    question_array = []

        file = UploadedFile.objects.get(file_id=file_id)
        question_count = len(question_list)
        test = question_list[lower_diapason:upper_diapason]
        test_str = ''
        for questions in test:
            for question in questions:
                test_str += question + "|SpLiTeR|"
            test_str += "||SpLiTeR||"

        new_test = Tests(user=request.user, file=file, test=test_str, question_count=question_count)
        new_test.save()

        messages.success(request, "Successful uploading! Юхуу!")

        context_data = {'file_id': file_id}
        return render(request, 'mainQuizApp/test.html', context=context_data)


def testing_page(request, test_id):
    if request.method == "POST":
        pass
    quiz_obj = Tests.objects.get(pk=int(test_id))
    test_str = quiz_obj.test
    pre_questions_list = test_str.split("||SpLiTeR||")
    print(len(pre_questions_list))
    pre_questions_list.pop()
    question_list = []
    for i in range(len(pre_questions_list)):
        questions = pre_questions_list[i].split("|SpLiTeR|")
        questions.pop()
        question_list.append(questions)

    return render(request, 'mainQuizApp/testing_page.html', {'questions_list': question_list})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('login')
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
