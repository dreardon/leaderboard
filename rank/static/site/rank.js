

function random_rgba() {
    var o = Math.round, r = Math.random, s = 255;
    return 'rgba(' + o(r()*s) + ',' + o(r()*s) + ',' + o(r()*s) + ',' + r().toFixed(1) + ')';
}

function buildTeamTrendGraph(teamName, teamId, sprintId, canvasElement) {

    d3.json('/api/teamSprintTrend/' + teamId+'/' + sprintId+'/', function (error, data) {
        cdata = data;
        var labeldata = [];
        var chrtdata = [];
        for(var i =0; i < cdata.length; i++)
        {
          labeldata.push(cdata[i].dataDate);
          chrtdata.push(cdata[i].daily_points)
        }
        var ctx = document.getElementById(canvasElement);
        ctx.height = 75;
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
                    ctx.fillStyle = this.chart.config.options.defaultFontColor;
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'bottom';
                    this.data.datasets.forEach(function (dataset) {
                        for (var i = 0; i < dataset.data.length; i++) {
                            var model = dataset._meta[Object.keys(dataset._meta)[0]].data[i]._model;
                            ctx.fillText(dataset.data[i], model.x, model.y - 5);
                        }

                    });
                }
            },
            maintainAspectRatio: false,
            legend: {
                display: false,
                labels: {
                    fontColor: 'rgb(255, 99, 132)'
                }
            },
             scales: {
                 xAxes: [{
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
                 }],
                 yAxes: [{
                        ticks: {
                            beginAtZero: true
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

function addData(chart, label, color, data) {
    var newDataSet = {
        label: label,
        fill:true,
        borderWidth: 2,
        backgroundColor: color,
        borderColor: color,
        data: data
    }
    chart.data.datasets.push(newDataSet);
    chart.update();
}

function buildTeamLeaderGraph(dateData) {
    var LeaderGraphData = {
        labels: dateData,
        datasets: []
    }

    var ctx = document.getElementById("lineChart");
    window.lineChart = new Chart(ctx, {
        type: 'line',
        data: LeaderGraphData,
        options: {
            legend: {
                labels: {
                    fontColor: '#000000'
                }
            },
            maintainAspectRatio: true,
             scales: {
                 xAxes: [{
                     type: 'time',
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
                     },
                 }],
             }
          }
    });

    var colors = ['rgba(7,74,79,0.6)','rgba(87,29,229,0.2)','rgba(3,18,47,0.2)','rgba(32,12,85,0.6)']
    $(".rankingPoints").each(function (index) {
        var randomColor = random_rgba()
        var teamName = $(this).attr('teamname')
        d3.json('/api/teamSprintPoints/' + $(this).attr('teamid')+'/' + $(this).attr('sprintid')+'/', function (error, data) {
            addData(lineChart,teamName,colors[index],data);
        });

    });
};

function updateRankingPage() {
    //$('#mix-wrapper').addClass("blur");
    for (i = 0; i < 7; i++) {
        $('#randomSort').click();
    }
    $('#descendingSort').click();
    //$('#mix-wrapper').removeClass("blur");
};


var mixer = mixitup('.container-fluid', {
    animation: {
        duration: 300
    }
});

mixitup('#mix-wrapper', {
  load: {
    sort: 'order:desc'
  },
  animation: {
    effects: 'fade rotateZ(-180deg)',
    duration: 300,
    queue: true,
    queueLimit: 15
  },
  classNames: {
    elementSort: 'sort-btn'
  },
  selectors: {
    target: '.mix-target'
  }
});


function loadCommits() {
    $.getJSON("media/commits.json", function (data) {
        var items = [];
        $.each(data, function (key, val) {
            alert(key+val);
        });
    });
};