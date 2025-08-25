const form = document.getElementById('updateNoteForm');

form.addEventListener('submit', async e => {
    e.preventDefault();

    const data = {
        title: form.title.value.trim(),
        content: form.content.value.trim()
    };

    const response = await fetch(`{{ request.url_for('update_note', note_id=note.id) }}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        window.location.href = "{{ request.url_for('notes') }}";
    } else {
        const result = await response.json();
        alert(result.detail || "Error while updating note");
    }
});
