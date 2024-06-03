document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.querySelector('.product-category');
    const subcategorySelect = document.querySelector('.product-subcategory');
    const childSubcategorySelect = document.querySelector('.product-childsubcategory');
    const hiddenSubcategory = document.querySelector(".add-product-form-field.subcategory");
    const hiddenChildSubcategory = document.querySelector(".add-product-form-field.child_subcategory");

    const allSubcategories = Array.from(subcategorySelect.options);
    const allChildSubcategories = Array.from(childSubcategorySelect.options);

    categorySelect.addEventListener('change', function () {
        const categoryId = this.value;

        // if no category is chosen
        if (!categoryId) {
            hiddenSubcategory.style.display = "none";
            hiddenChildSubcategory.style.display = "none";
            return;
        }

        hiddenSubcategory.style.display = "block";
        subcategorySelect.innerHTML = '<option value="">Select a subcategory</option>';
        childSubcategorySelect.innerHTML = '<option value="">Select a child subcategory</option>';

        const filteredSubcategories = allSubcategories.filter(option => option.dataset.categoryId === categoryId);
        filteredSubcategories.forEach(option => subcategorySelect.appendChild(option));
    });

    subcategorySelect.addEventListener('change', function () {
        const subcategoryId = this.value;

        if (!subcategoryId) {
            hiddenChildSubcategory.style.display = "none";
            childSubcategorySelect.innerHTML = '<option value="">Select a child subcategory</option>';
            return;
        }

        hiddenChildSubcategory.style.display = "block";
        childSubcategorySelect.innerHTML = '<option value="">Select a child subcategory</option>';

        const filteredChildSubcategories = allChildSubcategories.filter(option => option.dataset.subcategoryId === subcategoryId);
        filteredChildSubcategories.forEach(option => childSubcategorySelect.appendChild(option));
    });
});
