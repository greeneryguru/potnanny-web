function cbCreateChart(id, data, chartref) {
    var ctx = document.getElementById(id).getContext('2d');
    if (id in chartref) {
        chartref[id].destroy()
    }

    chartref[id] = new Chart(ctx, {
        type: 'line',
        options: {
            animation: {
                duration: 0
            },
            scales: {
                xAxes: [{
                    display: false
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero:false
                    }
                }],
            }
        },
        data: {
            labels: data['labels'],
            datasets: data['datasets']
        }
    });
}

function cbColorIndex(i) {
    var values = [
        "rgb(120, 200, 0)",
        "rgb(220, 220, 130)",
        "rgb(220, 180, 130)", 
        "rgb(120, 160, 130)", 
        "rgb(160, 160, 180)", 
    ];
    return values[i % values.length]
}

