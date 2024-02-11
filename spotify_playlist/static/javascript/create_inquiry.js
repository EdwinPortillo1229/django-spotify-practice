document.addEventListener('DOMContentLoaded', function() {
    var artist1Input = document.querySelector('input[name="artist1"]');
    var artist2Input = document.querySelector('input[name="artist2"]');
    var artist3Input = document.querySelector('input[name="artist3"]');

    artist1Input.addEventListener('change', function() {
        console.log('change');
    });
    artist1Input.addEventListener('keyup', function() {
        console.log('keyup');
    });

});
