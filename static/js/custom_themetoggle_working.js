document.addEventListener('DOMContentLoaded', function() {
    const sideMenu = document.querySelector("aside");
    const menuBtn = document.querySelector("#menu-btn");
    const closeBtn = document.querySelector("#close-btn");
    const themeToggler = document.querySelector(".theme-toggler");
    const lightModeIcon = themeToggler.querySelector('span:nth-child(1)');
    const darkModeIcon = themeToggler.querySelector('span:nth-child(2)');

    // Show side bar
    menuBtn.addEventListener('click', () => {
        sideMenu.style.display = 'block';
    });

    // Close side bar
    closeBtn.addEventListener('click', () => {
        sideMenu.style.display = 'none';
    });

    // Apply the saved theme on page load
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark-theme-variables');
        lightModeIcon.classList.remove('active');
        darkModeIcon.classList.add('active');
    } else {
        document.documentElement.classList.remove('dark-theme-variables');
        lightModeIcon.classList.add('active');
        darkModeIcon.classList.remove('active');
    }

    // Change theme on toggle button click
    themeToggler.addEventListener('click', () => {
        const isDarkTheme = document.documentElement.classList.contains('dark-theme-variables');
        if (isDarkTheme) {
            document.documentElement.classList.remove('dark-theme-variables');
            localStorage.setItem('theme', 'light');
            lightModeIcon.classList.add('active');
            darkModeIcon.classList.remove('active');
        } else {
            document.documentElement.classList.add('dark-theme-variables');
            localStorage.setItem('theme', 'dark');
            lightModeIcon.classList.remove('active');
            darkModeIcon.classList.add('active');
        }
    });
});
