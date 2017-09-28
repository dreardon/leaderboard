
function buildTeamTrendGraph(teamName, teamId,canvasElement) {

    d3.json('/api/teamSprintTrend/' + teamId+'/', function (error, data) {
        cdata = data;
        var labeldata = [];
        var chrtdata = [];
        for(var i =0; i < cdata.length; i++)
        {
          labeldata.push(cdata[i].ranking__dataDate);
          chrtdata.push(cdata[i].daily_points)
        }
        var ctx = document.getElementById(canvasElement);
        ctx.height = 75;
        var myChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labeldata,
            datasets: [{
              label: teamName,
              data: chrtdata,
              backgroundColor: "rgba(53,205,21,0.6)",

            }]
          },
          options: {
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
                     time: {
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
  buildTeamTrendGraph($(this).attr('teamName'),$(this).attr('team'),$(this).attr('id'))
});


//$( ".rankingPoints" ).each(function() {
//  buildTeamTrendGraph($(this).attr('teamId'),'myChart')
//});


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
