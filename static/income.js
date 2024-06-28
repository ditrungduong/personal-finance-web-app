document.getElementById('income-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const source = document.getElementById('source').value;
    const amount = document.getElementById('amount').value;
    const date = document.getElementById('date').value;

    fetch('/income', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source, amount, date })
    }).then(response => response.json())
      .then(data => {
          alert('Income added: ' + data.income.source);
          location.reload();
      })
      .catch(error => console.error('Error:', error));
});

function editIncome(id, source, amount, date) {
    const newSource = prompt("Enter new source:", source);
    const newAmount = prompt("Enter new amount:", amount);
    const newDate = prompt("Enter new date:", date);

    fetch(`/income/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source: newSource, amount: newAmount, date: newDate })
    }).then(response => response.json())
      .then(data => {
          alert(data.message);
          location.reload();
      })
      .catch(error => console.error('Error:', error));
}

function deleteIncome(id) {
    if (confirm("Are you sure you want to delete this income?")) {
        fetch(`/income/${id}`, {
            method: 'DELETE',
        }).then(response => response.json())
          .then(data => {
              alert(data.message);
              location.reload();
          })
          .catch(error => console.error('Error:', error));
    }
}
