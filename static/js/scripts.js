// change the rotation of the arrow for categories tab upon clicking for 3 buttons:
function dropdownCategory() {
    var dropdownList = document.getElementById("dropdownListCategory");
    dropdownList.classList.toggle("show-categories");

    var arrow = document.querySelector('.category-arrow');
    arrow.style.transform = dropdownList.classList.contains('show-categories') ? 'rotate(270deg)' : 'rotate(90deg)';
}

function dropdownLanguage() {
    var dropdownList = document.getElementById("dropdownListLanguage");
    dropdownList.classList.toggle("show-languages");

    var arrow = document.querySelector('.language-arrow');
    arrow.style.transform = dropdownList.classList.contains('show-languages') ? 'rotate(270deg)' : 'rotate(90deg)';
}

function dropdownCurrency() {
    var dropdownList = document.getElementById("dropdownListCurrency");
    dropdownList.classList.toggle("show-currencies");

    var arrow = document.querySelector('.currency-arrow');
    arrow.style.transform = dropdownList.classList.contains('show-currencies') ? 'rotate(270deg)' : 'rotate(90deg)';
}

window.onclick = function (event) {
    // Check for category dropdown
    if (!event.target.matches('.category-dropbtn')) {
        var categoryDropdowns = document.getElementsByClassName("categories-dropdown");
        var i;
        for (i = 0; i < categoryDropdowns.length; i++) {
            var openDropdown = categoryDropdowns[i];
            if (openDropdown.classList.contains('show-categories')) {
                openDropdown.classList.remove('show-categories');
                document.querySelector('.category-dropbtn img').style.transform = 'rotate(90deg)';
            }
        }
    }

    // Check for language dropdown
    if (!event.target.matches('.language-dropbtn')) {
        var languageDropdowns = document.getElementsByClassName("languages-dropdown");
        var j;
        for (j = 0; j < languageDropdowns.length; j++) {
            var openDropdown = languageDropdowns[j];
            if (openDropdown.classList.contains('show-languages')) {
                openDropdown.classList.remove('show-languages');
                document.querySelector('.language-dropbtn img').style.transform = 'rotate(90deg)';
            }
        }
    }

    // Check for currency dropdown
    if (!event.target.matches('.currency-dropbtn')) {
        var currencyDropdowns = document.getElementsByClassName("currencies-dropdown");
        var k;
        for (k = 0; k < currencyDropdowns.length; k++) {
            var openDropdown = currencyDropdowns[k];
            if (openDropdown.classList.contains('show-currencies')) {
                openDropdown.classList.remove('show-currencies');
                document.querySelector('.currency-dropbtn img').style.transform = 'rotate(90deg)';
            }
        }
    }
}

// add login and register fields transition
function addClass(){
    let parent = this.parentNode.parentNode;
    parent.classList.add("focus");
}

function removeClass(){
    let parent = this.parentNode.parentNode;
    if(this.value == ""){
        parent.classList.remove("focus");
    }

}

const loginInputs = document.querySelectorAll(".login-field");
const registerInputs = document.querySelectorAll(".register-field");

function setupFieldListeners(inputs) {
    inputs.forEach(input => {
        input.addEventListener("focus", addClass);
        input.addEventListener("blur", removeClass)
    });
}

setupFieldListeners(loginInputs);
setupFieldListeners(registerInputs);

// add button that displays password
function showPassword(passwordInputID, icon) {
    var userPassword = document.getElementById(passwordInputID);
    var icon = document.querySelector(icon);
    if (userPassword.type === 'password') {
        userPassword.type = "text";
        icon.style.color = "#cf3b3b";
    } else{
        userPassword.type = 'password';
        icon.style.color = "#c7b9b3";
    }
}

// display block for editing profile picture
function openImageBlock() {
    let block = document.getElementById("newImageBlock");
    let overlay = document.getElementById('overlay');

    block.style.display = "block";
    overlay.style.display = "block";
}

function closeImageBlock() {
    let block = document.getElementById("newImageBlock");
    let overlay = document.getElementById('overlay');

    block.style.display = "none";
    overlay.style.display = "none";
}

window.onclick = function(event) {
    var block = document.getElementById("newImageBlock");
    var overlay = document.getElementById("overlay")

    if (event.target == block) {
        block.style.display = "none";
        overlay.style.display = "none"
    }
}

// function to update the block width on window resize
function updateModalWidth() {
    var block = document.querySelector('.image-block-display');
    var windowWidth = window.innerWidth;
    var distanceFromEdge = 50;

    var newWidth = windowWidth - 2 * distanceFromEdge;

    block.style.width = newWidth + 'px';
}

window.addEventListener('resize', updateModalWidth);
updateModalWidth();
