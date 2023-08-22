// Select: Roof inclination 
const toggleButtons = document.querySelectorAll('.toggle-button');

toggleButtons.forEach(button => {
  button.addEventListener('click', () => {
    
    toggleButtons.forEach(otherButton => otherButton.classList.remove('active'));
    
    button.classList.add('active');
  });
});

// Convert: Address
document.getElementById("convertBtn").addEventListener("click", convertAddress);

function convertAddress() {
    const address = document.getElementById("address").value;
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                const latitude = data[0].lat;
                const longitude = data[0].lon;

                document.getElementById("coordinates").textContent = `Latitude: ${latitude}, Longitude: ${longitude}`;
            } else {
                document.getElementById("coordinates").textContent = "Address not found.";
            }
        })
        .catch(error => console.error("Error converting address:", error));
}