let deletion_form = document.getElementById('deletion_form');

deletion_form.addEventListener('submit', function(event) {
    event.preventDefault();

    const stat_name = document.getElementById('stat_name').value;

    // Retrieve CSRF token from cookies
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/api/delete_statistic/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Include CSRF token in headers
        },
        body: JSON.stringify({
            stat_name: stat_name,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.msg === 'ok') {
            window.location.href = '/stats';
        } else {
            alert(data.error || "An error occurred.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    });
});
