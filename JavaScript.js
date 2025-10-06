// Main JavaScript for SilverCare Portal

// Text-to-speech functionality
function readAloud(text) {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.8; // Slower for seniors
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    window.speechSynthesis.speak(utterance);
  } else {
    alert('Read aloud is not supported in your browser. Please call our helpline for assistance.');
  }
}

// Login functionality
function handleLogin(event) {
  if (event) event.preventDefault();
  
  const email = document.getElementById('email')?.value;
  const password = document.getElementById('password')?.value;
  const rememberMe = document.getElementById('rememberMe')?.checked;
  
  // Simple validation for login page
  if (email && password) {
    if (!email || !password) {
      showMessage('Please fill in all fields', 'error');
      return false;
    }
    
    // Show loading state
    const submitBtn = event?.target?.querySelector('button[type="submit"]');
    if (submitBtn) {
      const originalText = submitBtn.textContent;
      submitBtn.textContent = 'Signing In...';
      submitBtn.disabled = true;
    }
    
    // Simulate login process
    setTimeout(() => {
      simulateLoginSuccess(email, rememberMe);
      
      // Reset button if exists
      if (submitBtn) {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
      }
    }, 1500);
  }
  
  return false;
}

function simulateLoginSuccess(email, rememberMe) {
  showMessage('Login successful! Redirecting...', 'success');
  
  // Store login preference
  if (rememberMe) {
    localStorage.setItem('rememberedEmail', email);
  }
  
  // Store user session
  sessionStorage.setItem('userLoggedIn', 'true');
  sessionStorage.setItem('userEmail', email);
  
  // Redirect to dashboard after short delay
  setTimeout(() => {
    window.location.href = 'senior-dashboard.html';
  }, 1000);
}

function showMessage(message, type) {
  // Remove any existing messages
  const existingMessage = document.querySelector('.alert-message');
  if (existingMessage) {
    existingMessage.remove();
  }
  
  // Create new message element
  const messageDiv = document.createElement('div');
  messageDiv.className = alert alert-${type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'success'} alert-message;
  messageDiv.textContent = message;
  messageDiv.style.cssText = `
    position: fixed;
    top: 100px;
    right: 20px;
    z-index: 1060;
    min-width: 300px;
  `;
  
  document.body.appendChild(messageDiv);
  
  // Auto remove after 5 seconds
  setTimeout(() => {
    if (messageDiv.parentNode) {
      messageDiv.remove();
    }
  }, 5000);
}

function voiceLogin() {
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    showMessage('Voice login activated. Please say your email address.', 'info');
    
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onstart = function() {
      showMessage('Listening...', 'info');
    };
    
    recognition.onresult = function(event) {
      const transcript = event.results[0][0].transcript;
      const emailInput = document.getElementById('email');
      if (emailInput) {
        emailInput.value = transcript.toLowerCase().replace(/\s/g, '') + '@silvercare.org';
        showMessage('Email captured. Now please say your password.', 'info');
        
        // Listen for password
        setTimeout(() => {
          recognition.start();
        }, 1000);
      }
    };
    
    recognition.onerror = function(event) {
      showMessage('Voice recognition error: ' + event.error, 'error');
    };
    
    recognition.start();
  } else {
    showMessage('Voice recognition not supported in your browser', 'error');
  }
}

function simpleLogin() {
  // Simple login for users who prefer minimal interaction
  const simpleEmail = user${Math.floor(Math.random() * 1000)}@silvercare.org;
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  
  if (emailInput && passwordInput) {
    emailInput.value = simpleEmail;
    passwordInput.value = 'simple123';
    
    showMessage('Simple login credentials filled. Click Sign In to continue.', 'info');
    
    // Auto-submit after short delay
    setTimeout(() => {
      const loginForm = document.getElementById('loginForm');
      if (loginForm) {
        loginForm.dispatchEvent(new Event('submit'));
      }
    }, 500);
  }
}

function emergencyAccess() {
  // Emergency access - minimal verification
  if (confirm('Emergency access will log you in with limited functionality. Continue?')) {
    // Create emergency session
    sessionStorage.setItem('emergencyAccess', 'true');
    sessionStorage.setItem('emergencyLoginTime', new Date().toISOString());
    
    showMessage('Emergency access granted. Redirecting to emergency dashboard...', 'warning');
    
    setTimeout(() => {
      window.location.href = 'senior-dashboard.html?emergency=true';
    }, 1000);
  }
}

function enhanceAccessibility() {
  // Add ARIA labels and roles for better screen reader support
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  
  if (emailInput) {
    emailInput.setAttribute('aria-describedby', 'emailHelp');
  }
  
  if (passwordInput) {
    passwordInput.setAttribute('aria-describedby', 'passwordHelp');
  }
  
  // Add keyboard navigation enhancements
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
      // Close any open modals or focus on main content
      const activeModal = document.querySelector('.modal.show');
      if (activeModal) {
        const closeBtn = activeModal.querySelector('[data-bs-dismiss="modal"]');
        if (closeBtn) closeBtn.click();
      }
    }
  });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Check if we're on login page and initialize form
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
    
    // Check for remembered email
    const rememberedEmail = localStorage.getItem('rememberedEmail');
    if (rememberedEmail) {
      document.getElementById('email').value = rememberedEmail;
      document.getElementById('rememberMe').checked = true;
    }
  }
  
  // Enhance accessibility
  enhanceAccessibility();
  
  // Check login status for dashboard redirect
  const userLoggedIn = sessionStorage.getItem('userLoggedIn');
  const currentPage = window.location.pathname;
  
  if (userLoggedIn && currentPage.includes('login.html')) {
    // User is already logged in, redirect to dashboard
    window.location.href = 'senior-dashboard.html';
  }
  
  // Add click handlers for login buttons on home page
  const loginButtons = document.querySelectorAll('a[href="senior-dashboard.html"]');
  loginButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      if (!sessionStorage.getItem('userLoggedIn')) {
        e.preventDefault();
        window.location.href = 'login.html';
      }
    });
  });
});

// Utility function to check if user is logged in
function isUserLoggedIn() {
  return sessionStorage.getItem('userLoggedIn') === 'true';
}

// Logout function
function logout() {
  sessionStorage.removeItem('userLoggedIn');
  sessionStorage.removeItem('userEmail');
  sessionStorage.removeItem('emergencyAccess');
  window.location.href = 'index.html';
}