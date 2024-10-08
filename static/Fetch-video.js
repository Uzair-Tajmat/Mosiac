function fetchVideos() {
  const videoTitleElement = document.querySelector(".video-title-about");

  if (!videoTitleElement) {
    console.error("Element with class 'video-title-about' not found.");
    return;
  }

  const videoTitle = videoTitleElement.textContent.trim(); // Use textContent or innerText

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        var videos = JSON.parse(xhr.responseText);
        displayVideos(videos);
      } else {
        console.error("Failed to fetch videos. Status code: " + xhr.status);
      }
    }
  };
  xhr.open(
    "GET",
    `/fetch_videos/?title=${encodeURIComponent(videoTitle)}`,
    true
  ); // Replace '/fetch_videos/' with the URL of your Django view
  xhr.send();
}
function displayVideos(videos) {
  var playlistSection = document.querySelector(".playlist-section");
  var playlistHTML = "";
  videos.forEach(function (video, index) {
    var thumbnailUrl = "/static/default_thumnail.jpeg";
    var title = video.name.replace(/\.[^.]*$/, "");
    var videoId = "video-" + index;
    playlistHTML += `<a href="${video.path}" id="${videoId}" class="videoPlaylist" >
          <div class="thumbnail">
          <img src="${thumbnailUrl}"  class="img"/> </div>
          <div class="info-section">
              <h4 class="title">${title}</h4>
          </div>
      </a>`;
    playlistHTML += "<br>"; // Add line break
  });
  playlistSection.innerHTML = playlistHTML;
  videos.forEach(function (video, index) {
    var videoLink = document.getElementById("video-" + index);
    videoLink.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent the default link behavior
      var title = video.name.replace(/\.[^.]*$/, "");
      sendVideoPathToBackend(video.path, title);
    });
  });
}
function sendVideoPathToBackend(videoPath, vidIndex) {
  console.log(videoPath);
  fetch("Open", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ path: videoPath, id: vidIndex }),
  })
    .then((response) => {
      if (response.ok) {
        // Assuming the response is HTML content that you want to display
        return response.text();
      }
      throw new Error("Network response was not ok.");
    })
    .then((htmlContent) => {
      // You can create a new HTML page dynamically or navigate to a different URL
      // For example, you could dynamically insert the HTML into the current page
      document.open();
      document.write(htmlContent);
      document.close();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
window.onload = fetchVideos;
