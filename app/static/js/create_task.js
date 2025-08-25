document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('createTaskForm');
    
    if (!form) {
        return;
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        e.stopPropagation();

        const data = {
            title: form.title.value.trim(),
            description: form.description.value.trim(),
            due_date: form.due_date.value
        };

        console.log('Sending data:', data);

        try {
            const response = await fetch('/task/create', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                window.location.href = '/dashboard/tasks';
            } else {
                const result = await response.text();
                alert('error' + result);
            }
        } catch (error) {
            alert('Network error' + error.message);
        }
    });
});