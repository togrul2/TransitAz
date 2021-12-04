const logout_btn = document.querySelector('.logout-link');

if(logout_btn != null)
    logout_btn.addEventListener('click', () => {
        console.log("Removed");
        localStorage.removeItem('tickets');
    });