// script.js — FULL SweetAlert + Theme + Menu + Quick Add

document.addEventListener('DOMContentLoaded', () => {

  // =============== THEME ===============
  const body = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');

  const saved = localStorage.getItem('theme') || 'light';
  setTheme(saved);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = body.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      setTheme(next);
      localStorage.setItem('theme', next);
    });
  }

  function setTheme(name) {
    if (name === 'dark') {
      body.setAttribute('data-theme', 'dark');
      if (themeToggle) themeToggle.textContent = '☀️';
    } else {
      body.removeAttribute('data-theme');
      if (themeToggle) themeToggle.textContent = '🌙';
    }
  }


  // =============== HAMBURGER ===============
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('nav-links');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      if (navLinks.style.display === 'flex' || navLinks.style.display === 'block') {
        navLinks.style.display = 'none';
      } else {
        navLinks.style.display = 'flex';
      }
    });
  }


  // =============== USER DROPDOWN ===============
  const userBtn = document.getElementById('userBtn');
  const userDropdown = document.getElementById('userDropdown');

  if (userBtn && userDropdown) {
    userBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      userDropdown.style.display =
        userDropdown.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', () => {
      userDropdown.style.display = 'none';
    });
  }


  // =============== DELETE CONFIRM ===============
  document.addEventListener("click", function(e) {
    if (e.target.classList.contains("btn-delete")) {
      e.preventDefault();

      const url = e.target.getAttribute("href");

      Swal.fire({
        title: "Are you sure?",
        text: "You cannot undo this action!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete!",
      }).then((result) => {
        if (result.isConfirmed) {
          window.location.href = url;
        }
      });
    }
  });


  // =============== QUICK ADD FORM (AJAX + TOAST) ===============
  const form = document.getElementById("taskForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const title = document.getElementById("title").value;
      const description = document.getElementById("description").value;

      try {
        const res = await fetch("/add-task", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({ title, description })
        });

        const data = await res.json();

        if (data.status === "success") {

          Swal.fire({
            toast: true,
            icon: 'success',
            title: 'Task added successfully!',
            position: 'top-end',
            timer: 1500,
            showConfirmButton: false
          });

          form.reset();

        } else {
          Swal.fire({
            icon: 'error',
            title: 'Error!',
            text: data.message || 'Something went wrong.'
          });
        }

      } catch (err) {
        Swal.fire({
          icon: 'error',
          title: 'Request Failed!',
          text: 'Please try again.'
        });
      }
    });
  }

});


// Search bar submit on Enter key
const navSearchInput = document.getElementById("navSearchInput");

if (navSearchInput) {
    navSearchInput.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            const query = navSearchInput.value.trim();
            if (query) {
                window.location.href = "/search?q=" + encodeURIComponent(query);
            }
        }
    });
}
