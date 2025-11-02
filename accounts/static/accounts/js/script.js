"use strict";

document.addEventListener('DOMContentLoaded', function () {
    const volumeChartCanvas = document.getElementById('volumeChart');

    if (volumeChartCanvas) {
        const chartData = JSON.parse(volumeChartCanvas.dataset.chartData);

        new Chart(volumeChartCanvas, {
            type: 'line',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Total Volume (kg)',
                    data: chartData.data,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    const pieChartCanvas = document.getElementById('musclePieChart');
    
    if (pieChartCanvas) {
        const pieChartData = JSON.parse(pieChartCanvas.dataset.chartData);

        if (pieChartData.data.length > 0) {
            new Chart(pieChartCanvas, {
                type: 'pie',
                data: { 
                    labels: pieChartData.labels,
                    datasets: [{
                        label: 'Number of Sets',
                        data: pieChartData.data,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.8)', 'rgba(54, 162, 235, 0.8)',
                            'rgba(255, 206, 86, 0.8)', 'rgba(75, 192, 192, 0.8)',
                            'rgba(153, 102, 255, 0.8)', 'rgba(255, 159, 64, 0.8)',
                            'rgba(199, 199, 199, 0.8)'
                        ],
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                }
            });
        } else {
            pieChartCanvas.parentElement.innerHTML = "<p>No muscle group data found for the last 60 days.</p>";
        }
        
       
    }

    const freqChartCanvas = document.getElementById('frequencyChart');

    if (freqChartCanvas) {
        const weeklyData = JSON.parse(freqChartCanvas.dataset.weeklyData);
        const monthlyData = JSON.parse(freqChartCanvas.dataset.monthlyData);
        
        const showWeeklyBtn = document.getElementById('showWeeklyBtn');
        const showMonthlyBtn = document.getElementById('showMonthlyBtn');

        const frequencyChart = new Chart(freqChartCanvas, {
            type: 'bar',
            data: {
                labels: weeklyData.labels,
                datasets: [{
                    label: '# of Workouts',
                    data: weeklyData.data,
                    backgroundColor: 'rgba(153, 102, 255, 0.7)',
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1 
                        },
                        grid: {
                            display: false
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });

        function updateChart(chart, labels, data) {
            chart.data.labels = labels;
            chart.data.datasets[0].data = data;
            chart.update();
        }

        showWeeklyBtn.addEventListener('click', () => {
            updateChart(frequencyChart, weeklyData.labels, weeklyData.data);
            showWeeklyBtn.classList.add('active');
            showMonthlyBtn.classList.remove('active');
        });

        showMonthlyBtn.addEventListener('click', () => {
            updateChart(frequencyChart, monthlyData.labels, monthlyData.data);
            showMonthlyBtn.classList.add('active');
            showWeeklyBtn.classList.remove('active');
        });
    }

    const weightChartCanvas = document.getElementById('weightHistoryChart');

    if (weightChartCanvas) {
        const chartData = JSON.parse(weightChartCanvas.dataset.chartData)

        if (chartData.data.length > 0) {
            new Chart(weightChartCanvas, {
                type: 'line',
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        label: 'Weight (kg)',
                        data: chartData.data,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: false
                        }
                    }
                }
            });
        } else {
            weightChartCanvas.parentElement.innerHTML = "<p>No weight history found. Update your profile to start tracking!</p>"
        }

        
    }
});