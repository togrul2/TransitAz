const [...tickets] = document.querySelectorAll('.custom-card')
tickets.forEach(ticket=> {
    ticket.addEventListener('click', ()=>{
        ticket.children[1].classList.toggle('hidden');
    });
});

const [...selects] = document.querySelectorAll('.form-submit');
selects.forEach(select=>select.addEventListener('change', ()=>{
    document.forms[0].submit();
}));