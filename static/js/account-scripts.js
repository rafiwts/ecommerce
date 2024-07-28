// handle url while opening and closing blocks
document.addEventListener('DOMContentLoaded', function() {
    function toggleBlock(blockId, displayStyle) {
        let block = document.getElementById(blockId);
        let overlay = document.getElementById('overlay');

        block.style.display = displayStyle;
        overlay.style.display = displayStyle === 'flex' ? 'block' : 'none';

        updateUrl(blockId, displayStyle);
    }

    function openBlock(blockId) {
        toggleBlock(blockId, 'flex')
    }

    function closeBlock(blockId) {
        toggleBlock(blockId, 'none')
    }

    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    function updateUrl (blockId, displayStyle) {
        const urlParams = new URLSearchParams(window.location.search);
        if (displayStyle === 'flex') {
            urlParams.set('block', blockId)
        } else {
            urlParams.delete('block')
        }
        const newUrl = `${window.location.pathname}?${urlParams.toString()}`;
        history.pushState(null, '', newUrl);
    }

    const block = getQueryParam('block');
    if (block) {
        openBlock(block);
    }

    document.addEventListener('click', function(event) {
        const overlay = document.getElementById('overlay');
        if (overlay && event.target === overlay) {
            const blockId = getQueryParam('block');
            if (blockId) {
                closeBlock(blockId);
            }
        }
    });

    // make functions global
    window.openBlock = openBlock;
    window.closeBlock = closeBlock;
});

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
        icon.style.color = "#646160";
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

function closeErrorBlock(blockId) {
    let block = document.getElementById(blockId);

    block.style.display = "none";
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
    const newPasswordInput = document.getElementById("newPassword");
    const confirmPasswordInput = document.getElementById("confirmPassword");
    const newPasswordInputError = document.getElementById("passwordFormErrorNewPassword");
    const confirmPasswordInputError = document.getElementById("passwordFormErrorConfirmPassword");
    const errorBlock = document.getElementById("passwordErrorInfo")

    // remove all error messages upon resubmitting
    newPasswordInputError.innerHTML = "";
    confirmPasswordInputError.innerHTML = "";

    // remove all error syles upon resubmitting
    newPasswordInput.classList.remove("error");
    confirmPasswordInput.classList.remove("error");

    let formFields = [newPasswordInput, confirmPasswordInput];
    for (let i = 0; i < formFields.length; i++) {
        if (!formFields[i].value.trim()) {
            switch (formFields[i].id) {
                case "new_password":
                    newPasswordInputError.innerHTML = "New password is required.";
                    break;
                case "confirm_password":
                    confirmPasswordInputError.innerHTML = "The confirmation of the password is required.";
                    break;
            }

            event.preventDefault();
            return;
        }
    }

    //TODO: add css and class name to display an error
    if (!/[A-Z]/.test(newPasswordInput.value) && !/\d/.test(newPasswordInput.value)) {
        newPasswordInput.classList.add("error")
        errorBlock.style.display = "block"
        newPasswordInputError.innerHTML = "New password must contain at least one uppercase letter and one digit.";
        event.preventDefault();
        return;
    }

    if (!/[A-Z]/.test(newPasswordInput.value)) {
        newPasswordInput.classList.add("error")
        errorBlock.style.display = "block"
        newPasswordInputError.innerHTML = "New password must contain at least one uppercase letter.";
        event.preventDefault();
        return;
    }

    if (!/\d/.test(newPasswordInput.value)) {
        newPasswordInput.classList.add("error")
        errorBlock.style.display = "block"
        newPasswordInputError.innerHTML = "New password must contain at least one digit.";
        event.preventDefault();
        return;
    }

    // Check if passwords match
    if (newPasswordInput.value !== confirmPasswordInput.value) {
        let focusedElement = document.activeElement;
        confirmPasswordInput.classList.add("error")
        confirmPasswordInputError.innerHTML = "Passwords do not match.";
        event.preventDefault();
        focusedElement.blur();
        return;
    }
});

