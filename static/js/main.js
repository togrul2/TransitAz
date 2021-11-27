const logout_btn = document.querySelector('.logout-link')
logout_btn.addEventListener('click', () => {
    localStorage.removeItem('tickets');
});