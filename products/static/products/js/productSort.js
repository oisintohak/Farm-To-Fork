function sort(event) {
    var currentUrl = new URL(window.location);
    var sort;
    var direction;
    switch (event.target.id) {
        case 'sortDistanceAsc':
            sort = 'distance';
            direction = 'asc';
            break;
        case 'sortAlphaAsc':
            sort = 'alpha';
            direction = 'asc';
            break;
        case 'sortAlphaDesc':
            sort = 'alpha';
            direction = 'desc';
            break;
        case 'sortDateDesc':
            sort = 'date'
            direction = 'desc'
            break
        case 'sortDateAsc':
            sort = 'date'
            direction = 'asc'
            break;

    }
    if (sort && direction) {
        currentUrl.searchParams.set('sort', sort);
        currentUrl.searchParams.set('direction', direction);
        window.location.replace(currentUrl);
    }
}

document.querySelectorAll('.product-sort-link').forEach(function (element) {
    element.addEventListener('click', sort);
});

var shareLocationButton = document.querySelector('#shareLocationButton');
function geoLocate() {
    shareLocationButton.disabled = true;
    shareLocationButton.innerHTML = '<span class="spinner-grow spinner-grow-lg mx-3 align-middle" role="status" aria-hidden="true"></span><span class="align-middle">Searching</span>';
    if (!navigator.geolocation) {
        window.alert('Geolocation is not supported by your browser');
    } else {
        navigator.geolocation.getCurrentPosition(success, error);
    }
}
function success(position) {
    shareLocationButton.disabled = false;
    shareLocationButton.innerHTML = 'Share Location'
    var lat = position.coords.latitude;
    var long = position.coords.longitude;
    sortDistance(lat, long)
}

function sortDistance(lat, long) {
    var currentUrl = new URL(window.location);
    currentUrl.searchParams.delete('sort');
    currentUrl.searchParams.delete('direction');
    currentUrl.searchParams.set('sort', 'distance');
    currentUrl.searchParams.set('lat', lat);
    currentUrl.searchParams.set('long', long);
    window.location.replace(currentUrl);
}

function error() {
    shareLocationButton.disabled = false;
    shareLocationButton.innerHTML = 'Share Location';
    window.alert('unable to retrieve your location.');
}
shareLocationButton.addEventListener('click', geoLocate)
document.querySelector('#useProfileAddressButton').addEventListener('click', function () {
    var lat = document.querySelector('#userAddressLat').value;
    var long = document.querySelector('#userAddressLong').value;
    sortDistance(lat, long);
})