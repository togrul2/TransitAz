const data = JSON.parse(localStorage.getItem('tickets'));
const [table] = document.getElementsByClassName('table-body');

let str = "";
if(data)
for(let i = 0; i < data.length; i++) {
    str +=`
    <tr>
        <td>${i + 1}</td>
        <td>${data[i].type == 'bus-search' ? 'Avtobus' : 'Qatar'}</td>
        <td>${data[i].starting_point} - ${data[i].destination}</td>
        <td>${data[i].departures_at} - ${data[i].arrives_at}</td>
        <td class="ticket-price" data-price="${data[i].price}">${data[i].price}</td>
        <td><input class="quantity-input form-control-sm" type="number" min=1 max=${data[i].seats_remain} value=${data[i].count}></td>
        <td><button class='btn delete-btn' data-item_index="${i}"><i class="fas fa-trash-alt"></i></button><td>
    </tr>
    `;
}
table.innerHTML = str;




const [...quantity_input] = document.getElementsByClassName('quantity-input');
const [...prices] = document.getElementsByClassName('ticket-price');
const [...deleteBtns] = document.getElementsByClassName('delete-btn');

quantity_input.forEach((item, index) => {
    item.addEventListener('change', () => {
        let result = (prices[index].dataset.price * item.value).toFixed(2);
        prices[index].textContent = result;
        data[index].count = item.value;
        localStorage.setItem('tickets', JSON.stringify(data));
        updateCountBadge();
    })
})

// console.log(deleteBtns);

deleteBtns.forEach((item) => {
    item.addEventListener('click',() => {
        console.log("Clicked:", item.dataset.item_index);
        console.log(item.parentNode.parentNode)
        item.parentNode.parentNode.remove();
        data.pop(item.dataset.item_index);
        console.log(data);
        localStorage.setItem('tickets', JSON.stringify(data));
        updateCountBadge();
    })
})
