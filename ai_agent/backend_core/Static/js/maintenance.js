document.addEventListener('DOMContentLoaded', function() {
    const imgCount = 6;
    const idx = Math.floor(Math.random() * imgCount) + 1;
    const imgUrl = `/static/img/MAINTENANCE_MODE_IMG${idx}.jpg`;
    const bgDiv = document.getElementById('maintenance-bg');
    if (bgDiv) {
        bgDiv.style.backgroundImage = `url('${imgUrl}')`;
    }
}); 