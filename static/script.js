document.addEventListener("DOMContentLoaded", () => {
    // Only initialize map if we're on the main page
    if (document.getElementById("mapContainer")) {
        let map = L.map("mapContainer").setView([27.7, 85.3], 13);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: "&copy; OpenStreetMap contributors",
        }).addTo(map);

        let driverMarkers = {};

        async function updateDriverMarkers() {
            // In a real app, you'd fetch all active drivers from the server
            const res = await fetch("/get-location/driver1");
            const data = await res.json();
            
            if (!driverMarkers['driver1']) {
                driverMarkers['driver1'] = L.marker([data.lat, data.lng])
                    .addTo(map)
                    .bindPopup("Driver 1 Location");
            } else {
                driverMarkers['driver1'].setLatLng([data.lat, data.lng]);
            }
            
            // Center map on the first driver (in real app, you might want different logic)
            map.panTo([data.lat, data.lng]);
        }

        setInterval(updateDriverMarkers, 3000);
        updateDriverMarkers(); // Initial call
    }
});
