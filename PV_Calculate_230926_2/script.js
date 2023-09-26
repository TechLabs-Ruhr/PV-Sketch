document.addEventListener("DOMContentLoaded", function() {
    // Your JavaScript code here

    // Select: Roof inclination 
    const toggleButtons = document.querySelectorAll('.toggle-button');

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {

            toggleButtons.forEach(otherButton => otherButton.classList.remove('active'));

            button.classList.add('active');
        });
    });

    document.getElementById("show-button").addEventListener("click", function() {
        var moreInfo = document.getElementById("more-info");
        if (moreInfo.style.display === "none" || moreInfo.style.display === "") {
            moreInfo.style.display = "block";
            this.textContent = "Hide Further Information";
        } else {
            moreInfo.style.display = "none";
            this.textContent = "Show Further Information";
        }
    });
});

// document.getElementById("required").addEventListener("input", function() {
//     // Überprüfe, ob das Input-Feld einen Wert hat
//     if (this.value !== "") {
//         // Füge die CSS-Klasse "filled" hinzu, wenn es einen Wert gibt
//         this.classList.add("filled");
//     } else {
//         // Entferne die CSS-Klasse "filled", wenn das Feld leer ist
//         this.classList.remove("filled");
//     }
// });

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