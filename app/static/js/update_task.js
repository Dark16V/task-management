const form = document.getElementById('taskForm');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        title: form.title.value,
        description: form.description.value,
        due_date: form.due_date.value ? new Date(form.due_date.value).toISOString() : null
    };

    const response = await fetch(form.action || window.location.href, {
        method: "post",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        window.location.href = "{{ request.url_for('tasks') }}";
    } else {
        const result = await response.json();
        alert(result.detail || "Error updating task");
    }
});
