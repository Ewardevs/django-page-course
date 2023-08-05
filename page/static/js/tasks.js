// Obtén referencias a los elementos del DOM
var modalButtons = document.querySelectorAll(".card__subscribe__button");

modalButtons.forEach(modalButton => {
  const modal = document.getElementById(modalButton.dataset.id);
  const overlay = modal.querySelector(".modal__overlay");
  const cancelButton = modal.querySelector(".modal__footer .button--danger");

  modalButton.addEventListener("click", () => {
    modal.classList.add("modal--show")
  });

  overlay.addEventListener("click", () => {
    modal.classList.remove("modal--show")
  })

  cancelButton.addEventListener("click", () => {
    modal.classList.remove("modal--show")
  })
})
