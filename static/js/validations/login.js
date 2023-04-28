const onLoginSubmit = (event) => {
  event.preventDefault();
  let form = event.target;
  const [email, password] = form.elements;

  console.log("FIELDS", email.value, password.value);

  if (email && password) {
    window.location.replace("./dashboard.html");
  }
};
