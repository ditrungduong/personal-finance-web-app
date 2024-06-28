document.getElementById('income-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission
    const source = document.getElementById('source').value; // Get the source value
    const amount = document.getElementById('amount').value; // Get the amount value
    const date = document.getElementById('date').value; // Get the date value

    // Send a POST request to add the income
    fetch('/income', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source, amount, date })
    })
    .then(response => response.json())
    .then(data => {
        alert('Income added: ' + data.income.source);
        location.reload(); // Reload the page to reflect changes
    })
    .catch(error => console.error('Error:', error));
});

function editIncome(id, source, amount, date) {
    const newSource = prompt("Enter new source:", source); // Prompt for new source
    const newAmount = prompt("Enter new amount:", amount); // Prompt for new amount
    const newDate = prompt("Enter new date:", date); // Prompt for new date

    // Send a PUT request to edit the income
    fetch(`/income/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source: newSource, amount: newAmount, date: newDate })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload(); // Reload the page to reflect changes
    })
    .catch(error => console.error('Error:', error));
}

function deleteIncome(id) {
    if (confirm("Are you sure you want to delete this income?")) {
        // Send a DELETE request to delete the income
        fetch(`/income/${id}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload(); // Reload the page to reflect changes
        })
        .catch(error => console.error('Error:', error));
    }
}
