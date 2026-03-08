document.addEventListener('DOMContentLoaded', function () {
    const roomCards = document.querySelectorAll('.room__card');
    const modal = document.getElementById('roomModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalDescription = document.getElementById('modalDescription');
    const modalPrice = document.getElementById('modalPrice');
    const modalFacilities = document.getElementById('modalFacilities');
    const closeModal = document.querySelector('.close');
    const bookNowButton = document.querySelector('.modal-book-btn');

    roomCards.forEach(card => {
        card.addEventListener('click', () => {
            const title = card.querySelector('h4').textContent;
            const description = card.querySelector('p').textContent;
            const price = card.querySelector('h3').textContent;
            const facilities = card.querySelector('.room__facilities').innerHTML;

            modalTitle.textContent = title;
            modalDescription.textContent = description;
            modalPrice.textContent = price;
            modalFacilities.innerHTML = facilities;

            modal.style.display = 'block';
        });
    });

    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Book Now Button Action
    bookNowButton.addEventListener('click', () => {
        //alert(`Booking ${modalTitle.textContent} for ${modalPrice.textContent}`);
        // You can redirect to a booking page or perform other actions here
        window.location.href = "booking.html";
    });
});
document.addEventListener('DOMContentLoaded', function () {
    // Set today's date as default check-in
    const today = new Date();
    const checkinInput = document.getElementById('checkin');
    const checkoutInput = document.getElementById('checkout');

    // Format date as YYYY-MM-DD
    const formatDate = (date) => {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    // Set min date to today
    checkinInput.min = formatDate(today);
    checkoutInput.min = formatDate(today);

    // When check-in changes, update checkout min date
    checkinInput.addEventListener('change', function () {
        checkoutInput.min = this.value;
        if (new Date(checkoutInput.value) < new Date(this.value)) {
            checkoutInput.value = this.value;
        }
    });

    // Form submission
    const availabilityForm = document.getElementById('availabilityForm');
    const availabilityBanner = document.getElementById('availabilityBanner');
    const bannerDates = document.getElementById('bannerDates');

    availabilityForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const checkin = checkinInput.value;
        const checkout = checkoutInput.value;

        if (!checkin || !checkout) {
            alert('Please select both check-in and check-out dates');
            return;
        }

        if (new Date(checkin) >= new Date(checkout)) {
            alert('Check-out date must be after check-in date');
            return;
        }

        // Show banner with selected dates
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        const checkinDate = new Date(checkin).toLocaleDateString('en-US', options);
        const checkoutDate = new Date(checkout).toLocaleDateString('en-US', options);

        bannerDates.innerHTML = `<strong>Showing availability for:</strong> ${checkinDate} to ${checkoutDate}`;
        availabilityBanner.style.display = 'flex';

        // Check room availability for May 5-10 (special case)
        const may5 = new Date('2024-05-05');
        const may10 = new Date('2024-05-10');
        const selectedCheckin = new Date(checkin);
        const selectedCheckout = new Date(checkout);

        // Check if selected dates overlap with May 5-10
        const isMay5to10Unavailable =
            (selectedCheckin >= may5 && selectedCheckin <= may10) ||
            (selectedCheckout >= may5 && selectedCheckout <= may10) ||
            (selectedCheckin <= may5 && selectedCheckout >= may10);

        // Mark rooms as unavailable if dates overlap with May 5-10
        const roomCards = document.querySelectorAll('.room__card');

        roomCards.forEach(card => {
            // Reset any previous unavailable state
            card.classList.remove('room-unavailable');

            if (isMay5to10Unavailable) {
                // For demo, we'll mark some rooms as unavailable
                const roomType = card.querySelector('h4').textContent;

                // Mark specific rooms as unavailable
                if (roomType.includes('Standard Single') ||
                    roomType.includes('Presidential Suite') ||
                    roomType.includes('Royal Suite')) {
                    card.classList.add('room-unavailable');
                }
            }
        });
    });

    // Clear availability check
    document.getElementById('clearAvailability').addEventListener('click', function () {
        availabilityBanner.style.display = 'none';
        checkinInput.value = '';
        checkoutInput.value = '';

        // Reset all rooms to available
        document.querySelectorAll('.room__card').forEach(card => {
            card.classList.remove('room-unavailable');
        });
    });

    // Add today's price and offers
    const roomCards = document.querySelectorAll('.room__card');
    roomCards.forEach(card => {
        const priceElement = card.querySelector('h3');
        const originalPrice = parseFloat(card.dataset.price);

        // Apply 10% discount to some rooms
        if (card.querySelector('h4').textContent.includes('Deluxe') ||
            card.querySelector('h4').textContent.includes('Family')) {
            const discountedPrice = originalPrice * 0.9;

            const priceContainer = document.createElement('div');
            priceContainer.className = 'price-container';
            priceContainer.innerHTML = `
                <h3>₹${discountedPrice.toLocaleString('en-IN')} <span>/ night</span></h3>
                <span class="original-price">₹${originalPrice.toLocaleString('en-IN')}</span>
                <span class="discount-badge">10% OFF</span>
            `;

            priceElement.replaceWith(priceContainer);
        }
    });
});