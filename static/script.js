const videoElement = document.querySelector('video');
const videoSelect = document.querySelector('select#videoSource');
const captureButton = document.querySelector('#captureButton');

const classType = document.getElementById('classType');
const probability1 = document.getElementById('probability1');
const brand = document.getElementById('brand');
const finalclassType = document.getElementById('finalclassType');
const finalbrand = document.getElementById('finalbrand');

const saveImageButton = document.getElementById('saveImageButton');
const selectors = [videoSelect];

function gotDevices(deviceInfos) {
    // Handles being called several times to update labels. Preserve values.
    const values = selectors.map(select => select.value);
    selectors.forEach(select => {
        while (select.firstChild) {
            select.removeChild(select.firstChild);
        }
    });

    for (let i = 0; i !== deviceInfos.length; ++i) {
        const deviceInfo = deviceInfos[i];
        // const option = document.createElement('option');
        // option.value = deviceInfo.deviceId;
        if (deviceInfo.kind === 'videoinput') {
            const option = document.createElement('option');
            option.value = deviceInfo.deviceId;
            option.text = deviceInfo.label || `camera ${videoSelect.length + 1}`;
            videoSelect.appendChild(option);
        } else {
            console.log('Some other kind of source/device: ', deviceInfo);
        }
    }

    selectors.forEach((select, selectorIndex) => {
        if (Array.prototype.slice.call(select.childNodes).some(n => n.value === values[selectorIndex])) {
            select.value = values[selectorIndex];
        }
    });
}

navigator.mediaDevices.enumerateDevices().then(gotDevices).catch(handleError);

function gotStream(stream) {
    window.stream = stream; // make stream available to console
    videoElement.srcObject = stream;
    // Refresh button list in case labels have become available
    return navigator.mediaDevices.enumerateDevices();
}

function handleError(error) {
    console.log('navigator.MediaDevices.getUserMedia error: ', error.message, error.name);
}

function start() {
    if (window.stream) {
      window.stream.getTracks().forEach(track => {
        track.stop();
      });
    }

    const videoSource = videoSelect.value;
    const constraints = {
        video: {deviceId: videoSource ? {exact: videoSource} : undefined}
    };
    navigator.mediaDevices.getUserMedia(constraints).then(gotStream).then(gotDevices).catch(handleError);
}

videoSelect.onchange = start;

captureButton.addEventListener('click', () => {
    var canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;   
    canvas.getContext('2d').drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    var imageData = canvas.toDataURL('image/jpeg');
    
    // 获取图片元素
    var imageElement = document.getElementById('capturedImage');
    imageElement.src = imageData; // 设置图片元素的src属性为截取到的图片数据URL
    
    // 将图片数据发送到后端
    fetch('/predictions', {
      method: 'POST',
      body: JSON.stringify({ image: imageData }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
        classType.innerHTML = data.class1;
        brand.innerHTML = data.class2;
        finalclassType.innerHTML = data.finalclass;
        finalbrand.innerHTML = data.finalbrand;
    })    
    .catch(error => {
      console.error('error：', error);
    });
  });

saveImageButton.addEventListener('click', () => {
    const imageElement = document.getElementById('capturedImage');
    const imageData = imageElement.src;

    saveImage(imageData);
});

function saveImage(imageData) {
    const link = document.createElement('a');
    link.href = imageData;
    link.download = 'captured_image.jpg';

    link.click();
}
start();