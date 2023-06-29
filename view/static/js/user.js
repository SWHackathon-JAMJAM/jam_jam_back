/* signIn, signUp */
const nextToPw = document.querySelector('#next');
const nextToPlay = document.querySelector('#next-done');

if (nextToPlay === null) {
    nextToPw.addEventListener('click', (event) => {
        // check name
        window.location = 'http://127.0.0.1:5000/web/login_name_back';
    });
} else {
    nextToPlay.addEventListener('click', (event) => {
        // check pw
        window.location = 'http://127.0.0.1:5000/web/info';
    });
}