        // document.addEventListener('DOMContentLoaded', function () {
        //     // Set minimum date for check-in (today)
        //     const today = new Date().toISOString().split('T')[0];
        //     document.getElementById('checkIn').min = today;
            
        //     // Load booking data from URL parameters
        //     const urlParams = new URLSearchParams(window.location.search);
        //     const roomType = urlParams.get('roomType');
        //     const price = parseFloat(urlParams.get('price'));
        //     const facilities = JSON.parse(urlParams.get('facilities'));

        //     // Set room info
        //     document.getElementById('roomTypeDisplay').textContent = roomType;
        //     document.getElementById('roomPriceDisplay').textContent = `₹${price.toFixed(2)} per night`;
            
        //     // Calculate initial payment values
        //     updatePaymentValues(price, 1);
            
        //     // Display facilities
        //     const facilitiesList = document.getElementById('facilitiesList');
        //     facilities.forEach(facility => {
        //         const li = document.createElement('li');
        //         li.textContent = facility;
        //         facilitiesList.appendChild(li);
        //     });

        //     // Update payment when dates change
        //     document.getElementById('checkIn').addEventListener('change', function() {
        //         const checkOut = document.getElementById('checkOut');
        //         checkOut.min = this.value;
        //         updateBookingDetails();
        //     });
            
        //     document.getElementById('checkOut').addEventListener('change', updateBookingDetails);
        // });

        // function updateBookingDetails() {
        //     const checkIn = new Date(document.getElementById('checkIn').value);
        //     const checkOut = new Date(document.getElementById('checkOut').value);
            
        //     if (checkIn && checkOut && checkOut > checkIn) {
        //         const nights = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
        //         const urlParams = new URLSearchParams(window.location.search);
        //         const price = parseFloat(urlParams.get('price'));
        //         updatePaymentValues(price, nights);
        //     }
        // }

        // function updatePaymentValues(pricePerNight, nights) {
        //     const totalPayment = pricePerNight * nights;
        //     const gst = totalPayment * 0.18;
        //     const finalAmount = totalPayment + gst;

        //     document.getElementById('totalPaymentDisplay').textContent = `₹${totalPayment.toFixed(2)}`;
        //     document.getElementById('gstDisplay').textContent = `₹${gst.toFixed(2)}`;
        //     document.getElementById('finalAmountDisplay').textContent = `₹${finalAmount.toFixed(2)}`;
        // }

        // function proceedToPayment() {
        //     const form = document.getElementById('guestForm');
        //     if (form.checkValidity()) {
        //         // Show confirmation modal
        //         const modal = document.getElementById('confirmationModal');
        //         const summary = document.getElementById('bookingSummary');
                
        //         const roomType = document.getElementById('roomTypeDisplay').textContent;
        //         const checkIn = document.getElementById('checkIn').value;
        //         const checkOut = document.getElementById('checkOut').value;
        //         const guests = document.getElementById('guests').value;
        //         const totalAmount = document.getElementById('finalAmountDisplay').textContent;
        //         const fullName = document.getElementById('fullName').value;
                
        //         summary.innerHTML = `
        //             <p><strong>Room Type:</strong> <span>${roomType}</span></p>
        //             <p><strong>Check-in:</strong> <span>${new Date(checkIn).toLocaleDateString()}</span></p>
        //             <p><strong>Check-out:</strong> <span>${new Date(checkOut).toLocaleDateString()}</span></p>
        //             <p><strong>Guests:</strong> <span>${guests}</span></p>
        //             <p><strong>Name:</strong> <span>${fullName}</span></p>
        //             <p><strong>Total Amount:</strong> <span>${totalAmount}</span></p>
        //         `;
                
        //         modal.style.display = 'flex';
        //     } else {
        //         form.reportValidity();
        //     }
        // }

        // function redirectToPayment() {
        //     // Collect all booking data
        //     const bookingData = {
        //         roomType: document.getElementById('roomTypeDisplay').textContent,
        //         price: parseFloat(document.getElementById('finalAmountDisplay').textContent.replace('₹', '')),
        //         checkIn: document.getElementById('checkIn').value,
        //         checkOut: document.getElementById('checkOut').value,
        //         guests: document.getElementById('guests').value,
        //         fullName: document.getElementById('fullName').value,
        //         email: document.getElementById('email').value,
        //         phone: document.getElementById('phone').value,
        //         facilities: Array.from(document.querySelectorAll('#facilitiesList li')).map(li => li.textContent)
        //     };
            
        //     // Store in sessionStorage
        //     sessionStorage.setItem('bookingData', JSON.stringify(bookingData));
            
        //     // Redirect to payment page
        //     window.location.href = "payment.html";
        // }

        // function closeModal() {
        //     document.getElementById('confirmationModal').style.display = 'none';
        // }