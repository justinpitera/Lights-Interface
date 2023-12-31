$(document).ready(function() {
    $('#lightOn').click(function() {
        $.ajax({
            url: '/turn-on-light/',
            type: 'get',
            success: function(response) {
                console.log('Light ON:', response.status);
            },
            error: function() {
                console.log('Error turning on the light');
            }
        });
    });

    $('#lightOff').click(function() {
        $.ajax({
            url: '/turn-off-light/',
            type: 'get',
            success: function(response) {
                console.log('Light OFF:', response.status);
            },
            error: function() {
                console.log('Error turning off the light');
            }
        });
    });

    // JavaScript to handle color changes
    document.getElementById('colorPicker').addEventListener('change', function() {
        var colorValue = this.value;
        console.log('Color Changed to:', colorValue);
        // Send the color value to the server using AJAX
        fetch('/set_color/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Assuming you're using CSRF tokens
            },
            body: JSON.stringify({ color: colorValue })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        });
    });

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateBulbStatuses() {
        $.ajax({
            url: '/bulb-statuses-json/', // Adjust if the URL in your Django app is different
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                var tbodyHtml = '';
                response.bulbs.forEach(function(bulb) {
                    tbodyHtml += '<tr>' +
                        '<td>' + bulb.ip + '</td>' +
                        '<td>' + bulb.power + '</td>' +
                        '<td>' + bulb.bright + '</td>' +
                        '<td><input type="range" min="0" max="100" value="' + 
                        bulb.bright + '" class="slider" id="brightness_' + bulb.ip + 
                        '" onchange="changeBrightness(\'' + bulb.ip + '\')"></td>' + // Slider input
                        '<td>' + bulb.rgb + '</td>' +
                        '</tr>';
                });
                $('table tbody').html(tbodyHtml);
            },
            error: function() {
                console.error('Failed to fetch bulb statuses');
            }
        });
    }

    setInterval(updateBulbStatuses, 1000); // Refresh every second
    $(document).ready(updateBulbStatuses); // Initial population of the table
});
