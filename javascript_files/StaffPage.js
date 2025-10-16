document.addEventListener('DOMContentLoaded', function () {
  const sidebar = document.getElementById('appSidebar');
  const toggleBtn = document.getElementById('sidebarToggle');
  const collapseBtn = document.getElementById('collapseCompact');

  // initialize from saved preference
  const saved = localStorage.getItem('staff_sidebar_state');
  if (saved === 'compact') {
    sidebar.classList.remove('expanded');
    sidebar.classList.add('compact');
  } else {
    sidebar.classList.remove('compact');
    sidebar.classList.add('expanded');
  }

  // Toggle between expanded and compact
  function setCompact(compact) {
    if (compact) {
      sidebar.classList.add('compact');
      sidebar.classList.remove('expanded');
      localStorage.setItem('staff_sidebar_state', 'compact');
    } else {
      sidebar.classList.remove('compact');
      sidebar.classList.add('expanded');
      localStorage.setItem('staff_sidebar_state', 'expanded');
    }
  }

  if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
      // On small screens open/close drawer
      if (window.innerWidth < 992) {
        sidebar.classList.toggle('open');
        return;
      }
      const isCompact = sidebar.classList.contains('compact');
      setCompact(!isCompact);
    });
  }

  if (collapseBtn) {
    collapseBtn.addEventListener('click', function () {
      const isCompact = sidebar.classList.contains('compact');
      setCompact(!isCompact);
    });
  }

  // Close offcanvas on outside click (mobile)
  document.addEventListener('click', function (e) {
    if (window.innerWidth < 992) {
      if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    }
  });

  // keyboard accessibility: toggle with keyboard
  if (toggleBtn) {
    toggleBtn.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleBtn.click();
      }
    });
  }

  // document.addEventListener("DOMContentLoaded", () => {
  //   const links = document.querySelectorAll(".sidebar-nav .nav-link");
  //   const currentPath = window.location.pathname.split("/").pop();

  //   links.forEach(link => {
  //     const href = link.getAttribute("href");
  //     if (href === currentPath) {
  //       link.classList.add("active");
  //     }
  //     link.addEventListener("click", () => {
  //       links.forEach(l => l.classList.remove("active"));
  //       link.classList.add("active");
  //     });
  //   });
  // });

    document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('.sidebar-nav .nav-link');

    // When a Bootstrap pill/tab is shown, mark the matching link active
    document.addEventListener('shown.bs.tab', (e) => {
      const targetId = e.target.getAttribute('href'); // e.g., "#residents"
      links.forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === targetId);
        // ARIA polish:
        link.setAttribute('aria-current', link.classList.contains('active') ? 'page' : 'false');
      });
    });

    // On load, ensure the first active is marked for screen readers
    const current = document.querySelector('.sidebar-nav .nav-link.active');
    if (current) current.setAttribute('aria-current', 'page');
  });
  
});

