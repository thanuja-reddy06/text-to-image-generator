// Wait for page to load
document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const button = document.querySelector(".btn");

    // Create loading message
    const loadingText = document.createElement("p");
    loadingText.innerText = "⏳ Generating image, please wait...";
    loadingText.style.display = "none";
    loadingText.style.fontWeight = "bold";

    if (form) {
        form.appendChild(loadingText);

        form.addEventListener("submit", function () {

            // Change button text
            if (button) {
                button.innerText = "Generating...";
                button.disabled = true;
            }

            // Show loading message
            loadingText.style.display = "block";
        });
    }

});