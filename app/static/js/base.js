// ===================================================================
// Toggles display of sub navigation elements
// ===================================================================
var navDisplay = {
    display: 'flex',
    flexDirection: 'column'
};

$('.dropbtn').click(function (event) {
    event.stopPropagation();        // Prevent the click event from propagating to the document

    const menu = $(this).next('.dropdown-element'); // Get display element
    $('.dropdown-element').not(menu).hide();        // Hide any other elements displaying

    // Toggle the display when clicked
    if (menu.is(':visible')) {
        menu.hide();
    } else {
        menu.css(navDisplay).show();
    }

    // Add an event listener to hide the dropdown when clicking outside
    $(document).on('click', function (event) {
        // Check if the click is inside the dropdown or on the button
        if (!menu.is(event.target) && menu.has(event.target).length === 0 && !$(event.target).hasClass('dropbtn')) {
            menu.hide();
            $(document).off('click'); // Remove the event listener after hiding the dropdown
        }
    });
});

// ===================================================================
// Toggles Login and Sign Up elements
// ===================================================================
function toggleLogin(){
    const login = document.getElementsByClassName('active-container');
    const container = document.getElementById('container');

    if (login){
        container.classList.toggle("active-container");
    } else {
        container.classList.remove("active-container");
    }
};

// ===================================================================
// MANAGE PAGE
// ===================================================================
// Confirm deletion of the queried question before deleting it
document.querySelectorAll('.delete-cell').forEach(function (element) {
    element.addEventListener('click', function () {
        confirmDelete(element.dataset.record);
    });
});

// Display window prompt
function confirmDelete(element) {
    var record = element;
    var result = confirm("Are you sure you want to delete this record?");
    if (result) {
        window.location.href = "delete/" + encodeURIComponent(record);
    }
};

// ======================================================================================================
// FLASH MESSAGES [ERRORS, WARNINGS, INFO]
// ======================================================================================================
// Automatically hide flash messages after 5 seconds (adjust as needed)
setTimeout(function () {
    $('.flash-message').fadeOut('slow');
}, 5000);