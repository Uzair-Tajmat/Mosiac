const script = document.createElement("script");
const media = document.querySelector("video");
const controls = document.querySelector(".controls");

const play1 = document.querySelector(".play");
const stop = document.querySelector(".stop");
const rwd = document.querySelector(".rwd");
const fwd = document.querySelector(".fwd");

const timerWrapper = document.querySelector(".timer");
const timer = document.querySelector(".timer span");
const timerBar = document.querySelector(".timer div");

media.removeAttribute("controls");
controls.style.visibility = "visible";
const progress = document.querySelector(".progress");

play1.addEventListener("click", playPauseMedia);
stop.addEventListener("click", stopMedia);
media.addEventListener("ended", stopMedia);

rwd.addEventListener("click", mediaBackward);
fwd.addEventListener("click", mediaForward);
media.addEventListener("timeupdate", setTime);

let call;
function playPauseMedia() {
  rwd.classList.remove("active");
  fwd.classList.remove("active");
  clearInterval(intervalRwd);
  clearInterval(intervalFwd);
  if (media.paused) {
    play1.setAttribute("data-icon", "u");
    media.play();
    console.log("Playing");
  } else {
    play1.setAttribute("data-icon", "P");
    const isPaused = media.pause();
    const currentTime1 = media.currentTime;
    console.log("Paused");
    call = setInterval(calling(currentTime1), 3000);
  }
}
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function calling(ctr1) {
  clearInterval(call);
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const context = canvas.getContext("2d");

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  let imageDataUrl = canvas.toDataURL("image/jpg");
  var csrftoken = getCookie("csrftoken");
  $(document).ready(function () {
    var status = ctr1;
    $.ajax({
      url: "/pausedContent/",
      method: "POST",
      headers: { "X-CSRFToken": csrftoken },
      data: {},
      success: function (response) {
        console.log("Done");
        sendImageToBackend(imageDataUrl);
      },
      error: function (xhr, status, error) {},
    });
  });
}

function sendImageToBackend(imgData) {
  var formData = new FormData();
  formData.append("image_data", imgData);

  fetch("/pausedContent/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        console.log("Image sent successfully");
      } else {
        console.error("Failed to send image");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function stopMedia() {
  rwd.classList.remove("active");
  fwd.classList.remove("active");
  media.pause();
  media.currentTime = 0;
  clearInterval(intervalRwd);
  clearInterval(intervalFwd);
  play1.setAttribute("data-icon", "P");
}

let intervalFwd;
let intervalRwd;

function mediaBackward() {
  clearInterval(intervalFwd);
  fwd.classList.remove("active");

  if (rwd.classList.contains("active")) {
    rwd.classList.remove("active");
    clearInterval(intervalRwd);
    media.play();
  } else {
    rwd.classList.add("active");
    media.pause();
    intervalRwd = setInterval(windBackward, 200);
  }
}

function mediaForward() {
  clearInterval(intervalRwd);
  rwd.classList.remove("active");

  if (fwd.classList.contains("active")) {
    fwd.classList.remove("active");
    clearInterval(intervalFwd);
    media.play();
  } else {
    fwd.classList.add("active");
    media.pause();
    intervalFwd = setInterval(windForward, 200);
  }
}

function windBackward() {
  if (media.currentTime <= 3) {
    rwd.classList.remove("active");
    clearInterval(intervalRwd);
    stopMedia();
  } else {
    media.currentTime -= 3;
  }
}

function windForward() {
  if (media.currentTime >= media.duration - 3) {
    fwd.classList.remove("active");
    clearInterval(intervalFwd);
    stopMedia();
  } else {
    media.currentTime += 3;
  }
}

function setTime() {
  const minutes = Math.floor(media.currentTime / 60);
  const seconds = Math.floor(media.currentTime - minutes * 60);

  const minuteValue = minutes.toString().padStart(2, "0");
  const secondValue = seconds.toString().padStart(2, "0");

  const mediaTime = `${minuteValue}:${secondValue}`;
  timer.textContent = mediaTime;

  const barLength =
    timerWrapper.clientWidth * (media.currentTime / media.duration);
  timerBar.style.width = `${barLength}px`;
}
