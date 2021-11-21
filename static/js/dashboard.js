let [...buttons] = document.querySelectorAll('.form-select-type');
let [...forms] = document.querySelectorAll('.form-wrapper');

    console.log(buttons);
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            buttons.forEach(button => { button.classList.remove('active') });
            button.classList.add('active');
            
            forms.forEach(form=>{form.classList.add('hidden');})
            let form = document.querySelector(`.form-${button.dataset.form}`);
            form.classList.remove('hidden');
        })
    });