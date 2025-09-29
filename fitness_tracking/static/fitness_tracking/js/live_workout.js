"use strict"

document.addEventListener('DOMContentLoaded', () => {
    const exerciseSelect = document.getElementById('id_exercise_name');
    const repsInput = document.getElementById('id_reps');
    const weightInput = document.getElementById('id_weight_kg');

    exerciseSelect.addEventListener('change', () => {
        const exerciseId = exerciseSelect.value;
        if (exerciseId) {
            fetch(`/workouts/api/get-last-set/${exerciseId}/`)
            .then(response => response.json())
            .then(data => {
                repsInput.value = data.reps;
                weightInput.value = data.weight_kg;
            })
            .catch(error => console.error('Error fetching last set data:', error));
        }
    });
})