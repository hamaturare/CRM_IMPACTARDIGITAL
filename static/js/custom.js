const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");

// Show side bar
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
});

// Close side bar
closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
});

// Change theme
themeToggler.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme-variables');
    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
});

// Salvar o scroll horizontal da tabela, nao ta funcionando ainda. 

$(document).ready(function() {
    const tableContainer = $('#table-container');
    const sortableLinks = $('.sortable');

    // Save the scroll position on click
    sortableLinks.on('click', function() {
        localStorage.setItem('tableScrollPosition', tableContainer.scrollLeft());
    });

    // Restore the scroll position on page load
    const savedScrollPosition = localStorage.getItem('tableScrollPosition');
    if (savedScrollPosition) {
        tableContainer.scrollLeft(savedScrollPosition);
        localStorage.removeItem('tableScrollPosition');
    }
});

/*
// Add active class to sidebar links based on current URL
document.addEventListener('DOMContentLoaded', function() {
    const sideBarLinks = document.querySelectorAll('aside .sidebar a');
    const currentPath = window.location.pathname;

    sideBarLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        
        // Check if the current path matches the link path
        if (currentPath === linkPath) {
            link.classList.add('active');
        }

        // Add click event listener to add active class on click
        link.addEventListener('click', function() {
            // Remove the class 'active' from all links
            sideBarLinks.forEach(innerLink => {
                innerLink.classList.remove('active');
            });
            // Add the class 'active' to the clicked link
            this.classList.add('active');
        });
    });
});
*/