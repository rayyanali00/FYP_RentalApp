// function ApiCall(apiurl) {
//     axios.get(apiurl)
//         .then((response) => {
//             console.log(response.data)
//             for (var i = 0; i < response.data.length; i++) {
//                 dt = new Date(response.data[i]['dated'])
//                 date = moment(dt).format('MMMM-YYYY');
//                 labeldata.push(date);
//                 chrtdata.push(response.data[i].counted);
//             }
//         })
//         .catch((error) => {
//             console.log(error)
//         })
// }

// function plotGraph(id, label, apiUrl) {
//     var ctx = document.getElementById(id).getContext("2d");
//     var myChart = new Chart(ctx, {
//         type: 'line',
//         data: {
//             labels: labeldata,
//             datasets: [{
//                 label: label,
//                 data: chrtdata,
//                 backgroundColor: "rgba(153,255,51,0.6)",
//                 backgroundColor: [
//                     'rgba(255, 99, 132, 0.2)',
//                     'rgba(54, 162, 235, 0.2)',
//                     'rgba(255, 206, 86, 0.2)',
//                     'rgba(75, 192, 192, 0.2)',
//                     'rgba(153, 102, 255, 0.2)',
//                     'rgba(255, 159, 64, 0.2)'
//                 ],
//                 borderColor: [
//                     'rgba(255,99,132,1)',
//                     'rgba(54, 162, 235, 1)',
//                     'rgba(255, 206, 86, 1)',
//                     'rgba(75, 192, 192, 1)',
//                     'rgba(153, 102, 255, 1)',
//                     'rgba(255, 159, 64, 1)'
//                 ],
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             responsive: true,
//             maintainAspectRatio: false,
//             scales: {
//                 xAxes: [{
//                     ticks: {
//                         minRotation: 45,
//                         maxRotation: 45,
//                         autoSkip: true,
//                         maxTicksLimit: 5
//                     },
//                     gridLines: {
//                         color: "#f5f5f5"
//                     }
//                 }],
//                 yAxes: [{
//                     ticks: {
//                         autoSkip: true,
//                         maxTicksLimit: 3
//                     },
//                     gridLines: {
//                         color: "#f5f5f5"
//                     }
//                 }],
//             },
//             legend: {
//                 display: false,
//                 position: 'top',
//                 labels: {
//                     fontColor: 'gray'
//                 }
//             },
//             layout: {
//                 padding: {
//                     left: 50,
//                     right: 50,
//                     bottom: 0,
//                     top: 0
//                 }
//             },
//             tooltips: {
//                 enabled: true
//             },
//         },
//     });
//     setTimeout(function() {
//         myChart.update();
//     }, 1000);
// }

function plotGraph(id, label, apiUrl, btn_id) {
    var labeldata = [];
    var chrtdata = [];
    let dt;
    let date;
    axios.get(apiUrl)
        .then((response) => {
            var ctx = document.getElementById(id).getContext("2d");
            console.log(response.data)
            for (var i = 0; i < response.data.length; i++) {
                dt = new Date(response.data[i]['dated'])
                date = moment(dt).format('MMMM-YYYY');
                labeldata.push(date);
                chrtdata.push(response.data[i].counted);
            }
            var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labeldata,
                    datasets: [{
                        label: label,
                        data: chrtdata,
                        backgroundColor: "rgba(153,255,51,0.6)",
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255,99,132,1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        xAxes: [{
                            ticks: {
                                minRotation: 45,
                                maxRotation: 45,
                                autoSkip: true,
                                maxTicksLimit: 5
                            },
                            gridLines: {
                                color: "#f5f5f5"
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                autoSkip: true,
                                maxTicksLimit: 3
                            },
                            gridLines: {
                                color: "#f5f5f5"
                            }
                        }],
                    },
                    legend: {
                        display: false,
                        position: 'top',
                        labels: {
                            fontColor: 'gray'
                        }
                    },
                    layout: {
                        padding: {
                            left: 50,
                            right: 50,
                            bottom: 0,
                            top: 0
                        }
                    },
                    tooltips: {
                        enabled: true
                    },
                },
            });
            setTimeout(function() {
                myChart.update();
            }, 1000);
            $(`#${btn_id}`).on("click", function() {
                function reInitalizeChart(type) {
                    myChart = new Chart(ctx, {
                        type: type,
                        data: {
                            labels: labeldata,
                            datasets: [{
                                label: label,
                                data: chrtdata,
                                backgroundColor: "rgba(153,255,51,0.6)",
                                backgroundColor: [
                                    'rgba(255, 99, 132, 0.2)',
                                    'rgba(54, 162, 235, 0.2)',
                                    'rgba(255, 206, 86, 0.2)',
                                    'rgba(75, 192, 192, 0.2)',
                                    'rgba(153, 102, 255, 0.2)',
                                    'rgba(255, 159, 64, 0.2)'
                                ],
                                borderColor: [
                                    'rgba(255,99,132,1)',
                                    'rgba(54, 162, 235, 1)',
                                    'rgba(255, 206, 86, 1)',
                                    'rgba(75, 192, 192, 1)',
                                    'rgba(153, 102, 255, 1)',
                                    'rgba(255, 159, 64, 1)'
                                ],
                                borderWidth: 1
                            }]
                        },

                    });
                }
                myChart.destroy()
                console.log(myChart['config']['_config']['type'])
                if (myChart['config']['_config']['type'] == 'line') {
                    reInitalizeChart("bar")
                    $(this).html('Switch to <i class="fa fa-line-chart" aria-hidden="true"></i>')
                } else {
                    reInitalizeChart("line")
                    $(this).html('Switch to <i class="fa fa-bar-chart" aria-hidden="true"></i>')
                }
                // console.log(myChart)
                setTimeout(function() {
                    myChart.update();
                }, 1000);
            })

        })
        .catch((error) => {
            console.log(error)
        })
}