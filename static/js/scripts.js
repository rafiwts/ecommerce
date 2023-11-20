function dropdownBox() {
    var dropdownList = document.getElementById("dropdownList");
    dropdownList.classList.toggle("show");

    var arrow = document.querySelector('.tabs img');
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
                document.querySelector('.tabs img').style.transform = 'rotate(90deg)';
            }
        }
    }
}
