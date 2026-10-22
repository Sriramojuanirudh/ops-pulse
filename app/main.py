document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.primary-btn, .secondary-btn, .nav-btn');
  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      window.location.href = '/';
    });
  });
});
