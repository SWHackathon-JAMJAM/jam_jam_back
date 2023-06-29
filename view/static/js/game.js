const ok = document.querySelector('#ok');
const timer = document.querySelector('#timer span:last-child');
let time = 10;
let gameTime = 20;

function ruleHidden() {
    const ruleForm = document.querySelector('#game-rule');
    const timer = document.querySelector('#timer');
    ruleForm.classList.add('hidden');
    timer.classList.remove('hidden');
}

function timerStart() {
    gameTime = 20;
    setInterval(() => {
        --gameTime;
        timer.innerText = gameTime;
        if (gameTime < 0) {
            timer.innerText = "--";
            window.location.href = 'http://127.0.0.1:5000/menu/gameresult'
        }
    }, 1000);
}

setInterval(() => {
    time--;
    ok.innerText = `${time}초 후 자동으로 게임이 시작됩니다.`;
}, 1000);

function startGame() {
    const startText = document.querySelector('#reday-start');
    startText.classList.remove('hidden');
    setTimeout(() => {
        startText.innerText = "게임 시작";
    }, 2000);
    setTimeout(() => {
        startText.classList.add('hidden');
    }, 3000);
}

setTimeout(ruleHidden, 10000);
setTimeout(startGame, 10000);
setTimeout(timerStart, 14000); 