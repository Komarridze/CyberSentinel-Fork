document.addEventListener('DOMContentLoaded', () =>
{
    const socket = io();

    let paused = false;
    const logTableBody = document.querySelector("#log-table tbody");
    
    // Handle pause/resume button
    const pauseBtn = document.getElementById("pause-btn");
    pauseBtn.addEventListener("click", () =>
    {
        paused = !paused;
        pauseBtn.innerText = paused ? "Resume" : "Pause";
    });

    // Listen to new log events
    socket.on("new_log", (data) =>
    {
        if (!paused)
        {
            addLogEntry(data);
            updateSummary(data);
        }
    });

    function addLogEntry(log)
    {
        const row = document.createElement("tr");

        // Highlight specific log entries
        if (log.level === "ERROR")
        {
            row.classList.add("error");
        }
        else if (log.level === "WARNING")
        {
            row.classList.add("warning");
        }

        row.innerHTML = `
            <td>${log.timestamp}</td>
            <td>${log.level}</td>
            <td>${log.agent}</td>
            <td>${log.message}</td>
        `;

        // Insert new entries at the top for immediacy
        logTableBody.prepend(row);
    }

    function updateSummary(log)
    {
        let totalElem = document.getElementById("total-logs");
        let errorElem = document.getElementById("error-count");

        let total = parseInt(totalElem.textContent, 10) || 0;
        totalElem.textContent = total + 1;

        if (log.level === "ERROR")
        {
            let errorCount = parseInt(errorElem.textContent, 10) || 0;
            errorElem.textContent = errorCount + 1;
        }
    }

    // Filtering: Bind click event to apply filters
    document.getElementById("apply-filters").addEventListener("click", () => 
    {
        // Collect filter criteria
        const keyword = document.getElementById("keyword").value.trim();
        const level = document.getElementById("log-level").value;
        const startDate = document.getElementById("start_date").value;
        const endDate = document.getElementById("end_date").value;

        // Construct query string and fetch filtered logs via AJAX
        let query = `/api/logs?keyword=${keyword}&level=${level}&start_date=${startDate}&end_date=${endDate}`;

        fetch(query)
            .then(response => response.json())
            .then(data => 
            {
                // Clear current logs and repopulate the table.
                logTableBody.innerHTML = "";
                data.logs.forEach((log) => addLogEntry(log));
            })
            .catch(error => console.error("Error fetching logs: ", error));
    });
});