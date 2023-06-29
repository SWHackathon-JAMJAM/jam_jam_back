let recognition;
let recordButton;
let recordingStartTime;

// �����ν� API ���� ���� Ȯ��
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {   
    // �����ν� ��ü ����
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'ko-KR'; // �����ν� ��� ����

    // ���� �ν� ��� �̺�Ʈ ó��
    recognition.onresult = function(event) {
    const result = event.results[0][0].transcript;
    processVoiceCommand(result);
    };
} else {
    // �����ν� API�� �������� �ʴ� ��� ó��
    console.log('�����ν��� �������� �ʴ� �������Դϴ�.');
}

function startRecognition() {
    recognition.start();
    recordingStartTime = Date.now(); // ��� ���� �ð� ����
}

// �信�� ������ �� �����ν� �ٷ� ����
startRecognition();

function processVoiceCommand(command) {
    console.log('Recognized command:', command);

    // ������ ���̵�(�̸�) �Ǵ� ��й�ȣ ������
    // const nextToPw = document.querySelector('#next');
    // const nextToPlay = document.querySelector('#next-done');

    // if (nextToPlay === null) {
    //     nextToPw.addEventListener('click', (event) => {
    //         sessionStorage.setItem("name", command);
    //         window.location = 'signIn.html';
    //     });
    // } else {
    //     nextToPlay.addEventListener('click', (event) => {
    //         sessionStorage.setItem("password", command);
    //         window.location = 'gameStart.html';
    //     });
    // }

    const inputForm = document.getElementsByTagName('input');
    inputForm.value = command;
}

function updateRecordingTime() {
    const currentTime = Date.now();
    const elapsedSeconds = Math.floor((currentTime - recordingStartTime) / 1000);
    console.log(`Recording time: ${elapsedSeconds} seconds`);
}

setInterval(updateRecordingTime, 1000);