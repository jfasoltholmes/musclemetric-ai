document.addEventListener('DOMContentLoaded', function() {
    // Flash message handling
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        // Add delay to trigger fade-in effect
        setTimeout(function() {
            flashMessages.classList.remove('hide-msg');
            flashMessages.classList.add('show-msg');

            // Get success and error message elements
            const successMsg = document.getElementById('success-msg');
            const errorMsg = document.getElementById('error-msg');

            if (successMsg) {
                successMsg.classList.remove('hide-msg');
                successMsg.classList.add('show-msg');
            }
            if (errorMsg) {
                errorMsg.classList.remove('hide-msg');
                errorMsg.classList.add('show-msg');
            }

            // Set timeout to remove flash messages after 5 seconds
            setTimeout(function() {
                flashMessages.classList.remove('show-msg');
                flashMessages.classList.add('hide-msg');

                setTimeout(function() {
                    flashMessages.remove();
                }, 500); 
            }, 5000); // Show for 5 seconds
        }, 100);


        // Manual click removal, instant
        flashMessages.addEventListener('click', function() {
            flashMessages.remove();
        });
    }
});