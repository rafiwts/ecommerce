// change the rotation of the arrow for categories tab upon clicking
console.log('Script is running!');

function dropdownBox() {
    var dropdownList = document.getElementById("dropdownList");
    dropdownList.classList.toggle("show");

    var arrow = document.querySelector('.tab-bar img');
    arrow.style.transform = dropdownList.classList.contains('show') ? 'rotate(270deg)' : 'rotate(90deg)';
}

window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-categories");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');

                // Reset the arrow rotation
                document.querySelector('.tab-bar img').style.transform = 'rotate(90deg)';
            }
        }
    }
}

// resize sidebar depending on the width of the site
window.addEventListener('resize', updateSidebarWidth);

function updateSidebarWidth() {
    var tabs = document.querySelector('.tabs');
    var sidebar = document.getElementById('sidebar');

    if (tabs) {
        var marginLeft = window.getComputedStyle(tabs).getPropertyValue('margin-left');
        sidebar.style.width = marginLeft;

        // Check if the max-width is reached
        var maxWidth = parseInt(window.getComputedStyle(sidebar).getPropertyValue('max-width'));
        var adjustedMaxWidth = 250;

        if (parseInt(marginLeft) > adjustedMaxWidth) {
            sidebar.style.maxWidth = adjustedMaxWidth + 'px';
        } else {
            sidebar.style.maxWidth = '';
        }
    }
}

updateSidebarWidth();
