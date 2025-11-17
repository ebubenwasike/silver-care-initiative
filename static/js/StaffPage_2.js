document.addEventListener('DOMContentLoaded', () => {
  // --------- Short helpers ----------
  const $id = (id) => document.getElementById(id);
  const $all = (sel) => Array.from(document.querySelectorAll(sel));
  const isDesktop = () => window.innerWidth >= 992;

  const sidebar   = $id('appSidebar');
  const toggleBtn = $id('sidebarToggle');
  const collapseBtn = $id('collapseCompact'); // optional

  if (!sidebar) return;

  // --------- Sidebar state ----------
  const STORAGE_KEY = 'staff_sidebar_state';

  const setCompact = (compact) => {
    sidebar.classList.toggle('compact', compact);
    sidebar.classList.toggle('expanded', !compact);
    localStorage.setItem(STORAGE_KEY, compact ? 'compact' : 'expanded');
  };

  const applyInitialState = () => {
    const saved = localStorage.getItem(STORAGE_KEY) || 'expanded';
    sidebar.classList.remove('open'); // mobile closed by default
    if (isDesktop()) {
      setCompact(saved === 'compact');
    } else {
      sidebar.classList.remove('compact');
      sidebar.classList.add('expanded');
    }
  };

  applyInitialState();

  // Toggle (desktop: compact/expanded, mobile: drawer)
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      if (isDesktop()) {
        setCompact(!sidebar.classList.contains('compact'));
      } else {
        sidebar.classList.toggle('open');
      }
    });

    // a11y: Enter/Space activate
    toggleBtn.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleBtn.click();
      }
    });
  }

  // Optional separate collapse button
  if (collapseBtn) {
    collapseBtn.addEventListener('click', () => {
      setCompact(!sidebar.classList.contains('compact'));
    });
  }

  // Click-away to close mobile drawer
  document.addEventListener('click', (e) => {
    if (!isDesktop() && sidebar.classList.contains('open')) {
      const clickedToggle = toggleBtn && toggleBtn.contains(e.target);
      const clickedInside = sidebar.contains(e.target);
      if (!clickedInside && !clickedToggle) sidebar.classList.remove('open');
    }
  });

  // Restore intended state on resize
  window.addEventListener('resize', () => {
    if (isDesktop()) {
      const saved = localStorage.getItem(STORAGE_KEY) || 'expanded';
      sidebar.classList.remove('open');
      setCompact(saved === 'compact');
    } else {
      sidebar.classList.remove('compact');
      sidebar.classList.add('expanded');
    }
  });

  // --------- Sync active nav with Bootstrap tabs ----------
  const sideLinks = $all('.sidebar-nav .nav-link');

  document.addEventListener('shown.bs.tab', (e) => {
    const targetId = e.target.getAttribute('href'); // "#residents"
    sideLinks.forEach((link) => {
      const active = link.getAttribute('href') === targetId;
      link.classList.toggle('active', active);
      link.setAttribute('aria-current', active ? 'page' : 'false');
    });
  });

  // Initial active state (current tab-pane or location hash)
  (() => {
    const shownPane = document.querySelector('.tab-pane.show.active');
    const hash = shownPane ? `#${shownPane.id}` : (location.hash || null);
    if (hash) {
      sideLinks.forEach((link) => {
        const active = link.getAttribute('href') === hash;
        link.classList.toggle('active', active);
        link.setAttribute('aria-current', active ? 'page' : 'false');
      });
    } else {
      const current = document.querySelector('.sidebar-nav .nav-link.active');
      if (current) current.setAttribute('aria-current', 'page');
    }
  })();

  // --------- Global actions exposed to HTML ----------
  window.focusGlobalSearch = () => $id('globalSearch')?.focus();

  window.openAddAppt = () => {
    const el = $id('addApptModal');
    if (!el) return;
    new bootstrap.Modal(el).show();
  };

  window.ackAlerts        = () => toast('Alerts acknowledged (demo)');
  window.filterResidents  = () => toast('Residents filtered (demo)');
  window.sendReminders    = () => toast('Reminders sent (demo)');
  window.addTaskPrompt    = () => toast('Add task dialog opened (demo)');
  window.completeSelected = () => toast('Tasks marked complete (demo)');
  window.clearCompleted   = () => toast('Completed tasks cleared (demo)');
  window.openNewNote      = () => toast('New note dialog opened (demo)');

  window.sendMsg = () => {
    const box = $id('msgInput');
    if (box && box.value.trim()) {
      toast('Message sent: ' + box.value.trim());
      box.value = '';
    }
  };

  window.saveSBAR = () => {
    const s = $id('sbarStatus');
    if (s) s.textContent = 'Draft saved at ' + new Date().toLocaleTimeString();
  };

  window.clearSBAR = () => {
    ['sbarS','sbarB','sbarA','sbarR'].forEach((id) => { const el = $id(id); if (el) el.value = ''; });
    const s = $id('sbarStatus');
    if (s) s.textContent = 'Form cleared';
  };

  window.readAloudSBAR = () => toast('SBAR read aloud (demo)');

  window.saveAppointment = () => {
    toast('Appointment saved (demo)');
    const el = $id('addApptModal');
    const inst = el && bootstrap.Modal.getInstance(el);
    inst?.hide();
  };

  window.showHelp = () => toast('Help documentation opened (demo)');

  // --------- Toast utility ----------
  window.toast = (message, type = 'info') => {
    const ctn = $id('toastCtn');
    if (!ctn) return;

    const map = { info:'info', success:'success', warn:'warning', warning:'warning', error:'danger', danger:'danger' };
    const bsType = map[type] || 'info';

    const el = document.createElement('div');
    el.className = `toast align-items-center text-bg-${bsType} border-0`;
    el.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    `;
    ctn.appendChild(el);

    const t = new bootstrap.Toast(el);
    t.show();
    el.addEventListener('hidden.bs.toast', () => el.remove());
  };

  // --------- TTS utility ----------
  window.speak = (text) => {
    if (!('speechSynthesis' in window)) return;
    speechSynthesis.speak(new SpeechSynthesisUtterance(text));
  };

  // --------- Keyboard shortcuts ----------
  document.addEventListener('keydown', (e) => {
    // Focus search on "/"
    if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey) {
      e.preventDefault();
      $id('globalSearch')?.focus();
    }
    // Shift+N => Quick Add (triggers your top-right "＋ New" button)
    if (e.shiftKey && e.key === 'N') {
      e.preventDefault();
      $id('btn-quickAdd')?.click();
    }
    // Shift+A => New Appointment
    if (e.shiftKey && e.key === 'A') {
      e.preventDefault();
      window.openAddAppt();
    }
  });
});
