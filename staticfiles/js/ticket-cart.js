let data = JSON.parse(localStorage.getItem('tickets'));
const table = document.querySelector('#tickets_accordion');
let content = "";
if(data)
for(let i = 0; i < data.length; i++) {
    const t1 = new Date(0,0,0, data[i].departure_time.substr(11, 2), data[i].departure_time.substr(14, 2))
    const t2 = new Date(0,0,0, data[i].arrive_time.substr(11, 2), data[i].arrive_time.substr(14, 2))
    let result = t2.getTime() - t1.getTime();
    let seat_btns_txt = "";
    for (let j = 1;j <= Number(data[i].total_seats); j++) {
        if (JSON.parse(data[i].seats).includes(j)) {
            if(data[i].seats_selected.includes(j))
                seat_btns_txt += `<button data-parent="${data[i].id}" class="seat-btn-${data[i].id} seat-btn btn active btn-outline-primary btn-sm m-1">${j}</button>`;
            else
                seat_btns_txt += `<button data-parent="${data[i].id}" class="seat-btn-${data[i].id} seat-btn btn btn-outline-primary btn-sm m-1">${j}</button>`;
        }
        else
            seat_btns_txt += `<button class="btn btn-outline-primary btn-sm m-1" disabled>${j}</button>`;
    }

    content += `
        <div class="accordion-item">
            <h2 class="accordion-header" id="heading-${data[i].id}">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapse-${data[i].id}" aria-expanded="false" aria-controls="flush-collapse-${data[i.id]}">
                    <i class="fas fa-${data[i].type === 'Bus' ? 'bus' : 'train'}"></i>&nbsp;
                    ${data[i].name}
                    ${data[i].departure_time.substr(0,10)}&nbsp;
                    <i class="fas fa-user"></i>&nbsp;
                    <span class="counts">${data[i].count}</span>
                </button>
            </h2>
            <div id="flush-collapse-${data[i].id}" class="accordion-collapse collapse" aria-labelledby="flush-heading-${data[i].id}" data-bs-parent="#tickets_accordion">
                <div class="accordion-body">
                    <p>${data[i].name}: ${data[i].departure_time.substr(0, 10)} ${data[i].departure_time.substr(11,5)} - ${data[i].arrive_time.substr(11,5)}</p>
                    <p>Kategoriya: ${data[i].type}</p>
                    <p>Qiymet: <span class="prices">${data[i].price}</span> AZN</p>
                    <p>Yerl??r: </p> 
                    <div class="seats" id="seats_of_${data[i].id}">${seat_btns_txt}</div>
                    <button class="delete-btn btn btn-danger my-2" data-id="${data[i].id}">Delete</button>
                </div>
            </div>
        </div>
    `
}
else
    content='<div class="alert alert-warning">Hal haz??rda s??b??t bo??dur. S??b??t?? bilet ??lav?? etm??k ??????n <a href="/ticket/">axtar????</a> hiss??sin?? ke??in</div>';

table.innerHTML = content;

let [...seat_btns] = document.getElementsByClassName('seat-btn');

seat_btns.forEach(btn=>{
    btn.addEventListener('click', () => {
        let item = data.find(el => el.id === btn.dataset.parent);
        let index = data.findIndex(el => el.id === btn.dataset.parent);
        item.seats_selected.push(Number(btn.textContent));
        item.seats_selected.shift();
        console.log(item.seats_selected)
        let buttons = document.querySelectorAll(`.seat-btn-${item.id}`);
        for(let j = 0; j < buttons.length; j++){
            buttons[j].classList.remove("active");
            if (item.seats_selected.includes(Number(buttons[j].textContent)))
                buttons[j].classList.add("active");
        }
        data[index] = item;
        localStorage.setItem("tickets", JSON.stringify(data));
    });
});

function updateValues(){
    const ps = document.querySelectorAll('.info_p');
    const [...prices] = document.getElementsByClassName('prices');
    const [...counts] = document.getElementsByClassName('counts');
    console.log(counts)
    let total = 0, count = 0;
    for(let i = 0; i < prices.length; i++){
        total += Number(prices[i].textContent);
        count += Number(counts[i].textContent);
    }
    ps[0].textContent = `Toplam m??bl????: ${total.toFixed(2)} AZN`;
    ps[1].textContent = `Bilet say??: ${count} ??d??d`;
}

updateValues();

const [...deleteBtns] = document.getElementsByClassName('delete-btn');

deleteBtns.forEach((btn) => {
    btn.addEventListener('click',() => {
        data = data.filter(el => el.id !== btn.dataset.id)
        localStorage.setItem('tickets', JSON.stringify(data));
        updateCountBadge();
        location.reload();
        hidePurchaseButton();
    })
})

function hidePurchaseButton(){
    if(data == null || data.length === 0) {
        const pay_group_item = document.querySelector('.pay-group-item');
        pay_group_item.classList.add('hidden');
    }
}
//
hidePurchaseButton();


const purchaseButton = document.querySelector('.pay-btn');
purchaseButton.addEventListener('click', () => {
    fetch('/ticket/proceedtopay/',{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(localStorage.getItem('tickets'))
    })
    .then(response => {
        console.log(response.status)
        if (response.status === 200)
            localStorage.removeItem('tickets');
        return response.json()
    })
});
