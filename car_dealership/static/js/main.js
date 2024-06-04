document.addEventListener("DOMContentLoaded", function () {
  // Profile Dropdown
  const profileDropdown = document.getElementById("navbarDropdown");
  if (profileDropdown) {
    const menuBar = document.getElementById("menu-bar");
    profileDropdown.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent the default action
      menuBar.classList.toggle("active");
    });
  }

  // Filters
  const filterButton = document.getElementById("filter-toggle");
  const navSearchFilters = document.getElementById("nav-search-filters");
  if (filterButton && navSearchFilters) {
    const isFilterActive = window.localStorage.getItem("filtertab") === "true";
    if (isFilterActive) navSearchFilters.classList.add("active");

    filterButton.addEventListener("click", (event) => {
      event.preventDefault();
      const isFilterActive = navSearchFilters.classList.toggle("active");
      window.localStorage.setItem("filtertab", isFilterActive);
    });
  }

  // Search Input
  const searchInput = document.getElementById("search-input");
  const itemList = document.getElementById("item-list");
  const noResults = document.getElementById("no-results");
  const hiddenInput = document.getElementById("hidden-input");

  if (searchInput && itemList && noResults && hiddenInput) {
    searchInput.addEventListener("input", function () {
      let filter = this.value.toLowerCase();
      let items = itemList.querySelectorAll(".list-group-item");
      let found = false;

      items.forEach((item) => {
        if (item.textContent.toLowerCase().includes(filter)) {
          item.style.display = "";
          found = true;
        } else {
          item.style.display = "none";
        }
      });

      if (found) {
        noResults.style.display = "none";
      } else {
        hiddenInput.value = this.value;
        noResults.style.display = "block";
      }
    });
  }
});
