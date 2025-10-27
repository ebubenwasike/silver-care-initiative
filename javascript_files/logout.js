  const role = localStorage.getItem("userRole");
  if (role) {
    document.getElementById("welcome").textContent = 
      role === "nurse" ? "👩‍⚕️ Nurse Dashboard" : "👵 Resident Dashboard";
  }

  function logout() {
    // Show confirmation popup
    const confirmLogout = confirm("Are you sure you want to leave this page?");
    
    if (confirmLogout) {
      // User clicked "OK" → proceed to logout
      localStorage.removeItem("userRole");
      alert("✅ You have been logged out.");
      window.location.href = "index.html"; // redirect to homepage
    } else {
      // User clicked "Cancel" → stay on page
      alert("🔄 Logout cancelled. You’re still logged in.");
    }
  }
