document.addEventListener("DOMContentLoaded", function () {
    const result = document.querySelector('.result');
    if (result) {
        result.style.transform = "scale(1.05)";
        result.style.transition = "all 0.3s ease";
    }
});