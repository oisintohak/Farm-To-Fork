function init() {
  const geocoder = new google.maps.Geocoder();
  document.getElementById('geocode-form').addEventListener('submit', (e) => {
    e.preventDefault();
    geocodeAddress(geocoder);
  });
  document.getElementById('submit-form').disabled = false;
}

function geocodeAddress(geocoder) {
  let submitButton = document.getElementById('submit-form');
  submitButton.disabled = true;
  submitButton.innerHTML = '<span class="spinner-grow mx-1 align-middle" role="status" aria-hidden="true"></span>'
    + '<span class="align-middle">Checking Address...</span>';
  let address = '';
  const addressInputIDs = [
    'id_street_address1',
    'id_street_address2',
    'id_town_or_city',
    'id_county',
    'id_postcode',
    'id_country'
  ]
  for (let id of addressInputIDs) {
    address += `${document.getElementById(id).value}, `;
  }
  console.log(address)
  geocoder
    .geocode({ address: address })
    .then(({ results }) => {
      document.querySelector('#id_latitude').value =
        results[0].geometry.location.lat();
      document.querySelector('#id_longitude').value =
        results[0].geometry.location.lng();
      document.getElementById('geocode-form').submit();
    })
    .catch(() => {
      let submitModal = new bootstrap.Modal(
        document.getElementById('submit-modal')
      );
      submitModal.show();
      submitButton.disabled = false;
      submitButton.innerHTML = 'Submit';
    });
}
