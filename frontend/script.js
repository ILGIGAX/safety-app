document.addEventListener('DOMContentLoaded', function() {
  // Elementi per lo switch delle schede
  const tabRegister = document.getElementById('tab-register');
  const tabLogin = document.getElementById('tab-login');
  const formRegister = document.getElementById('form-register');
  const formLogin = document.getElementById('form-login');

  tabRegister.addEventListener('click', () => {
      tabRegister.classList.add('active');
      tabLogin.classList.remove('active');
      formRegister.style.display = 'block';
      formLogin.style.display = 'none';
  });

  tabLogin.addEventListener('click', () => {
      tabLogin.classList.add('active');
      tabRegister.classList.remove('active');
      formLogin.style.display = 'block';
      formRegister.style.display = 'none';
  });

  // URL del backend locale
  const backendURL = "http://localhost:8000";

  // Regex per la validazione della password
  function validatePassword(password) {
      const regex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!£\$%&\/\(=\?\^]).+$/;
      return regex.test(password);
  }

  // Gestione della registrazione
  const signupForm = document.getElementById('signupForm');
  signupForm.addEventListener('submit', function(e) {
      e.preventDefault();

      // Raccolta dei dati del form
      const formData = new FormData(signupForm);
      const data = Object.fromEntries(formData.entries());

      // Validazione della password
      if (!validatePassword(data.password)) {
          alert("La password non soddisfa i requisiti.");
          return;
      }

      // Invio dei dati al backend
      fetch(`${backendURL}/register`, {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({
              email: data.email,
              password: data.password,
              nome: data.firstName,
              cognome: data.lastName,
              data_nascita: data.dob,
              genere: data.gender,
              motivo_iscrizione: data.reason || ""
          }),
      })
      .then(response => {
          if (response.ok) {
              alert("Registrazione completata con successo!");
              signupForm.reset();
          } else {
              response.json().then(data => {
                  alert(data.detail || "Errore nella registrazione.");
              });
          }
      })
      .catch(error => {
          console.error("Errore nella registrazione:", error);
          alert("Errore nella registrazione.");
      });
  });

  // Gestione del login
  const signinForm = document.getElementById('signinForm');
  signinForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const formData = new FormData(signinForm);
      const data = Object.fromEntries(formData.entries());

      // Invio dei dati di login al backend
      fetch(`${backendURL}/login`, {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({
              email: data.email,
              password: data.password,
          }),
      })
      .then(response => response.json())
      .then(result => {
          if (result.authenticated) {
              alert("Accesso effettuato con successo!");
              window.location.href = "dashboard.html";
          } else {
              alert("Email o password errati.");
          }
      })
      .catch(error => {
          console.error("Errore durante il login:", error);
          alert("Errore durante il login.");
      });
  });
});
