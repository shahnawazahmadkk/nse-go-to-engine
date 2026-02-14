let DATA = null;
let currentTab = "short_term";

function safeNum(x) {
  if (x === null || x === undefined) return -999999;
  if (typeof x === "number") return x;
  const n = Number(x);
  return Number.isFinite(n) ? n : -999999;
}

function tradingViewUrl(ticker) {
  // yfinance tickers look like RELIANCE.NS
  // TradingView uses NSE:RELIANCE
  if (!ticker) return "https://www.tradingview.com/";
  const base = ticker.replace(".NS", "").replace(".BO", "");
  return "https://www.tradingview.com/chart/?symbol=NSE:" + encodeURIComponent(base);
}

function renderTable(rows) {
  const wrap = document.getElementById("tableWrap");

  if (!rows || rows.length === 0) {
    wrap.innerHTML = `<div style="padding:18px;color:#9fb0d0">No signals found in this bucket today.</div>`;
    return;
  }

  let html = `
    <table>
      <thead>
        <tr>
          <th>Ticker</th>
          <th>Price</th>
          <th>Decision</th>
          <th>Score</th>
          <th>Stoploss</th>
          <th>Target</th>
          <th>RR</th>
          <th>RSI</th>
          <th>ADX</th>
          <th>VolRatio</th>
          <th>Chart</th>
        </tr>
      </thead>
      <tbody>
  `;

  for (const r of rows) {
    html += `
      <tr>
        <td><b>${r.Ticker}</b></td>
        <td>${r.Price ?? ""}</td>
        <td><span class="badge">${r.Decision}</span></td>
        <td><b>${r.Score}</b></td>
        <td>${r.Stoploss ?? ""}</td>
        <td>${r.Target ?? ""}</td>
        <td>${r.RR ?? ""}</td>
        <td>${r.RSI ?? ""}</td>
        <td>${r.ADX ?? ""}</td>
        <td>${r.VolRatio ?? ""}</td>
        <td><a class="tvbtn" href="${tradingViewUrl(r.Ticker)}" target="_blank" rel="noopener">TradingView</a></td>
      </tr>
    `;
  }

  html += `</tbody></table>`;
  wrap.innerHTML = html;
}



function updateUI() {
  const rows = getActiveRows();
  renderTable(rows);
}

async function loadSignals() {
  const marketRegime = document.getElementById("marketRegime");
  const updatedAt = document.getElementById("updatedAt");

  marketRegime.textContent = "Loading...";
  updatedAt.textContent = "Loading...";

  const res = await fetch("signals.json?v=" + Date.now());
  DATA = await res.json();

  marketRegime.textContent = DATA.market_regime || "UNKNOWN";
  updatedAt.textContent = DATA.updated_at_utc || "Unknown";

  updateConfidenceBadge();
  updateUI();
}

function initTabs() {
  document.querySelectorAll(".tab").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
      btn.classList.add("active");
      currentTab = btn.dataset.tab;
      updateConfidenceBadge();
  updateUI();
    });
  });
}

function initControls() {
  document.getElementById("searchBox").addEventListener("input", updateUI);
  document.getElementById("sortBy").addEventListener("change", updateUI);
  document.getElementById("buyOnly").addEventListener("change", updateUI);
  document.getElementById("minScore").addEventListener("input", () => {
    document.getElementById("minScoreVal").textContent = document.getElementById("minScore").value;
    updateUI();
  });
  document.getElementById("copyTickers").addEventListener("click", copyTickers);
  document.getElementById("refreshBtn").addEventListener("click", loadSignals);
  document.getElementById("dlJson").addEventListener("click", downloadJson);
  document.getElementById("dlCsv").addEventListener("click", downloadCsv);
}

initTabs();
initControls();
if (document.getElementById('minScoreVal')) document.getElementById('minScoreVal').textContent = document.getElementById('minScore').value;
loadSignals();


function confidenceFromData() {
  if (!DATA) return { label: "Unknown", level: "UNKNOWN" };

  const regime = (DATA.market_regime || "").toUpperCase();
  const all = []
    .concat(DATA.short_term || [])
    .concat(DATA.swing || [])
    .concat(DATA.positional || []);

  if (all.length === 0) {
    return { label: regime === "BULL" ? "Medium" : "Low", level: "LOW" };
  }

  const scores = all.map(x => safeNum(x.Score)).filter(x => x > 0);
  const avg = scores.length ? (scores.reduce((a,b)=>a+b,0) / scores.length) : 0;

  // Simple confidence model:
  // - Bull regime increases confidence
  // - Higher average score increases confidence
  let points = 0;
  if (regime === "BULL") points += 2;
  if (avg >= 75) points += 2;
  else if (avg >= 65) points += 1;
  else points += 0;

  if (points >= 4) return { label: "High", level: "HIGH" };
  if (points >= 2) return { label: "Medium", level: "MEDIUM" };
  return { label: "Low", level: "LOW" };
}

function updateConfidenceBadge() {
  const el = document.getElementById("confidenceBadge");
  if (!el) return;

  const c = confidenceFromData();
  el.textContent = c.label;

  // Just subtle styling using existing badge class
  // (No colors hardcoded, keep minimal)
  el.setAttribute("data-level", c.level);
}

function getActiveRows() {
  if (!DATA) return [];

  const rows = DATA[currentTab] || [];

  const q = document.getElementById("searchBox").value.trim().toUpperCase();
  const buyOnly = document.getElementById("buyOnly")?.checked;
  const minScore = Number(document.getElementById("minScore")?.value || 0);

  let filtered = rows;

  if (buyOnly) {
    filtered = filtered.filter(r => (r.Decision || "") === "BUY");
  }

  filtered = filtered.filter(r => safeNum(r.Score) >= minScore);

  if (q.length > 0) {
    filtered = filtered.filter(r => (r.Ticker || "").toUpperCase().includes(q));
  }

  const sortBy = document.getElementById("sortBy").value;
  filtered.sort((a, b) => safeNum(b[sortBy]) - safeNum(a[sortBy]));

  return filtered;
}

function currentCsvFile() {
  if (currentTab === "short_term") return "nse_short_term_20.csv";
  if (currentTab === "swing") return "nse_swing_20.csv";
  return "nse_positional_20.csv";
}

function downloadText(filename, text) {
  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();

  URL.revokeObjectURL(url);
}

async function downloadJson() {
  if (!DATA) return;
  downloadText("signals.json", JSON.stringify(DATA, null, 2));
}

async function downloadCsv() {
  const file = currentCsvFile();
  const res = await fetch(file + "?v=" + Date.now());
  const text = await res.text();
  downloadText(file, text);
}


async function copyTickers() {
  const rows = getActiveRows();
  if (!rows || rows.length === 0) return;

  const txt = rows.map(r => r.Ticker).join("\n");
  try {
    await navigator.clipboard.writeText(txt);
    alert("Copied " + rows.length + " tickers to clipboard.");
  } catch (e) {
    // fallback
    downloadText("tickers.txt", txt);
  }
}