// edit address  client validation
document.getElementById("editAddressForm").addEventListener("submit", function(event) {
    const streetInput = document.getElementById("street");
    const zipCodeInput = document.getElementById("zipCode");
    const cityInput = document.getElementById("city");
    const stateInput = document.getElementById("state");
    const countryInput = document.getElementById("country");
    const streetInputError = document.getElementById("editAddressErrorStreet");
    const zipCodeInputError = document.getElementById("editAddressErrorZipCode");
    const cityInputError = document.getElementById("editAddressErrorCity");
    const stateInputError = document.getElementById("editAddressErrorState");
    const countryInputError = document.getElementById("editAddressErrorCountry");

    streetInputError.innerHTML = "";
    zipCodeInputError.innerHTML = "";
    cityInputError.innerHTML = "";
    stateInputError.innerHTML = "";
    countryInputError.innerHTML = "";

    streetInput.classList.remove("error");
    zipCodeInput.classList.remove("error");
    cityInput.classList.remove("error");
    stateInput.classList.remove("error");
    countryInput.classList.remove("error");

    let formFields = [streetInput, zipCodeInput, cityInput, stateInput, countryInput];
    for (let i = 0; i < formFields.length; i++) {
        if (!formFields[i].value.trim()) {
            switch (formFields[i].id) {
                case "street":
                    streetInput.classList.add("error")
                    streetInputError.innerHTML = "Street is required.";
                    break;
                case "zipCode":
                    zipCodeInput.classList.add("error")
                    zipCodeInputError.innerHTML = "Zip code is required.";
                    break;
                case "city":
                    cityInput.classList.add("error")
                    cityInputError.innerHTML = "City is required.";
                    break;
                case "state":
                    stateInput.classList.add("error")
                    stateInputError.innerHTML = "State is required.";
                    break;
                case "country":
                    countryInput.classList.add("error")
                    countryInputError.innerHTML = "Country is required.";
                    break;
            }

            event.preventDefault();
            return;
        }
    }

    if(streetInput.value.length > 50) {
        streetInput.classList.add("error")
        streetInputError.innerHTML = "The 'street' field has too many characters.";
        event.preventDefault();
        return;
    }

    if(zipCodeInput.value.length > 10) {
        zipCodeInput.classList.add("error")
        zipCodeInputError.innerHTML = "Zip code is too long.";
        event.preventDefault();
        return;
    }

    if(cityInput.value.length > 58) {
        cityInput.classList.add("error")
        cityInputError.innerHTML = "The 'city' field has too many characters.";
        event.preventDefault();
        return;
    }

    if(stateInput.value.length > 40) {
        stateInput.classList.add("error")
        stateInputError.innerHTML = "The 'state' field has too many characters.";
        event.preventDefault();
        return;
    }

    if(countryInput.value.length > 50) {
        countryInput.classList.add("error")
        countryInputError.innerHTML = "Thie 'country' field has too many characters.";
        event.preventDefault();
        return;
    }
});

// edit address client validation
document.getElementById("editAccountForm").addEventListener("submit", function(event) {
    const firstNameInput = document.getElementById("firstName");
    const lastNameInput = document.getElementById("lastName");
    const birthDateInput = document.getElementById("dateOfBirth");
    const phoneNumberInput = document.getElementById("id_phone_1");
    const firstNameInputError = document.getElementById("editAccountErrorFirstName");
    const surnameInputError = document.getElementById("editAccountErrorLastName");
    const birthDateInputError = document.getElementById("editAccountErrorBirth");
    const phoneNumberInputError = document.getElementById("editAccountErrorPhone");

    firstNameInputError.innerHTML = "";
    surnameInputError.innerHTML = "";
    birthDateInputError.innerHTML = "";
    phoneNumberInputError.innerHTML = "";

    firstNameInput.classList.remove("error");
    lastNameInput.classList.remove("error");
    birthDateInput.classList.remove("error");
    phoneNumberInput.classList.remove("error");

    let formFields = [firstNameInput, lastNameInput, birthDateInput, phoneNumberInput];
    for (let i = 0; i < formFields.length; i++) {
        if (!formFields[i].value.trim()) {
            switch (formFields[i].id) {
                case "firstName":
                    firstNameInput.classList.add("error")
                    firstNameInputError.innerHTML = "First name is required.";
                    break;
                case "lastName":
                    lastNameInput.classList.add("error")
                    surnameInputError.innerHTML = "Last name is required.";
                    break;
                case "dateOfBirth":
                    birthDateInput.classList.add("error")
                    birthDateInputError.innerHTML = "Date of birth is required.";
                    break;
                case "id_phone_1":
                    phoneNumberInput.classList.add("error")
                    phoneNumberInputError.innerHTML = "Phone is required.";
                    break;
            }

            event.preventDefault();
            return;
        }
    }
    // TODO: add a logic that check the validity of a phone number
});
