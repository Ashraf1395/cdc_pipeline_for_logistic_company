// orders.js

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

// Function to fetch and display orders
function fetchAndDisplayOrders() {
    fetchData('/api/orders', 'GET')
        .then(orders => {
            // Clear the existing table body
            const orderTableBody = document.getElementById('orderList');
            orderTableBody.innerHTML = '';

            // Iterate through the array of orders and create table rows
            orders.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${order[0]}</td>
                    <td>${order[1]}</td>
                    <td>${order[2]}</td>
                    <td>${order[3]}</td>
                    <td>${order[4]}</td>
                    <td>${order[5]}</td>
                    <td>${order[6]}</td>
                    <td>${order[7]}</td>
                    <td>${order[8]}</td>
                    <td>${order[9]}</td>
                    <td>${order[10]}</td>
                    <td>${order[11]}</td>
                `;
                orderTableBody.appendChild(row);
            });
        });
}

// Example usage: Fetch and display orders when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchAndDisplayOrders();
});
