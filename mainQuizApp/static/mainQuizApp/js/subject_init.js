let count_from = +localStorage['count_from']
let count_to = +localStorage['count_to']
let count = +localStorage['count']
let quizData = ''

switch (localStorage['current_subject']) {
    case "history":
        quizData = history
        break
    case "psycho":
        quizData = psycho
        break
    case "pedagogics":
        quizData = pedagogics
        break
    case "testing":
        quizData = testing
        break
}

