// Obtén referencias a los elementos del DOM
var modals = document.querySelectorAll(".modal");
var btnAbrirModales = document.querySelectorAll("#openModalBtn");
var spansCerrar = document.querySelectorAll(".close");

// Abre los modales cuando se hace clic en los botones de apertura
btnAbrirModales.forEach(function (btnAbrirModal, index) {
  btnAbrirModal.addEventListener("click", function () {
    modals[index].style.display = "block";
  });
});

// Cierra los modales cuando se hace clic en las 'x'
spansCerrar.forEach(function (spanCerrar, index) {
  spanCerrar.addEventListener("click", function () {
    modals[index].style.display = "none";
  });
});

// Cierra los modales si se hace clic fuera de ellos
window.addEventListener("click", function (event) {
  modals.forEach(function (modal) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
});
