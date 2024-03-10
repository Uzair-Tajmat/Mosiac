const script = document.createElement('script');
script.src = 'https://cdn.jsdelivr.net/npm/tesseract.js@2.4.2/dist/tesseract.min.js';
document.head.appendChild(script);
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
    const isPaused=media.pause();
    console.log("Paused");
    const currentTime1=media.currentTime;
    console.log(currentTime1);
    call=setInterval(calling,3000);
    // if (isPaused && currentTime >180) {
    //     console.log("More than 3 minutes");
    // }
    
  }
}
let resultShow=document.getElementById('#output');
function calling(){
    console.log("Done");
    clearInterval(call);
    const video = document.getElementById('video');
      const canvas = document.getElementById('canvas');
      const context = canvas.getContext('2d');
      
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      let imageDataUrl = canvas.toDataURL('image/png');
      // window.open(dataURL);
      script.onload = async () => {
        try {
          const result = await Tesseract.recognize(
            imageDataUrl,
            'eng', // language
            { logger: m => console.log(m) } // logger
          );
          // Display the extracted text
          document.getElementById('#output').innerText = result.data.text;
        } catch (error) {
          console.error('Error during text recognition:', error);
        }
      };     
       
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


  // const canvas=document.querySelector('canvas');
  // const ctx=canvas.getContext('2d');
  
  // // media.addEventListener('loadedmetadata',()=>{
  // //   canvas.height=media.height;
  // //   canvas.width=media.width;
  // // })
  
  // media.addEventListener('play',()=>{
  //   ctx.drawImage(media,0,0 )
  // })

