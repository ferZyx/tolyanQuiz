form = document.querySelector('#form')
count_from_error = document.querySelector('#count-from-error-msg')
count_to_error = document.querySelector('#count-to-error-msg')
count_error = document.querySelector('#count-error-msg')


function deleteErrors(){
    count_from_error.innerHTML = ""
    count_to_error.innerHTML = ""
    count_error.innerHTML = ""
}

form.addEventListener('submit', function (e) {
    e.preventDefault()
    count_from = document.querySelector('#lower').value
    count_to = document.querySelector('#high').value
    count = document.querySelector('#count').value
    current_subject = document.querySelector("#selector").value
    
    if (count_from && count_to && count){
        localStorage['count_from'] = count_from
        localStorage['count_to'] = count_to
        localStorage['count'] = count
        localStorage['current_subject'] = current_subject
        
        window.location.href = 'test.html'
        }
    else{
        deleteErrors()
        if (!count_from){
            count_from_error.innerHTML = "Введите нижний диапазон вопросов"
        }
        if (!count_to){
            count_to_error.innerHTML = "Введите верхний диапазон вопросов"
        }
        if (!count){
            count_error.innerHTML = "Введите сколько вопросов хотите прорешать"
        }
    }

})