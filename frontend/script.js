async function optimizePortfolio() {
    const symbols = document.getElementById('symbols').value.split(',');
    const response = await fetch('/api/optimize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem('token')
        },
        body: JSON.stringify({ symbols })
    });
    const data = await response.json();
    renderChart(data.optimized_weights);
}

function renderChart(weights) {
    const ctx = document.getElementById('portfolio-chart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(weights),
            datasets: [{
                data: Object.values(weights),
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
                ]
            }]
        }
    });
}