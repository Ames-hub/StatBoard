status_detector = document.getElementById("status_detector");
status_text = document.getElementById("status_text");

function pingServer() {
    fetch("/api/ping/", {
        method: "GET",
        headers: {
            "X-CSRFToken": csrf_token
        }
    })
    .then(response => response.json())
    .then(data => {
        let is_ok = (data.msg === "ok")
        status_detector.style.backgroundColor = is_ok ? "green" : "red";
        status_text.innerHTML = is_ok ? "Online" : "Offline";
    })
    .catch(error => console.error("Error:", error));
}

// Ping every 10 seconds (10000 milliseconds)
pingServer();
setInterval(pingServer, 10000);
