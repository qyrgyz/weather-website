document.addEventListener('DOMContentLoaded', (event) => {
    // Select all radio buttons for unit toggle
    const unitRadios = document.querySelectorAll('.unit-toggle input[type="radio"]');
    unitRadios.forEach(radio => {
        // Add change event listener to each radio button
        radio.addEventListener('change', () => {
            // Get the search form and current city value
            const form = document.querySelector('.search-container');
            const currentCity = document.querySelector('.search-container input[name="city"]').value;
            const unit = radio.value; // Get the selected unit value
            // Redirect to the updated URL with the selected unit and current city
            const url = `/?city=${currentCity}&unit=${unit}`;
            window.location.href = url;
        });
    });

    // Select all forecast items to apply custom background colors based on time of day
    const forecastItems = document.querySelectorAll('.forecast-item');
    forecastItems.forEach(item => {
        // Get the time text and extract the hour
        const timeText = item.querySelector('.forecast-time').innerText;
        const hour = parseInt(timeText.split(':')[0]);

        // Apply class based on the hour
        if (hour >= 20 || hour < 6) {
            item.classList.add('night');
        } else if (hour >= 6 && hour < 12) {
            item.classList.add('morning');
        } else if (hour >= 12 && hour < 20) {
            item.classList.add('day');
        }
    });

    // Remove unit toggle and geolocation button if not on home page
    if (window.location.pathname !== '/' && !window.location.pathname.startsWith('/geo')) {
        const unitToggle = document.querySelector('.unit-toggle');
        if (unitToggle) {
            unitToggle.remove();
        }
        const geoButton = document.getElementById('geoButton');
        if (geoButton) {
            geoButton.remove();
        }
    }
});

// Geolocation button handler
document.getElementById('geoButton')?.addEventListener('click', function() {
    if (navigator.geolocation) {
        // Get the current position of the user
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const unit = document.querySelector('.unit-toggle input[type="radio"]:checked').value;
            // Redirect to the URL with latitude, longitude, and unit
            const url = `/geo_weather?lat=${lat}&lon=${lon}&unit=${unit}`;
            window.location.href = url;
        }, function(error) {
            // Handle errors
            alert('Unable to retrieve your location. Please try again.');
        });
    } else {
        // Alert if geolocation is not supported
        alert('Geolocation is not supported by this browser.');
    }
});
