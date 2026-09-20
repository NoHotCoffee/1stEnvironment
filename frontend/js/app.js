if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {});
  });
}

const $ = (id) => document.getElementById(id);
const todayStr = () => new Date().toISOString().slice(0, 10);

/* ---------------- Auth screen ---------------- */

let authMode = "login";

function showAuthError(msg) {
  const el = $("auth-error");
  el.textContent = msg;
  el.classList.remove("hidden");
}

function initAuthScreen() {
  $("auth-toggle").addEventListener("click", () => {
    authMode = authMode === "login" ? "register" : "login";
    $("auth-submit").textContent = authMode === "login" ? "Log in" : "Create account";
    $("auth-toggle").textContent =
      authMode === "login" ? "Need an account? Register" : "Already have an account? Log in";
    $("auth-error").classList.add("hidden");
  });

  $("auth-submit").addEventListener("click", async () => {
    const email = $("auth-email").value.trim();
    const password = $("auth-password").value;
    $("auth-error").classList.add("hidden");

    if (!email || password.length < 8) {
      showAuthError("Enter an email and a password of at least 8 characters.");
      return;
    }

    try {
      if (authMode === "login") {
        await Api.login(email, password);
      } else {
        await Api.register(email, password);
      }
      await enterApp();
    } catch (err) {
      showAuthError(err.message);
    }
  });
}

function showAuthScreen() {
  $("auth-screen").classList.remove("hidden");
  $("app").classList.add("hidden");
}

/* ---------------- App shell / navigation ---------------- */

const VIEWS = ["dashboard", "add", "diary", "settings"];

function switchView(view) {
  VIEWS.forEach((v) => {
    $(`view-${v}`).classList.toggle("hidden", v !== view);
  });
  document.querySelectorAll(".nav-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.view === view);
  });
  const titles = { dashboard: "Today", add: "Add food", diary: "History", settings: "Settings" };
  $("page-title").textContent = titles[view];

  if (view === "dashboard") loadDashboard();
  if (view === "diary") loadDiaryForDate($("diary-date").value || todayStr());
  if (view === "settings") loadSettings();
}

function initNav() {
  document.querySelectorAll(".nav-btn").forEach((btn) => {
    btn.addEventListener("click", () => switchView(btn.dataset.view));
  });
}

async function enterApp() {
  $("auth-screen").classList.add("hidden");
  $("app").classList.remove("hidden");
  switchView("dashboard");
}

window.addEventListener("calbell:unauthorized", () => {
  showAuthScreen();
});

/* ---------------- Dashboard ---------------- */

function renderMacroBar(barId, textId, value, goal, unit) {
  const pct = goal > 0 ? Math.min(100, (value / goal) * 100) : 0;
  $(barId).style.width = `${pct}%`;
  $(textId).textContent = `${Math.round(value)} / ${Math.round(goal)}${unit}`;
}

