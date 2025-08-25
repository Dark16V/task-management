const form = document.getElementById('createTaskFormFriend');

form.addEventListener('submit', async e => {
    e.preventDefault();

    const data = {
        username: form.friend_username.value.trim(),
        title: form.title.value.trim(),
        description: form.description.value.trim(),
        due_date: form.due_date.value
    };

    const response = await fetch("/task/for_friend/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        window.location.href = "/dashboard/tasks";
    } else {
        const result = await response.json();
        alert(result.detail || "Error while creating task");
    }
});
