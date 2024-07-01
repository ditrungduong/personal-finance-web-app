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
    document.getElementById('add-income-form').style.display = 'block'; // Show the add income form
    document.getElementById('form-title').textContent = 'Add Income'; // Set form title
    document.getElementById('cancel-edit').style.display = 'inline'; // Show the cancel button
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
    const existingForm = document.querySelector('.edit-income-form');
    if (existingForm) {
        existingForm.remove(); // Remove the edit form if the user cancels
    }

    const addIncomeForm = document.getElementById('add-income-form');
    if (addIncomeForm && addIncomeForm.style.display === 'block') {
        addIncomeForm.style.display = 'none'; // Hide the add income form if it's being displayed
    }

    // Reset the form fields
    document.getElementById('income-id').value = '';
    document.getElementById('source').value = '';
    document.getElementById('amount').value = '';
    document.getElementById('date').value = '';
}
