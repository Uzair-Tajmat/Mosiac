const videoElement = document.querySelector("video");
const controlsContainer = document.querySelector(".controls");
var exerciseContainer = document.querySelector(".exercise-container");
const playButton = document.querySelector(".play");
const stopButton = document.querySelector(".stop");
const rewindButton = document.querySelector(".rwd");
const forwardButton = document.querySelector(".fwd");

const timerWrapper1 = document.querySelector(".timer");
const timerDisplay1 = document.querySelector(".timer span");
const timerBar1 = document.querySelector(".timer div");
let resultOutput = document.querySelector(".output");
videoElement.removeAttribute("controls");
controlsContainer.style.visibility = "visible";
const progressElement = document.querySelector(".progress");

playButton.addEventListener("click", togglePlayPause);
stopButton.addEventListener("click", stopVideo);
videoElement.addEventListener("ended", stopVideo);

rewindButton.addEventListener("click", rewindVideo);
forwardButton.addEventListener("click", forwardVideo);
videoElement.addEventListener("timeupdate", updateTimer);

let rewindInterval;
let forwardInterval;

function togglePlayPause() {
  rewindButton.classList.remove("active");
  forwardButton.classList.remove("active");
  clearInterval(rewindInterval);
  clearInterval(forwardInterval);

  if (videoElement.paused) {
    playButton.setAttribute("data-icon", "u");
    videoElement.play();
    console.log("Playing");
  } else {
    playButton.setAttribute("data-icon", "P");
    const isPaused = videoElement.pause();
    const currentPausedTime = Math.floor(videoElement.currentTime);
    console.log("Paused at:", currentPausedTime, "seconds");
    sendPauseTime(currentPausedTime);
  }
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

let receivedData;
let globalTitle;

function sendPauseTime(currentTime) {
  const csrftoken = getCookie("csrftoken");
  fetch("Main/handle_pause_time/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ paused_time: currentTime }),
  })
    .then((response) => response.json())
    .then((data) => {
      var exerciseHTML = "";
      data.generatedResponse.forEach((responseItem) => {
        exerciseHTML += `<form class="content" action="AllContent" method="post">
          <h3 class="title" id="title">${responseItem.title}</h3>
          <input type="hidden" name="title" id="titleInput" value="${responseItem.title}">
          <input type="hidden" name="data" class="data" id="data" value="${responseItem.response}">
          <button class="goTo" type="submit"><p class="arrow">&rarr;</p></button>
        </form>`;
      });

      exerciseContainer.innerHTML = exerciseHTML;
      console.log("Success:", data.generatedResponse);
      console.log(data.title);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function stopVideo() {
  rewindButton.classList.remove("active");
  forwardButton.classList.remove("active");
  videoElement.pause();
  videoElement.currentTime = 0;
  clearInterval(rewindInterval);
  clearInterval(forwardInterval);
  playButton.setAttribute("data-icon", "P");
}

function rewindVideo() {
  clearInterval(forwardInterval);
  forwardButton.classList.remove("active");

  if (rewindButton.classList.contains("active")) {
    rewindButton.classList.remove("active");
    clearInterval(rewindInterval);
    videoElement.play();
  } else {
    rewindButton.classList.add("active");
    videoElement.pause();
    rewindInterval = setInterval(rewindPlayback, 200);
  }
}

function forwardVideo() {
  console.log(videoElement.currentTime);
  clearInterval(rewindInterval);
  rewindButton.classList.remove("active");

  if (forwardButton.classList.contains("active")) {
    forwardButton.classList.remove("active");
    clearInterval(forwardInterval);
    videoElement.play();
  } else {
    forwardButton.classList.add("active");
    videoElement.pause();
    forwardInterval = setInterval(forwardPlayback, 200);
  }
}

function rewindPlayback() {
  if (videoElement.currentTime <= 3) {
    rewindButton.classList.remove("active");
    clearInterval(rewindInterval);
    stopVideo();
  } else {
    videoElement.currentTime -= 3;
  }
}

function forwardPlayback() {
  if (videoElement.currentTime >= videoElement.duration - 3) {
    forwardButton.classList.remove("active");
    clearInterval(forwardInterval);
    stopVideo();
  } else {
    videoElement.currentTime += 3;
  }
}

function updateTimer() {
  const minutes = Math.floor(videoElement.currentTime / 60);
  const seconds = Math.floor(videoElement.currentTime - minutes * 60);

  const minuteValue = minutes.toString().padStart(2, "0");
  const secondValue = seconds.toString().padStart(2, "0");

  const mediaTime = `${minuteValue}:${secondValue}`;
  timerDisplay1.textContent = mediaTime;

  const barLength =
    timerWrapper1.clientWidth *
    (videoElement.currentTime / videoElement.duration);
  timerBar1.style.width = `${barLength}px`;
}
