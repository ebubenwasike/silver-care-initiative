document.addEventListener('DOMContentLoaded', () => {
  console.log('[StaffPage_2.js] Resident table v2 loaded');
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

  window.filterResidents  = () => toast('Residents filtered (demo)');
  window.sendReminders    = () => toast('Reminders sent (demo)');
  window.addTaskPrompt    = () => toast('Add task dialog opened (demo)');
  window.completeSelected = () => toast('Tasks marked complete (demo)');
  window.clearCompleted   = () => toast('Completed tasks cleared (demo)');

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
    // Shift+A => New Appointment
    if (e.shiftKey && e.key === 'A') {
      e.preventDefault();
      window.openAddAppt();
    }
  });

  // --------- Load staff patients (dynamic residents) ----------
  let renderPatients = (patients) => {
    const table = document.getElementById('resTable');
    if (!table) return;

    let tbody = table.querySelector('tbody');
    if (!tbody) {
      tbody = document.createElement('tbody');
      table.appendChild(tbody);
    }

    tbody.innerHTML = '';

    if (!Array.isArray(patients) || patients.length === 0) {
      const tr = document.createElement('tr');
      const td = document.createElement('td');
      td.colSpan = 6;
      td.className = 'text-muted';
      td.textContent = 'No residents found. Use “＋ Add New Resident” to create one.';
      tr.appendChild(td);
      tbody.appendChild(tr);
    } else {
      patients.forEach((p) => {
        const tr = document.createElement('tr');
        const name = `${p.first_name || ''} ${p.last_name || ''}`.trim();
        const lastUpdated = p.created_at || '-';

        tr.innerHTML = `
          <td>${name || '-'}</td>
          <td>-</td>
          <td><span class="chip ${recentStatus(p.created_at)}">${recentStatus(p.created_at).replace('-', ' ')}</span></td>
          <td>-</td>
          <td>${lastUpdated}</td>
          <td class="d-flex flex-column gap-1">
            <button class="btn btn-sm btn-outline-primary" onclick="openBookingModal(${p.id}, '${name.replace(/'/g, "&#39;")}')">Schedule</button>
            <button class="btn btn-sm btn-outline-secondary" onclick="openVitalsModal(${p.id}, '${name.replace(/'/g, "&#39;")}')">Vitals</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    const badge = document.getElementById('assignedCount');
    if (badge) badge.textContent = String(patients?.length || 0);
  };

  // --- Overwrite renderPatients with new column layout (Last, First, PHN, Age, Actions) ---
  renderPatients = (patients) => {
    const table = document.getElementById('resTable');
    if (!table) return;
    const tbody = table.querySelector('tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    if (!Array.isArray(patients) || patients.length === 0) {
      const tr = document.createElement('tr');
      const td = document.createElement('td');
      td.colSpan = 5;
      td.className = 'text-muted';
      td.textContent = 'No residents found. Use “＋ Add New Resident” to create one.';
      tr.appendChild(td);
      tbody.appendChild(tr);
      return;
    }
    patients.forEach(p => {
      const tr = document.createElement('tr');
      const first = p.first_name || '';
      const last = p.last_name || '';
      const phn = p.phn || '-';
      const age = (() => {
        if (!p.dob) return '-';
        let dobStr = p.dob;
        // Normalize possible date formats from MySQL (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
        if (typeof dobStr === 'string' && dobStr.length > 10) dobStr = dobStr.slice(0,10);
        const parts = dobStr.split('-');
        if (parts.length !== 3) return '-';
        const year = parseInt(parts[0],10); const month = parseInt(parts[1],10)-1; const day = parseInt(parts[2],10);
        if (Number.isNaN(year) || Number.isNaN(month) || Number.isNaN(day)) return '-';
        const birth = new Date(year, month, day);
        let a = new Date().getFullYear() - birth.getFullYear();
        const m = new Date().getMonth() - birth.getMonth();
        if (m < 0 || (m === 0 && new Date().getDate() < birth.getDate())) a--;
        return a;
      })();
      const safeFirst = first.replace(/'/g, "&#39;");
      const safeLast = last.replace(/'/g, "&#39;");
      tr.innerHTML = `
        <td><a href="/patient/${p.id}" class="text-decoration-none">${last}</a></td>
        <td><a href="/patient/${p.id}" class="text-decoration-none">${first}</a></td>
        <td>${phn}</td>
        <td>${age}</td>
        <td class="d-flex flex-wrap gap-1">
          <button class="btn btn-sm btn-outline-secondary" onclick="openVitalsModal(${p.id}, '${safeFirst} ${safeLast}')">Vitals</button>
          <button class="btn btn-sm btn-outline-danger" onclick="deletePatient(${p.id})">Delete</button>
        </td>`;
      tbody.appendChild(tr);
    });
  };

  const loadStaffPatients = () => {
  fetch('/get_staff_patients')  // 🔁 use staff-specific endpoint
    .then((r) => r.json())
    .then((data) => {
      if (data.success) {
        const patients = data.patients || [];
        window._allPatients = patients;

        renderPatients(patients);
        populateApptResidentSelect(patients);

        // update “Total Residents” badge using the array length
        const totalSpan = document.getElementById('totalResidents');
        if (totalSpan) {
          totalSpan.textContent = patients.length;
        }
      } else {
        renderPatients([]);
      }
    })
    .catch(() => renderPatients([]));
};


  // Initial load and refresh when switching to Residents tab
  loadStaffPatients();
  document.addEventListener('shown.bs.tab', (e) => {
    if (e.target && e.target.getAttribute('href') === '#residents') {
      loadStaffPatients();
    }
  });

  const searchInput = document.getElementById('resSearch');
  const sortNameSel = document.getElementById('resSortName');
  const sortAddedSel = document.getElementById('resSortAdded');

  // Filter + sort residents (single responsibility; listeners attached once below)
  window.filterResidents = () => {
    if (!Array.isArray(window._allPatients)) return;
    let list = [...window._allPatients];

    // 1) Search filter
    const q = (searchInput?.value || '').trim().toLowerCase();
    if (q) {
      list = list.filter(p => {
        const parts = [p.first_name, p.last_name, p.phn, p.email, p.phone, p.id != null ? String(p.id) : ''];
        return parts.some(val => String(val || '').toLowerCase().includes(q));
      });
    }

    // 2) Sorting (only one sort active at a time)
    const sortName = sortNameSel?.value || '';
    const sortAdded = sortAddedSel?.value || '';

    if (sortName) {
      list.sort((a, b) => {
        const nameA = `${a.last_name || ''}, ${a.first_name || ''}`.toLowerCase().trim();
        const nameB = `${b.last_name || ''}, ${b.first_name || ''}`.toLowerCase().trim();
        if (nameA < nameB) return sortName === 'name-asc' ? -1 : 1;
        if (nameA > nameB) return sortName === 'name-asc' ? 1 : -1;
        return 0;
      });
    } else if (sortAdded) {
      list.sort((a, b) => {
        const da = a.created_at ? new Date(String(a.created_at).replace(' ', 'T')) : new Date(0);
        const db = b.created_at ? new Date(String(b.created_at).replace(' ', 'T')) : new Date(0);
        if (sortAdded === 'created-asc') {
          return da - db; // oldest first
        } else {
          return db - da; // newest first
        }
      });
    }

    renderPatients(list);
  }; // <-- close filterResidents

  // Attach search & sort listeners once (avoid duplicate registrations)
  if (searchInput) searchInput.addEventListener('input', window.filterResidents);
  if (sortNameSel) sortNameSel.addEventListener('change', window.filterResidents);
  if (sortAddedSel) sortAddedSel.addEventListener('change', window.filterResidents);

  // --------- Appointments: fetch, render, delete ----------
  const apptListEl = document.getElementById('apptList');

  const formatApptDate = (iso) => {
    try {
      const d = new Date(iso);
      if (Number.isNaN(d.getTime())) return iso || '-';
      return d.toLocaleDateString('en-US', {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
      });
    } catch (_) {
      return iso || '-';
    }
  };

  const renderAppointments = (items) => {
    if (!apptListEl) return;
    if (!Array.isArray(items) || items.length === 0) {
      apptListEl.innerHTML = '<p class="text-muted">No appointments scheduled yet. Use the buttons to add one.</p>';
      return;
    }
    const html = items.map((a) => {
      const dateTxt = formatApptDate(a.appointment_date);
      const notes = a.notes ? `<strong>Notes:</strong> ${a.notes}<br>` : '';
      return `
        <div class="appointment-item border-bottom pb-2 mb-2">
          <strong>Patient:</strong> ${a.first_name || ''} ${a.last_name || ''}<br>
          <strong>Type:</strong> ${a.appointment_type || '-'}<br>
          <strong>Date:</strong> ${dateTxt}<br>
          <strong>Time:</strong> ${a.appointment_time || '-'}<br>
          ${notes}
          <small class="text-muted">Status: ${a.status || 'scheduled'}</small><br>
          <button class="btn btn-outline-secondary btn-sm delete-btn" onclick="deleteAppointment(${a.id})" title="Delete appointment">🗑</button>
        </div>`;
    }).join('');
    apptListEl.innerHTML = html;
  };

  window.loadStaffAppointments = () => {
    fetch('/get_staff_appointments')
      .then((r) => r.json())
      .then((data) => {
        if (data.success) renderAppointments(data.appointments || []);
        else renderAppointments([]);
        updateOverviewApptResidents(data.appointments || []);
      })
      .catch(() => renderAppointments([]));
  };

  window.deleteAppointment = (id) => {
    if (!confirm('Are you sure you want to delete this appointment?')) return;
    fetch(`/delete_appointment/${id}`, { method: 'DELETE' })
      .then((r) => r.json())
      .then((data) => {
        if (data.success) {
          window.toast && window.toast('Appointment deleted', 'success');
          window.loadStaffAppointments();
        } else {
          window.toast && window.toast('Error deleting: ' + (data.error || 'Unknown'), 'error');
        }
      })
      .catch(() => window.toast && window.toast('Network error deleting appointment', 'error'));
  };

  // Delete patient (calls backend and refreshes list + total count)
  window.deletePatient = (id) => {
    if (!confirm('Delete this patient and all related data?')) return;
    fetch(`/delete_patient/${id}`, { method: 'DELETE' })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          window.toast && window.toast('Patient deleted', 'success');
          loadStaffPatients();
        } else {
          window.toast && window.toast('Error: ' + (data.error || 'Unknown'), 'error');
        }
      })
      .catch(() => window.toast && window.toast('Network error', 'error'));
  };

  // Initial load and refresh when switching to Appointments tab
  window.loadStaffAppointments();
  document.addEventListener('shown.bs.tab', (e) => {
    if (e.target && e.target.getAttribute('href') === '#appointments') {
      window.loadStaffAppointments();
    }
  });

  // ----- Helpers for status / recent -----
  window.recentStatus = (createdAt) => {
    if (!createdAt) return 'stable';
    const dt = new Date(createdAt.replace(' ', 'T'));
    if (Number.isNaN(dt.getTime())) return 'stable';
    const diffDays = (Date.now() - dt.getTime()) / 86400000;
    if (diffDays < 3) return 'new';
    if (diffDays < 14) return 'review';
    return 'stable';
  };

  // ----- Overview: list unique residents who have any appointments with this staff -----
  const updateOverviewApptResidents = (appointments) => {
    const list = document.getElementById('staffApptResidentsList');
    if (!list) return;
    const map = new Map();
    appointments.forEach(a => {
      const key = a.patient_id || `${a.first_name}-${a.last_name}`;
      if (!map.has(key)) map.set(key, a);
    });
    list.innerHTML = '';
    if (map.size === 0) {
      list.innerHTML = '<li class="text-muted">No appointments found.</li>';
      return;
    }
    Array.from(map.values()).forEach(a => {
      const name = `${a.first_name || ''} ${a.last_name || ''}`.trim();
      const li = document.createElement('li');
      li.textContent = name || 'Unnamed';
      list.appendChild(li);
    });
  };

  // ----- Appointment creation (POST) -----
  const populateApptResidentSelect = (patients) => {
    const sel = document.getElementById('apptResident');
    if (!sel) return;
    sel.innerHTML = '<option value="">Select resident...</option>' + patients.map(p => `<option value="${p.id}">${p.first_name} ${p.last_name}</option>`).join('');
  };

  window.saveAppointment = () => {
    const residentId = document.getElementById('apptResident')?.value;
    const type = document.getElementById('apptType')?.value;
    const date = document.getElementById('apptNewDate')?.value;
    const time = document.getElementById('apptNewTime')?.value;
    const notes = document.getElementById('apptNotes')?.value;
    if (!residentId || !type || !date || !time) {
      window.toast && window.toast('Fill required fields', 'warn');
      return;
    }
    const fd = new FormData();
    fd.append('patient_id', residentId);
    fd.append('appointment_type', type);
    fd.append('appointment_date', date);
    fd.append('appointment_time', time);
    fd.append('notes', notes || '');
    fetch('/book_appointment', { method: 'POST', body: fd })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          window.toast && window.toast('Appointment booked', 'success');
          const el = document.getElementById('addApptModal');
          const inst = el && bootstrap.Modal.getInstance(el);
          inst?.hide();
          window.loadStaffAppointments();
        } else {
          window.toast && window.toast('Error: ' + (data.error || 'Unknown'), 'error');
        }
      })
      .catch(() => window.toast && window.toast('Network error', 'error'));
  };

  // ----- Vitals editing -----
  window.openVitalsModal = (patientId, patientName) => {
    const idField = document.getElementById('vitalsPatientId');
    const nameField = document.getElementById('vitalsPatientName');
    if (!idField || !nameField) return;
    idField.value = patientId;
    nameField.textContent = patientName;
    // Clear existing values
    document.querySelectorAll('#vitalsForm input').forEach(inp => { if (inp.name !== 'patient_id') inp.value = ''; });
    // Load existing vitals
    fetch(`/get_vitals/${patientId}`)
      .then(r => r.json())
      .then(data => {
        if (data.success && data.vitals) {
          Object.entries(data.vitals).forEach(([k,v]) => {
            const f = document.querySelector(`#vitalsForm [name="${k}"]`);
            if (f) f.value = v || '';
          });
        }
      });
    const modal = new bootstrap.Modal(document.getElementById('vitalsModal'));
    modal.show();
  };

  window.submitVitals = () => {
    const form = document.getElementById('vitalsForm');
    if (!form) return;
    const fd = new FormData(form);
    if (!fd.get('patient_id')) {
      window.toast && window.toast('No patient selected', 'warn');
      return;
    }
    fetch('/update_vitals', { method: 'POST', body: fd })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          window.toast && window.toast('Vitals saved', 'success');
          const modalEl = document.getElementById('vitalsModal');
          const inst = modalEl && bootstrap.Modal.getInstance(modalEl);
          inst?.hide();
        } else {
          window.toast && window.toast('Error saving vitals', 'error');
        }
      })
      .catch(() => window.toast && window.toast('Network error', 'error'));
  };
});
