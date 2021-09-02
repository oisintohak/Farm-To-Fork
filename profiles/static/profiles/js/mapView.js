const map = L.map('map', {
  center: [53.2625652, -9.070427],
  zoom: 9
});


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png?{foo}', {
  foo: 'bar',
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
const markers = JSON.parse(document.getElementById('markers-data').textContent);
let url = "{% url 'profile' 'replacethistext' %}";
let feature = L.geoJSON(markers).bindPopup(function (layer) {
  let profileUrl = url.replace('replacethistext', layer.feature.properties.user)
  return `
  <div class="card bg-l-green border-d-green row g-0">
      <div class="col-12 text-center">
          <h6>${layer.feature.properties.first_name} ${layer.feature.properties.last_name}<h6>
              <span>
                  ${layer.feature.properties.area}
              </span>
          </div>
      <div class="col-12 text-center">
          <a class="btn btn-sm cta-button-secondary" href="${profileUrl}">Profile</a>
      </div>
  </div>
  `
}).addTo(map);