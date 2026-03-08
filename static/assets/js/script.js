const menuBtn = document.getElementById("menu-btn");
const navLinks = document.getElementById("nav-links");
const menuBtnIcon = menuBtn.querySelector("i");

menuBtn.addEventListener("click", (e) => {
    navLinks.classList.toggle("open");

    const isOpen = navLinks.classList.contains("open");
    menuBtnIcon.setAttribute("class", isOpen ? "ri-close-line" : "ri-menu-line");
});

navLinks.addEventListener("click", (e) => {
    navLinks.classList.remove("open");
    menuBtnIcon.setAttribute("class", "ri-menu-line");
});


document.addEventListener('DOMContentLoaded', function () {
    const summary = document.getElementById('rooms-guests-summary');
    const details = document.getElementById('rooms-guests-details');
    const dropdown = document.getElementById('rooms-guests-dropdown');
    const childrenAgesContainer = document.getElementById('children-ages');
    
    // Set minimum date for check-in to today
    const checkInInput = document.getElementById('check-in');
    const checkOutInput = document.getElementById('check-out');
    
    const today = new Date().toISOString().split('T')[0];
    checkInInput.setAttribute('min', today);
    checkOutInput.setAttribute('min', today);
    
    // Check-in date change handler
    checkInInput.addEventListener('change', function() {
        const checkInDate = this.value;
        if (checkInDate) {
            // Set check-out minimum to be at least one day after check-in
            const nextDay = new Date(checkInDate);
            nextDay.setDate(nextDay.getDate() + 1);
            const nextDayStr = nextDay.toISOString().split('T')[0];
            checkOutInput.setAttribute('min', nextDayStr);
            
            // If check-out is before check-in, update it
            if (checkOutInput.value && checkOutInput.value <= checkInDate) {
                checkOutInput.value = nextDayStr;
            }
        }
    });

    // Dropdown toggle functionality - Click to show/hide
    if (summary && dropdown) {
        summary.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdown.classList.toggle('active');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('active');
            }
        });
        
        // Prevent dropdown close when clicking inside details
        details.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    // Done button to close dropdown
    const doneBtn = document.querySelector('.dropdown-done-btn');
    if (doneBtn) {
        doneBtn.addEventListener('click', function() {
            dropdown.classList.remove('active');
        });
    }

    // Increment/Decrement functionality
    const quantityButtons = document.querySelectorAll('.quantity__plus, .quantity__minus');

    quantityButtons.forEach(button => {
        button.addEventListener('click', function () {
            const target = button.getAttribute('data-target');
            const input = document.getElementById(target);
            let value = parseInt(input.value);

            if (button.classList.contains('quantity__plus')) {
                value++;
            } else if (button.classList.contains('quantity__minus')) {
                value--;
            }

            // Ensure the value stays within the min and max range
            value = Math.max(parseInt(input.min), Math.min(value, parseInt(input.max)));
            input.value = value;

            // Update summary
            updateSummary();

            // Update children's age dropdowns
            if (target === 'children') {
                updateChildrenAges(value);
            }
        });
    });

    // Function to update the summary
    function updateSummary() {
        const rooms = document.getElementById('rooms').value;
        const adults = document.getElementById('adults').value;
        const children = document.getElementById('children').value;

        summary.textContent = `${rooms} Room${rooms > 1 ? 's' : ''}, ${adults} Adult${adults > 1 ? 's' : ''}, ${children} Child${children > 1 ? 'ren' : ''}`;
        
        // Re-add the arrow icon
        const arrow = document.createElement('i');
        arrow.className = 'ri-arrow-down-s-line dropdown-arrow';
        summary.appendChild(arrow);
    }

    // Function to update children's age dropdowns
    function updateChildrenAges(numberOfChildren) {
        // Clear existing dropdowns
        childrenAgesContainer.innerHTML = '';

        // Add dropdowns for each child
        for (let i = 1; i <= numberOfChildren; i++) {
            const dropdownEl = document.createElement('div');
            dropdownEl.classList.add('children-age__dropdown');

            const label = document.createElement('label');
            label.textContent = `Child ${i} Age`;
            dropdownEl.appendChild(label);

            const select = document.createElement('select');
            select.name = `child-age-${i}`;

            // Add options for ages (from <1 year to 17 years)
            for (let age = 0; age <= 17; age++) {
                const option = document.createElement('option');
                option.value = age;
                option.textContent = age === 0 ? '<1 year' : `${age} year${age > 1 ? 's' : ''}`;
                select.appendChild(option);
            }

            dropdownEl.appendChild(select);
            childrenAgesContainer.appendChild(dropdownEl);
        }
    }

    // Initialize children's age dropdowns if children are already selected
    const initialChildren = parseInt(document.getElementById('children').value);
    if (initialChildren > 0) {
        updateChildrenAges(initialChildren);
    }
    
    // Form validation on submit
    const bookingForm = document.querySelector('.booking__form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            const checkIn = document.getElementById('check-in').value;
            const checkOut = document.getElementById('check-out').value;
            
            if (!checkIn || !checkOut) {
                e.preventDefault();
                alert('Please select both check-in and check-out dates.');
                return false;
            }
            
            const todayDate = new Date();
            todayDate.setHours(0, 0, 0, 0);
            const checkInDate = new Date(checkIn);
            const checkOutDate = new Date(checkOut);
            
            if (checkInDate < todayDate) {
                e.preventDefault();
                alert('Check-in date cannot be in the past. Please select a valid date.');
                return false;
            }
            
            if (checkOutDate <= checkInDate) {
                e.preventDefault();
                alert('Check-out date must be after check-in date.');
                return false;
            }
        });
    }
});

