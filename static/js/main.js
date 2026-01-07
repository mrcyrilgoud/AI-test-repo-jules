document.addEventListener('DOMContentLoaded', () => {
    fetchEmails();
    document.getElementById('refreshBtn').addEventListener('click', fetchEmails);
});

function fetchEmails() {
    const tableBody = document.getElementById('emailTableBody');
    const loading = document.getElementById('loading');

    // Show loading
    loading.style.display = 'flex';
    tableBody.innerHTML = ''; // Clear current list

    fetch('/api/emails')
        .then(response => {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert('Error fetching emails: ' + data.error);
                return;
            }
            renderEmails(data);
        })
        .catch(err => {
            console.error(err);
            alert('An error occurred. Check console.');
        })
        .finally(() => {
            loading.style.display = 'none';
        });
}

function renderEmails(emails) {
    const tableBody = document.getElementById('emailTableBody');

    if (emails.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="5" class="text-center p-4">No emails found.</td></tr>';
        return;
    }

    emails.forEach((email, index) => {
        // Color coding for scores
        const severityClass = email.severity >= 8 ? 'text-danger fw-bold' : '';
        const valueClass = email.content_value >= 8 ? 'text-success fw-bold' : '';
        const rowClass = email.urgency_score > 60 ? 'urgency-high' : '';

        // Main Row
        const row = document.createElement('tr');
        row.className = rowClass;
        row.innerHTML = `
            <td><span class="badge bg-secondary score-badge">${email.urgency_score}</span></td>
            <td class="${severityClass}">${email.severity}/10</td>
            <td class="${valueClass}">${email.content_value}/10</td>
            <td>
                <div class="fw-bold text-truncate" style="max-width: 400px;">${email.subject}</div>
                <div class="small text-muted">${email.sender}</div>
            </td>
            <td><span class="badge bg-info text-dark">${email.response_time}</span></td>
        `;

        // Details Row (Hidden by default)
        const detailsRow = document.createElement('tr');
        detailsRow.className = 'details-row';
        detailsRow.innerHTML = `
            <td colspan="5" class="p-4 bg-light">
                <div class="row">
                    <div class="col-md-4">
                        <h6 class="text-uppercase small text-muted">Analysis</h6>
                        <p><strong>Reasoning:</strong> ${email.reasoning}</p>
                    </div>
                    <div class="col-md-8 border-start">
                        <h6 class="text-uppercase small text-muted">Original Message</h6>
                        <div class="p-3 bg-white border rounded">
                            <small class="text-muted d-block mb-2">${email.date}</small>
                            <p style="white-space: pre-wrap;">${email.body.substring(0, 500)}...</p>
                        </div>
                    </div>
                </div>
            </td>
        `;

        // Toggle Details on Click
        row.addEventListener('click', () => {
            const isVisible = detailsRow.style.display === 'table-row';
            detailsRow.style.display = isVisible ? 'none' : 'table-row';
        });

        tableBody.appendChild(row);
        tableBody.appendChild(detailsRow);
    });
}
