let imgSubmission = document.getElementById('img-submission');
let imageInput = document.getElementById('image-input');
let photoButton = document.getElementById('photo-button');
let submissionContainer = document.getElementById('submission-container');
let origSubmissionContainerHTML;

// Function to handle image preview
function handleImageChange() {
    let imgLink = URL.createObjectURL(imageInput.files[0]);

    imgSubmission.style.backgroundImage = `url(${imgLink})`;
    imgSubmission.innerHTML= '';

    imgSubmission.removeEventListener('mouseover', imgSubmissionMouseOver);
    imgSubmission.removeEventListener('mouseout', imgSubmissionMouseOut);

    imgSubmission.style.border = '';
    imgSubmission.style.cursor = '';

    const label = imgSubmission.closest('label');
    if (label) {
        label.style.pointerEvents = 'none';
    }

    const buttonNav = document.getElementById('disclaimer');
    buttonNav.innerHTML = `
        <button id="cancel-button">Cancel</button>
        <button type="submit" id="analyze-button">Analyze</button>`;

    document.getElementById('cancel-button').addEventListener('click', function(e) {
        e.stopPropagation();
        cancelUpload();
    });
};

imageInput.addEventListener('change', handleImageChange);
// End of image preview function

// Set-up reusable event listeners
function setupEventListeners() {
    // Photo button
    photoButton.addEventListener('click', function(e) {
        e.preventDefault();
        imageInput.click();
    });

    photoButton.addEventListener('mouseover', function() {
        photoButton.style.backgroundColor = '#f0f0f0';
        photoButton.style.cursor = 'pointer';
    });

    photoButton.addEventListener('mouseout', function() {
        photoButton.style.backgroundColor = '';
    });

    // imgSubmission mouseover and mouseout
    imgSubmission.addEventListener('mouseover', imgSubmissionMouseOver);
    imgSubmission.addEventListener('mouseout', imgSubmissionMouseOut);

    // Drag and drop functionality
    imgSubmission.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        imgSubmission.style.border = 'dashed 2px #999999';
        imgSubmission.style.backgroundColor = '#f0f0f0';
        imgSubmission.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-image-plus-icon lucide-image-plus"><path d="M16 5h6"/><path d="M19 2v6"/><path d="M21 11.5V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7.5"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/><circle cx="9" cy="9" r="2"/></svg>
        <h3 id="dragdrop">Drop your image here</h3>`;
    });

    imgSubmission.addEventListener('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        if (!imgSubmission.contains(e.relatedTarget)) {
            submissionContainer.innerHTML = origSubmissionContainerHTML;

            imgSubmission = document.getElementById('img-submission');
            imageInput = document.getElementById('image-input');
            photoButton = document.getElementById('photo-button');
            submissionContainer = document.getElementById('submission-container');
            setupEventListeners();
        }
    });

    imgSubmission.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        imageInput.files = e.dataTransfer.files;
        handleImageChange();
    });

    // Image input change listener
    imageInput.addEventListener('change', handleImageChange);
}


// Function to cancel image upload
function cancelUpload() {
    submissionContainer.innerHTML = origSubmissionContainerHTML;

    imgSubmission = document.getElementById('img-submission');
    imageInput = document.getElementById('image-input');
    photoButton = document.getElementById('photo-button');

    setupEventListeners();

    imageInput.value = '';
};
// End of cancel image upload function

// imgSubmission hover effects
function imgSubmissionMouseOver() {
    imgSubmission.style.border = 'dashed 2px #999999';
    imgSubmission.style.cursor = 'pointer';
}

function imgSubmissionMouseOut() {
    imgSubmission.style.border = '';
}


// Function for type text animation
const subTitle = document.getElementById('sub-title');
const cursor = document.querySelector('.cursor');
const words = [
    "Scan.\xa0",
    "Analyze.\xa0",
    "Progress.",
];
let textIndex = 0;
let charIndex = 0;
let currentText = '';
function typeText() {
    if (charIndex <= words[textIndex].length - 1) {
        currentText += words[textIndex].charAt(charIndex);
        subTitle.innerHTML = currentText + '<div class="cursor blink">&nbsp;</div>';
        charIndex++;
        setTimeout(typeText, 125);
    } else {
        textIndex++;
        charIndex = 0;

        if ( textIndex < words.length) {
            setTimeout(typeText, 575);
        }
    }
}
// End of type text animation


document.addEventListener('DOMContentLoaded', function() {
    //Store original HTML content to use when canceling upload
    origSubmissionContainerHTML = submissionContainer.innerHTML;

    // Set up initial event listeners
    setupEventListeners();
    
    //typeText animation
    setTimeout(typeText, 120);

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

