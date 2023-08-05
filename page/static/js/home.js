var btn = document.querySelectorAll(".card__unsubscribe__button");

btn.forEach(function(boton) {
  boton.addEventListener("click", function(e) {
    var confirm_message = confirm(
      "¿Desea eliminar? Una vez confirmado, no podrá deshacer esta acción."
    );

    if (!confirm_message) {
      e.preventDefault(); // Prevenir la acción predeterminada solo si no se confirma
    } else {
      alert("Has dado de baja este curso. Ya no podrás deshacerlo.");
    }
  });
});
