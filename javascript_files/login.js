  document.addEventListener("DOMContentLoaded", () => {
    const dummySenior = { email: "seniortest@silvercare.org", password: "12345" };
    const dummyNurse  = { email: "nursetest@silvercare.org", password: "admin123" };
    const loginForm = document.getElementById("loginForm");
    const messageArea = document.getElementById("messageArea");

    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value.trim();
      messageArea.innerHTML = "";

      if (email === dummySenior.email && password === dummySenior.password) {
        showMessage("👵 Welcome, SilverCare Resident! Redirecting...", "success");
        setTimeout(() => window.location.href = "SeniorPage.html", 1500);
      } 
      else if (email === dummyNurse.email && password === dummyNurse.password) {
        showMessage("👩 Welcome, Nurse! Redirecting...", "success");
        setTimeout(() => window.location.href = "StaffPage.html", 1500);
      } 
      else {
        showMessage("❌ Invalid email or password. Please try again.", "danger");
      }
    });

    function showMessage(text, type) {
      const alertDiv = document.createElement("div");
      alertDiv.className = `alert alert-${type}`;
      alertDiv.textContent = text;
      messageArea.appendChild(alertDiv);
    }
  });
