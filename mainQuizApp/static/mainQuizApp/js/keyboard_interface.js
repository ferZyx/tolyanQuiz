document.addEventListener("keypress", (event) => {
   current_answer_elements = document.querySelectorAll('.answer');

   ;
   if (event.code === 'Enter' || event.code === "NumpadAdd" || event.code === "NumpadEnter") {
      btn_click();
   }
   if (event.code == 'Digit1' || event.code === "Numpad1") {
      current_answer_elements[0].checked = true;
   }
   if (event.code == 'Digit2' || event.code === "Numpad2") {
      current_answer_elements[1].checked = true;
   }
   if (event.code == 'Digit3' || event.code === "Numpad3") {
      current_answer_elements[2].checked = true;
   }
   if (event.code == 'Digit4' || event.code === "Numpad4") {
      current_answer_elements[3].checked = true;
   }
   if (event.code == 'Digit5' || event.code === "Numpad5") {
      current_answer_elements[4].checked = true;
   }
});