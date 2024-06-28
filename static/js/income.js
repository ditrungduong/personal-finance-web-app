document.getElementById('income-form').addEventListener('submit', function(e) {
    e.preventDefault();
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
    .then(response => response.json())
    .then(data => {
        alert(id ? 'Income updated' : 'Income added');
        location.reload();
    })
    .catch(error => console.error('Error:', error));
});

function showAddIncomeForm() {  // New function to show the form
    document.getElementById('income-form').style.display = 'block';
    document.getElementById('form-title').textContent = 'Add Income';
    document.getElementById('cancel-edit').style.display = 'inline';
}

function editIncome(id, source, amount, date) {
    document.getElementById('income-id').value = id;
    document.getElementById('source').value = source;
    document.getElementById('amount').value = amount;
    document.getElementById('date').value = date;

    document.getElementById('form-title').textContent = 'Edit Income';
    document.getElementById('income-form').style.display = 'block';  // Show form when editing
    document.getElementById('cancel-edit').style.display = 'inline';
}

function deleteIncome(id) {
    if (confirm("Are you sure you want to delete this income?")) {
        fetch(`/income/${id}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload();
        })
        .catch(error => console.error('Error:', error));
    }
}

function cancelEdit() {  // Function to cancel editing
    document.getElementById('income-id').value = '';
    document.getElementById('source').value = '';
    document.getElementById('amount').value = '';
    document.getElementById('date').value = '';

    document.getElementById('form-title').textContent = 'Add Income';
    document.getElementById('income-form').style.display = 'none';  // Hide form when canceling
    document.getElementById('cancel-edit').style.display = 'none';
}
