const form = document.getElementById('noteForm');
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        title: form.title.value,
        content: form.content.value
    };

    const response = await fetch(form.action || window.location.pathname, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        window.location.href = document.referrer || "/notes";
    } else {
        const result = await response.json();
        alert(result.detail || "Error while creating note");
    }
});
