// For displayig different search forms
const [...forms] = document.querySelectorAll('.form-wrapper');
const [...formButtons] = document.querySelectorAll('.radio-choice');

forms.forEach(form => {form.classList.add('hidden')});
if(formButtons[0].checked)
    forms[0].classList.remove('hidden');
else if(formButtons[1].checked)
    forms[1].classList.remove('hidden');

formButtons.forEach(formbutton =>{
    formbutton.addEventListener('change',() => {
       forms[0].classList.toggle('hidden');
       forms[1].classList.toggle('hidden');
    });
});

// Disabling choosing past dates and arrive date for one way tickets

const [...dateInputs] = document.querySelectorAll('.date-input');
const date = new Date();
const str = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
const is_one_way = document.querySelector('#gedis-tek');
const [...arrive_dates] = document.querySelectorAll('.arrive-date');

document.forms[0].addEventListener('change', ()=>{
    arrive_dates.forEach(arrive_date=>{
        arrive_date.disabled = is_one_way.checked;
    })
})

dateInputs.forEach(dateInput => {
    dateInput.min = str;
});

const [...info_btns] = document.querySelectorAll('.more-info-btn');
const data = JSON.parse(localStorage.getItem('tickets'));
info_btns.forEach(info_btn=>{
    let id = info_btn.dataset.id.split('_')[1];
    if(data && data.find(value => value.id == id))
        info_btn.classList.add('added');
});

// Add action
const [...addBtns] = document.querySelectorAll('.add-btn');
addBtns.forEach(btn => {
    btn.addEventListener('click', ()=>{
        let data = JSON.parse(localStorage.getItem("tickets"));
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

        item.seats_selected = JSON.parse(item.seats).slice(0, item.count)

        if(data == null){
            data = [item];
        }else{
            if(!data.filter(el=>el.id===item.id).length)
                data.push(item);
        }
        localStorage.setItem('tickets', JSON.stringify(data));

        updateCountBadge();
    });
});

// [...addButtons] = document.getElementsByClassName('add-button');
//
// addButtons.forEach(addButton => {
//     addButton.addEventListener('click', () => {
//         data = JSON.parse(localStorage.getItem("tickets"));
//
//         const item = {
//             id: data ? data.length: 0,
//             back_id: addButton.dataset.item_id,
//             type:addButton.dataset.item_type,
//             name: addButton.dataset.item_name,
//             price: addButton.dataset.item_price,
//             starting_point: addButton.dataset.item_starting_point,
//             destination: addButton.dataset.item_destination,
//             departures_at : addButton.dataset.item_departures_at ,
//             arrives_at: addButton.dataset.item_arrives_at,
//             seats_remain: addButton.dataset.item_seats_remain,
//             count:1,
//         };
//
//
//         let tickets;
//         if(data != null){
//             tickets = [...data]
//             if(data.filter(e => e.id === item.id && e.type === item.type).length === 0)
//                 tickets.push(item);
//         }
//         else
//             tickets = [item];
//
//         localStorage.setItem("tickets", JSON.stringify(tickets));
//         updateCountBadge();
//     });
// });
