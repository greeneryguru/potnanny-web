// //////////////////////////////////////////////////////////////////////////
//
// functions used by our Gauge html element. For displaying sensor info with
// a bit of graphing included
//
// //////////////////////////////////////////////////////////////////////////


/*
createChart()

build a chart in a named dom element, with provided data

params:
    1. the id of the Canvas element, like "chart-3"
    2. a data object, containing the data for a chart
    3. reference to an object where active chart references are stored
*/
function createChart(id, data, chartref) {
    var ctx = $("#" + id).get(0).getContext('2d');
     if (id in chartref) {
        chartref[id].destroy();
    }

    chartref[id] = new Chart(ctx, data);
}


/* 
return the proper line color for a dataset, depending on what sequence number
it is
*/
function indexLineColor(i) {
    var values = [
        "rgb(120, 200, 0)",
        "rgb(20, 140, 220)",
        "rgb(220, 70, 20)",
        "rgb(220, 220, 130)",
        "rgb(220, 180, 130)"   
    ];
    return values[i % values.length]
}



