const loginForm = document.querySelector('.login');
const loginBtn = loginForm.querySelector('button');
const gameForm = document.querySelector('#game');

function onCLickLogin() {
    loginForm.classList.add('hidden');
    gameForm.classList.remove('hidden');
    const cam = document.createElement('video');
    const game = document.createElement('canvas');
    gameForm.append(cam);
    gameForm.append(game);
}

loginBtn.addEventListener('click', onCLickLogin);