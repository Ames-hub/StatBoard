const add_form = document.getElementById('add_form');

add_form.addEventListener('submit', (event) => {
    event.preventDefault();

    const stat_name = document.getElementById('stat_name').value;
    const stat_desc = document.getElementById('stat_desc').value;

    if (!stat_name || !stat_desc) {
        alert("Please enter all fields.");
        return;
    }

    if (stat_name === '*') {
        alert("The name '*' is reserved by the system.");
        return;
    }

    if (!/^[a-zA-Z0-9_ ]+$/.test(stat_name)) {
        alert("Statistic name can only contain letters, numbers, spaces, and underscores.");
        return;
    }

    if (stat_name.length > 50) {
        alert("Statistic name is too long.");
        return;
    }

    if (stat_desc.length > 200) {
        alert("Statistic description is too long.");
        return;
    }

    // Get the CSRF token from the cookie
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/api/add_statistic/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            stat_name: stat_name,
            stat_desc: stat_desc
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
