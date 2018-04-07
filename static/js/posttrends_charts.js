// Extract JSON


// <---- Likes trend ---->

var ctx = document.getElementById("likesChart");

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: newOldArr,
        datasets: [{
        	fill: false,
        	pointRadius: 0,
            data: {{all_data['likes']}},
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
            data: {{all_data['comments']}},
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

var dayLabel = {{all_data['days']|safe}}.map(function(tuple) {
    return tuple[0];
});
var dayValue = {{all_data['days']|safe}}.map(function(tuple) {
    return tuple[1];
});

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

var hourLabel = {{all_data['hours']|safe}}.map(function(tuple) {
    return tuple[0];
});
var hourValue = {{all_data['hours']|safe}}.map(function(tuple) {
    return tuple[1];
});

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


var ctx = document.getElementById("filtersBar");

var hourLabel = {{all_data['filters']|safe}}.map(function(tuple) {
    return tuple[0];
});
var hourValue = {{all_data['filters']|safe}}.map(function(tuple) {
    return tuple[1];
});

var data = {
    labels: hourLabel,
    datasets: [
        {
            backgroundColor: "#918EF4",
            hoverBackgroundColor: "#918EF4",
            borderWidth: 0,
            data: hourValue
        }
    ]
};

var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: data,
    options: {
        responsive: false,
        legend: {
            display: false,
        },
        scales: {
		    xAxes: [{
		                gridLines: {
		                    display:false
		                }
		            }],
		    yAxes: [{
		                gridLines: {
		                    display:false
		                },
		                ticks: {
		              		display: false
		                }   
		            }]
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
            data: [{{all_data['basic']['counts']['followed_by']}}, {{all_data['basic']['counts']['follows']}}],
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


// tag position 

var ctx = document.getElementById("tagPos");

var tagPos = {{all_data['tag_positions']}};
var tagArr = [];

for (var i = 0; i < tagPos.length; i++) {
    
    tagArr.push( 
        {
            x: tagPos[i][0],
            y: tagPos[i][1],
            r: 5
        });
};

console.log(tagArr);


var data = {

    datasets: [
        {
            data: tagArr,
            backgroundColor:"#FF6384",
            hoverBackgroundColor: "#FF6384",
        }]
};