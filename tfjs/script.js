const video = document.getElementById('webcam');
const localStream = document.getElementById('localStream');
const enableWebcamButton = document.getElementById('webcamButton');

const modelsSection = document.getElementById('models');

const optionsSection = document.getElementById('options');
const cocoSsdOptionsSection = document.getElementById('cocoSsdOptions');
const handPoseOptionsSection = document.getElementById('handPoseOptions');

const detectPersonToggleSwitch = document.getElementById('personSwitch');
const detectObjectToggleSwitch = document.getElementById('objectSwitch');

// function to hide a section of the page
function hideSection(section) {
  section.classList.add('hidden');
}

// function to show a section of the page
function showSection(section) {
  section.classList.remove('hidden');
}

// function to hide all options sections of the page
function hideAllOptionsSections() {
  hideSection(cocoSsdOptionsSection);
  hideSection(handPoseOptionsSection);
}


function optionsManager() {
  hideAllOptionsSections();
  if (modelType == "ssd") {
    showSection(cocoSsdOptionsSection);
  } else if (modelType == "handpose") {
    showSection(handPoseOptionsSection);
  }
}

var model = undefined;
var modelType = undefined;

// var faceMeshModel = undefined; // face mesh model for face tracking
var cocoSsdModel = undefined; // object detection model for object detection
var bodyPixModel = undefined; // body segmentation model for person segmentation
var faceLandmarksModel = undefined; // face landmarks model for face tracking
var handPoseModel = undefined; // hand pose model for hand tracking
// var irisModel = undefined; // iris model for eye tracking
// var semanticSegmentationModel = undefined; // semantic segmentation model for image labeling
var toxicityModel = undefined; // toxicity model for text labeling


// function to load all models
async function loadModels() {
  // timer to measure how long it takes to load all models
  const start = performance.now();
  cocoSsdModel = await cocoSsd.load();
  faceMeshModel = await facemesh.load();
  bodyPixModel = await bodyPix.load();
  // faceLandmarksModel = await faceLandmarksDetection.load(faceLandmarksDetection.SupportedPackages.mediapipeFacemesh);
  handPoseModel = await handpose.load();
  // irisModel = await iris.load();
  // semanticSegmentationModel = await semanticSegmentation.load(semanticSegmentation.SupportedPackages.pascal);
  toxicityModel = await toxicity.load();
  // stop the timer and log the time it took to load all models
  const end = performance.now();
  // write the time it took to load all the models to the models section of the page
  let modelsLoadTime = Math.round((end - start) / 1000);
  document.getElementById('modelsLoadTime').innerHTML = `Models loaded in ${modelsLoadTime} seconds`;
  // show the model selection section
  showSection(modelsSection);
}

// determine which model type has been selected from the radio buttons
function determineModelType() {
  modelType = document.querySelector('input[name="modelType"]:checked').value;
  if (modelType == "facemesh") {
    model = faceMeshModel;
  } else if (modelType == "bodypix") {
    model = bodyPixModel;
  } else if (modelType == "facelandmarks") {
    model = faceLandmarksModel;
  } else if (modelType == "handpose") {
    model = handPoseModel;
  } else if (modelType == "iris") {
    model = irisModel;
  } else if (modelType == "semanticsegmentation") {
    model = semanticSegmentationModel;
  } else if (modelType == "toxicity") {
    model = toxicityModel;
  } else {
    model = cocoSsdModel;
  }

  // show the demo section
  showSection(optionsSection);
  optionsManager();
}

// load all models
loadModels();

// wait for the user to select a model type
document.querySelectorAll('input[name="modelType"]').forEach(el => el.addEventListener('change', (event) => {
  determineModelType();
}));

// Check if webcam access is supported.
function getUserMediaSupported() {
  return !!(navigator.mediaDevices &&
    navigator.mediaDevices.getUserMedia);
}


if (getUserMediaSupported()) {
  enableWebcamButton.addEventListener('click', enableCam);
} else {
  console.warn('getUserMedia() is not supported by your browser');
}

function enableCam(event) {
  if (!model) {
    return;
  }
  event.target.classList.add('removed');
  const constraints = {

    video: {
      width: { ideal: 600 },
      height: { ideal: 400 }
    }
  };
  video.setAttribute('autoplay', '');
  video.setAttribute('muted', '');
  video.setAttribute('playsinline', '');
  navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
    video.srcObject = stream;
    video.addEventListener('loadeddata', predictWebcam);
  });
}

var box = [];


function predictWebcam() {

  if (modelType == "ssd") {
    model.detect(video).then(function (predictions) {
      for (let i = 0; i < box.length; i++) {
        localStream.removeChild(box[i]);
      }
      box.splice(0);
      for (let n = 0; n < predictions.length; n++) {
        if (predictions[n].class == 'person' && !detectPersonToggleSwitch.checked) {
          continue;
        }
        // If the prediction is not a person but the object switch is not on, skip it.
        if (predictions[n].class != 'person' && !detectObjectToggleSwitch.checked) {
          continue;
        }


        // If we are over 50% sure we are sure we classified it right, draw the frame and label
        if (predictions[n].score > 0.50) {
          const p = document.createElement('p');
          let score = parseFloat(predictions[n].score) * 100;
          p.innerText = predictions[n].class + ': '
            + score.toFixed(2)
            + '% certainty';
          p.style = 'margin-left: ' + predictions[n].bbox[0] + 'px; margin-top: '
            + (predictions[n].bbox[1]) + 'px; width: '
            + (predictions[n].bbox[2]) + 'px; top: 0; left: 0;';

          const frame = document.createElement('div');
          frame.setAttribute('class', 'frame');
          frame.style = 'left: ' + predictions[n].bbox[0] + 'px; top: '
            + predictions[n].bbox[1] + 'px; width: '
            + predictions[n].bbox[2] + 'px; height: '
            + predictions[n].bbox[3] + 'px;';

          localStream.appendChild(frame);
          localStream.appendChild(p);
          box.push(frame);
          box.push(p);
        }
      }
      window.requestAnimationFrame(predictWebcam);
    });
  } else if (modelType == "handpose") {
    // display the webcam video but do not run the model
    window.requestAnimationFrame(predictWebcam);
  } else if (modelType == "facemesh") {
  } else if (modelType == "bodypix") {
  }
}


