const subscribeForms = document.querySelectorAll(".card__subscribe");

subscribeForms.forEach(subscribeForm => {
  const subscribeButton = subscribeForm.querySelector(".card__subscribe__button");

  subscribeButton.addEventListener("click", (ev) => {
    subscribeButton.setAttribute("disabled", "true");
    subscribeButton.innerText = "Loading..";
    subscribeForm.submit();
  })
});
