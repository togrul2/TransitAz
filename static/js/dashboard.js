let [...forms] = document.querySelectorAll('.form-wrapper');
let [...buttons] = document.querySelectorAll('.radio-choice');

buttons.forEach(button =>{
    button.addEventListener('change',() => {
    forms.forEach(form => {form.classList.add('hidden')});
    if(button.id === 'radio-bus')
        forms[0].classList.remove('hidden');
    else if(button.id === 'radio-train')
        forms[1].classList.remove('hidden');
    });
});

