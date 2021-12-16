const [...tickets] = document.querySelectorAll('.custom-card')
tickets.forEach(ticket=> {
    ticket.addEventListener('click', ()=>{
        ticket.children[1].classList.toggle('hidden');
    });
});

const filter_select = document.querySelector("#filter");
filter_select.addEventListener('change', ()=>{
    document.forms[0].submit();
})
