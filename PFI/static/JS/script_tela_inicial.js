const slides = document.querySelectorAll(".slide");
let currentSlide = 0;

setInterval(() => {
  slides[currentSlide].classList.remove("active");
  currentSlide = (currentSlide + 1) % slides.length;
  slides[currentSlide].classList.add("active");
}, 3000);


function irParaLogin() {
  window.location.href = "/login/";
}

function irParaRegistro() {
  window.location.href = "/registrar/";
}
