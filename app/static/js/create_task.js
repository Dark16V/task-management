const form = document.getElementById('createTaskForm');

form.addEventListener('submit', async e => {
    e.preventDefault();

    const data = {
        title: form.title.value.trim(),
        description: form.description.value.trim(),
        due_date: form.due_date.value
    };

    const response = await fetch("{{ request.url_for('create_task') }}", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        window.location.href = "{{ request.url_for('tasks') }}";
    } else {
        const result = await response.json();
        alert(result.detail || "Error while creating task");
    }
});
