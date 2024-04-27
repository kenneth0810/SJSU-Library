// this script makes an anchor tag act as a submit button for the logout function
// for navigation bar aesthetic reasons
const logoutBtn = document.getElementById('logout-btn');
const logoutForm = document.getElementById('logout-form');

logoutBtn.addEventListener('click', (e) => {
    e.preventDefault();
    logoutForm.submit();
})

