const quiz = document.getElementById('quiz');
const answerElements = document.querySelectorAll('.answer');
const questionElement = document.getElementById('question');
const questionList = document.querySelector(".question-numlist")
const questionWrapper = document.querySelector(".shit")
let quizCounterCQ = document.querySelector(".quiz-counter__current-question")
let quizCounterQA = document.querySelector(".quiz-counter__question-amount")

const a_text = document.getElementById('a_text');
const b_text = document.getElementById('b_text');
const c_text = document.getElementById('c_text');
const d_text = document.getElementById('d_text');
const e_text = document.getElementById('e_text');

let currentQuestion = 0

function deselectCurrentQuestion() {
    const questionNumbers = document.querySelectorAll(".question-numitem")
    questionNumbers.forEach(element => {
        element.classList.remove("current")
    })
}

function selectFinishedQuestion() {
    const questionNumbers = document.querySelectorAll(".question-numitem")
    questionNumbers[currentQuestion].classList.add("finished")
}


quizCounterQA.innerHTML = quizData.length

function loadQuiz(currentQuestionID) {
    const currentQuizData = quizData[currentQuestionID];
    questionElement.innerHTML = currentQuizData.question;
    quizCounterCQ.innerHTML = currentQuestionID + 1


    a_text.innerHTML = currentQuizData.a;
    b_text.innerHTML = currentQuizData.b;
    c_text.innerHTML = currentQuizData.c;
    d_text.innerHTML = currentQuizData.d;
    e_text.innerHTML = currentQuizData.e;

    answer = myAnswers[currentQuestionID]
    if (answer) {
        document.querySelector("#" + answer).checked = true
    }

    deselectCurrentQuestion()
    const questionNumbers = document.querySelectorAll(".question-numitem")
    questionNumbers[currentQuestionID].classList.add("current")


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

function pushAnswer(answerId, myAnswer) {
    myAnswers[answerId] = myAnswer
}



//Для выбора ответов
let li_list = document.querySelectorAll(".li");
li_list.forEach(element => {
    element.addEventListener("click", (event) => {
        if (!event.target.className) {
            pushAnswer(currentQuestion, event.target.closest(".text").previousElementSibling.id)

            selectFinishedQuestion()
        }
        if (event.target.className == "answer") {
            pushAnswer(currentQuestion, event.target.id)

            selectFinishedQuestion()
        }
        event.target.childNodes.forEach(element => {
            if (element.className == "answer") {
                event.target.childNodes[1].checked = true
                pushAnswer(currentQuestion, event.target.childNodes[1].id)

                selectFinishedQuestion()
            }
        })
        // Боже мой сколько форычей, за то мне кажется я нашёл ошибку в мобильной версии тестов
    })
})


for (let i = 1; i <= quizData.length; i++) {
    questionList.innerHTML += `<div class="question-numitem">
    <div class="question-num">${i}</div>
    </div>`
}
questionList.insertAdjacentElement("afterbegin", questionWrapper)

loadQuiz(currentQuestion);
/*Это мои кнопочки отображают состояние current finished and standard*/
const questionItem = document.querySelectorAll(".question-numitem")
questionItem.forEach(element => {
    element.addEventListener("click", (e) => {

        li_list.forEach(element => {
            element.childNodes[1].checked = false
        })

        currentQuestion = e.target.innerText - 1
        loadQuiz(currentQuestion)

    })
})

const no = document.querySelector(".areusure-no")
const popup = document.querySelector(".popup-areusure")
const submit = document.querySelector("#submit")
console.log(popup)
no.addEventListener("click", () => {
    popup.classList.toggle("popup-fuck")
})

submit.addEventListener("click", () => {
    popup.classList.toggle("popup-fuck")
})

popup.addEventListener("click", (e) => {
    if (e.target == popup) {
        popup.classList.toggle("popup-fuck")
    }
})

const yes = document.querySelector('.areusure-yes')
yes.addEventListener('click', () => {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Добавление CSRF токена в заголовок
        },
        body: JSON.stringify(myAnswers)
    };
    console.log(myAnswers)
    fetch('http://127.0.0.1:8000/finish_test/' || 'tolyanquiz.onrender.com/finish_test/' , options)
        .then(response => response.json())
        .then(data => {
    if ('redirect' in data) {
      window.location.href = data.redirect;
    }
        });
})


