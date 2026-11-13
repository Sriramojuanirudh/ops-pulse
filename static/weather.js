(() => {
  const form = document.getElementById('city-form');
  const input = document.getElementById('city-input');
  const button = document.getElementById('search-button');
  const status = document.getElementById('status-message');
  const currentCard = document.getElementById('current-weather');
  const forecastSection = document.getElementById('forecast-section');
  const forecastGrid = document.getElementById('forecast-grid');
  const weatherIcons = {
    clear: '☀',
    partly: '⛅',
    cloudy: '☁',
    fog: '〰',
    rain: '☂',
    snow: '❄',
    storm: 'ϟ',
  };

  function iconFor(condition) {
    const text = condition.toLowerCase();
    if (text.includes('thunder')) return weatherIcons.storm;
    if (text.includes('snow') || text.includes('ice') || text.includes('freezing')) return weatherIcons.snow;
    if (text.includes('rain') || text.includes('drizzle') || text.includes('shower')) return weatherIcons.rain;
    if (text.includes('fog')) return weatherIcons.fog;
    if (text.includes('overcast')) return weatherIcons.cloudy;
    if (text.includes('cloud')) return weatherIcons.partly;
    return weatherIcons.clear;
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
  }

  function renderWeather(data) {
    const location = [data.city, data.country].filter(Boolean).join(', ');
    document.getElementById('location-name').textContent = location;
    document.getElementById('today-label').textContent = new Intl.DateTimeFormat(undefined, {
      weekday: 'long', month: 'long', day: 'numeric',
    }).format(new Date());
    document.getElementById('current-icon').textContent = iconFor(data.condition);
    document.getElementById('temperature').textContent = Math.round(data.temperature);
    document.getElementById('condition').textContent = data.condition;
    document.getElementById('feels-like').textContent = Math.round(data.feels_like);
    document.getElementById('humidity').textContent = Math.round(data.humidity);
    document.getElementById('wind-speed').textContent = Math.round(data.wind_speed);
    document.getElementById('coordinates').textContent = `${Number(data.latitude).toFixed(2)}°, ${Number(data.longitude).toFixed(2)}°`;

    forecastGrid.replaceChildren();
    data.daily.forEach((day, index) => {
      const card = document.createElement('article');
      card.className = `forecast-day${index === 0 ? ' is-today' : ''}`;
      const label = document.createElement('p');
      label.className = 'forecast-day-name';
      label.textContent = dayName(day.date, index);
      const icon = document.createElement('span');
      icon.className = 'forecast-icon';
      icon.setAttribute('aria-hidden', 'true');
      icon.textContent = iconFor(day.condition);
      const condition = document.createElement('p');
      condition.className = 'forecast-condition';
      condition.textContent = day.condition;
      const range = document.createElement('p');
      range.className = 'temperature-range';
      const high = document.createElement('strong');
      high.textContent = `${Math.round(day.high)}°`;
      const low = document.createElement('span');
      low.textContent = `${Math.round(day.low)}°`;
      range.append(high, low);
      card.append(label, icon, condition, range);
      forecastGrid.append(card);
    });

    status.hidden = true;
    status.classList.remove('is-error');
    currentCard.hidden = false;
    forecastSection.hidden = false;
  }

  async function loadWeather(city) {
    const query = city.trim();
    if (!query) return;
    button.disabled = true;
    button.innerHTML = '<span class="button-spinner" aria-hidden="true"></span> Loading';
    status.textContent = `Finding the forecast for ${query}…`;
    status.classList.remove('is-error');
    status.hidden = false;
    currentCard.hidden = true;
    forecastSection.hidden = true;

    try {
      const response = await fetch(`/api/weather?city=${encodeURIComponent(query)}`);
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Unable to load weather right now.');
      renderWeather(data);
      input.value = data.city;
    } catch (error) {
      showError(error.message || 'Something went wrong. Please try another city.');
    } finally {
      button.disabled = false;
      button.innerHTML = 'Search <span aria-hidden="true">→</span>';
    }
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    loadWeather(input.value);
  });

  loadWeather(input.value || 'San Francisco');
})();
