async function fetchDashboard() {
  const metricsResponse = await fetch('/metrics');
  const alertsResponse = await fetch('/alerts');
  const incidentsResponse = await fetch('/incidents');

  const metrics = await metricsResponse.json();
  const alerts = await alertsResponse.json();
  const incidents = await incidentsResponse.json();

  renderSummary(metrics.summary);
  renderServices(metrics.services);
  renderAlerts(alerts);
  renderIncidents(incidents);
}

function renderSummary(summary) {
  const cards = [
    { label: 'Healthy', value: summary.healthy_services, trend: '+12% vs last hour' },
    { label: 'Warnings', value: summary.warning_services, trend: '3 services trending up' },
    { label: 'Critical', value: summary.critical_services, trend: '1 service needs review' },
    { label: 'MTTR', value: '19m', trend: 'down from 24m' },
  ];

  const container = document.getElementById('summary-grid');
  container.innerHTML = cards
    .map(
      (card) => `
        <div class="stat-card">
          <div class="label">${card.label}</div>
          <div class="value">${card.value}</div>
          <div class="trend">${card.trend}</div>
        </div>
      `
    )
    .join('');
}

function renderServices(services) {
  const container = document.getElementById('services-table');
  container.innerHTML = `
    <table class="service-table">
      <thead>
        <tr>
          <th>Service</th>
          <th>Latency</th>
          <th>Error</th>
          <th>Throughput</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        ${services
          .map(
            (service) => `
              <tr>
                <td>${service.name}</td>
                <td>${service.latency_ms} ms</td>
                <td>${service.error_rate * 100}%</td>
                <td>${service.throughput}</td>
                <td><span class="status-pill status-${service.status}">${service.status}</span></td>
              </tr>
            `
          )
          .join('')}
      </tbody>
    </table>
  `;
}

function renderAlerts(alerts) {
  const container = document.getElementById('alerts-list');
  container.innerHTML = alerts
    .map(
      (alert) => `
        <div class="alert-item">
          <div class="alert-meta">
            <strong>${alert.service}</strong>
            <span>${alert.message}</span>
          </div>
          <span class="${alert.severity === 'high' ? 'red-dot' : alert.severity === 'medium' ? 'orange-dot' : 'green-dot'}"></span>
        </div>
      `
    )
    .join('');
}

function renderIncidents(incidents) {
  const container = document.getElementById('incidents-list');
  container.innerHTML = incidents
    .map(
      (incident) => `
        <div class="incident-item">
          <div class="incident-meta">
            <strong>${incident.id} · ${incident.service}</strong>
            <span>${incident.summary}</span>
          </div>
          <span class="status-pill status-${incident.status === 'Investigating' ? 'critical' : 'warning'}">${incident.status}</span>
        </div>
      `
    )
    .join('');
}

fetchDashboard();
