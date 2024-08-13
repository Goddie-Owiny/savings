document.addEventListener('DOMContentLoaded', function() {
    const toggler = document.getElementById('drawer-toggler');
    const sidebar = document.getElementById('logo-sidebar');
    
    toggler.addEventListener('click', function() {
        sidebar.classList.toggle('hidden');
    });
});