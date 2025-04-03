
document.addEventListener('DOMContentLoaded', function() {
    // Get references to the input fields and button
    const productUrlInput = document.getElementById('product_url');
    const targetPriceInput = document.getElementById('target_price');
    const trackPriceButton = document.getElementById('trackPriceButton');

    // Function to check if both inputs are filled
    function checkFormValidity() {
        // Check if both fields are filled
        if (productUrlInput.value && targetPriceInput.value) {
            // Enable the button if both inputs are filled
            trackPriceButton.disabled = false;
        } else {
            // Otherwise, keep the button disabled
            trackPriceButton.disabled = true;
        }
    }

    // Attach the checkFormValidity function to the input fields' input event
    productUrlInput.addEventListener('input', checkFormValidity);
    targetPriceInput.addEventListener('input', checkFormValidity);

    // Initial check in case the form is already partially filled (e.g., if the page is refreshed)
    checkFormValidity();
});


// to show a confirmation alert when the user submits the form.

document.querySelector("form").addEventListener("submit", function(event) {
    alert("Tracking price...");
});
