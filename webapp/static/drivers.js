// drivers.js

// Fetch function to send requests to the backend
function fetchData(url, method, data) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    if (data) {
        options.body = JSON.stringify(data);
    }

    return fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
        });
}

// Function to fetch and display drivers
function fetchAndDisplayDrivers() {
    fetchData('/api/drivers', 'GET')
        .then(drivers => {
            // Clear the existing table body
            const driverTableBody = document.getElementById('driverList');
            driverTableBody.innerHTML = '';

            // Iterate through the array of drivers and create table rows
            drivers.forEach(driver => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${driver[0]}</td>
                    <td>${driver[1]}</td>
                    <td>${driver[2]}</td>
                    <td>${driver[3]}</td>
                    <td>${driver[4]}</td>
                    <td>${driver[5]}</td>
                    <td>${driver[6]}</td>
                    <td>${driver[7]}</td>
                    <td>${driver[8]}</td>
                    <td>${driver[9]}</td>
                    <td>${driver[10]}</td>
                `;
                driverTableBody.appendChild(row);
            });
        });
}

// Example function to add a new driver
function addDriver(driverData) {
    fetchData('/api/drivers', 'POST', driverData)
        .then(response => {
            console.log(response);
            // Refresh driver list after adding
            fetchAndDisplayDrivers();
        });
}

// Example function to delete a driver
function deleteDriver(driverId) {
    fetchData(`/api/drivers/${driverId}`, 'DELETE')
        .then(response => {
            console.log(response);
            // Refresh driver list after deletion
            fetchAndDisplayDrivers();
        });
}

// Example usage: Fetch and display drivers when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchAndDisplayDrivers();
});

// Example usage: Add a new driver when a form is submitted
document.getElementById('driverForm').addEventListener('submit', event => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const driverData = {
        driver_name: formData.get('driver_name'),
        driver_contact_number: formData.get('driver_contact_number'),
        // Add more fields as needed
    };
    addDriver(driverData);
});

// Example usage: Delete a driver when a delete button is clicked
document.addEventListener('click', event => {
    if (event.target && event.target.classList.contains('delete-driver')) {
        const driverId = event.target.dataset.driverId;
        deleteDriver(driverId);
    }
});
