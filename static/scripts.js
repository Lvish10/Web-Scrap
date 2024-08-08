document.addEventListener('DOMContentLoaded', function () {
    // Fetch job data
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById('jobsTable').getElementsByTagName('tbody')[0];

            data.forEach(job => {
                const newRow = table.insertRow();
                newRow.insertCell().textContent = job.job_title;
                newRow.insertCell().textContent = job.sector;
                newRow.insertCell().textContent = job.company;
                newRow.insertCell().textContent = job.country;
                newRow.insertCell().textContent = job.closing_date;
            });
        });

    // Fetch sector data
    fetch('/sector-data')
        .then(response => response.json())
        .then(sectorCounts => {
            const sectorChartData = {
                labels: Object.keys(sectorCounts),
                datasets: [{
                    data: Object.values(sectorCounts),
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#FF5733', '#DAF7A6']
                }]
            };

            new Chart(document.getElementById('sectorChart'), {
                type: 'pie',
                data: sectorChartData,
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    return `${tooltipItem.label}: ${tooltipItem.raw}`;
                                }
                            }
                        }
                    }
                }
            });

            // Spider chart example (radar chart)
            const spiderChartData = {
                labels: Object.keys(sectorCounts),
                datasets: [{
                    label: 'Jobs by Sector',
                    data: Object.values(sectorCounts),
                    fill: true,
                    backgroundColor: 'rgba(179, 181, 198, 0.2)',
                    borderColor: 'rgba(179, 181, 198, 1)',
                    pointBackgroundColor: 'rgba(179, 181, 198, 1)',
                    pointBorderColor: '#fff'
                }]
            };

            new Chart(document.getElementById('spiderChart'), {
                type: 'radar',
                data: spiderChartData,
                options: {
                    responsive: true,
                    scales: {
                        r: {
                            angleLines: {
                                display: false
                            },
                            suggestedMin: 0
                        }
                    }
                }
            });
        });
});
