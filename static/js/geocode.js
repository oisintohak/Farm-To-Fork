function init() {
  const geocoder = new google.maps.Geocoder();
  document.getElementById('profile-form').addEventListener('submit', (e) => {
    e.preventDefault();
    geocodeAddress(geocoder);
  });
  document.getElementById('submit-form').disabled = false;
}

function geocodeAddress(geocoder) {
  let submitButton = document.getElementById('submit-form');
  submitButton.disabled = true;
  submitButton.value = 'Checking Address...';

  let inputs = Array.from(
    document.querySelectorAll('input[type=text], select')
  );
  let address;
  for (let item of inputs) {
    if (
      item.id !== 'id_first_name' &&
      item.id !== 'id_last_name' &&
      item.id !== 'id_phone_number'
    ) {
      address += `${item.value}, `;
    }
  }
  geocoder
    .geocode({ address: address })
    .then(({ results }) => {
      document.querySelector('#id_latitude').value =
        results[0].geometry.location.lat();
      document.querySelector('#id_longitude').value =
        results[0].geometry.location.lng();
      document.getElementById('profile-form').submit();
    })
    .catch(() => {
      let submitModal = new bootstrap.Modal(
        document.getElementById('submit-modal')
      );
      submitModal.show();
      submitButton.disabled = false;
      submitButton.textContent = 'Submit';
    });
}
