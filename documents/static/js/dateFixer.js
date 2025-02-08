// Initialize flatpickr for the date fields
document.addEventListener('DOMContentLoaded', function() {
    flatpickr("#id_date", {
        dateFormat: "Y-m-d", // Day-Month-Year format
        locale: {
            firstDayOfWeek: 7, // Start week on Sunday
            dir: "rtl", // Right-to-left support
            weekdays: {
                shorthand: ["أحد", "اثنين", "ثلاثاء", "أربعاء", "خميس", "جمعة", "سبت"], // Arabic week day names
                longhand: ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"] // Full day names
            },
            months: {
                shorthand: ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"], // Arabic month names
                longhand: ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"] // Full month names
            }
        },
        allowInput: true, // Allow user input
    });

    // Initialize flatpickr for the orig_date field
    flatpickr("#id_orig_date", {
        dateFormat: "Y-m-d", // Day-Month-Year format
        locale: {
            firstDayOfWeek: 7, // Start week on Sunday
            dir: "rtl", // Right-to-left support
            weekdays: {
                shorthand: ["أحد", "اثنين", "ثلاثاء", "أربعاء", "خميس", "جمعة", "سبت"], // Arabic week day names
                longhand: ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"] // Full day names
            },
            months: {
                shorthand: ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"], // Arabic month names
                longhand: ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"] // Full month names
            }
        },
        allowInput: true, // Allow user input
    });
});


// (( DateField Input Correction Functions ))
// Function to transform date from YYYY-MM-DD to DD-MM-YYYY format
function transformDateToDDMMYYYY(ids) {
    ids.forEach(id => {
        let input = document.getElementById(id);  // Reference to the date field by ID
        if (!input) return; // Skip if the input is not found
        
        let dateValue = input.value.trim();

        // If input is empty, do nothing
        if (dateValue === '') {
            return;
        }

        // Check if the date is in YYYY-MM-DD format
        let isoDateRegex = /^\d{4}-\d{2}-\d{2}$/; // YYYY-MM-DD format
        if (isoDateRegex.test(dateValue)) {
            // If in correct format, convert to DD-MM-YYYY
            let parts = dateValue.split('-');
            let day = parts[2].padStart(2, '0');  // Ensure two digits for day
            let month = parts[1].padStart(2, '0');  // Ensure two digits for month
            input.value = `${day}-${month}-${parts[0]}`;
        }
    });
}

// Function to transform date from DD-MM-YYYY to YYYY-MM-DD format
function transformDateToYYYYMMDD(ids) {
    ids.forEach(id => {
        let input = document.getElementById(id);  // Reference to the date field by ID
        if (!input) return; // Skip if the input is not found
        
        let dateValue = input.value.trim();

        // Check if the date is in DD-MM-YYYY format
        let dateRegex = /^(\d{1,2})-(\d{1,2})-(\d{4})$/; // DD-MM-YYYY format
        let match = dateValue.match(dateRegex);

        if (match) {
            // Ensure two digits for day and month, and four digits for year
            let day = match[1].padStart(2, '0');   // Ensure two digits for day
            let month = match[2].padStart(2, '0'); // Ensure two digits for month
            let year = match[3];                   // Year is already in the correct format

            // Set the input value to YYYY-MM-DD format
            input.value = `${year}-${month}-${day}`;
        }
    });
}

// Function to automatically add dashes to date field only if they are not already present
function autoAddDashes(ids) {
    ids.forEach(id => {
        let input = document.getElementById(id);  // Reference to the date field by ID
        if (!input) return; // Skip if the input is not found
        
        let dateValue = input.value.trim();

        // Check if the value already contains more than 1 dash (indicating proper formatting already exists)
        let dashCount = (dateValue.match(/-/g) || []).length;
        if (dashCount >= 2) {
            return;  // Skip adding dashes if they are already present
        }

        // Remove any non-digit characters
        dateValue = dateValue.replace(/\D/g, ''); 

        // Automatically add dashes as the user types (DD-MM-YYYY)
        if (dateValue.length <= 2) {
            input.value = dateValue; // Only day
        } else if (dateValue.length <= 4) {
            input.value = dateValue.slice(0, 2) + '-' + dateValue.slice(2); // DD-MM
        } else if (dateValue.length <= 6) {
            input.value = dateValue.slice(0, 2) + '-' + dateValue.slice(2, 4) + '-' + dateValue.slice(4); // DD-MM-YYYY
        } else {
            input.value = dateValue.slice(0, 2) + '-' + dateValue.slice(2, 4) + '-' + dateValue.slice(4, 8); // Limit to 8 digits
        }
    });
}

// Function to validate date value
function isValidDate(day, month, year) {
    const currentYear = new Date().getFullYear();
    if (year < 1900 || year > currentYear) return false;
    if (month < 1 || month > 12) return false;
    const daysInMonth = new Date(year, month, 0).getDate();
    return day >= 1 && day <= daysInMonth;
}

// Function to validate the date input
function validateDateInput(input) {
    const dateValue = input.value.trim();
    const dateRegex = /^(\d{1,2})-(\d{1,2})-(\d{4})$/; // DD-MM-YYYY format
    const match = dateValue.match(dateRegex);

    if (match) {
        const day = parseInt(match[1], 10);
        const month = parseInt(match[2], 10);
        const year = parseInt(match[3], 10);

        // Validate the date
        if (!isValidDate(day, month, year)) {
            alert("Please enter a valid date.");
            input.value = ""; // Optionally clear the input
        }
    }
}

// event listeners to the date field
document.addEventListener('DOMContentLoaded', function () {
    const dateIds = ['id_date', 'id_orig_date']; // IDs
    const dateInputs = dateIds.map(id => document.getElementById(id));
    // Loop through each date input field and attach event listeners if the field exists
    dateInputs.forEach(input => {
        // Check if the input element exists before adding event listeners
        if (input) {
            // Trigger conversion to DD-MM-YYYY when the field is focused
            input.addEventListener('focus', () => transformDateToDDMMYYYY(dateIds));

            // Trigger conversion to YYYY-MM-DD when the field loses focus (blur event)
            input.addEventListener('blur', () => transformDateToYYYYMMDD(dateIds));

            // Add listener for input change to automatically add dashes only if necessary
            input.addEventListener('input', () => autoAddDashes(dateIds));

            input.addEventListener('input', function () {
            validateDateInput(input);
        });
        } else {
            // If the input is not found, log a message or handle it as needed
            console.log('Date input field not found:', input);
        }
    });
});

