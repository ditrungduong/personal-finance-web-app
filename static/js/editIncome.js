// editIncome.js
function editIncome(id, source, amount, date) {
    // Remove any existing edit forms
    const existingForm = document.querySelector('.edit-income-form');
    if (existingForm) {
        existingForm.remove(); // Remove the previously inserted edit form
    }

    // Get the row where the form should be inserted
    const row = document.getElementById(`income-row-${id}`);
    
    // Create the edit form HTML dynamically
    const editFormHtml = `
        <tr class="edit-income-form">
            <td colspan="4">
                <form id="edit-income-form">
                    <h2 id="form-title">Edit Income</h2>
                    <input type="hidden" id="income-id" name="income-id" value="${id}">
                    <div class="form-group">
                        <label for="source">Source:</label>
                        <input type="text" id="source" name="source" value="${source}" required>
                    </div>
                    <div class="form-group">
                        <label for="amount">Amount:</label>
                        <input type="number" id="amount" name="amount" value="${amount}" required>
                    </div>
                    <div class="form-group">
                        <label for="date">Date:</label>
                        <input type="date" id="date" name="date" value="${date}" required>
                    </div>
                    <div class="form-group">
                        <button type="submit">Submit</button>
                        <button type="button" id="cancel-edit" onclick="cancelEdit()">Cancel</button>
                    </div>
                </form>
            </td>
        </tr>
    `;

    // Insert the edit form after the current row
    row.insertAdjacentHTML('afterend', editFormHtml);

    // Add event listener to the dynamically created edit form
    document.getElementById('edit-income-form').addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission behavior
        const id = document.getElementById('income-id').value;
        const source = document.getElementById('source').value;
        const amount = document.getElementById('amount').value;
        const date = document.getElementById('date').value;

        fetch(`/income/${id}`, {
            method: 'PUT',
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
            alert('Income updated');
            location.reload(); // Reload the page to reflect changes
        })
        .catch(error => {
            console.error('Error:', error); // Log error for debugging
            alert('An error occurred. Please try again.');
        });
    });
}