function renderEntryList(listEl, emptyEl, entries, onDelete) {
  listEl.innerHTML = "";
  if (entries.length === 0) {
    emptyEl.classList.remove("hidden");
    return;
  }
  emptyEl.classList.add("hidden");

  entries.forEach((entry) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div>
        <div>${escapeHtml(entry.name)}</div>
        <div class="entry-meta">${entry.meal_type} &middot; ${Math.round(entry.serving_grams)}g</div>
      </div>
      <div style="display:flex;align-items:center;gap:10px;">
        <span class="entry-cal">${Math.round(entry.calories)} kcal</span>
        <button class="secondary" data-id="${entry.id}" style="padding:6px 10px;">✕</button>
      </div>
    `;
    li.querySelector("button").addEventListener("click", () => onDelete(entry.id));
    listEl.appendChild(li);
  });
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

async function loadDashboard() {
  try {
    const summary = await Api.getDiary(todayStr());
    $("dash-cal-total").textContent = Math.round(summary.total_calories);
    $("dash-cal-goal").textContent = Math.round(summary.calorie_goal);
    $("dash-cal-remaining").textContent = Math.round(
      Math.max(0, summary.calorie_goal - summary.total_calories)
    );
    const pct =
      summary.calorie_goal > 0
        ? Math.min(100, (summary.total_calories / summary.calorie_goal) * 100)
        : 0;
    $("dash-cal-bar").style.width = `${pct}%`;

    renderMacroBar("dash-protein-bar", "dash-protein-text", summary.total_protein_g, summary.protein_goal_g, "g");
    renderMacroBar("dash-carb-bar", "dash-carb-text", summary.total_carb_g, summary.carb_goal_g, "g");
    renderMacroBar("dash-fat-bar", "dash-fat-text", summary.total_fat_g, summary.fat_goal_g, "g");

    renderEntryList($("dash-entry-list"), $("dash-empty"), summary.entries, async (id) => {
      await Api.deleteEntry(id);
      loadDashboard();
    });
  } catch (err) {
    console.error(err);
  }
}

/* ---------------- Diary / history ---------------- */

function initDiaryView() {
  $("diary-date").value = todayStr();
  $("diary-date").addEventListener("change", (e) => loadDiaryForDate(e.target.value));
}

async function loadDiaryForDate(dateStr) {
  try {
    const summary = await Api.getDiary(dateStr);
    renderEntryList($("diary-entry-list"), $("diary-empty"), summary.entries, async (id) => {
      await Api.deleteEntry(id);
      loadDiaryForDate(dateStr);
    });
  } catch (err) {
    console.error(err);
  }
}

/* ---------------- Settings ---------------- */

async function loadSettings() {
  try {
    const me = await Api.me();
    $("goal-calories").value = me.calorie_goal;
    $("goal-protein").value = me.protein_goal_g;
    $("goal-carb").value = me.carb_goal_g;
    $("goal-fat").value = me.fat_goal_g;
    $("settings-email").textContent = me.email;
  } catch (err) {
    console.error(err);
  }
}

function initSettingsView() {
  $("goals-save").addEventListener("click", async () => {
    try {
      await Api.updateGoals({
        calorie_goal: Number($("goal-calories").value),
        protein_goal_g: Number($("goal-protein").value),
        carb_goal_g: Number($("goal-carb").value),
        fat_goal_g: Number($("goal-fat").value),
      });
      $("goals-saved").classList.remove("hidden");
      setTimeout(() => $("goals-saved").classList.add("hidden"), 1500);
    } catch (err) {
      alert(err.message);
    }
  });

  $("logout-btn").addEventListener("click", () => {
    Api.logout();
    showAuthScreen();
  });
}

/* ---------------- Add food: tabs ---------------- */

function initAddTabs() {
  document.querySelectorAll(".add-tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".add-tab").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      document.querySelectorAll(".add-panel").forEach((p) => p.classList.add("hidden"));
      $(`add-${btn.dataset.tab}`).classList.remove("hidden");
    });
  });
}

/* ---------------- Add food: manual ---------------- */

function initManualEntry() {
  $("manual-add").addEventListener("click", async () => {
    const name = $("manual-name").value.trim();
    const calories = Number($("manual-calories").value);
    $("manual-error").classList.add("hidden");

    if (!name || !calories) {
      $("manual-error").textContent = "Enter a name and calorie amount.";
      $("manual-error").classList.remove("hidden");
      return;
    }

    try {
      await Api.addEntry({
        name,
        calories,
        protein_g: Number($("manual-protein").value) || 0,
        carb_g: Number($("manual-carb").value) || 0,
        fat_g: Number($("manual-fat").value) || 0,
        serving_grams: Number($("manual-serving").value) || 100,
        meal_type: $("manual-meal").value,
        source: "manual",
      });
      $("manual-name").value = "";
      $("manual-calories").value = "";
      $("manual-protein").value = "0";
      $("manual-carb").value = "0";
      $("manual-fat").value = "0";
      switchView("dashboard");
    } catch (err) {
      $("manual-error").textContent = err.message;
      $("manual-error").classList.remove("hidden");
    }
  });
}

/* ---------------- Add food: barcode scanning ---------------- */

let scannerStream = null;
let scannerDetector = null;
let scannerLoopId = null;
let currentBarcodeProduct = null;

function initBarcodeTab() {
  const supported = "BarcodeDetector" in window;
  if (!supported) {
    $("barcode-unsupported").classList.remove("hidden");
    $("scan-start").classList.add("hidden");
  } else {
    scannerDetector = new window.BarcodeDetector({
      formats: ["ean_13", "ean_8", "upc_a", "upc_e", "code_128", "qr_code"],
    });
  }

  $("scan-start").addEventListener("click", startScanner);
  $("scan-stop").addEventListener("click", stopScanner);
  $("barcode-lookup").addEventListener("click", () => {
    const code = $("barcode-manual").value.trim();
    if (code) doBarcodeLookup(code);
  });
  $("barcode-add").addEventListener("click", addBarcodeEntry);
}

async function startScanner() {
  try {
    scannerStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" },
    });
    const video = $("scanner-video");
    video.srcObject = scannerStream;
    video.classList.remove("hidden");
    await video.play();
    $("scan-start").classList.add("hidden");
    $("scan-stop").classList.remove("hidden");
    scanLoop();
  } catch (err) {
    $("barcode-error").textContent = "Could not access camera: " + err.message;
    $("barcode-error").classList.remove("hidden");
  }
}

function stopScanner() {
  if (scannerLoopId) cancelAnimationFrame(scannerLoopId);
  if (scannerStream) {
    scannerStream.getTracks().forEach((t) => t.stop());
    scannerStream = null;
  }
  $("scanner-video").classList.add("hidden");
  $("scan-start").classList.remove("hidden");
  $("scan-stop").classList.add("hidden");
}

async function scanLoop() {
  if (!scannerStream) return;
  try {
    const codes = await scannerDetector.detect($("scanner-video"));
    if (codes.length > 0) {
      const value = codes[0].rawValue;
      stopScanner();
      $("barcode-manual").value = value;
      doBarcodeLookup(value);
      return;
    }
  } catch (err) {
    // detection errors are transient; keep looping
  }
  scannerLoopId = requestAnimationFrame(scanLoop);
}

async function doBarcodeLookup(code) {
  $("barcode-error").classList.add("hidden");
  $("barcode-result").classList.add("hidden");
  try {
    const product = await Api.lookupBarcode(code);
    currentBarcodeProduct = product;
    $("barcode-name").textContent = product.name;
    $("barcode-brand").textContent = product.brand || "";
    $("barcode-per100").textContent =
      `Per 100g: ${Math.round(product.per_100g.calories)} kcal, ` +
      `${product.per_100g.protein_g}g protein, ${product.per_100g.carb_g}g carbs, ${product.per_100g.fat_g}g fat`;
    $("barcode-serving").value = product.serving_grams || 100;
    $("barcode-result").classList.remove("hidden");
  } catch (err) {
    $("barcode-error").textContent = err.message;
    $("barcode-error").classList.remove("hidden");
  }
}

async function addBarcodeEntry() {
  if (!currentBarcodeProduct) return;
  const servingGrams = Number($("barcode-serving").value) || 100;
  const ratio = servingGrams / 100;
  const p = currentBarcodeProduct.per_100g;

  try {
    await Api.addEntry({
      name: currentBarcodeProduct.name,
      calories: p.calories * ratio,
      protein_g: p.protein_g * ratio,
      carb_g: p.carb_g * ratio,
      fat_g: p.fat_g * ratio,
      serving_grams: servingGrams,
      meal_type: $("barcode-meal").value,
      source: "barcode",
      barcode: currentBarcodeProduct.barcode,
    });
    $("barcode-result").classList.add("hidden");
    $("barcode-manual").value = "";
    currentBarcodeProduct = null;
    switchView("dashboard");
  } catch (err) {
    $("barcode-error").textContent = err.message;
    $("barcode-error").classList.remove("hidden");
  }
}

/* ---------------- Add food: photo recognition ---------------- */

let selectedCandidate = null;

function initPhotoTab() {
  $("photo-take").addEventListener("click", () => $("photo-input").click());
  $("photo-input").addEventListener("change", handlePhotoSelected);
  $("photo-add").addEventListener("click", addPhotoEntry);
}

async function handlePhotoSelected(e) {
  const file = e.target.files[0];
  if (!file) return;

  $("photo-error").classList.add("hidden");
  $("photo-result").classList.add("hidden");
  $("photo-take").disabled = true;
  $("photo-take").textContent = "Analyzing...";

  try {
    const result = await Api.recognizePhoto(file);
    renderPhotoCandidates(result.candidates);
    $("photo-serving").value = result.default_serving_grams;
    $("photo-result").classList.remove("hidden");
  } catch (err) {
    $("photo-error").textContent = err.message;
    $("photo-error").classList.remove("hidden");
  } finally {
    $("photo-take").disabled = false;
    $("photo-take").textContent = "Take / choose photo";
    e.target.value = "";
  }
}

function renderPhotoCandidates(candidates) {
  selectedCandidate = candidates[0] || null;
  const container = $("photo-candidates");
  container.innerHTML = "";

  candidates.forEach((c, idx) => {
    const div = document.createElement("div");
    div.className = "candidate" + (idx === 0 ? " selected" : "");
    div.innerHTML = `
      <div>
        <div>${escapeHtml(c.label.replace(/_/g, " "))}</div>
        <div class="confidence">${Math.round(c.confidence * 100)}% confident &middot; ${Math.round(c.per_100g.calories)} kcal/100g</div>
      </div>
    `;
    div.addEventListener("click", () => {
      selectedCandidate = c;
      container.querySelectorAll(".candidate").forEach((el) => el.classList.remove("selected"));
      div.classList.add("selected");
    });
    container.appendChild(div);
  });

  $("photo-add").disabled = candidates.length === 0;
}

async function addPhotoEntry() {
  if (!selectedCandidate) return;
  const servingGrams = Number($("photo-serving").value) || 150;
  const ratio = servingGrams / 100;
  const p = selectedCandidate.per_100g;

  try {
    await Api.addEntry({
      name: selectedCandidate.label.replace(/_/g, " "),
      calories: p.calories * ratio,
      protein_g: p.protein_g * ratio,
      carb_g: p.carb_g * ratio,
      fat_g: p.fat_g * ratio,
      serving_grams: servingGrams,
      meal_type: $("photo-meal").value,
      source: "photo",
    });
    $("photo-result").classList.add("hidden");
    selectedCandidate = null;
    switchView("dashboard");
  } catch (err) {
    $("photo-error").textContent = err.message;
    $("photo-error").classList.remove("hidden");
  }
}

/* ---------------- Boot ---------------- */

function init() {
  initAuthScreen();
  initNav();
  initDiaryView();
  initSettingsView();
  initAddTabs();
  initManualEntry();
  initBarcodeTab();
  initPhotoTab();

  if (Api.isLoggedIn()) {
    enterApp();
  } else {
    showAuthScreen();
  }
}

document.addEventListener("DOMContentLoaded", init);
