// prepare likes/comments data
var dateLabels = [];
var likesList = [];
var commentsList = [];
var likesSum = 0;
var commentsSum = 0;

for (var i = allData['media_info'].length - 1; i >= 0; i--) {
    dateLabels.push(allData['media_info'][i]['date']);
    likesList.push(allData['media_info'][i]['likes']);
    commentsList.push(allData['media_info'][i]['comments']);
    likesSum += allData['media_info'][i]['likes'];
    commentsSum += allData['media_info'][i]['comments'];
}

// prepare days radar data
var daysPostedLabels = [];
var daysPostedList = [];

for (var i = 0; i < allData['weekdays_count'].length; i++) {
    daysPostedLabels.push(allData['weekdays_count'][i][0]);
    daysPostedList.push(allData['weekdays_count'][i][1]);
}

// prepare days radar data
var hoursPostedLabels = [];
var hoursPostedList = [];

for (var i = 0; i < allData['hours_count'].length; i++) {
    hoursPostedLabels.push(allData['hours_count'][i][0]);
    hoursPostedList.push(allData['hours_count'][i][1]);
}

// update headers
$('#total_likes').text(likesSum);
$('#total_comments').text(commentsSum);

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
        labels: dateLabels,
        datasets: [{
            fill: false,
            pointRadius: 0,
            data: commentsList,
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
    labels: daysPostedLabels,
    datasets: [
        {
            backgroundColor: "#5FBB97",
        	pointRadius: 0,
            borderColor: "#5FBB97",
            pointBackgroundColor: "rgba(179,181,198,1)",
            pointBorderColor: "#fff",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(179,181,198,1)",
            data: daysPostedList
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
    labels: hoursPostedLabels,
    datasets: [
        {
            backgroundColor: "#FE938C",
        	pointRadius: 0,
            borderColor: "#FE938C",
            pointBackgroundColor: "rgba(179,181,198,1)",
            pointBorderColor: "#fff",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(179,181,198,1)",
            data: hoursPostedList
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
            data: [allData['user_info']['followed_by'], allData['user_info']['following']],
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


