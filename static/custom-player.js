const media = document.querySelector("video");
const controls = document.querySelector(".controls");
var exerciseSection = document.querySelector(".exercise-container");
const play1 = document.querySelector(".play");
const stop = document.querySelector(".stop");
const rwd = document.querySelector(".rwd");
const fwd = document.querySelector(".fwd");

const timerWrapper = document.querySelector(".timer");
const timer = document.querySelector(".timer span");
const timerBar = document.querySelector(".timer div");
let resultShow = document.querySelector(".output");
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
    const currentTime1 = Math.floor(media.currentTime);
    console.log("Paused at:", currentTime1, "seconds");
    sendPauseTime(currentTime1);
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

let dataRecieved;
let globaltitle;
function sendPauseTime(currentTime) {
  const csrftoken = getCookie("csrftoken");
  fetch("Main/handle_pause_time/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken, // Include the CSRF token in the headers
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

      exerciseSection.innerHTML = exerciseHTML;
      console.log("Success:", data.generatedResponse);
      console.log(data.title);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// function fetchdata() {
//   console.log("CALLED");
//   fetch("./static/response_data.json")
//     .then((response) => {
//       if (!response.ok) {
//         throw new Error("Network response was not ok");
//       }
//       return response.json();
//     })
//     .then((data) => {
//       var exerciseHTML = "";

//       data.forEach(function (item, index) {
//
//       });

//       // Set the inner HTML of the exercise section to the generated HTML
//       exerciseSection.innerHTML = exerciseHTML;
//     })
//     .catch((error) => {
//       console.error("Error fetching data:", error);
//     });
// }
// setInterval(fetchdata(), 5000);
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
  console.log(media.currentTime);
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
