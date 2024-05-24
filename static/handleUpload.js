function uploadFile() {
  const fileInput = document.getElementById("upload-file");
  const file = fileInput.files[0];

  if (!file) {
    alert("No file selected.");
    return;
  }
  console.log("File REcived");
  const formData = new FormData();
  formData.append("file", file);

  fetch("Upload/", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        alert("File uploaded successfully!");
      } else {
        throw new Error("Failed to upload file.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while uploading the file.");
    });
}
