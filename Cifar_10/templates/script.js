document.addEventListener("DOMContentLoaded", function () {
    const uploadForm = document.getElementById("uploadForm");
    const imageInput = document.getElementById("imageInput");
    const previewImg = document.getElementById("previewImg");
    const resultText = document.getElementById("resultText");

    // Event listener for file input change to preview the image
    imageInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                previewImg.src = e.target.result;
                previewImg.style.display = "block";  // Display the image preview
            };
            reader.readAsDataURL(file);  // Read and preview the image
        }
    });

    // Event listener for form submission
    uploadForm.addEventListener("submit", function (event) {
        event.preventDefault();  // Prevent page reload

        // Create a FormData object to send the file to the server
        const formData = new FormData();
        formData.append("file", imageInput.files[0]);

        // Send the image to the server via AJAX
        fetch("/predict", {
            method: "POST",
            body: formData,
        })
        .then(response => response.text())
        .then(data => {
            // Update the result text with the server's response
            resultText.innerText = data;
        })
        .catch(error => {
            console.error("Error:", error);
            resultText.innerText = "An error occurred. Please try again.";
        });
    });
});
