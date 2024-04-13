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

// Function to fetch and display assignments
function fetchAndDisplayAssignments() {
    fetchData('/api/assignments', 'GET')
        .then(assignments => {
            // Clear the existing table body
            const assignmentTableBody = document.getElementById('assignmentList');
            assignmentTableBody.innerHTML = '';

            // Iterate through the array of assignments and create table rows
            assignments.forEach(assignment => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${assignment[0]}</td>
                    <td>${assignment[1]}</td>
                    <td>${assignment[2]}</td>
                    <td>${assignment[3]}</td>
                    <td>${assignment[4]}</td>
                    <td>${assignment[5]}</td>
                `;
                assignmentTableBody.appendChild(row);
            });
        });
}

// Example usage: Fetch and display assignments when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchAndDisplayAssignments();
});
