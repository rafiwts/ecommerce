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

// suggestions while searching - to improve
$(document).ready(function() {
    const autocompleteUrl = $('#search-input').data('autocomplete-url');

    $('#search-input').on('input', function() {
        let query = $(this).val();
        if (query.length > 1) {
            $.ajax({
                url: autocompleteUrl,
                data: {'q': query},
                dataType: 'json',
                success: function(data) {
                    console.log('Data received:', data);
                    $('#autocomplete-list').empty();
                    if (data.length > 0) {
                        data.forEach(item => {
                            let suggestion = `<div class="autocomplete-suggestion" data-url="${item.url}" data-type="${item.type}">${item.name}</div>`;
                            $('#autocomplete-list').append(suggestion);
                        });
                        $('.autocomplete-suggestions').removeClass("no-data");
                        $('.autocomplete-suggestions').addClass("has-data");
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('Error:', textStatus, errorThrown);
                }
            });
        } else {
            $('#autocomplete-list').empty();
            $('.autocomplete-suggestions').removeClass('has-data');
            $('.autocomplete-suggestions').addClass("no-data")
        }
    });

    $('.search-input').on('focus', function() {
        setTimeout(function() { // Delay to allow click on suggestion
            if (!$('#search-input').val()) {
                $('.autocomplete-suggestions').removeClass('has-data');
                $('.autocomplete-suggestions').addClass('no-data');
            }
        }, 100);
    });

    $(document).on('click', '.autocomplete-suggestion', function() {
        let url = $(this).data('url');
        if (url) {
            window.location.href = url;
        }
    });

    $(document).click(function(e) {
        if (!$(e.target).closest('#search-input').length) {
            $('#autocomplete-list').empty();
        }
    });
});
