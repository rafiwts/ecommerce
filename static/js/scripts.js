// changes the rotation of the arrow for categories tab upon clicking for 3 buttons:
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
    // checks for category dropdown
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

    // checks for language dropdown
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

    // checks for currency dropdown
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

// adds login and register fields transition
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

// adds button that displays password
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

// displays and closes block for editing profile picture
function openImageBlock() {
    let block = document.getElementById("editImageBlock");
    let overlay = document.getElementById('overlay');

    block.style.display = "flex";
    overlay.style.display = "block";
}

function closeImageBlock() {
    let block = document.getElementById("editImageBlock");
    let overlay = document.getElementById('overlay');
    const filePreview = document.getElementById("uploadFilePreview");

    // deletes an uploaded file if it was not saved in the database
    while (filePreview.firstChild) {
        filePreview.removeChild(filePreview.firstChild);
    }

    block.style.display = "none";
    overlay.style.display = "none";
}

function toggleBlock(blockId, displayStyle) {
    let block = document.getElementById(blockId);
    let overlay = document.getElementById('overlay');

    block.style.display = displayStyle;
    overlay.style.display = displayStyle === 'flex' ? 'block' : 'none';
}

function openBlock(blockId) {
    toggleBlock(blockId, 'flex');
}

function closeBlock(blockId) {
    toggleBlock(blockId, 'none');
}

function openEditShippingAddressBlock(blockID) {
    let block = document.getElementById(blockID);
    let overlay = document.getElementById('overlay');

    block.style.display = "flex";
    overlay.style.display = "block";
}

function closeEditShippingAddressBlock(blockID) {
    let block = document.getElementById(blockID);
    let overlay = document.getElementById('overlay');

    block.style.display = "none";
    overlay.style.display = "none";
}


window.onclick = function(event) {
    let block = document.getElementById("editImageBlock");
    let blockContent = document.getElementById("editImageBlockContent")
    let overlay = document.getElementById("overlay")

    if (event.target == block || event.target == blockContent) {
        block.style.display = "none";
        overlay.style.display = "none"
    }
}

// function to update the block width on window resize
function updateModalWidth() {
    var block = document.querySelector('.edit-image-block-display');
    var windowWidth = window.innerWidth;
    var distanceFromEdge = 50;

    var newWidth = windowWidth - 2 * distanceFromEdge;

    block.style.width = newWidth + 'px';
}

window.addEventListener('resize', updateModalWidth);
updateModalWidth();

// displays a preview of the image before saving
document.getElementById("uploadProfileImage").addEventListener("change", function () {
    var fileInput = document.getElementById("uploadProfileImage");
    var filePreview = document.getElementById("uploadFilePreview");

    while (filePreview.firstChild) {
            filePreview.removeChild(filePreview.firstChild);
        }

    if (fileInput.files && fileInput.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            filePreview.innerHTML += "<br><img src='" + e.target.result + "' />";
        };
        reader.readAsDataURL(fileInput.files[0]);
    }
    });

// change password client validation
document.getElementById("passwordForm").addEventListener("submit", function(event) {
    const oldPasswordInput = document.getElementById("old_password");
    const newPasswordInput = document.getElementById("new_password");
    const confirmPasswordInput = document.getElementById("confirm_password");
    const validationMsg = document.getElementById("password-validation-msg");

    console.log(newPasswordInput.value)
    console.log(confirmPasswordInput.value)

    //TODO: temporary resolution for displaying validation errors
    validationMsg.innerHTML = '';

    let formFields = [oldPasswordInput, newPasswordInput, confirmPasswordInput];
    for (let i = 0; i < formFields.length; i++) {
        if (!formFields[i].value.trim()) {
            validationMsg.innerHTML = "All fields must have input.";
            event.preventDefault();
            return;
        }
    }

    //TODO: temporary resolution for displaying errors - change to a given box
    if (!/[A-Z]/.test(newPasswordInput.value) && !/\d/.test(newPasswordInput.value)) {
        validationMsg.innerHTML = "New password must contain at least one uppercase letter and one digit.";
        event.preventDefault();
        return;
    }

    if (!/[A-Z]/.test(newPasswordInput.value)) {
        validationMsg.innerHTML = "New password must contain at least one uppercase letter.";
        event.preventDefault();
        return;
    }

    if (!/\d/.test(newPasswordInput.value)) {
        validationMsg.innerHTML = "New password must contain at least one digit.";
        event.preventDefault();
        return;
    }

    // Check if passwords match
    if (newPasswordInput.value !== confirmPasswordInput.value) {
        validationMsg.innerHTML = "Passwords do not match.";
        event.preventDefault();
        return;
    }
});

// edit address  client validation
document.getElementById("editAddressForm").addEventListener("submit", function(event) {
    const streetInput = document.getElementById("street");
    const zipCodeInput = document.getElementById("zip_code");
    const cityInput = document.getElementById("city");
    const stateInput = document.getElementById("state");
    const countryInput = document.getElementById("country");
    const validationMsg = document.getElementById("edit-address-validation-msg");

    //TODO: temporary resolution for displaying validation errors
    let formFields = [streetInput, zipCodeInput, cityInput, stateInput, countryInput];
    for (let i = 0; i < formFields.length; i++) {
        if (!formFields[i].value.trim()) {
            validationMsg.innerHTML = "All fields must have input.";
            event.preventDefault();
            return;
        }
    }

    //TODO: temporary resolution for displaying errors - change to a given box
    if(streetInput.value.length >= 50) {
        validationMsg.innerHTML = "Thie field has too many characters";
        event.preventDefault();
        return;
    }

    if(zipCodeInput.value.length >= 10) {
        validationMsg.innerHTML = "Thie field has too many characters";
        event.preventDefault();
        return;
    }

    if(cityInput.value.length >= 58) {
        validationMsg.innerHTML = "Thie field has too many characters";
        event.preventDefault();
        return;
    }

    if(stateInput.value.length >= 30) {
        validationMsg.innerHTML = "Thie field has too many characters";
        event.preventDefault();
        return;
    }

    if(countryInput.value.length >= 50) {
        validationMsg.innerHTML = "Thie field has too many characters";
        event.preventDefault();
        return;
    }
});
