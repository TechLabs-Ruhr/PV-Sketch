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


// test für front-end code für die verbindung von front-end und back-end

document.getElementById("calculateButton").addEventListener("click", () => {
    const selectedInclinationButton = document.querySelector(".toggle-button.active");
    const selectedInclination = selectedInclinationButton.getAttribute("data-inclination");
    
    const data = {
        postalcode: document.getElementById("postalCodeInput").value,
        city: document.getElementById("cityInput").value,
        street: document.getElementById("streetInput").value,
        number: document.getElementById("numberInput").value,
        roofinclination: selectedInclination
    };
    
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Display the calculation result in your front-end
        document.getElementById("resultContainer").textContent = `Efficiency: ${result.efficiency * 100}%`;
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
