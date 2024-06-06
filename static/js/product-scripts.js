document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.querySelector('.product-category');
    const subcategorySelect = document.querySelector('.product-subcategory');
    const childSubcategorySelect = document.querySelector('.product-childsubcategory');
    const hiddenSubcategory = document.querySelector(".add-product-form-field.subcategory");
    const hiddenChildSubcategory = document.querySelector(".add-product-form-field.child_subcategory");

    const allSubcategories = Array.from(subcategorySelect.options);
    const allChildSubcategories = Array.from(childSubcategorySelect.options);

    console.log(allSubcategories)
    console.log(allChildSubcategories)

    function updateSubcategories(categoryId) {
        if (!categoryId) {
            hiddenSubcategory.style.display = "none";
            hiddenChildSubcategory.style.display = "none";
            return;
        }

        hiddenSubcategory.style.display = "block";
        subcategorySelect.innerHTML = '<option value="">Select a subcategory</option>';
        const filteredSubcategories = allSubcategories.filter(option => option.dataset.categoryId === categoryId);
        filteredSubcategories.forEach(option => subcategorySelect.appendChild(option));
    }

    function updateChildSubcategories(subcategoryId) {
        if (!subcategoryId) {
            hiddenChildSubcategory.style.display = "none";
            childSubcategorySelect.innerHTML = '<option value="">Select a child subcategory</option>';
            return;
        }

        hiddenChildSubcategory.style.display = "block";
        childSubcategorySelect.innerHTML = '<option value="">Select a child subcategory</option>';
        const filteredChildSubcategories = allChildSubcategories.filter(option => option.dataset.subcategoryId === subcategoryId);
        filteredChildSubcategories.forEach(option => childSubcategorySelect.appendChild(option));
    }

    // fetch initial values
    const initialCategoryId = categorySelect.value;
    const initialSubcategoryId = subcategorySelect.value;

    updateSubcategories(initialCategoryId);
    updateChildSubcategories(initialSubcategoryId);

    // event listeners for changing value
    categorySelect.addEventListener('change', function () {
        updateSubcategories(this.value);
        childSubcategorySelect.innerHTML = '<option value="">Select a child subcategory</option>';
    });

    subcategorySelect.addEventListener('change', function () {
        updateChildSubcategories(this.value);
    });
});
