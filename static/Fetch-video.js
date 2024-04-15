function fetchVideos() {
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
  xhr.open("GET", "/fetch_videos/", true); // Replace '/fetch_videos/' with the URL of your Django view
  xhr.send();
}

function displayVideos(videos) {
  var playlistSection = document.querySelector(".playlist-section");
  var playlistHTML = "";
  videos.forEach(function (video) {
    var thumbnailUrl = "/static/default_thumnail.jpeg";
    var title = video.name.replace(/\.[^.]*$/, "");
    playlistHTML += `<a href="${video.path}" class="videoPlaylist">
          <div class="thumbnail">
          <img src="${thumbnailUrl}"  class="img"/> </div>
          <div class="info-section">
              <h4 class="title">${title}</h4>
          </div>
      </a>`;
    playlistHTML += "<br>"; // Add line break
  });
  playlistSection.innerHTML = playlistHTML;
}

window.onload = fetchVideos;
