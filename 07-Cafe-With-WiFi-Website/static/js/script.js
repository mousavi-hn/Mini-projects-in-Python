let map;
let markers = [];
let infoWindow;

function clearMarkers() {
  for (const m of markers) {
    m.setMap(null);
  }
  markers = [];
}

function initMapAndAutocomplete() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 47.4979, lng: 19.0402 }, // Budapest default
    zoom: 12,
    mapTypeControl: false,
    streetViewControl: false,
  });

  infoWindow = new google.maps.InfoWindow();

  const input = document.getElementById("city-search");

  const autocomplete = new google.maps.places.Autocomplete(input, {
    types: ["(cities)"],
    fields: ["place_id", "geometry", "name", "formatted_address"],
  });

  autocomplete.addListener("place_changed", () => {
    const place = autocomplete.getPlace();

    if (!place.geometry || !place.geometry.location) {
      alert("Please select an option from the dropdown list.");
      return;
    }

    const loc = place.geometry.location;

    // Move map to city
    map.panTo(loc);
    map.setZoom(13);

    // Clear previous cafe markers
    clearMarkers();

    // Fetch cafes near city center
    fetch(`/cafes?lat=${loc.lat()}&lng=${loc.lng()}&radius=5000`)
      .then((r) => r.json())
      .then((data) => {
        const cafes = data.cafes || [];
        console.log("Cafes received:", cafes.length);

        if (cafes.length === 0) return;

        const bounds = new google.maps.LatLngBounds();

        for (const cafe of cafes) {
          // Defensive: skip if missing coordinates
          if (typeof cafe.lat !== "number" || typeof cafe.lng !== "number") continue;

          const pos = { lat: cafe.lat, lng: cafe.lng };
          bounds.extend(pos);

          const marker = new google.maps.Marker({
            position: pos,
            map: map,
            title: cafe.name || "Cafe",
          });

          marker.addListener("click", () => {
            const name = cafe.name ?? "Unknown cafe";
            const rating = cafe.rating != null ? `⭐ ${cafe.rating}` : "No rating";
            const addr = cafe.vicinity ?? "";
            const mapsUrl = cafe.place_id
            ? `https://www.google.com/maps/place/?q=place_id:${encodeURIComponent(cafe.place_id)}`
            : null;

            infoWindow.setContent(`
                <div style="min-width:220px">
                  <div style="font-weight:600; margin-bottom:6px;">${name}</div>
                  <div style="margin-bottom:6px;">${rating}</div>
                  <div style="color:#444;">${addr}</div>
                  ${
                    mapsUrl
                      ? `<div style="margin-top:10px;">
                           <a href="${mapsUrl}" target="_blank" rel="noopener noreferrer">
                             Open in Google Maps
                           </a>
                         </div>`
                      : ""
                  }
                </div>
              `);

              infoWindow.open(map, marker);
            });

          markers.push(marker);
        }

        // Zoom to show all cafes (nice UX)
        map.fitBounds(bounds);

        // Optional: don’t zoom in too far if results are very clustered
        // google maps doesn't expose maxZoom directly here; you can clamp with an idle listener if needed.
      })
      .catch((err) => console.error("Failed to fetch cafes:", err));
  });
}

window.onload = initMapAndAutocomplete;
