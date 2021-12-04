let data = JSON.parse(localStorage.getItem('tickets'));
const [table] = document.getElementsByClassName('table-body');

let str = "";
if(data)
for(let i = 0; i < data.length; i++) {
    str +=`
    <tr>
        <td>${i + 1}</td>
        <td>${data[i].type === 'bus-search' ? 'Avtobus' : 'Qatar'}</td>
        <td>${data[i].starting_point} - ${data[i].destination}</td>
        <td>${data[i].departures_at} - ${data[i].arrives_at}</td>
        <td class="ticket-price" data-price="${data[i].price}">${data[i].price}</td>
        <td><input class="quantity-input form-control-sm" type="number" min=1 max=${data[i].seats_remain} value=${data[i].count}></td>
        <td><button class='btn delete-btn' data-item_index="${data[i].id}"><i class="fas fa-trash-alt"></i></button><td>
    </tr>
    `;
}

table.innerHTML = str;

updateValues();

const [...quantity_input] = document.getElementsByClassName('quantity-input');
const [...prices] = document.getElementsByClassName('ticket-price');
const [...deleteBtns] = document.getElementsByClassName('delete-btn');

quantity_input.forEach((item, index) => {
    item.addEventListener('change', () => {
        prices[index].textContent = (prices[index].dataset.price * item.value).toFixed(2);
        data[index].count = item.value;
        localStorage.setItem('tickets', JSON.stringify(data));
        updateCountBadge();
        updateValues();
    })
})


deleteBtns.forEach((item) => {
    item.addEventListener('click',() => {
        item.parentNode.parentNode.remove();
        data = data.filter(element => element.id !== Number(item.dataset.item_index));
        localStorage.setItem('tickets', JSON.stringify(data));
        updateCountBadge();
        updateValues();
        hidePurchaseButton();
    })
})


function updateValues(){
    const ps = document.querySelectorAll('.info_p');
    const [...prices] = document.getElementsByClassName('ticket-price');
    const [...quantity_input] = document.getElementsByClassName('quantity-input');
    let total = 0, count = 0;
    for(let i = 0; i < prices.length; i++){
        total += Number(prices[i].textContent);
        count += Number(quantity_input[i].value);
    }
    ps[0].textContent = `Toplam məbləğ: ${total.toFixed(2)} AZN`;
    ps[1].textContent = `Bilet sayı: ${count} ədəd`;
}


function hidePurchaseButton(){
    if(data == null || data.length === 0) {
        const pay_group_item = document.querySelector('.pay-group-item');
        pay_group_item.classList.add('hidden');
    }
}

hidePurchaseButton();

// Purchase action
const purchaseButton = document.querySelector('.pay-btn');
purchaseButton.addEventListener('click', () => {
    fetch('/ticket/proceedtopay/',{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(localStorage.getItem('tickets'))
    }
    ).then(response => {
        if (response.status == 200)
            localStorage.removeItem('tickets');        
        return response.json()});
});
