"use strict";

document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.delete-btn');

    deleteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const sessionId = button.dataset.sessionId;
            const confirmation = confirm("Are you sure you want to delete this session?");

            if (confirmation) {
                fetch(`/workouts/api/delete-session/${sessionId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'), // Important for Django security
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        // If deletion is successful, remove the table row
                        const row = document.getElementById(`session-row-${sessionId}`);
                        row.remove();
                    } else {
                        // Handle errors
                        alert("Something went wrong. Could not delete the session.");
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});