function initMap() {
        var mapElement = document.getElementById('map');
        var address = mapElement.getAttribute('data-direccion'); // Dirección del salón
        var salonNombre = mapElement.getAttribute('data-nombre'); // Nombre del salón

        var map = L.map('map').setView([-43.24895, -65.30505], 12); // Inicializa el mapa en Trelew

        // Cargar el mapa de OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }).addTo(map);

        var geocodingUrl = 'https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(address + ', Trelew, Argentina');

        fetch(geocodingUrl)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    var lat = data[0].lat;
                    var lon = data[0].lon;

                    // Centrar el mapa en la ubicación
                    map.setView([lat, lon], 15);

                    // Agregar un marcador
                    L.marker([lat, lon]).addTo(map).bindPopup(salonNombre).openPopup();
                } else {
                    alert('No se pudo encontrar la dirección.');
                }
            })
            .catch(error => {
                console.error('Error en la geocodificación:', error);
            });
    }

window.onload = initMap;
