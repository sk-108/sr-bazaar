// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get the message timer element
    const messageTimer = document.getElementById("message-timer");
    
    // Only proceed if the element exists and has a style property
    if (messageTimer && messageTimer.style) {
        setTimeout(function() {
            try {
                // Double-check the element still exists and has style
                const timer = document.getElementById("message-timer");
                if (timer && timer.style) {
                    timer.style.display = "none";
                }
            } catch (error) {
                console.warn("Could not hide message timer:", error);
            }
        }, 2500);
    }
});
