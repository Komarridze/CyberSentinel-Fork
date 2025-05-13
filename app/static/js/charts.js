document.addEventListener("DOMContentLoaded", () =>
{
    const ctx = document.getElementById('logChart').getContext('2d');
    // Initial dummy data; replace with data from your API
    const logChart = new Chart(ctx, 
    {
        type: 'bar',
        data: 
        {
            labels: ['INFO', 'WARNING', 'ERROR'],
            datasets: 
            [{
                label: 'Log Count',
                data: [0, 0, 0],
                backgroundColor: ['green', 'orange', 'red']
            }]
        },
        options:
        {
            responsive: true,
            scales:
            {
                y:
                {
                    beginAtZero: true
                }
            }
        }
    });

    // Update chart with new data from an AJAX call
    function updateChart()
    {
        fetch('/api/log_summary')
            .then(response => response.json())
            .then(data => 
            {
                logChart.data.datasets[0].data = [data.INFO, data.WARNING, data.ERROR];
                logChart.update();
            })
            .catch(error => console.error("Error updating chart: ", error));
    }

    // Set an interval to refresh the chart every 30 seconds
    setInterval(updateChart, 30000);
    updateChart();
});