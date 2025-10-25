document.addEventListener('DOMContentLoaded', () => {
  const sidebar   = document.getElementById('appSidebar');
  const toggleBtn = document.getElementById('sidebarToggle');
  // Only keep this if you actually have a button with id="collapseCompact"
  const collapseBtn = document.getElementById('collapseCompact');

  if (!sidebar) return; // nothing to do

  const STORAGE_KEY = 'staff_sidebar_state';
  const isDesktop = () => window.innerWidth >= 992;

  // ----- Sidebar state helpers -----
  function setCompact(compact) {
    if (compact) {
      sidebar.classList.add('compact');
      sidebar.classList.remove('expanded');
      localStorage.setItem(STORAGE_KEY, 'compact');
    } else {
      sidebar.classList.remove('compact');
      sidebar.classList.add('expanded');
      localStorage.setItem(STORAGE_KEY, 'expanded');
    }
  }

  function applyInitialState() {
    const saved = localStorage.getItem(STORAGE_KEY) || 'expanded';
    sidebar.classList.remove('open'); // mobile drawer closed by default
    if (isDesktop()) {
      setCompact(saved === 'compact');
    } else {
      // On mobile we ignore compact/expanded classes visually; keep expanded for width calc on lg+
      sidebar.classList.remove('compact');
      sidebar.classList.add('expanded');
    }
  }

  applyInitialState();

  // ----- Toggle button behavior -----
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      if (!isDesktop()) {
        // Mobile: act like an off-canvas drawer
        sidebar.classList.toggle('open');
      } else {
        // Desktop: toggle compact vs expanded
        const isCompactNow = sidebar.classList.contains('compact');
        setCompact(!isCompactNow);
      }
    });

    // Keyboard accessibility
    toggleBtn.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleBtn.click();
      }
    });
  }

  // Optional extra collapse button if present
  if (collapseBtn) {
    collapseBtn.addEventListener('click', () => {
      const isCompactNow = sidebar.classList.contains('compact');
      setCompact(!isCompactNow);
    });
  }

  // Close drawer on outside click (mobile only)
  document.addEventListener('click', (e) => {
    if (!isDesktop() && sidebar.classList.contains('open')) {
      const clickedToggle = toggleBtn && toggleBtn.contains(e.target);
      const clickedInside = sidebar.contains(e.target);
      if (!clickedInside && !clickedToggle) {
        sidebar.classList.remove('open');
      }
    }
  });

  // Keep things sane on resize: close mobile drawer; restore desktop compact/expanded
  window.addEventListener('resize', () => {
    if (isDesktop()) {
      const saved = localStorage.getItem(STORAGE_KEY) || 'expanded';
      sidebar.classList.remove('open');
      setCompact(saved === 'compact');
    } else {
      // Reset to expanded class for consistent styles when going small
      sidebar.classList.remove('compact');
      sidebar.classList.add('expanded');
    }
  });

  // ----- Sync active state with Bootstrap tabs/pills -----
  const sideLinks = Array.from(document.querySelectorAll('.sidebar-nav .nav-link'));

  // Mark correct sidebar link when a tab is shown
  document.addEventListener('shown.bs.tab', (e) => {
    const targetId = e.target.getAttribute('href'); // e.g. "#residents"
    sideLinks.forEach(link => {
      const isActive = link.getAttribute('href') === targetId;
      link.classList.toggle('active', isActive);
      link.setAttribute('aria-current', isActive ? 'page' : 'false');
    });
  });

  // Initial active marking on load (pick already active tab OR hash)
  (function initActiveLink() {
    // Prefer the currently shown tab-pane
    const shownPane = document.querySelector('.tab-pane.show.active');
    const hash = shownPane ? `#${shownPane.id}` : (location.hash || null);

    if (hash) {
      sideLinks.forEach(link => {
        const isActive = link.getAttribute('href') === hash;
        link.classList.toggle('active', isActive);
        link.setAttribute('aria-current', isActive ? 'page' : 'false');
      });
    } else {
      // Fallback: first link gets aria-current if already has .active in markup
      const current = document.querySelector('.sidebar-nav .nav-link.active');
      if (current) current.setAttribute('aria-current', 'page');
    }
  })();

  window.focusGlobalSearch = function() {
    const searchInput = document.getElementById('globalSearch');
    if (searchInput) searchInput.focus();
  };

  window.openAddAppt = function() {
    const modal = new bootstrap.Modal(document.getElementById('addApptModal'));
    modal.show();
  };

  window.ackAlerts = function() {
    toast('Alerts acknowledged (demo)');
  };

  window.filterResidents = function() {
    toast('Residents filtered (demo)');
  };

  window.sendReminders = function() {
    toast('Reminders sent (demo)');
  };

  window.addTaskPrompt = function() {
    toast('Add task dialog opened (demo)');
  };

  window.completeSelected = function() {
    toast('Tasks marked complete (demo)');
  };

  window.clearCompleted = function() {
    toast('Completed tasks cleared (demo)');
  };

  window.openNewNote = function() {
    toast('New note dialog opened (demo)');
  };

  window.sendMsg = function() {
    const msgInput = document.getElementById('msgInput');
    if (msgInput && msgInput.value.trim()) {
      toast('Message sent: ' + msgInput.value);
      msgInput.value = '';
    }
  };

  window.saveSBAR = function() {
    document.getElementById('sbarStatus').textContent = 'Draft saved at ' + new Date().toLocaleTimeString();
  };

  window.clearSBAR = function() {
    ['sbarS', 'sbarB', 'sbarA', 'sbarR'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = '';
    });
    document.getElementById('sbarStatus').textContent = 'Form cleared';
  };

  window.readAloudSBAR = function() {
    toast('SBAR read aloud (demo)');
  };

  window.saveAppointment = function() {
    toast('Appointment saved (demo)');
    const modal = bootstrap.Modal.getInstance(document.getElementById('addApptModal'));
    modal.hide();
  };

  window.showHelp = function() {
    toast('Help documentation opened (demo)');
  };

  window.toast = function(message, type = 'info') {
    const toastCtn = document.getElementById('toastCtn');
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-bg-${type === 'error' ? 'danger' : type} border-0`;
    toastEl.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>
    `;
    toastCtn.appendChild(toastEl);
    const bsToast = new bootstrap.Toast(toastEl);
    bsToast.show();
    
    // Clean up after hide
    toastEl.addEventListener('hidden.bs.toast', () => {
      toastEl.remove();
    });
  };

  window.speak = function(text) {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      speechSynthesis.speak(utterance);
    }
  };

  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    // Global search focus on "/"
    if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      const searchInput = document.getElementById('globalSearch');
      if (searchInput) searchInput.focus();
    }
    
    // Quick add on Shift+N
    if (e.key === 'N' && e.shiftKey) {
      e.preventDefault();
      document.getElementById('btn-quickAdd')?.click();
    }
    
    // Quick appointment on Shift+A
    if (e.key === 'A' && e.shiftKey) {
      e.preventDefault();
      openAddAppt();
    }
  });
}); 


