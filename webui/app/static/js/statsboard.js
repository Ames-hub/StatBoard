const stats_container = document.getElementById('stats_container');
const threshold = 5; // Threshold for the line color change

function createStatCard(data, threshold) {
    const name = data['name'];
    const stats = data['stats'];

    console.log("Creating stat card for:", name);

    const labels = Object.keys(stats); // Dates
    const values = Object.values(stats); // Stats for each date

    // Create an anchor tag for the stat card
    const a_tag = document.createElement('a');
    a_tag.href = window.location.origin + '/stats/v/' + name;
    a_tag.className = "stat-item";

    // Create a title element with the stat name
    const h1_tag = document.createElement('h1');
    h1_tag.innerHTML = name;
    a_tag.appendChild(h1_tag);

    // Create a canvas element for the chart
    const canvas = document.createElement('canvas');
    canvas.id = name;
    canvas.className = "graph";
    a_tag.appendChild(canvas);

    // Append the card to the container
    stats_container.appendChild(a_tag);

    const ctx = canvas.getContext('2d');

    // Determine line colors based on the threshold
    const colors = values.map((value, index) => {
        if (index > 0 && value < values[index - 1] - threshold) {
            return 'rgba(255, 0, 0, 1)'; // Red for dips below threshold
        }
        return 'rgba(75, 192, 192, 1)'; // Default color
    });

    // Initialize or update the chart
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels, // Use date labels from stats
            datasets: [{
                label: name,
                data: values, // Stats values
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: colors,
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            animation: false // Disable animations
        }
    });

    myChart.update();
}

async function fetchStats(targetName) {
    try {
        const response = await fetch('/api/getstats/?target_name=' + encodeURIComponent(targetName), {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Error:", errorData.error);
            return;
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Fetch error:", error);
    }
}

let current_data = {};
async function update(target_name = "*", with_data = {}) {
    let data;

    if (Object.keys(with_data).length === 0) {
        data = await fetchStats(target_name);
    } else {
        data = with_data;
    }

    if (!data || !data.stats) {
        console.error("No data or 'stats' key found in response");
        return;
    }

    if (target_name !== "*") {
        createStatCard({ name: target_name, stats: data.stats[target_name] }, threshold); // Handle specific target
    } else {
        // Loop through each stat in the stats object
        Object.entries(data.stats).forEach(([key, stats]) => {
            createStatCard({ name: key, stats }, threshold);
        });
    }

    current_data = data;
}

function destroy_all_charts() {
    Chart.helpers.each(Chart.instances, instance => instance.destroy());
    stats_container.innerHTML = ''; // Clear all chart containers
}

update();

window.addEventListener('resize', function() {
    destroy_all_charts();
    if (current_data && current_data.stats) {
        Object.entries(current_data.stats).forEach(([key, stats]) => {
            createStatCard({ name: key, stats }, threshold);
        });
    }
});

function send_statdata_entry(target_stat, value) {
    fetch('/api/enter_stat_data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            'target': target_stat,
            'value': value
        })
    }).then(response => {
        if (!response.ok) {
            console.error("Error adding stat data");
            return;
        }

        console.log("Stat data added successfully");
        destroy_all_charts();
        update();
    }).catch(error => {
        console.error("Error adding stat data:", error);
    });
}

function send_statdata_deletion(target_stat, date) {
    // Ensures date is in the format of YYYY-MM-DD
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
        alert("Please enter a valid date in the format of YYYY-MM-DD");
        console.error("Invalid date format:", date);
        return;
    }

    fetch('/api/delete_stat_data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            'target': target_stat,
            'date': date
        })
    }).then(response => {
        if (!response.ok) {
            console.error("Error deleting stat data");
            return;
        }

        console.log("Stat data deleted successfully");
        destroy_all_charts();
        update();
    }).catch(error => {
        console.error("Error deleting stat data:", error);
    });
}

if (window.location.pathname === '/stats/') {
    console.log("On the stats page, adding event listeners for buttons");

    // buttons used for adding/deleting a stat
    const delete_btn = document.getElementById('delete');
    const add_new_btn = document.getElementById('add_new');

    add_new_btn.addEventListener('click', function() {
        window.location.href = 'create';
    });

    delete_btn.addEventListener('click', function() {
        window.location.href = 'delete';
    });

    let log_submit_btn = document.getElementById('log_submit_btn');

    // Event listener for the log submit button
    log_submit_btn.addEventListener('click', function(event) {
        event.preventDefault();
        let log_name_inp = document.getElementById('log_name_inp');
        let stat_value_inp = document.getElementById('stat_value_inp');

        let target_stat = log_name_inp.value;
        let value = stat_value_inp.value;

        // Ensures that the fields are not empty
        if (target_stat === "" || value === "") {
            alert("Please fill in all fields");
            return;
        }

        // Ensures that the value is a number
        if (isNaN(value)) {
            alert("Please enter a valid number for the value");
            return;
        }

        send_statdata_entry(target_stat, value);
    });

    let delete_log_form = document.getElementById('delete_log_form');

    // Event listener for the delete log form
    delete_log_form.addEventListener('submit', function(event) {
        event.preventDefault();

        let target_stat = document.getElementById('del_name_inp').value;
        let date = document.getElementById('delete_date_inp').value;

        // Ensures that the fields are not empty
        if (target_stat === "" || date === "") {
            alert("Please fill in all fields");
            return;
        }

        send_statdata_deletion(target_stat, date);
    });
    
}
