// Loading bar & submit button disable
const submitButton = document.querySelector('input[type="submit"]');
if (submitButton) {
  loadingDiv = document.getElementById('loading-bar');
  loadingDiv.style.width = '0%';
  submitButton.addEventListener('click', () => {
    loadingDiv.style.width = '100%';
    submitButton.classList.remove('ease-out-back-little');
    submitButton.classList.add('ease-out');
    setTimeout(() => {
      submitButton.disabled = true;
    }, 10);
  });
}


// Toast
const toastCloseButton = document.getElementById('toast-close-button');
if (toastCloseButton) {
  setTimeout(() => {
    toastCloseButton.parentElement.style = `
      transform: translateX(0%) translateY(0%);
      transition: transform 0.25s cubic-bezier(0.87, 0, 0.13, 1);
    `;
  }, 50);
  toastCloseButton.addEventListener('click', () => {
    toastCloseButton.parentElement.style = `
      transform: translateX(100%);
      transition: transform 0.25s cubic-bezier(0.87, 0, 0.13, 1);
    `;
  });

  const toastProgress = document.getElementById('toast-progress');
  if (toastProgress) {
    toastProgress.style.width = '0%';
    setTimeout(() => {
      toastProgress.style.width = '100%';
      setTimeout(() => {
        toastCloseButton.click();
      }, 5000);
    }, 50);
  }
}