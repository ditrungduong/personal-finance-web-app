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
            return JSON.parse(text); // Attempt to parse JSON manually
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

function showAddIncomeForm() {
    document.getElementById('income-form').reset(); // Reset form fields
    document.getElementById('form-title').textContent = 'Add Income'; // Set form title
    document.getElementById('cancel-edit').style.display = 'none'; // Hide the cancel button
}

function editIncome(id, source, amount, date) {
    document.getElementById('income-id').value = id;
    document.getElementById('source').value = source;
    document.getElementById('amount').value = amount;
    document.getElementById('date').value = date;

    document.getElementById('form-title').textContent = 'Edit Income'; // Set form title to Edit Income
    document.getElementById('cancel-edit').style.display = 'inline'; // Show the cancel button
}

function deleteIncome(id) {
    if (confirm("Are you sure you want to delete this income?\n\nWarning: This action is irreversible. Once deleted, the expense data will be permanently lost and cannot be recovered.")) {
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
                return JSON.parse(text); // Attempt to parse JSON manually
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
    document.getElementById('income-form').reset(); // Reset form fields
    document.getElementById('form-title').textContent = 'Add Income'; // Reset form title to Add Income
    document.getElementById('cancel-edit').style.display = 'none'; // Hide the cancel button
}
