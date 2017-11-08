
function buildTeamTrendGraph(teamName, teamId, sprintId, canvasElement) {

    d3.json('/api/teamSprintTrend/' + teamId+'/'+ sprintId+'/', function (error, data) {
        cdata = data;
        var labeldata = [];
        var chrtdata = [];
        for(var i =0; i < cdata.length; i++)
        {
          labeldata.push(cdata[i].dataDate);
          chrtdata.push(cdata[i].daily_points)
        }
        var ctx = document.getElementById(canvasElement);
        ctx.height = 125;
        var myChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: labeldata,
            datasets: [{
              label: teamName,
              data: chrtdata,
              backgroundColor: "rgba(53,205,21,0.6)",

            }]
          },
          options: {
            animation: {
                duration: 1500,
                onComplete: function () {
                    var ctx = this.chart.ctx;
                    ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, 'normal', Chart.defaults.global.defaultFontFamily);
                    ctx.fillStyle = 'rgb(0,0,0)';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'bottom';
                    this.data.datasets.forEach(function (dataset) {
                        for (var i = 0; i < dataset.data.length; i++) {
                            var model = dataset._meta[Object.keys(dataset._meta)[0]].data[i]._model;
                            ctx.fillText(dataset.data[i], model.x, model.y - 5);
                        }

                    });
                }},
            maintainAspectRatio: false,
            legend: {
                display: false,
                labels: {
                    fontColor: 'rgb(0,0,0)'
                }
            },
             scales: {
                yAxes: [{
                    ticks: {
                        fontColor: "#000000",
                        beginAtZero: true
                    }
                 }],
                 xAxes: [{
                     ticks: {
                      fontColor: "#000000",
                      },
                     type: 'time',
                     maxBarThickness: 50,
                     time: {
                         unit: 'day',
                         displayFormats: {
                             'millisecond': 'MMM DD',
                             'second': 'MMM DD',
                             'minute': 'MMM DD',
                             'hour': 'MMM DD',
                             'day': 'MMM DD',
                             'week': 'MMM DD',
                             'month': 'MMM DD',
                             'quarter': 'MMM DD',
                             'year': 'MMM DD',
                         }
                     }
                 }]
             }
          }
        });
    });
};

$( ".teamGraph" ).each(function() {
  buildTeamTrendGraph($(this).attr('teamName'),$(this).attr('team'),$(this).attr('sprint'),$(this).attr('id'))
});
