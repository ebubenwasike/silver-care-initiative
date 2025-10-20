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

    const passwordInput = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");
    const eyeIcon = document.getElementById("eyeIcon");

    togglePassword.addEventListener("click", function () {
    const type = passwordInput.type === "password" ? "text" : "password";
    passwordInput.type = type;

    // Toggle icon
    if (type === "text") {
      eyeIcon.innerHTML = `<path d="M13.359 11.238l1.42 1.42a.75.75 0 1 1-1.06 1.06l-1.42-1.42A7.97 7.97 0 0 1 8 13.5c-5 0-8-5.5-8-5.5a15.634 15.634 0 0 1 2.54-2.778l-1.42-1.42a.75.75 0 1 1 1.06-1.06l1.42 1.42A7.97 7.97 0 0 1 8 2.5c5 0 8 5.5 8 5.5a15.634 15.634 0 0 1-2.54 2.778zM8 4.5c-3.314 0-6 3.134-6 4.5s2.686 4.5 6 4.5 6-3.134 6-4.5-2.686-4.5-6-4.5zm0 2a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5z"/>`;
    } else {
      eyeIcon.innerHTML = `<path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zm-8 4.5c-3.314 0-6-3.134-6-4.5s2.686-4.5 6-4.5 6 3.134 6 4.5-2.686 4.5-6 4.5z"/><path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zm0 4a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>`;
    }
  });
  // ...existing code...
});