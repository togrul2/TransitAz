// For displayig different search forms
let [...forms] = document.querySelectorAll('.form-wrapper');
let [...formButtons] = document.querySelectorAll('.radio-choice');

formButtons.forEach(formbutton =>{
    formbutton.addEventListener('change',() => {
    forms.forEach(form => {form.classList.add('hidden')});
    if(formbutton.id === 'radio-bus')
        forms[0].classList.remove('hidden');
    else if(formbutton.id === 'radio-train')
        forms[1].classList.remove('hidden');
    });
});

// Disabling chosing past dates

let [...dateInputs] = document.querySelectorAll('.date-input');
const date = new Date();
const str = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;

dateInputs.forEach(dateInput => {
    dateInput.min = str;
});

// Add action

[...addButtons] = document.getElementsByClassName('add-button');

addButtons.forEach(addButton => {
    addButton.addEventListener('click', () => {
        const item = {
            id: addButton.dataset.item_id,
            type:addButton.dataset.item_type,
            name: addButton.dataset.item_name,
            price: addButton.dataset.item_price,
            starting_point: addButton.dataset.item_starting_point,
            destination: addButton.dataset.item_destination,
            departures_at : addButton.dataset.item_departures_at ,
            arrives_at: addButton.dataset.item_arrives_at,
            seats_remain: addButton.dataset.item_seats_remain,
            count:1,
        };
        
        data = JSON.parse(localStorage.getItem("tickets"));
        if(data)
            if(data.filter(e => e.id === item.id && e.type === item.type).length === 0)
                data.push(item);
        else if(data == [])
            data = [item];
        
        localStorage.setItem("tickets", JSON.stringify(data));
        updateCountBadge();
    });
});
