document.getElementById('expense-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission behavior
    const id = document.getElementById('expense-id') ? document.getElementById('expense-id').value : null;
    const category = document.getElementById('category').value;
    const amount = document.getElementById('amount').value;
    const date = document.getElementById('date').value;

    const method = id ? 'PUT' : 'POST';
    const url = id ? `/expenses/${id}` : '/expenses';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category, amount, date })
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
        alert(id ? 'Expense updated' : 'Expense added');
        location.reload(); // Reload the page to reflect changes
    })
    .catch(error => {
        console.error('Error:', error); // Log error for debugging
        alert('An error occurred. Please try again.');
    });
});

function showAddExpenseForm() {
    document.getElementById('expense-form').reset(); // Reset form fields
    document.getElementById('form-title').textContent = 'Add Expense'; // Set form title
    document.getElementById('cancel-edit').style.display = 'none'; // Hide the cancel button
}

function editExpense(id, category, amount, date) {
    document.getElementById('expense-id').value = id;
    document.getElementById('category').value = category;
    document.getElementById('amount').value = amount;
    document.getElementById('date').value = date;

    document.getElementById('form-title').textContent = 'Edit Expense'; // Set form title to Edit Expense
    document.getElementById('cancel-edit').style.display = 'inline'; // Show the cancel button
}

function deleteExpense(id) {
    if (confirm("Are you sure you want to delete this expense?")) {
        fetch(`/expenses/${id}`, {
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
    document.getElementById('expense-form').reset(); // Reset form fields
    document.getElementById('form-title').textContent = 'Add Expense'; // Reset form title to Add Expense
    document.getElementById('cancel-edit').style.display = 'none'; // Hide the cancel button
}
