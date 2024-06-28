document.getElementById('income-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission behavior
    const id = document.getElementById('income-id').value;
    const source = document.getElementById('source').value;
    const amount = document.getElementById('amount').value;
    const date = document.getElementById('date').value;

    const method = id ? 'PUT' : 'POST';
    const url = id ? `/income/${id}` : '/income';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source, amount, date })
    })
    .then(response => {
        console.log('Response status:', response.status); // Log response status
        return response.text().then(text => {
            console.log('Response text:', text); // Log response text
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            try {
                return JSON.parse(text); // Attempt to parse JSON manually
            } catch (error) {
                console.error('JSON parse error:', error);
                throw new Error('Failed to parse JSON: ' + error.message);
            }
        });
    })
    .then(data => {
        console.log('Server response:', data); // Log server response for debugging
        alert(id ? 'Income updated' : 'Income added');
        location.reload(); // Reload the page to reflect changes
    })
    .catch(error => {
        console.error('Error:', error); // Log error for debugging
        alert('An error occurred. Please try again.');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const editForms = document.querySelectorAll('.edit-income-form');

    editForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent the default form submission behavior

            const id = form.querySelector('.income-id').value;
            const source = form.querySelector('.source').value;
            const amount = form.querySelector('.amount').value;
            const date = form.querySelector('.date').value;

            const url = `/income/${id}`;

            fetch(url, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source, amount, date })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok: ' + response.statusText);
                }
                return response.json(); // Parse response as JSON
            })
            .then(data => {
                // Update table row with new data
                const row = document.getElementById(`income-row-${id}`);
                row.querySelector('.income-source').textContent = data.source;
                row.querySelector('.income-amount').textContent = data.amount;
                row.querySelector('.income-date').textContent = data.date;
                row.querySelector('.actions').innerHTML = `<button onclick="editIncome(${id}, '${data.source}', ${data.amount}, '${data.date}')">Edit</button> <button onclick="deleteIncome(${id})">Delete</button>`;

                alert('Income updated successfully.');
            })
            .catch(error => {
                console.error('Error updating income:', error);
                alert('An error occurred while updating income. Please try again.');
            });
        });
    });
});

function editIncome(id, source, amount, date) {
    // Create an edit form
    const formHtml = `
        <form class="edit-income-form">
            <input type="hidden" class="income-id" value="${id}">
            <div class="form-group">
                <label for="source">Source:</label>
                <input type="text" class="source" value="${source}" required>
            </div>
            <div class="form-group">
                <label for="amount">Amount:</label>
                <input type="number" class="amount" value="${amount}" required>
            </div>
            <div class="form-group">
                <label for="date">Date:</label>
                <input type="date" class="date" value="${date}" required>
            </div>
            <div class="form-group">
                <button type="submit">Update</button>
                <button type="button" onclick="cancelEdit(${id}, '${source}', ${amount}, '${date}')">Cancel</button>
            </div>
        </form>
    `;

    // Replace the table row with the edit form
    const row = document.getElementById(`income-row-${id}`);
    const actionsCell = row.querySelector('.actions');
    actionsCell.innerHTML = formHtml;
}

function cancelEdit(id, source, amount, date) {
    // Restore the original action buttons
    const row = document.getElementById(`income-row-${id}`);
    const actionsCell = row.querySelector('.actions');
    actionsCell.innerHTML = `
        <button onclick="editIncome(${id}, '${source}', ${amount}, '${date}')">Edit</button>
        <button onclick="deleteIncome(${id})">Delete</button>
    `;
}

function deleteIncome(id) {
    if (confirm("Are you sure you want to delete this income?")) {
        fetch(`/income/${id}`, {
            method: 'DELETE',
        })
        .then(response => {
            console.log('Response status:', response.status); // Log response status
            return response.text().then(text => {
                console.log('Response text:', text); // Log response text
                if (!response.ok) {
                    throw new Error('Network response was not ok: ' + response.statusText);
                }
                try {
                    return JSON.parse(text); // Attempt to parse JSON manually
                } catch (error) {
                    console.error('JSON parse error:', error);
                    throw new Error('Failed to parse JSON: ' + error.message);
                }
            });
        })
        .then(data => {
            console.log('Server response:', data); // Log server response for debugging
            alert(data.message);
            location.reload(); // Reload the page to reflect changes
        })
        .catch(error => {
            console.error('Error:', error); // Log error for debugging
            alert('An error occurred. Please try again.');
        });
    }
}

function cancelEdit() {
    const existingForm = document.querySelector('.edit-income-form');
    if (existingForm) {
        existingForm.remove(); // Remove the edit form if the user cancels
    }
}
