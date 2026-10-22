* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Inter, Arial, sans-serif;
  background: linear-gradient(180deg, #050d18 0%, #0b1727 100%);
  color: #edf4ff;
}

.landing-body {
  min-height: 100vh;
}

.dashboard-body {
  min-height: 100vh;
  background: #07111f;
}

.landing-header {
  padding: 22px 6vw;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  background: rgba(7, 15, 25, 0.7);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 10;
}

.landing-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
}

.brand-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 700;
}

.logo {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: linear-gradient(135deg, #48b1ff, #7c67ff);
  color: white;
}

.nav-links {
  display: flex;
  gap: 28px;
}

.nav-links a {
  color: #e2ebff;
  text-decoration: none;
  font-size: 0.95rem;
  opacity: 0.8;
}

.nav-btn,
.primary-btn,
.secondary-btn {
  border: none;
  border-radius: 10px;
  padding: 12px 18px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.nav-btn,
.primary-btn {
  background: linear-gradient(135deg, #3ea8ff, #685df2);
  color: white;
}

.secondary-btn {
  background: rgba(255,255,255,0.04);
  color: #edf4ff;
  border: 1px solid rgba(255,255,255,0.08);
}

.hero {
  max-width: 1200px;
  margin: 0 auto;
  padding: 70px 6vw 50px;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 30px;
  align-items: center;
}

.tag {
  display: inline-block;
  padding: 8px 12px;
  background: rgba(73, 130, 255, 0.12);
  border: 1px solid rgba(110, 170, 255, 0.18);
  border-radius: 999px;
  color: #a9d0ff;
  letter-spacing: 0.12em;
  font-size: 0.72rem;
  margin-bottom: 18px;
}

.hero-copy h1 {
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  line-height: 1.02;
  margin: 0 0 18px;
}

.hero-copy p {
  max-width: 620px;
  font-size: 1.08rem;
  color: #c5d7f9;
  line-height: 1.7;
}

.cta-row {
  display: flex;
  gap: 14px;
  margin-top: 24px;
}

.mini-metrics {
  display: flex;
  gap: 22px;
  flex-wrap: wrap;
  margin-top: 28px;
}

.mini-metrics div {
  display: flex;
  flex-direction: column;
  min-width: 120px;
}

.mini-metrics strong {
  font-size: 1.7rem;
}

.mini-metrics span {
  color: #aebfe0;
  font-size: 0.8rem;
}

.hero-visual {
  display: flex;
  justify-content: center;
}

.graph-card {
  width: min(100%, 520px);
  background: rgba(10, 19, 31, 0.9);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 20px 60px rgba(16, 29, 47, 0.55);
}

.graph-header,
.graph-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.live-pill {
  background: rgba(93, 243, 176, 0.14);
  color: #75efb2;
  border-radius: 999px;
  padding: 6px 9px;
  font-size: 0.72rem;
}

.bars {
  height: 220px;
  display: flex;
  align-items: end;
  gap: 14px;
  margin: 26px 0;
  padding-top: 18px;
}

.bars span {
  display: block;
  flex: 1;
  border-radius: 12px 12px 0 0;
  background: linear-gradient(180deg, #7fd3ff 0%, #5e8bff 100%);
  min-height: 30px;
}

.graph-footer {
  gap: 12px;
}

.graph-footer div {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.graph-footer small {
  color: #a7bcec;
}

.info-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 6vw 80px;
}

.alt-bg {
  background: rgba(255,255,255,0.02);
}

.section-heading {
  margin-bottom: 24px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #9bc7ff;
  font-size: 0.72rem;
}

.section-heading h2 {
  font-size: clamp(2rem, 3vw, 3rem);
  margin: 8px 0 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(220px, 1fr));
  gap: 18px;
}

.feature-card {
  background: rgba(11, 21, 33, 0.72);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 18px;
  padding: 22px;
}

.feature-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
}

.feature-card p {
  color: #bfd2ef;
  line-height: 1.7;
  margin-bottom: 0;
}

.compact-grid {
  grid-template-columns: repeat(3, minmax(220px, 1fr));
}

.app-shell {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100vh;
}

.sidebar {
  background: #0d1b2a;
  border-right: 1px solid rgba(255,255,255,0.08);
  padding: 28px 18px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 30px;
}

.brand h1 {
  margin: 0;
  font-size: 1.2rem;
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

.topbar h2 {
  margin: 0;
  font-size: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(170px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: rgba(17, 30, 46, 0.8);
  border: 1px solid rgba(255,255,255,0.06);
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
  border: 1px solid rgba(255,255,255,0.06);
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
  border-bottom: 1px solid rgba(255,255,255,0.04);
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
  border-bottom: 1px solid rgba(255,255,255,0.05);
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

@media (max-width: 860px) {
  .landing-nav {
    flex-direction: column;
    gap: 18px;
  }

  .nav-links {
    gap: 14px;
    flex-wrap: wrap;
    justify-content: center;
  }

  .hero {
    grid-template-columns: 1fr;
  }

  .feature-grid,
  .stats-grid,
  .content-grid {
    grid-template-columns: 1fr;
  }

  .app-shell {
    grid-template-columns: 1fr;
  }

  .sidebar {
    border-right: none;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
}
