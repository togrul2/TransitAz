// For displaying different search forms
const forms = document.querySelectorAll('.form-wrapper');
const formButtons = document.querySelectorAll('.radio-choice');

forms.forEach(form => {form.classList.add('hidden')});
if(formButtons[0].checked)
    forms[0].classList.remove('hidden');
else if(formButtons[1].checked)
    forms[1].classList.remove('hidden');

formButtons.forEach(formButton =>{
    formButton.addEventListener('change',() => {
       forms[0].classList.toggle('hidden');
       forms[1].classList.toggle('hidden');
    });
});

// Disabling choosing past dates and arrive date for one way tickets
const dateInputs = document.querySelectorAll('.date-input');
const zeroPad = (num, places) => String(num).padStart(places, '0')
const date = new Date();
const str = `${date.getFullYear()}-${zeroPad(date.getMonth() + 1, 2)}-${zeroPad(date.getDate(), 2)}`;
const is_one_way = document.getElementById('gedis-tek');
const arrive_dates = document.querySelectorAll('.arrive-date');
document.forms[0].addEventListener('change', ()=>{
    arrive_dates.forEach(arrive_date=>arrive_date.disabled=is_one_way.checked);
});

dateInputs.forEach(dateInput => {
    dateInput.min = str;
});

const info_buttons = document.querySelectorAll('.more-info-btn');
const data = JSON.parse(localStorage.getItem('tickets'));
info_buttons.forEach(info_btn=>{
    let id = info_btn.dataset.id.split('_')[1];
    if(data && data.find(value => value.id === id))
        info_btn.classList.add('added');
});

// Add action
const add_buttons = document.querySelectorAll('.add-btn');
add_buttons.forEach(btn => {
    let data = JSON.parse(localStorage.getItem("tickets"));
    if(data && data.find(value => value.id === btn.dataset.id && value.type === btn.dataset.type))
        btn.classList.add('added');

    btn.addEventListener('click', ()=>{
        const item = {
            id:btn.dataset.id,
            name:btn.dataset.name,
            type:btn.dataset.type,
            count:btn.dataset.count,
            departure_time:btn.dataset.departure_time,
            arrive_time:btn.dataset.arrive_time,
            transport:btn.dataset.transport,
            price:Number(Number(btn.dataset.price) * Number(btn.dataset.count)).toFixed(2),
            seats:btn.dataset.seats,
            total_seats:btn.dataset.total_seats,
        };
        const parent_btn = document.getElementById(btn.dataset.btn_target);
        parent_btn.classList.add('added');
        btn.classList.add('added');
        // console.log(parent_btn);

        item.seats_selected = JSON.parse(item.seats).slice(0, item.count);

        if(data == null)
            data = [item];
        else if(!data.filter(el=>el.id===item.id).length)
            data.push(item);

        localStorage.setItem('tickets', JSON.stringify(data));
        updateCountBadge();
    });
});
