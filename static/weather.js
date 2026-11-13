(() => {
  const form = document.getElementById('city-form');
  const input = document.getElementById('city-input');
  const button = document.getElementById('search-button');
  const locationButton = document.getElementById('location-button');
  const saveCurrentCityButton = document.getElementById('save-current-city');
  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  const status = document.getElementById('status-message');
  const currentCard = document.getElementById('current-weather');
  const forecastSection = document.getElementById('forecast-section');
  const hourlySection = document.getElementById('hourly-section');
  const forecastGrid = document.getElementById('forecast-grid');
  const hourlyGrid = document.getElementById('hourly-grid');
  const favoritesList = document.getElementById('favorites-list');
  const defaultFavorites = ['San Francisco', 'New York', 'Tokyo', 'London'];
  const icons = { clear: '☀', partly: '⛅', cloudy: '☁', fog: '〰', rain: '☂', snow: '❄', storm: 'ϟ' };

  function readFavorites() {
    try {
      const stored = JSON.parse(localStorage.getItem('weather-favorites') || '[]');
      return Array.isArray(stored) ? stored.filter(Boolean) : [];
    } catch (_err) {
      return [];
    }
  }

  function writeFavorites(items) {
    try {
      localStorage.setItem('weather-favorites', JSON.stringify(items));
    } catch (_err) {
      // ignore storage failures
    }
  }

  function renderFavorites() {
    const favorites = readFavorites();
    const items = favorites.length ? favorites : defaultFavorites;
    favoritesList.innerHTML = '';
    items.forEach((city) => {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'favorite-chip';
      chip.textContent = city;
      chip.addEventListener('click', () => {
        input.value = city;
        loadWeather(city);
      });
      favoritesList.appendChild(chip);
    });
  }

  function saveCurrentCity() {
    const city = (input.value || '').trim();
    if (!city) return;
    const favorites = readFavorites();
    const next = [city, ...favorites.filter((entry) => entry.toLowerCase() !== city.toLowerCase())].slice(0, 6);
    writeFavorites(next);
    renderFavorites();
  }

  function iconFor(condition) {
    const text = condition.toLowerCase();
    if (text.includes('thunder')) return icons.storm;
    if (text.includes('snow') || text.includes('ice') || text.includes('freezing')) return icons.snow;
    if (text.includes('rain') || text.includes('drizzle') || text.includes('shower')) return icons.rain;
    if (text.includes('fog')) return icons.fog;
    if (text.includes('overcast')) return icons.cloudy;
    if (text.includes('cloud')) return icons.partly;
    return icons.clear;
  }

  function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    const isLight = theme === 'light';
    themeIcon.textContent = isLight ? '☾' : '☼';
    themeToggle.setAttribute('aria-label', `Switch to ${isLight ? 'dark' : 'light'} theme`);
    try { localStorage.setItem('weather-theme', theme); } catch (_) {}
  }

  function dayName(dateString, index) {
    if (index === 0) return 'Today';
    return new Intl.DateTimeFormat(undefined, { weekday: 'short' }).format(new Date(`${dateString}T12:00:00`));
  }

  function showError(message) {
    status.textContent = message;
    status.classList.add('is-error');
    status.hidden = false;
    currentCard.hidden = true;
    forecastSection.hidden = true;
    hourlySection.hidden = true;
  }

  function renderWeather(data) {
    document.getElementById('location-name').textContent = [data.city, data.country].filter(Boolean).join(', ');
    document.getElementById('today-label').textContent = new Intl.DateTimeFormat(undefined, { weekday: 'long', month: 'long', day: 'numeric' }).format(new Date());
    document.getElementById('current-icon').textContent = iconFor(data.condition);
    document.getElementById('temperature').textContent = Math.round(data.temperature);
    document.getElementById('condition').textContent = data.condition;
    document.getElementById('feels-like').textContent = Math.round(data.feels_like);
    document.getElementById('humidity').textContent = Math.round(data.humidity);
    document.getElementById('wind-speed').textContent = Math.round(data.wind_speed);
    document.getElementById('coordinates').textContent = `${Number(data.latitude).toFixed(2)}°, ${Number(data.longitude).toFixed(2)}°`;

    forecastGrid.replaceChildren();
    (data.daily || []).forEach((day, index) => {
      const card = document.createElement('article');
      card.className = `forecast-day${index === 0 ? ' is-today' : ''}`;
      const label = document.createElement('p'); label.className = 'forecast-day-name'; label.textContent = dayName(day.date, index);
      const icon = document.createElement('span'); icon.className = 'forecast-icon'; icon.setAttribute('aria-hidden', 'true'); icon.textContent = iconFor(day.condition);
      const condition = document.createElement('p'); condition.className = 'forecast-condition'; condition.textContent = day.condition;
      const range = document.createElement('p'); range.className = 'temperature-range';
      const high = document.createElement('strong'); high.textContent = `${Math.round(day.high)}°`;
      const low = document.createElement('span'); low.textContent = `${Math.round(day.low)}°`;
      range.append(high, low); card.append(label, icon, condition, range); forecastGrid.append(card);
    });

    hourlyGrid.replaceChildren();
    (data.hourly || []).forEach((hour, index) => {
      const card = document.createElement('article');
      card.className = `hour-card${index === 0 ? ' is-current-hour' : ''}`;
      const time = document.createElement('span'); time.className = 'hour-time';
      const parsed = new Date(hour.time);
      time.textContent = index === 0 ? 'Now' : new Intl.DateTimeFormat(undefined, { hour: 'numeric' }).format(parsed);
      const icon = document.createElement('span'); icon.className = 'hour-icon'; icon.setAttribute('aria-hidden', 'true'); icon.textContent = iconFor(hour.condition);
      const temperature = document.createElement('strong'); temperature.className = 'hour-temperature'; temperature.textContent = `${Math.round(hour.temperature)}°`;
      const rain = document.createElement('span'); rain.className = 'hour-rain'; rain.textContent = `☂ ${Math.round(hour.precipitation_probability || 0)}%`;
      card.append(time, icon, temperature, rain); hourlyGrid.append(card);
    });

    status.hidden = true;
    status.classList.remove('is-error');
    currentCard.hidden = false;
    hourlySection.hidden = !data.hourly || data.hourly.length === 0;
    forecastSection.hidden = false;
  }

  async function fetchWeather(url, label) {
    button.disabled = true;
    locationButton.disabled = true;
    button.innerHTML = '<span class="button-spinner" aria-hidden="true"></span> Loading';
    status.textContent = `Finding the forecast for ${label}…`;
    status.classList.remove('is-error');
    status.hidden = false;
    currentCard.hidden = true;
    forecastSection.hidden = true;
    hourlySection.hidden = true;
    try {
      const response = await fetch(url);
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Unable to load weather right now.');
      renderWeather(data);
      if (data.city !== 'Your location') input.value = data.city;
    } catch (error) {
      showError(error.message || 'Something went wrong. Please try another city.');
    } finally {
      button.disabled = false;
      locationButton.disabled = false;
      button.innerHTML = 'Search <span aria-hidden="true">→</span>';
    }
  }

  function loadWeather(city) {
    const query = city.trim();
    if (!query) return;
    fetchWeather(`/api/weather?city=${encodeURIComponent(query)}`, query);
  }

  form.addEventListener('submit', (event) => { event.preventDefault(); loadWeather(input.value); });

  locationButton.addEventListener('click', () => {
    if (!navigator.geolocation) {
      showError('Location is not available in this browser. You can search for a city instead.');
      return;
    }
    status.textContent = 'Requesting your location…';
    status.hidden = false;
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => fetchWeather(`/api/weather?latitude=${encodeURIComponent(coords.latitude)}&longitude=${encodeURIComponent(coords.longitude)}`, 'your location'),
      (error) => {
        const message = error.code === error.PERMISSION_DENIED
          ? 'Location permission was denied. Search for a city to see its weather.'
          : 'Could not determine your location. Please search for a city instead.';
        showError(message);
      },
      { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 },
    );
  });

  saveCurrentCityButton.addEventListener('click', saveCurrentCity);
  themeToggle.addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'light' ? 'dark' : 'light'));

  let savedTheme = 'dark';
  try { savedTheme = localStorage.getItem('weather-theme') || 'dark'; } catch (_) {}
  setTheme(savedTheme);
  renderFavorites();
  loadWeather(input.value || 'San Francisco');
})();
