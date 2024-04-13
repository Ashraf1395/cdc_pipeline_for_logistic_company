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

// Function to fetch and display customers
function fetchAndDisplayCustomers() {
    fetchData('/api/customers', 'GET')
        .then(customers => {
            // Clear the existing table body
            const customerTableBody = document.getElementById('customerList');
            customerTableBody.innerHTML = '';

            // Iterate through the array of customers and create table rows
            customers.forEach(customer => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${customer[0]}</td>
                    <td>${customer[1]}</td>
                    <td>${customer[2]}</td>
                    <td>${customer[3]}</td>
                    <td>${customer[4]}</td>
                    <td>${customer[5]}</td>
                    <td>${customer[6]}</td>
                    <td>${customer[7]}</td>
                    <td>${customer[8]}</td>
                `;
                customerTableBody.appendChild(row);
            });
        });
}
// Example function to add a new customer
function addCustomer(customerData) {
    fetchData('/api/customers', 'POST', customerData)
        .then(response => {
            console.log(response);
            // Refresh customer list after adding
            fetchAndDisplayCustomers();
        });
}

// Example function to delete a customer
function deleteCustomer(customerId) {
    fetchData(`/api/customers/${customerId}`, 'DELETE')
        .then(response => {
            console.log(response);
            // Refresh customer list after deletion
            fetchAndDisplayCustomers();
        });
}

// Example usage: Fetch and display customers when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchAndDisplayCustomers();
});

// Example usage: Add a new customer when a form is submitted
document.getElementById('customerForm').addEventListener('submit', event => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const customerData = {
        customer_name: formData.get('customer_name'),
        customer_address: formData.get('customer_address'),
        // Add more fields as needed
    };
    addCustomer(customerData);
});

// Example usage: Delete a customer when a delete button is clicked
document.addEventListener('click', event => {
    if (event.target && event.target.classList.contains('delete-customer')) {
        const customerId = event.target.dataset.customerId;
        deleteCustomer(customerId);
    }
});
