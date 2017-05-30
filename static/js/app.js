fetch('/bank_data/')
  .then((response) => response.json())
  .then((json) => json['data'])
  .then((data) => {
  var date_format = d3.time.format('%d/%m/%y');
  nv.addGraph(function() {
    var chart = nv.models.lineWithFocusChart();
    chart.xAxis
    .tickFormat(function(d) {
        return date_format(new Date(d));
    });
    chart.x2Axis
    .tickFormat(function(d) {
        return date_format(new Date(d));
    });
    chart.yAxis
    .tickFormat(d3.format(',.2f'));
    chart.y2Axis
    .tickFormat(d3.format(',.2f'));
    d3.select('svg')
    .datum([{
        key: 'money',
        values: data
    }])
    .transition()
    .duration(500)
    .call(chart);
    nv.utils.windowResize(chart.update);
    return chart;
  });
});