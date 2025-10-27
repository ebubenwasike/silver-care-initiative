 // Logout Confirmation
  function confirmLogout() {
    if (confirm("Are you sure you want to log out?")) {
      window.location.href = "login.html"; // redirect to login page
    }
  }

  // Read Aloud
  function readAloud(text) {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.8;
      window.speechSynthesis.speak(utterance);
    } else {
      alert('Read aloud not supported.');
    }
  }

  // Bootstrap form validation
  (() => {
    'use strict';
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  })();

  // Emergency Contacts
  function clearForm() {
    document.getElementById('contactForm').reset();
    document.getElementById('contactForm').classList.remove('was-validated');
  }

  function formatPhoneNumber(phone) {
    if (phone.length === 10) return `(${phone.substring(0,3)}) ${phone.substring(3,6)}-${phone.substring(6)}`;
    return phone;
  }

  function addEmergencyContact() {
    const name = document.getElementById('contactName').value.trim();
    const relationship = document.getElementById('relationship').value;
    const phone = document.getElementById('contactPhone').value.trim();
    const email = document.getElementById('contactEmail').value.trim();
    const isPrimary = document.getElementById('primaryContact').checked;

    const contactCard = document.createElement('div');
    contactCard.className = 'contact-card';
    contactCard.innerHTML = `
      <div class="d-flex justify-content-between align-items-start">
        <div>
          <h5>${name} ${isPrimary ? '<span class="badge bg-danger ms-2">Primary</span>' : ''}</h5>
          <p class="mb-1"><strong>Relationship:</strong> ${relationship}</p>
          <p class="mb-1"><strong>Phone:</strong> ${formatPhoneNumber(phone)}</p>
          ${email ? `<p class="mb-1"><strong>Email:</strong> ${email}</p>` : ''}
        </div>
        <div>
          <button class="btn btn-sm btn-outline-danger" onclick="this.closest('.contact-card').remove()">
            <i class="fas fa-trash"></i> Remove
          </button>
        </div>
      </div>
    `;

    if (isPrimary) {
      const existing = document.querySelectorAll('.contact-card');
      existing.forEach(c => {
        c.querySelector('.badge')?.remove();
      });
    }

    document.getElementById('contactList').appendChild(contactCard);
    clearForm();
  }

  document.getElementById('contactForm').addEventListener('submit', function(e){
    e.preventDefault(); e.stopPropagation();
    if(this.checkValidity()) addEmergencyContact();
    this.classList.add('was-validated');
  });

  // Appointment Booking
  function toggleAppointmentBooking() {
    const section = document.getElementById('appointmentSection');
    section.style.display = section.style.display === 'none' ? 'block' : 'none';
  }

  function selectNurse(nurseName) {
    window.selectedNurse = nurseName;
    document.getElementById('calendarSection').style.display = 'block';
  }

  function submitAppointment() {
    const date = document.getElementById('appointmentDate').value;
    const time = document.getElementById('appointmentTime').value;

    if (!date || !time) {
      alert('Please select both date and time.');
      return;
    }

    document.getElementById('nextAppointment').innerText = `Next Appointment: ${date} with ${window.selectedNurse}`;
    // Hide nurse cards and calendar
    document.getElementById('appointmentSection').style.display = 'none';
    alert('Appointment booked successfully!');
  }
