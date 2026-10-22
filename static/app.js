* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Inter, Arial, sans-serif;
  background: #07111f;
  color: #e6edf7;
}

.app-shell {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100vh;
}

.sidebar {
  background: #0d1b2a;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  padding: 28px 18px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 30px;
}

.logo {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #3ba0ff, #6f5ef7);
  font-weight: 700;
  color: white;
}

.brand h1 {
  font-size: 1.2rem;
  margin: 0;
}

.brand p {
  margin: 4px 0 0;
  color: #8aa4c3;
  font-size: 0.75rem;
}

nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

nav a {
  text-decoration: none;
  color: #c6d6ef;
  padding: 10px 12px;
  border-radius: 10px;
  transition: 0.2s ease;
}

nav a.active,
nav a:hover {
  background: rgba(59, 160, 255, 0.12);
  color: #fff;
}

.main-panel {
  padding: 28px;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #70b8ff;
  font-size: 0.7rem;
  margin: 0 0 6px;
}

.topbar h2 {
  margin: 0;
  font-size: 2rem;
}

.primary-btn {
  background: linear-gradient(135deg, #42a5f5, #6f5ef7);
  border: none;
  color: white;
  padding: 12px 18px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(170px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: rgba(17, 30, 46, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  padding: 18px;
}

.stat-card .label {
  color: #8aa4c3;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.stat-card .value {
  font-size: 2rem;
  margin: 8px 0 4px;
  font-weight: 700;
}

.stat-card .trend {
  font-size: 0.82rem;
  color: #8de5b1;
}

.content-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.panel {
  background: rgba(17, 30, 46, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  padding: 18px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.panel-header h3 {
  margin: 0;
}

.panel-header span {
  color: #8aa4c3;
  font-size: 0.78rem;
}

.service-table {
  width: 100%;
  border-collapse: collapse;
}

.service-table th,
.service-table td {
  text-align: left;
  padding: 10px 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.service-table th {
  color: #8aa4c3;
  font-size: 0.74rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-pill {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
}

.status-healthy {
  background: rgba(76, 175, 80, 0.12);
  color: #87f2a1;
}

.status-warning {
  background: rgba(255, 193, 7, 0.12);
  color: #ffd166;
}

.status-critical {
  background: rgba(244, 67, 54, 0.12);
  color: #ff7b7b;
}

.alert-item,
.incident-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.alert-item:last-child,
.incident-item:last-child {
  border-bottom: none;
}

.alert-meta strong,
.incident-meta strong {
  display: block;
}

.alert-meta span,
.incident-meta span {
  color: #8aa4c3;
  font-size: 0.8rem;
}

.red-dot,
.orange-dot,
.green-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.red-dot { background: #ff6b6b; }
.orange-dot { background: #ffb703; }
.green-dot { background: #4cc9a7; }

@media (max-width: 920px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .sidebar {
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .content-grid,
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
