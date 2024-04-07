function getCookie1(name) {
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

window.addEventListener("beforeunload", (event) => {
  var video = document.getElementById("video");
  var totalDuration = video.duration;
  var csrftoken = getCookie1("csrftoken");
  var playbackTime = video.currentTime;

  $.ajax({
    url: "/closingWindow/",
    type: "POST",
    headers: { "X-CSRFToken": csrftoken },
    data: { total_duration: totalDuration, playback_time: playbackTime },
    dataType: "json",
    success: function (response) {
      console.log("Playback time sent successfully.");
    },
    error: function (xhr, errmsg, err) {
      console.error("Failed to send playback time:", errmsg);
    },
  });
  event.returnValue = " ";
});
