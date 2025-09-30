"use strict";

document.addEventListener('DOMContentLoaded', () => {
    const exerciseSelect = document.getElementById('exercise-select');
    const progressChartCanvas = document.getElementById('progressChart');
    const chartPrompt = document.getElementById('chart-prompt');
    const showMaxWeightBtn = document.getElementById('showMaxWeightBtn');
    const showTotalVolumeBtn = document.getElementById('showTotalVolumeBtn');

    let progressChart;

    exerciseSelect.addEventListener('change', () => {
        const exerciseId = exerciseSelect.value;

        if (progressChart) {
            progressChart.destroy();
        }

        if (exerciseId) {
            chartPrompt.style.display = 'none';
            progressChartCanvas.style.display = 'block';

            fetch(`/workouts/api/get-exercise-progress/${exerciseId}/`)
                .then(response => response.json())
                .then(data => {
                    renderProgressChart(data);
                })
                .catch(error => console.error('Error fetching exercise progress data: ', error));

        } else {
            chartPrompt.style.display = 'block';
            progressChartCanvas.style.display = 'none';
        }
    });

    function renderProgressChart(data) {
        const ctx = progressChartCanvas.getContext('2d');
        progressChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Max Weight (kg)',
                        data: data.max_weight_data,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        hidden: false,
                    },
                    {
                        label: 'Total Volume (kg)',
                        data: data.total_volume_data,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        hidden: true,
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                    }
                }
            }
        });
    }

    showMaxWeightBtn.addEventListener('click', () => {
        if (progressChart) {
            progressChart.data.datasets[0].hidden = false;
            progressChart.data.datasets[1].hidden = true;
            progressChart.update();
            showMaxWeightBtn.classList.add('active');
            showTotalVolumeBtn.classList.remove('active');
        }
    });

    showTotalVolumeBtn.addEventListener('click', () => {
        if (progressChart) {
            progressChart.data.datasets[0].hidden = true;
            progressChart.data.datasets[1].hidden = false;
            progressChart.update();
            showTotalVolumeBtn.classList.add('active');
            showMaxWeightBtn.classList.remove('active');
        }
    });
});