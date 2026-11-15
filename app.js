(function () {
  "use strict";

  const DATA = window.PROFILE_DATA || {};

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function safeUrl(raw) {
    if (!raw || typeof raw !== "string") return "";
    const trimmed = raw.trim();
    if (!trimmed) return "";
    if (/^(https?:\/\/|mailto:|\/|\.\/|assets\/)/i.test(trimmed)) {
      return trimmed;
    }
    return "";
  }

  function svgWrap(paths, viewBox = "0 0 24 24", size = 16, extraAttrs = "") {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="${viewBox}" fill="none" aria-hidden="true" ${extraAttrs}>${paths}</svg>`;
  }

  const UI_ICONS = {
    edit: svgWrap(
      `<path d="M12 20h9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>`,
      "0 0 24 24",
      15
    ),
    users: svgWrap(
      `<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="9" cy="7" r="4" stroke="currentColor" stroke-width="1.8"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>`,
      "0 0 24 24",
      15
    ),
    location: svgWrap(
      `<path d="M12 21s-6-5.33-6-10a6 6 0 1 1 12 0c0 4.67-6 10-6 10z" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="11" r="2.2" stroke="currentColor" stroke-width="1.8"/>`,
      "0 0 24 24",
      15
    ),
    link: svgWrap(
      `<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>`,
      "0 0 24 24",
      15
    ),
    linkedin: svgWrap(
      `<rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="1.8"/><path d="M8 11v5M8 8v.01M12 16v-5m0 2.5a2.5 2.5 0 0 1 5 0V16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>`,
      "0 0 24 24",
      15
    ),
    mail: svgWrap(
      `<rect x="3" y="5" width="18" height="14" rx="2.5" stroke="currentColor" stroke-width="1.8"/><path d="m4 7 8 6 8-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>`,
      "0 0 24 24",
      15
    ),
    github: svgWrap(
      `<path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.15-1.11-1.46-1.11-1.46-.91-.62.07-.61.07-.61 1 .07 1.53 1.03 1.53 1.03.9 1.53 2.35 1.09 2.92.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.95 0-1.09.39-1.99 1.03-2.69-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.03a9.5 9.5 0 0 1 5 0c1.91-1.3 2.75-1.03 2.75-1.03.55 1.38.2 2.4.1 2.65.64.7 1.03 1.6 1.03 2.69 0 3.85-2.34 4.7-4.57 4.94.36.31.68.92.68 1.85v2.75c0 .27.18.58.69.48A10 10 0 0 0 12 2z" fill="currentColor"/>`,
      "0 0 24 24",
      15
    ),
    wrench: svgWrap(
      `<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" fill="#38bdf8" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>`,
      "0 0 24 24",
      17
    ),
    rocket: svgWrap(
      `<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" fill="#f97316"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5" stroke-linejoin="round"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5" stroke="#ef4444" stroke-width="1.6" stroke-linecap="round"/>`,
      "0 0 24 24",
      17
    ),
    wave: svgWrap(
      `<path d="M7.5 11.5V6a1.5 1.5 0 0 1 3 0v4.5M10.5 10V4.5a1.5 1.5 0 0 1 3 0V10M13.5 10V5.5a1.5 1.5 0 0 1 3 0v6.5M16.5 10.5a1.5 1.5 0 0 1 3 0V14a6.5 6.5 0 0 1-13 0v-3.5a1.5 1.5 0 0 1 3 0" fill="#facc15" fill-opacity="0.7" stroke="#facc15" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 5.5c1-1.2 2.2-1.8 3.5-2M19.5 4.5c1 .8 1.8 1.9 2.2 3.2" stroke="#fde047" stroke-width="1.7" stroke-linecap="round"/>`,
      "0 0 24 24",
      20
    ),
    graduation: svgWrap(
      `<path d="M12 4 2 9l10 5 10-5-10-5z" fill="#60a5fa" fill-opacity="0.45" stroke="#60a5fa" stroke-width="1.8" stroke-linejoin="round"/><path d="M6 11.5v4.5c0 1.8 2.7 3.2 6 3.2s6-1.4 6-3.2v-4.5M21 10v5" stroke="#60a5fa" stroke-width="1.8" stroke-linecap="round"/>`,
      "0 0 24 24",
      17
    ),
    briefcase: svgWrap(
      `<rect x="3" y="7" width="18" height="13" rx="2.5" fill="#d97706" fill-opacity="0.35" stroke="#f59e0b" stroke-width="1.8"/><path d="M8.5 7V5A1.5 1.5 0 0 1 10 3.5h4A1.5 1.5 0 0 1 15.5 5v2M3 12h18" stroke="#f59e0b" stroke-width="1.8" stroke-linecap="round"/>`,
      "0 0 24 24",
      17
    ),
    target: svgWrap(
      `<circle cx="12" cy="12" r="8.5" fill="#f85149" fill-opacity="0.2" stroke="#f85149" stroke-width="1.8"/><circle cx="12" cy="12" r="4.5" stroke="#f85149" stroke-width="1.8"/><circle cx="12" cy="12" r="2" fill="#f85149"/>`,
      "0 0 24 24",
      17
    ),
    sparkles: svgWrap(
      `<path d="m12 3 1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9L12 3z" fill="#38bdf8" fill-opacity="0.35" stroke="#38bdf8" stroke-width="1.7" stroke-linejoin="round"/>`,
      "0 0 24 24",
      17
    ),
    brain: svgWrap(
      `<path d="M9.5 4.5A3.5 3.5 0 0 0 6 8c0 .4.1.8.2 1.2A3.2 3.2 0 0 0 4 12.2c0 1.3.8 2.4 2 2.9-.1.3-.2.7-.2 1.1a3.3 3.3 0 0 0 3.3 3.3c1.3 0 2.4-.7 2.9-1.8V5.8A3 3 0 0 0 9.5 4.5zm5 0A3.5 3.5 0 0 1 18 8c0 .4-.1.8-.2 1.2a3.2 3.2 0 0 1 2.2 3c0 1.3-.8 2.4-2 2.9.1.3.2.7.2 1.1a3.3 3.3 0 0 1-3.3 3.3c-1.3 0-2.4-.7-2.9-1.8V5.8a3 3 0 0 1 2.5-1.3z" fill="#f472b6" fill-opacity="0.45" stroke="#f472b6" stroke-width="1.7" stroke-linejoin="round"/>`,
      "0 0 24 24",
      20
    ),
    cpu: svgWrap(
      `<rect x="6" y="6" width="12" height="12" rx="2" stroke="#38bdf8" stroke-width="1.8"/><rect x="9.5" y="9.5" width="5" height="5" rx="0.8" fill="#38bdf8"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round"/>`,
      "0 0 24 24",
      17
    ),
    chat: svgWrap(
      `<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v7a2.5 2.5 0 0 1-2.5 2.5H10l-4.5 4v-4H6.5A2.5 2.5 0 0 1 4 13.5z" fill="#60a5fa" fill-opacity="0.22" stroke="#60a5fa" stroke-width="1.8" stroke-linejoin="round"/><circle cx="9" cy="10" r="1.1" fill="#60a5fa"/><circle cx="12" cy="10" r="1.1" fill="#60a5fa"/><circle cx="15" cy="10" r="1.1" fill="#60a5fa"/>`,
      "0 0 24 24",
      17
    ),
    gear: svgWrap(
      `<circle cx="12" cy="12" r="3.4" stroke="#7dd3fc" stroke-width="1.8"/><path d="M12 2.5v2.3M12 19.2v2.3M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6M2.5 12h2.3M19.2 12h2.3M4.9 19.1l1.6-1.6M17.5 6.5l1.6-1.6" stroke="#7dd3fc" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="12" r="6.8" stroke="#7dd3fc" stroke-width="1.4" stroke-opacity="0.65"/>`,
      "0 0 24 24",
      17
    ),
    database: svgWrap(
      `<ellipse cx="12" cy="6" rx="7.5" ry="3" fill="#22d3ee" fill-opacity="0.22" stroke="#22d3ee" stroke-width="1.8"/><path d="M4.5 6v12c0 1.66 3.36 3 7.5 3s7.5-1.34 7.5-3V6M4.5 12c0 1.66 3.36 3 7.5 3s7.5-1.34 7.5-3" stroke="#22d3ee" stroke-width="1.8"/>`,
      "0 0 24 24",
      17
    ),
    code: svgWrap(
      `<path d="m8 7-5 5 5 5M16 7l5 5-5 5M13.5 5l-3 14" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>`,
      "0 0 24 24",
      17
    ),
    shield: svgWrap(
      `<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.8 7.5 9.8 4.3-1 7.5-5.2 7.5-9.8V6L12 3z" fill="#38bdf8" fill-opacity="0.2" stroke="#38bdf8" stroke-width="1.8" stroke-linejoin="round"/>`,
      "0 0 24 24",
      17
    ),
    check: svgWrap(
      `<path d="M5 12.5 9.5 17 19 7.5" stroke="#3fb950" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>`,
      "0 0 24 24",
      13
    ),
    star: svgWrap(
      `<path d="m12 2.8 2.8 5.7 6.3.9-4.5 4.4 1.1 6.2-5.7-3-5.7 3 1.1-6.2-4.5-4.4 6.3-.9z" fill="#facc15"/>`,
      "0 0 24 24",
      19
    ),
    scales: svgWrap(
      `<path d="M12 3v17M7.5 20h9M5 7h14M5 7l-2.5 6h5L5 7zm14 0-2.5 6h5L19 7z" stroke="#38bdf8" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>`,
      "0 0 24 24",
      21
    ),
    k8s: svgWrap(
      `<path d="M12 3l7.8 3.8 1.9 8.4-5.4 6.6H7.7L2.3 15.2 4.2 6.8z" fill="#38bdf8" fill-opacity="0.22" stroke="#38bdf8" stroke-width="1.7" stroke-linejoin="round"/><circle cx="12" cy="12" r="3" stroke="#38bdf8" stroke-width="1.7"/><path d="M12 4.5V9M12 15v4.5M5.5 9l4 2M14.5 13l4 2M18.5 9l-4 2M9.5 13l-4 2" stroke="#38bdf8" stroke-width="1.5" stroke-linecap="round"/>`,
      "0 0 24 24",
      21
    ),
    phone: svgWrap(
      `<rect x="6.5" y="2.5" width="11" height="19" rx="2.3" fill="#38bdf8" fill-opacity="0.16" stroke="#38bdf8" stroke-width="1.7"/><path d="M10.5 5.5h3M11.5 18.5h1" stroke="#38bdf8" stroke-width="1.7" stroke-linecap="round"/><path d="M12 9.2v2.4m0 0a2.2 2.2 0 1 0 0 4.4 2.2 2.2 0 0 0 0-4.4z" stroke="#60a5fa" stroke-width="1.5" stroke-linecap="round"/>`,
      "0 0 24 24",
      21
    ),
    bot: svgWrap(
      `<rect x="4" y="7" width="16" height="12" rx="3" fill="#38bdf8" fill-opacity="0.18" stroke="#38bdf8" stroke-width="1.7"/><path d="M12 3v4M9 13h.01M15 13h.01M9.5 16h5" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round"/>`,
      "0 0 24 24",
      21
    ),
    layers: svgWrap(
      `<path d="m12 3 9 4.5-9 4.5-9-4.5L12 3z" fill="#38bdf8" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1.7" stroke-linejoin="round"/><path d="m3 12 9 4.5 9-4.5M3 16.5l9 4.5 9-4.5" stroke="#38bdf8" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>`,
      "0 0 24 24",
      21
    ),
    chart: svgWrap(
      `<rect x="3" y="13" width="4" height="8" rx="1" fill="#38bdf8"/><rect x="10" y="7" width="4" height="14" rx="1" fill="#3fb950"/><rect x="17" y="10" width="4" height="11" rx="1" fill="#a78bfa"/>`,
      "0 0 24 24",
      19
    ),
  };

  const TECH_ICONS = {
    python: svgWrap(
      `<path d="M12 3c-3 0-2.8 1.3-2.8 1.3V6h2.9v.7H8S5 6.4 5 10.6s2.6 4 2.6 4H9v-2s-.1-2.5 2.5-2.5h4s2.2.1 2.2-2.2V5.3S18 3 12 3zm-1.6 1.3a.7.7 0 1 1 0 1.4.7.7 0 0 1 0-1.4z" fill="#3b82f6"/><path d="M12 21c3 0 2.8-1.3 2.8-1.3V18h-2.9v-.7H16s3 .3 3-3.9-2.6-4-2.6-4H15v2s.1 2.5-2.5 2.5h-4s-2.2-.1-2.2 2.2v2.6S6 21 12 21zm1.6-1.3a.7.7 0 1 1 0-1.4.7.7 0 0 1 0 1.4z" fill="#facc15"/>`,
      "0 0 24 24",
      14
    ),
    go: svgWrap(
      `<circle cx="12" cy="12" r="9" fill="#00add8" fill-opacity="0.2" stroke="#00add8" stroke-width="1.8"/><text x="12" y="15.2" text-anchor="middle" fill="#38bdf8" font-size="9" font-weight="800" font-family="sans-serif">GO</text>`,
      "0 0 24 24",
      14
    ),
    rust: svgWrap(
      `<circle cx="12" cy="12" r="7" stroke="#fb923c" stroke-width="2" stroke-dasharray="3 2"/><circle cx="12" cy="12" r="3" fill="#fb923c"/>`,
      "0 0 24 24",
      14
    ),
    pytorch: svgWrap(
      `<path d="M15.8 7.2a5.8 5.8 0 1 1-7.6 0l1.6 1.6a3.6 3.6 0 1 0 4.4 0l1.6-1.6z" fill="#ee4c2c"/><circle cx="14.5" cy="5.5" r="1.4" fill="#ee4c2c"/>`,
      "0 0 24 24",
      14
    ),
    docker: svgWrap(
      `<path d="M4 13h16c0 4-3 7-8 7s-8-3-8-7z" fill="#2496ed"/><path d="M7 9h2v3H7zm3 0h2v3h-2zm3 0h2v3h-2zm-3-3h2v2.5h-2z" fill="#60a5fa"/>`,
      "0 0 24 24",
      14
    ),
    kubernetes: svgWrap(
      `<polygon points="12,3 19.8,7.2 21.5,15.5 16,21 8,21 2.5,15.5 4.2,7.2" fill="#326ce5" fill-opacity="0.28" stroke="#60a5fa" stroke-width="1.6"/><circle cx="12" cy="12" r="2.6" stroke="#93c5fd" stroke-width="1.6"/>`,
      "0 0 24 24",
      14
    ),
    airflow: svgWrap(
      `<path d="M12 12c0-4 3-7 7-7-1 4-3 7-7 7zm0 0c4 0 7 3 7 7-4-1-7-3-7-7zm0 0c0 4-3 7-7 7 1-4 3-7 7-7zm0 0c-4 0-7-3-7-7 4 1 7 3 7 7z" fill="#01cee3"/>`,
      "0 0 24 24",
      14
    ),
    mlflow: svgWrap(
      `<rect x="3" y="4" width="18" height="16" rx="4" fill="#0194e2" fill-opacity="0.24" stroke="#38bdf8" stroke-width="1.6"/><path d="M7.5 15V9l4.5 4.2L16.5 9v6" stroke="#7dd3fc" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>`,
      "0 0 24 24",
      14
    ),
    kserve: svgWrap(
      `<circle cx="12" cy="12" r="8.5" fill="#38bdf8" fill-opacity="0.2" stroke="#38bdf8" stroke-width="1.7"/><path d="M9.5 7.5v9M15 7.5 10.5 12 15 16.5" stroke="#bae6fd" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>`,
      "0 0 24 24",
      14
    ),
    fastapi: svgWrap(
      `<circle cx="12" cy="12" r="9" fill="#009688"/><path d="M13 6.5 8.5 13h3.2L11 17.5l4.8-6.5h-3.2L13 6.5z" fill="#ffffff"/>`,
      "0 0 24 24",
      14
    ),
    postgresql: svgWrap(
      `<ellipse cx="12" cy="10" rx="6.5" ry="6" fill="#336791" fill-opacity="0.38" stroke="#60a5fa" stroke-width="1.7"/><path d="M9 14v5M15 14v5M9 9.5h.01M15 9.5h.01" stroke="#93c5fd" stroke-width="1.7" stroke-linecap="round"/>`,
      "0 0 24 24",
      14
    ),
    qdrant: svgWrap(
      `<polygon points="12,3 20,7.5 20,16.5 12,21 4,16.5 4,7.5" fill="#dc244c" fill-opacity="0.25" stroke="#f43f5e" stroke-width="1.7"/><circle cx="12" cy="12" r="3" fill="#fb7185"/>`,
      "0 0 24 24",
      14
    ),
    minio: svgWrap(
      `<circle cx="12" cy="12" r="8.5" fill="#c72e49" fill-opacity="0.25" stroke="#fb7185" stroke-width="1.7"/><path d="M7.5 15V9.5l4.5 4 4.5-4V15" stroke="#fda4af" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>`,
      "0 0 24 24",
      14
    ),
    default: svgWrap(
      `<circle cx="12" cy="12" r="5" fill="#38bdf8"/>`,
      "0 0 24 24",
      12
    ),
  };

  function avatarPlaceholderSvg() {
    return `
      <svg class="avatar-svg-fallback" viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Profile avatar placeholder">
        <defs>
          <linearGradient id="avatarSky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#173256"/>
            <stop offset="60%" stop-color="#11223a"/>
            <stop offset="100%" stop-color="#0b1422"/>
          </linearGradient>
        </defs>
        <rect width="240" height="240" fill="url(#avatarSky)"/>
        <path d="M0 175 L55 130 L108 162 L162 118 L240 168 L240 240 L0 240 Z" fill="#132640" opacity="0.75"/>
        <circle cx="120" cy="96" r="36" fill="#28466f" stroke="#58a6ff" stroke-opacity="0.45" stroke-width="2"/>
        <path d="M56 212c8-36 33-54 64-54s56 18 64 54" fill="#1e385b" stroke="#58a6ff" stroke-opacity="0.4" stroke-width="2"/>
      </svg>`;
  }

  function mountainBgSvg() {
    return `
      <svg class="quote-mountain-bg" viewBox="0 0 220 90" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M0 90 L48 44 L84 68 L134 24 L178 62 L202 45 L220 64 L220 90 Z" fill="#1a273b"/>
        <path d="M38 90 L94 46 L132 72 L176 36 L220 74 L220 90 Z" fill="#131e2f"/>
      </svg>`;
  }

  function renderSectionHeader(iconHtml, title, rightLinkHtml = "") {
    return `
      <div class="section-header">
        <div class="section-title-group">
          <span class="section-icon">${iconHtml}</span>
          <h2 class="section-title">${escapeHtml(title)}</h2>
        </div>
        ${rightLinkHtml}
      </div>`;
  }

  function renderSidebar(sidebar) {
    const el = document.getElementById("profile-sidebar");
    if (!el || !sidebar) return;

    const avatarSrc = safeUrl(sidebar.avatarUrl);
    const avatarInner = avatarSrc
      ? `<img class="avatar-img" src="${escapeHtml(avatarSrc)}" alt="${escapeHtml(sidebar.name)}" />`
      : avatarPlaceholderSvg();

    const btnUrl = safeUrl(sidebar.actionButton && sidebar.actionButton.url);
    const btnLabel = (sidebar.actionButton && sidebar.actionButton.label) || "GitHub Profile";
    const actionBtnHtml = btnUrl
      ? `<a class="sidebar-action-btn" href="${escapeHtml(btnUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(btnLabel)}</a>`
      : `<div class="sidebar-action-btn">${escapeHtml(btnLabel)}</div>`;

    const detailsHtml = (sidebar.details || [])
      .map((item) => {
        const iconHtml = UI_ICONS[item.icon] || UI_ICONS.link;
        const link = safeUrl(item.url);
        const isExternal = /^https?:\/\//i.test(link);
        const textContent = link
          ? `<a class="detail-link" href="${escapeHtml(link)}"${
              isExternal ? ' target="_blank" rel="noopener noreferrer"' : ""
            }>${escapeHtml(item.label)}</a>`
          : `<span>${escapeHtml(item.label)}</span>`;
        return `<li class="detail-item"><span class="detail-icon">${iconHtml}</span>${textContent}</li>`;
      })
      .join("");

    const techHtml = (sidebar.techStack || [])
      .map((tech) => {
        const iconKey = String(tech.icon || "").toLowerCase();
        const iconHtml = TECH_ICONS[iconKey] || TECH_ICONS.default;
        return `<span class="tech-pill">${iconHtml}<span>${escapeHtml(tech.name)}</span></span>`;
      })
      .join("");

    const exploringHtml = (sidebar.exploring || [])
      .map(
        (topic) =>
          `<li class="exploring-item"><span class="exploring-dot"></span><span>${escapeHtml(
            topic
          )}</span></li>`
      )
      .join("");

    el.innerHTML = `
      <div class="avatar-wrapper">
        <div class="avatar-frame">${avatarInner}</div>
        <span class="avatar-status-badge" title="${escapeHtml(
          sidebar.avatarStatusTooltip || ""
        )}">${UI_ICONS.edit}</span>
      </div>

      <h1 class="sidebar-name">${escapeHtml(sidebar.name)}</h1>
      <p class="sidebar-username">${escapeHtml(sidebar.username)}</p>
      <p class="sidebar-headline">${escapeHtml(sidebar.headline)}</p>
      <p class="sidebar-bio">${escapeHtml(sidebar.bio)}</p>

      ${actionBtnHtml}

      <div class="follow-row">
        <span class="detail-icon">${UI_ICONS.users}</span>
        <span><strong>${Number(sidebar.followers || 0)}</strong> followers &middot; <strong>${Number(
      sidebar.following || 0
    )}</strong> following</span>
      </div>

      <ul class="details-list">${detailsHtml}</ul>

      <hr class="sidebar-divider" />

      <section>
        <h2 class="sidebar-section-title">${UI_ICONS.wrench}<span>${escapeHtml(
      sidebar.techStackTitle || "Tech Stack"
    )}</span></h2>
        <div class="tech-pills">${techHtml}</div>
      </section>

      <section class="exploring-block">
        <h2 class="sidebar-section-title">${UI_ICONS.rocket}<span>${escapeHtml(
      sidebar.exploringTitle || "Currently Exploring"
    )}</span></h2>
        <ul class="exploring-list">${exploringHtml}</ul>
      </section>
    `;
  }

  function renderBanner(banner) {
    if (!banner) return "";
    const src = safeUrl(banner.image) || "assets/profile-banner.png";
    const overlay =
      banner.overlayText && banner.overlayText.enabled
        ? `<div class="banner-overlay">
             <p class="banner-overlay-title">${escapeHtml(banner.overlayText.title)}</p>
             <p class="banner-overlay-subtitle">${escapeHtml(banner.overlayText.subtitle)}</p>
           </div>`
        : "";

    return `
      <section class="banner-card">
        <img class="banner-img" src="${escapeHtml(src)}" alt="${escapeHtml(
      banner.alt || "Profile Banner"
    )}" />
        ${overlay}
      </section>`;
  }

  function renderAbout(about) {
    if (!about) return "";
    const highlightsHtml = (about.highlights || [])
      .map((item) => {
        const iconHtml = UI_ICONS[item.icon] || UI_ICONS.sparkles;
        return `
          <div class="highlight-item">
            <span class="highlight-icon">${iconHtml}</span>
            <span><span class="highlight-label">${escapeHtml(
              item.label
            )}</span>${escapeHtml(item.value)}</span>
          </div>`;
      })
      .join("");

    return `
      <section>
        ${renderSectionHeader(UI_ICONS.wave, about.title || "About Me")}
        <div class="about-grid">
          <p class="about-description">${escapeHtml(about.description)}</p>
          <div class="about-highlights">${highlightsHtml}</div>
        </div>
      </section>`;
  }

  function renderExpertise(expertise) {
    if (!expertise) return "";
    const cardsHtml = (expertise.cards || [])
      .map((card) => {
        const iconHtml = UI_ICONS[card.icon] || UI_ICONS.cpu;
        const itemsHtml = (card.items || [])
          .map((line) => `<li>${UI_ICONS.check}<span>${escapeHtml(line)}</span></li>`)
          .join("");
        return `
          <article class="expertise-card">
            <div class="expertise-card-top">
              <div class="expertise-icon-box">${iconHtml}</div>
              <h3 class="expertise-card-title">${escapeHtml(card.title)}</h3>
            </div>
            <hr class="expertise-divider" />
            <ul class="expertise-list">${itemsHtml}</ul>
          </article>`;
      })
      .join("");

    return `
      <section>
        ${renderSectionHeader(UI_ICONS.brain, expertise.title || "Core Expertise")}
        <div class="expertise-grid">${cardsHtml}</div>
      </section>`;
  }

  function renderExperienceAndProjects(experience, projects) {
    const expItemsHtml = ((experience && experience.items) || [])
      .map(
        (item) => `
        <div class="timeline-item">
          <span class="timeline-dot" aria-hidden="true"></span>
          <div class="timeline-head">
            <h3 class="timeline-role">${escapeHtml(item.role)}</h3>
            <span class="timeline-period">${escapeHtml(item.period)}</span>
          </div>
          <p class="timeline-summary">${escapeHtml(item.summary)}</p>
        </div>`
      )
      .join("");

    const projViewAllUrl = safeUrl(projects && projects.viewAllUrl);
    const viewAllHtml =
      projects && projects.viewAllLabel && projViewAllUrl
        ? `<a class="section-link" href="${escapeHtml(
            projViewAllUrl
          )}" target="_blank" rel="noopener noreferrer">${escapeHtml(
            projects.viewAllLabel
          )}</a>`
        : "";

    const projCardsHtml = ((projects && projects.items) || [])
      .map((proj) => {
        const iconHtml = UI_ICONS[proj.icon] || UI_ICONS.code;
        const projUrl = safeUrl(proj.url);
        const tagsHtml = (proj.tags || [])
          .map((tag) => {
            const dot = tag.dotColor
              ? `<span class="project-tag-dot" style="background:${escapeHtml(
                  tag.dotColor
                )}"></span>`
              : "";
            return `<span class="project-tag">${dot}${escapeHtml(tag.label)}</span>`;
          })
          .join("");

        const tagOpen = projUrl
          ? `<a class="project-card" href="${escapeHtml(
              projUrl
            )}" target="_blank" rel="noopener noreferrer">`
          : `<article class="project-card">`;
        const tagClose = projUrl ? `</a>` : `</article>`;

        return `
          ${tagOpen}
            <div class="project-icon-box">${iconHtml}</div>
            <h3 class="project-title">${escapeHtml(proj.title)}</h3>
            <p class="project-desc">${escapeHtml(proj.description)}</p>
            <div class="project-tags">${tagsHtml}</div>
          ${tagClose}`;
      })
      .join("");

    return `
      <section class="exp-proj-grid">
        <div>
          ${renderSectionHeader(
            UI_ICONS.briefcase,
            (experience && experience.title) || "Professional Experience"
          )}
          <div class="timeline">${expItemsHtml}</div>
        </div>
        <div>
          ${renderSectionHeader(
            UI_ICONS.star,
            (projects && projects.title) || "Featured Projects",
            viewAllHtml
          )}
          <div class="projects-grid">${projCardsHtml}</div>
        </div>
      </section>`;
  }

  function generateSeededHeatmap(rows, cols, totalContributions) {
    let seed = Number(totalContributions) || 233;
    function nextRand() {
      seed = (seed * 1664525 + 1013904223) >>> 0;
      return seed / 4294967296;
    }

    const matrix = [];
    for (let r = 0; r < rows; r++) {
      const row = [];
      for (let c = 0; c < cols; c++) {
        const wave = 0.25 + 0.45 * Math.sin(c * 0.48 + r * 0.6) ** 2;
        const v = nextRand() * 0.75 + wave * 0.45;
        let level = 0;
        if (v > 0.98) level = 4;
        else if (v > 0.78) level = 3;
        else if (v > 0.56) level = 2;
        else if (v > 0.36) level = 1;
        row.push(level);
      }
      matrix.push(row);
    }
    return matrix;
  }

  function renderHeatmapCells(stats) {
    const matrix =
      Array.isArray(stats.customHeatmap) && stats.customHeatmap.length > 0
        ? stats.customHeatmap
        : generateSeededHeatmap(5, 23, stats.totalContributions);

    const cols = matrix[0] ? matrix[0].length : 23;
    const months = stats.months || [];
    const cellsHtml = [];

    for (let r = 0; r < matrix.length; r++) {
      for (let c = 0; c < cols; c++) {
        const rawLevel = Number(matrix[r][c] || 0);
        const level = Math.max(0, Math.min(4, Math.round(rawLevel)));
        const monthIdx = Math.min(
          months.length - 1,
          Math.floor((c / cols) * months.length)
        );
        const monthLabel = months[monthIdx] || "";
        const label =
          level === 0
            ? `No contributions (${monthLabel})`
            : `${level * 2} contributions (${monthLabel})`;
        cellsHtml.push(
          `<span class="heatmap-cell level-${level}" title="${escapeHtml(label)}"></span>`
        );
      }
    }

    return { cols, cellsHtml: cellsHtml.join("") };
  }

  function buildDonutMarkup(languages) {
    const items = (languages || []).filter((l) => Number(l.percentage) > 0);
    const total = items.reduce((acc, cur) => acc + Number(cur.percentage), 0) || 100;
    const radius = 31;
    const circumference = 2 * Math.PI * radius;
    const gap = items.length > 1 ? 2.5 : 0;

    let offset = 0;
    const circles = items
      .map((lang, idx) => {
        const share = Number(lang.percentage) / total;
        const arcLen = Math.max(0, share * circumference - gap);
        const strokeColor = lang.arcColor || lang.color || "#38bdf8";
        const circle = `<circle
          class="donut-segment"
          data-lang-idx="${idx}"
          cx="41"
          cy="41"
          r="${radius}"
          fill="transparent"
          stroke="${escapeHtml(strokeColor)}"
          stroke-width="11"
          stroke-dasharray="${arcLen.toFixed(2)} ${(circumference - arcLen).toFixed(2)}"
          stroke-dashoffset="${(-offset).toFixed(2)}"
        />`;
        offset += share * circumference;
        return circle;
      })
      .join("");

    const primary = items[0] || { name: "", percentage: 0 };
    const legendHtml = items
      .map((lang, idx) => {
        const dotColor = lang.arcColor || lang.color || "#38bdf8";
        return `
          <li class="lang-legend-item" data-lang-idx="${idx}">
            <span class="lang-name-wrap">
              <span class="lang-dot" style="background:${escapeHtml(dotColor)}"></span>
              <span>${escapeHtml(lang.name)}</span>
            </span>
            <span class="lang-pct">${Number(lang.percentage).toFixed(1)}%</span>
          </li>`;
      })
      .join("");

    return `
      <div class="lang-body">
        <div class="donut-wrap">
          <svg class="donut-svg" viewBox="0 0 82 82" role="img" aria-label="Top Languages Donut Chart">
            <circle cx="41" cy="41" r="${radius}" fill="transparent" stroke="#182233" stroke-width="11"/>
            ${circles}
          </svg>
          <div class="donut-center-text">
            <span class="donut-center-pct" id="donut-center-pct">${Number(
              primary.percentage
            ).toFixed(1)}%</span>
            <span class="donut-center-name" id="donut-center-name">${escapeHtml(
              primary.name
            )}</span>
          </div>
        </div>
        <ul class="lang-legend">${legendHtml}</ul>
      </div>`;
  }

  function formatQuoteWithEmoji(text, emoji) {
    const cleanText = String(text || "").trim();
    const cleanEmoji = String(emoji || "").trim();
    if (!cleanEmoji) return escapeHtml(cleanText);
    const parts = cleanText.split(/\s+/);
    if (parts.length === 0 || !cleanText) return escapeHtml(cleanEmoji);
    const lastWord = parts.pop();
    const prefix = parts.length > 0 ? `${escapeHtml(parts.join(" "))} ` : "";
    return `${prefix}<span style="white-space:nowrap">${escapeHtml(lastWord)} ${escapeHtml(
      cleanEmoji
    )}</span>`;
  }

  function renderStatsAndQuote(stats, quote) {
    const s = stats || {};
    const q = quote || {};
    const monthsHtml = (s.months || [])
      .map((m) => `<span>${escapeHtml(m)}</span>`)
      .join("");
    const heatmap = renderHeatmapCells(s);

    return `
      <section>
        ${renderSectionHeader(UI_ICONS.chart, s.title || "GitHub Stats")}
        <div class="stats-row">
          <div class="stats-card contrib-card">
            <div class="contrib-summary">
              <div class="contrib-label">${escapeHtml(
                s.contributionLabel || "Total Contributions"
              )}</div>
              <div class="contrib-total">${escapeHtml(s.totalContributions ?? 0)}</div>
              <div class="contrib-period">${escapeHtml(
                s.contributionPeriod || "in the last year"
              )}</div>
            </div>
            <div class="heatmap-wrap">
              <div class="heatmap-months">${monthsHtml}</div>
              <div class="heatmap-grid" style="--heatmap-cols:${heatmap.cols}">
                ${heatmap.cellsHtml}
              </div>
              <div class="heatmap-legend">
                <span>Less</span>
                <span class="legend-box heatmap-cell level-0"></span>
                <span class="legend-box heatmap-cell level-1"></span>
                <span class="legend-box heatmap-cell level-2"></span>
                <span class="legend-box heatmap-cell level-3"></span>
                <span class="legend-box heatmap-cell level-4"></span>
                <span>More</span>
              </div>
            </div>
          </div>

          <div class="stats-card lang-card">
            <h3 class="lang-card-title">${escapeHtml(
              s.topLanguagesTitle || "Top Languages"
            )}</h3>
            <div id="top-languages-container">${buildDonutMarkup(s.languages)}</div>
          </div>

          <div class="quote-panel">
            <p class="quote-text">${formatQuoteWithEmoji(q.text, q.emoji)}</p>
            ${mountainBgSvg()}
          </div>
        </div>
      </section>`;
  }

  function bindDonutInteractions(languages) {
    const container = document.getElementById("top-languages-container");
    if (!container || !Array.isArray(languages) || languages.length === 0) return;

    const pctEl = document.getElementById("donut-center-pct");
    const nameEl = document.getElementById("donut-center-name");
    const segments = container.querySelectorAll(".donut-segment");
    const legendItems = container.querySelectorAll(".lang-legend-item");

    function highlight(idx) {
      const target = languages[idx] || languages[0];
      if (pctEl) pctEl.textContent = `${Number(target.percentage).toFixed(1)}%`;
      if (nameEl) nameEl.textContent = target.name;
      segments.forEach((seg) => {
        const segIdx = Number(seg.getAttribute("data-lang-idx"));
        seg.style.opacity = segIdx === idx ? "1" : "0.45";
      });
    }

    function reset() {
      const primary = languages[0];
      if (pctEl) pctEl.textContent = `${Number(primary.percentage).toFixed(1)}%`;
      if (nameEl) nameEl.textContent = primary.name;
      segments.forEach((seg) => {
        seg.style.opacity = "1";
      });
    }

    segments.forEach((seg) => {
      const idx = Number(seg.getAttribute("data-lang-idx"));
      seg.addEventListener("mouseenter", () => highlight(idx));
      seg.addEventListener("mouseleave", reset);
    });

    legendItems.forEach((item) => {
      const idx = Number(item.getAttribute("data-lang-idx"));
      item.addEventListener("mouseenter", () => highlight(idx));
      item.addEventListener("mouseleave", reset);
    });
  }

  async function maybeHydrateLiveLanguages(stats) {
    if (!stats || !stats.liveLanguagesFromGitHub || !stats.githubUsername) return;
    try {
      const url = `https://api.github.com/users/${encodeURIComponent(
        stats.githubUsername
      )}/repos?per_page=100&type=owner`;
      const res = await fetch(url);
      if (!res.ok) return;
      const repos = await res.json();
      if (!Array.isArray(repos)) return;

      const counts = {};
      let total = 0;
      repos.forEach((repo) => {
        if (!repo.fork && repo.language) {
          counts[repo.language] = (counts[repo.language] || 0) + 1;
          total += 1;
        }
      });
      if (total === 0) return;

      const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
      const palette = ["#facc15", "#38bdf8", "#64748b"];
      const topTwo = sorted.slice(0, 2).map(([name, count], idx) => ({
        name,
        percentage: Number(((count / total) * 100).toFixed(1)),
        color: palette[idx],
        arcColor: palette[idx],
      }));
      const restPct = Number(
        Math.max(0, 100 - topTwo.reduce((sum, item) => sum + item.percentage, 0)).toFixed(1)
      );
      const merged =
        restPct > 0
          ? [...topTwo, { name: "Other", percentage: restPct, color: palette[2], arcColor: palette[2] }]
          : topTwo;

      const container = document.getElementById("top-languages-container");
      if (container) {
        container.innerHTML = buildDonutMarkup(merged);
        bindDonutInteractions(merged);
      }
    } catch (_) {
      // Keep configured static languages on offline/rate-limit errors
    }
  }

  function init() {
    if (DATA.pageTitle) {
      document.title = DATA.pageTitle;
    }

    renderSidebar(DATA.sidebar);

    const mainEl = document.getElementById("profile-main");
    if (mainEl) {
      mainEl.innerHTML = [
        renderBanner(DATA.banner),
        renderAbout(DATA.about),
        renderExpertise(DATA.expertise),
        renderExperienceAndProjects(DATA.experience, DATA.projects),
        renderStatsAndQuote(DATA.stats, DATA.quote),
      ].join("");
    }

    if (DATA.stats && Array.isArray(DATA.stats.languages)) {
      bindDonutInteractions(DATA.stats.languages);
      maybeHydrateLiveLanguages(DATA.stats);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
