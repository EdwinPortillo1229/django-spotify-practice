document.addEventListener('DOMContentLoaded', function() {
    var artist1Input = document.querySelector('input[name="artist1"]');
    var artist2Input = document.querySelector('input[name="artist2"]');
    var artist3Input = document.querySelector('input[name="artist3"]');
    var vibeInput = document.querySelector('input[name="vibe"]');
    var submitButton = document.querySelector('#submit-button');

    artist1Input.addEventListener('change', function() {
        const artist1 = artist1Input.value;
        const artist2 = artist2Input.value;
        const artist3 = artist3Input.value;
        const vibe = vibeInput.value;

        if (artist1 && artist2 && artist3 && vibe) {
            submitButton.disabled = false;
            submitButton.classList.remove('disabled');
        } else {
            submitButton.disabled = true;
            submitButton.classList.add('disabled');
        }
    });
    artist1Input.addEventListener('keyup', function() {
        const artist1 = artist1Input.value;
        const artist2 = artist2Input.value;
        const artist3 = artist3Input.value;
        const vibe = vibeInput.value;

        if (artist1 && artist2 && artist3 && vibe) {
            submitButton.disabled = false;
            submitButton.classList.remove('disabled');
        } else {
            submitButton.disabled = true;
            submitButton.classList.add('disabled');
        }
    });

    artist2Input.addEventListener('change', function() {
        const artist1 = artist1Input.value;
        const artist2 = artist2Input.value;
        const artist3 = artist3Input.value;
        const vibe = vibeInput.value;

        if (artist1 && artist2 && artist3 && vibe) {
            submitButton.disabled = false;
            submitButton.classList.remove('disabled');
        } else {
            submitButton.disabled = true;
            submitButton.classList.add('disabled');
        }
    });

    artist2Input.addEventListener('keyup', function() {
        const artist1 = artist1Input.value;
        const artist2 = artist2Input.value;
        const artist3 = artist3Input.value;
        const vibe = vibeInput.value;

        if (artist1 && artist2 && artist3 && vibe) {
            submitButton.disabled = false;
            submitButton.classList.remove('disabled');
        } else {
            submitButton.disabled = true;
            submitButton.classList.add('disabled');
        }
    });

    artist3Input.addEventListener('change', function() {
        const artist1 = artist1Input.value;
        const artist2 = artist2Input.value;
        const artist3 = artist3Input.value;
        const vibe = vibeInput.value;

        if (artist1 && artist2 && artist3 && vibe) {
            submitButton.disabled = false;
            submitButton.classList.remove('disabled');
        } else {
            submitButton.disabled = true;
            submitButton.classList.add('disabled');
        }
    });

    artist3Input.addEventListener('keyup', function() {
        const artist1 = artist1Input.value;
        const artist2 = artist2Input.value;
        const artist3 = artist3Input.value;
        const vibe = vibeInput.value;

        if (artist1 && artist2 && artist3 && vibe) {
            submitButton.disabled = false;
            submitButton.classList.remove('disabled');
        } else {
            submitButton.disabled = true;
            submitButton.classList.add('disabled');
        }
    });

    vibeInput.addEventListener('change', function() {
        const artist1 = artist1Input.value;
        const artist2 = artist2Input.value;
        const artist3 = artist3Input.value;
        const vibe = vibeInput.value;

        if (artist1 && artist2 && artist3 && vibe) {
            submitButton.disabled = false;
            submitButton.classList.remove('disabled');
        } else {
            submitButton.disabled = true;
            submitButton.classList.add('disabled');
        }
    });

    vibeInput.addEventListener('keyup', function() {
        const artist1 = artist1Input.value;
        const artist2 = artist2Input.value;
        const artist3 = artist3Input.value;
        const vibe = vibeInput.value;

        if (artist1 && artist2 && artist3 && vibe) {
            submitButton.disabled = false;
            submitButton.classList.remove('disabled');
        } else {
            submitButton.disabled = true;
            submitButton.classList.add('disabled');
        }
    });

    vibeInput.dispatchEvent(new Event('keyup'));
});
