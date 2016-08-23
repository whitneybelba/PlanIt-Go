var city = document.getElementById("city");

city.addEventListener("submit", function (event) {
  if (city.validity.typeMismatch) {
    email.setCustomValidity("Please enter a state");
  } else {
    email.setCustomValidity("");
  }
});
