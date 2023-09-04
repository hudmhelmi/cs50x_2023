document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('lore-header').addEventListener('click', function() {
        let content = document.getElementById('lore-content');
        if (content.style.display === 'none') {
            content.style.display = 'block';
        } else {
            content.style.display = 'none';
        }
    });
});
