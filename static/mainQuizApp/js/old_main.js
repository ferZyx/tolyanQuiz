const quiz = document.getElementById('quiz');
const questionElement = document.getElementById('question');
let quizCounterCQ = document.querySelector(".quiz-counter__current-question")
let quizCounterQA = document.querySelector(".quiz-counter__question-amount")

const a_text = document.getElementById('a_text');
const b_text = document.getElementById('b_text');
const c_text = document.getElementById('c_text');
const d_text = document.getElementById('d_text');
const e_text = document.getElementById('e_text');

const mainBtn = document.getElementById("mainBtn")

let currentQuestion = 0

let isAnswered = false

let correct_li = undefined


quizCounterQA.innerHTML = quizData.length

function loadQuiz(currentQuestionID) {
    const  currentQuizData = quizData[currentQuestionID];
    questionElement.innerHTML = currentQuizData.question;
    quizCounterCQ.innerHTML = currentQuestionID + 1

    li_list.forEach(element => {
        element.childNodes[1].checked = false
    })
    quiz.classList.remove('correct')
    quiz.classList.remove('incorrect')

    a_text.innerHTML = currentQuizData.a;
    b_text.innerHTML = currentQuizData.b;
    c_text.innerHTML = currentQuizData.c;
    d_text.innerHTML = currentQuizData.d;
    e_text.innerHTML = currentQuizData.e;


    answer = myAnswers[currentQuestionID]
    if (answer) {
        document.querySelector("#" + answer).checked = true
    }


}

/*Это то что тебе нужно брат // */
/*                          <=  */

// Получение CSRF токена из cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Найдем CSRF токен, если он есть
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const myAnswers = {
    csrfmiddlewaretoken: getCookie('csrftoken'), // Получение CSRF токена из cookies
    test_pk: window.location.pathname.split('/').slice(-2, -1)[0],
};

function pushAnswer(currentQuestionID, myAnswer) {
    myAnswers[currentQuestionID] = myAnswer
}


//Для выбора ответов
let li_list = document.querySelectorAll(".li");
li_list.forEach(element => {
    element.addEventListener("click", (event) => {
        if (!event.target.className) {
            pushAnswer(currentQuestion, event.target.closest(".text").previousElementSibling.id)

        }
        if (event.target.className == "answer") {
            pushAnswer(currentQuestion, event.target.id)

        }
        event.target.childNodes.forEach(element => {
            if (element.className == "answer") {
                event.target.childNodes[1].checked = true
                pushAnswer(currentQuestion, event.target.childNodes[1].id)

            }
        })
        // Боже мой сколько форычей, за то мне кажется я нашёл ошибку в мобильной версии тестов
    })
})

mainBtn.addEventListener("click", (event) => {
    if(isAnswered){
        currentQuestion += 1

        if (currentQuestion < quizData.length) {
            isAnswered = false
            mainBtn.innerHTML = "Ответить"

            correct_li.style = ""

            loadQuiz(currentQuestion)
        }
        else {
            mainBtn.innerHTML = "Считаю результат, жди"
            mainBtn.disabled = true;
            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Добавление CSRF токена в заголовок
                },
                body: JSON.stringify(myAnswers)
            };
            console.log(myAnswers)
            fetch(window.location.origin + '/finish_test/'  , options)
                .then(response => response.json())
                .then(data => {
                    if ('redirect' in data) {
                        window.location.href = data.redirect;
                    }
                });
        }
    }
    else {
        if(myAnswers[currentQuestion]){
            if(myAnswers[currentQuestion] == quizData[currentQuestion].correct){
                quiz.classList.add('correct')

                correct = document.querySelector('#' + quizData[currentQuestion].correct)
                correct_li = correct.closest('li');
                correct_li.style.border = 'solid LimeGreen'

            }
            else{
                correct = document.querySelector('#' + quizData[currentQuestion].correct)
                correct_li = correct.closest('li');

                correct_li.style.border = 'solid LimeGreen'

                quiz.classList.add('incorrect')
            }
            console.log(myAnswers)
            isAnswered = true
            mainBtn.innerHTML = "Дальше"
        }
        else{
            console.log("Вариант ответа выбери, придурок.")
        }
    }
})




loadQuiz(currentQuestion);
