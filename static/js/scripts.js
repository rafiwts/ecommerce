// change the rotation of the arrow for categories tab upon clicking
function dropdownBox() {
    var dropdownList = document.getElementById("dropdownList");
    dropdownList.classList.toggle("show");

    var arrow = document.querySelector('.arrow');
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

// change the rotation of the arrow for categories tab upon clicking
function dropdownBoxHelp() {
    var dropdownList = document.getElementById("dropdownListHelp");
    dropdownList.classList.toggle("dupsko");

    var arrow = document.querySelector('.arrow-help');
    arrow.style.transform = dropdownList.classList.contains('dupsko') ? 'rotate(270deg)' : 'rotate(90deg)';
}

window.onclick = function (event) {
    if (!event.target.matches('.dropbtn-help')) {
        var dropdowns = document.getElementsByClassName("dropdown-categories-help");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('dupsko')) {
                openDropdown.classList.remove('dupsko');

                // Reset the arrow rotation
                document.querySelector('.right-help-bar img').style.transform = 'rotate(90deg)';
            }
        }
    }
}
