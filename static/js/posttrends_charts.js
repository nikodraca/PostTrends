// prepare data

var dateLabels = [];
var likesList = [];
var commentsList = [];

for (var i = allData['media_info'].length - 1; i >= 0; i--) {
    dateLabels.push(allData['media_info'][i]['date']);
    likesList.push(allData['media_info'][i]['likes']);
    commentsList.push(allData['media_info'][i]['comments']);

}

// <---- Likes trend ---->

var ctx = document.getElementById("likesChart");

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: dateLabels,
        datasets: [{
        	fill: false,
        	pointRadius: 0,
            data: likesList,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
            ],
            borderColor: [
                '#DA627D',        
            ],
            borderWidth: 3
        },
        ]
    },
    options: {
        responsive: false,
        scales: {
            xAxes: [{
            	display: true,
	        	gridLines: {display: false},
                ticks: {
                    display: true
                }
            }],

	        yAxes: [{
                display: true,
                ticks: {
                    display: false,
                    maxTicksLimit: 5
                },

	        	gridLines: {display: false},
                ticks: {
                    beginAtZero:false
                }
            }],

        },
        legend: {
        	display: false,
        },

    }
});
// <---- End likes trend ---->

// <---- Comments trend ---->

var ctx = document.getElementById("commentsChart");

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: newOldArr,
        datasets: [{
            fill: false,
            pointRadius: 0,
            data: null,
            backgroundColor: [
                'rgba(30, 80, 190, 0.2)',
            ],
            borderColor: [
                '#5AB1BB',
            ],
            borderWidth: 3
        },
        ]
    },
    options: {
        responsive: false,
        scales: {
            xAxes: [{
                display: true,
                gridLines: {display: false},
                ticks: {
                    display: true
                }
            }],

            yAxes: [{
                display: true,
                ticks: {
                    display: false,
                    maxTicksLimit: 5
                },

                gridLines: {display: false},
                ticks: {
                    beginAtZero:false
                }
            }],
        },
        legend: {
            display: false,
        },
    }
});
// <---- End Comments trend ---->

// <---- Days ---->

var ctx = document.getElementById("daysRadar");

var data = {
    labels: dayLabel,
    datasets: [
        {
            backgroundColor: "#5FBB97",
        	pointRadius: 0,
            borderColor: "#5FBB97",
            pointBackgroundColor: "rgba(179,181,198,1)",
            pointBorderColor: "#fff",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(179,181,198,1)",
            data: dayValue
        }
    ]
};

var myRadarChart = new Chart(ctx, {
    type: 'radar',
    data: data,
    options: {
	        responsive: false,

        legend: {
            display: false,
        },
        scale: {
            gridLines: {display: false},
            ticks: {
                display: false
            }
        }


    }
});

// <---- Days end ---->


// <---- Hours ---->

var ctx = document.getElementById("hoursRadar");


var data = {
    labels: hourLabel,
    datasets: [
        {
            backgroundColor: "#FE938C",
        	pointRadius: 0,
            borderColor: "#FE938C",
            pointBackgroundColor: "rgba(179,181,198,1)",
            pointBorderColor: "#fff",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(179,181,198,1)",
            data: hourValue
        }
    ]
};

var myRadarChart = new Chart(ctx, {
    type: 'radar',
    data: data,
    options: {
	        responsive: false,

        legend: {
            display: false,
        },
        scale: {
            gridLines: {display: false},
            ticks: {
                display: false
            }
        }


    }
});



var ctx = document.getElementById("followRatio");

var data = {
	labels: ['Followers', 'Following'],
    datasets: [
        {
            backgroundColor: ['#DA627D','#5AB1BB'],
            hoverBackgroundColor: ['#DA627D','#5AB1BB'],
            data: null,
            borderWidth: 2,
        }
    ]
};

var myDoughnut = new Chart(ctx, {
    type: 'doughnut',
    data: data,
    options: {
    	cutoutPercentage: 70,	
        responsive: false,
        legend: {
            display: false,
        },
    }
});


