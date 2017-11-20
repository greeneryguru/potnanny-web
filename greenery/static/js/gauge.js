// //////////////////////////////////////////////////////////////////////////
//
// functions used by our Gauge html element. For displaying sensor info with
// a bit of graphing included
//
// //////////////////////////////////////////////////////////////////////////


/*
  params:
    1. the id number only of the element, like "chart-3"
    2. a global dict where status of charts is kept
    3. the datasets
    4. any annotations needed
*/
function indexLineColor(idx) {
    var values = [
        "rgb(120, 200, 0)",
        "rgb(220, 220, 130)",
        "rgb(220, 180, 130)", 
        "rgb(120, 160, 130)", 
        "rgb(160, 160, 180)", 
    ];
}

function createChart(id, tracker, labels, datasets, annotations=false) {

    var ctx = $("#" + id).getContext('2d');
    if (id in tracker) {
        // destroy our old chart object, before making a new one
        tracker[id].destroy()
    }

    chart = {
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

        }
    }
    if (labels) {
        chart.data.labels = labels
    }
    if (datasets) {
        chart.data.datasets = datasets
    }
    if (annotations) {

    }
    tracker[id] = new Chart(ctx, {
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
            datasets: [{
                data: data['data'],
                fill: false,
                lineTension: 0.1,
                borderColor: "rgb(120, 200, 0)",
            }]
        }
    });
}
function setMeasurement(id, data) {
    var m = data['value']
    if (data['type-name'] == 'temperature') {
        m += String.fromCharCode(176);
    } else if (data['type-name'] == 'humidity') {
        m += "%";
    } else if (data['type-name'] == 'soil moisture') {
        m += "%";
    }
    $("#measurement-" + id).text(m);
    return false;
}
function setSubtext(id, data) {
    $("#subtext-" + id).text(data['date-time']);
    return false;
}
