document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('logo-sidebar');

    toggleButton.addEventListener('click', () => {
        sidebar.classList.toggle('-translate-x-full');
    });
});