/* ==========================================================================
   CropWise — Frontend Logic
   This file is organized into clearly separated concerns:
     1. Navbar & mobile menu
     2. Scroll-reveal animations
     3. Info tooltips
     4. Model performance metrics (dashboard)
     5. Crop recommendation form: validation, mock prediction, rendering
   The mock prediction in section 5 is intentionally isolated so it can be
   swapped for a real API call once the backend model is ready.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  initNavbar();
  initScrollReveal();
  initTooltips();
  initHeroCounter();
  renderModelMetrics();
  initRecommendationForm();
});

/**
 * Shared count-up utility used by the hero stat, the performance metrics,
 * and the confidence ring so numbers animate in rather than snapping into
 * place. Purely a presentation touch — it doesn't affect the underlying value.
 */
function animateCountUp(el, target, { suffix = "", duration = 1000 } = {}) {
  const start = performance.now();
  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    el.textContent = `${Math.round(target * eased)}${suffix}`;
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

/** Counts the hero's "Input Features" stat up from 0 once the page loads. */
function initHeroCounter() {
  const el = document.getElementById("heroFeatureCount");
  if (!el) return;
  setTimeout(() => animateCountUp(el, 7, { duration: 900 }), 650);
}

/* ==========================================================================
   1. NAVBAR
   ========================================================================== */
function initNavbar() {
  const navbar = document.getElementById("navbar");
  const navToggle = document.getElementById("navToggle");
  const navLinks = document.getElementById("navLinks");

  const onScroll = () => {
    navbar.classList.toggle("scrolled", window.scrollY > 12);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  navToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("open");
    navToggle.classList.toggle("open", isOpen);
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  // Close mobile menu after choosing a link
  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("open");
      navToggle.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });
}

/* ==========================================================================
   2. SCROLL REVEAL
   Adds a subtle fade/slide-in the first time each section enters view.
   ========================================================================== */
function initScrollReveal() {
  const targets = document.querySelectorAll(".section-head, .form-card, .steps, .math-card, .feature-grid, .influence-grid, .concept-grid, .metrics-grid, .performance-lower, .future-card, .tech-list");
  targets.forEach((el) => el.classList.add("reveal"));

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  targets.forEach((el) => observer.observe(el));
}

/* ==========================================================================
   3. INFO TOOLTIPS
   Small "i" buttons next to each input show a contextual explanation.
   ========================================================================== */
function initTooltips() {
  const bubble = document.getElementById("tooltipBubble");
  const infoButtons = document.querySelectorAll(".info-btn");

  const showBubble = (btn) => {
    bubble.textContent = btn.getAttribute("data-tip");
    bubble.hidden = false;
    const rect = btn.getBoundingClientRect();
    const bubbleRect = bubble.getBoundingClientRect();
    let left = rect.left + rect.width / 2 - bubbleRect.width / 2;
    left = Math.max(12, Math.min(left, window.innerWidth - bubbleRect.width - 12));
    bubble.style.left = `${left}px`;
    bubble.style.top = `${rect.top - bubbleRect.height - 10}px`;
  };
  const hideBubble = () => { bubble.hidden = true; };

  infoButtons.forEach((btn) => {
    btn.addEventListener("mouseenter", () => showBubble(btn));
    btn.addEventListener("focus", () => showBubble(btn));
    btn.addEventListener("mouseleave", hideBubble);
    btn.addEventListener("blur", hideBubble);
    btn.addEventListener("click", (e) => e.preventDefault());
  });

  window.addEventListener("scroll", hideBubble, { passive: true });
}

/* ==========================================================================
   4. MODEL PERFORMANCE METRICS
   Values are left null until a trained model is connected. Demo values are
   shown as clearly-labelled placeholders instead of invented statistics.
   ========================================================================== */
const modelMetrics = {
  accuracy: null,
  precision: null,
  recall: null,
  f1: null,
};

// Demo-only values so the dashboard has something to show a professor.
// Replace this object (or feed real numbers into `modelMetrics`) once the
// trained model produces real evaluation results.
const demoMetrics = {
  accuracy: 95,
  precision: 94,
  recall: 93,
  f1: 93,
};

function renderModelMetrics() {
  const grid = document.getElementById("metricsGrid");
  const labels = { accuracy: "Accuracy", precision: "Precision", recall: "Recall", f1: "F1 Score" };

  grid.innerHTML = Object.keys(labels)
    .map((key) => {
      const real = modelMetrics[key];
      const demo = demoMetrics[key];
      const hasReal = real !== null && real !== undefined;

      if (hasReal) {
        return `
          <div class="metric-card">
            <span class="metric-value" data-count-target="${real}">0%</span>
            <span class="metric-label">${labels[key]}</span>
          </div>`;
      }
      if (demo !== null && demo !== undefined) {
        return `
          <div class="metric-card">
            <span class="metric-value" data-count-target="${demo}">0%</span>
            <span class="metric-label">${labels[key]}</span>
            <span class="metric-tag">Demo value</span>
          </div>`;
      }
      return `
        <div class="metric-card">
          <span class="metric-value pending">Awaiting trained model</span>
          <span class="metric-label">${labels[key]}</span>
        </div>`;
    })
    .join("");

  // Count the percentages up once, the first time the dashboard scrolls into view.
  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        grid.querySelectorAll(".metric-value[data-count-target]").forEach((el, i) => {
          const target = Number(el.getAttribute("data-count-target"));
          setTimeout(() => animateCountUp(el, target, { suffix: "%", duration: 1100 }), i * 120);
        });
        obs.disconnect();
      });
    },
    { threshold: 0.4 }
  );
  observer.observe(grid);
}

/* ==========================================================================
   5. CROP RECOMMENDATION FORM
   ========================================================================== */

// Sensible real-world ranges used purely for frontend input validation.
const FIELD_RULES = {
  nitrogen:    { label: "Nitrogen",    min: 0,   max: 150,  allowDecimal: true },
  phosphorus:  { label: "Phosphorus",  min: 0,   max: 150,  allowDecimal: true },
  potassium:   { label: "Potassium",   min: 0,   max: 210,  allowDecimal: true },
  temperature: { label: "Temperature", min: -5,  max: 55,   allowDecimal: true },
  humidity:    { label: "Humidity",    min: 0,   max: 100,  allowDecimal: true },
  ph:          { label: "Soil pH",     min: 0,   max: 14,   allowDecimal: true },
  rainfall:    { label: "Rainfall",    min: 0,   max: 500,  allowDecimal: true },
};

// Crop metadata used only for the frontend demo visuals (emoji + display name).
const CROP_INFO = {
  rice:       { emoji: "🌾", name: "Rice" },
  maize:      { emoji: "🌽", name: "Maize" },
  chickpea:   { emoji: "🫘", name: "Chickpea" },
  cotton:     { emoji: "🌱", name: "Cotton" },
  coffee:     { emoji: "☕", name: "Coffee" },
  banana:     { emoji: "🍌", name: "Banana" },
  mango:      { emoji: "🥭", name: "Mango" },
  watermelon: { emoji: "🍉", name: "Watermelon" },
  lentil:     { emoji: "🌿", name: "Lentil" },
  jute:       { emoji: "🧵", name: "Jute" },
};

function initRecommendationForm() {
  const form = document.getElementById("cropForm");
  const tryAnotherBtn = document.getElementById("tryAnotherBtn");

  form.addEventListener("submit", handleFormSubmit);
  tryAnotherBtn.addEventListener("click", resetRecommendation);

  // Clear a field's error as soon as the user edits it again.
  Object.keys(FIELD_RULES).forEach((id) => {
    const input = document.getElementById(id);
    input.addEventListener("input", () => clearFieldError(id));
  });
}

async function handleFormSubmit(event) {
  event.preventDefault();

  const errors = validateForm();
  if (Object.keys(errors).length > 0) {
    showValidationErrors(errors);
    return;
  }

  const formData = getFormData();
  const recommendBtn = document.getElementById("recommendBtn");
  const loadingState = document.getElementById("loadingState");
  const resultArea = document.getElementById("resultArea");

  recommendBtn.disabled = true;
  loadingState.hidden = false;
  resultArea.hidden = true;

  const prediction = await getPrediction(formData);

  loadingState.hidden = true;
  recommendBtn.disabled = false;

  displayPrediction(prediction);
  displayProbabilities(prediction.probabilities, prediction.crop);
  displayInputSummary(formData);

  resultArea.hidden = false;
  resultArea.scrollIntoView({ behavior: "smooth", block: "start" });
}

/**
 * Reads and validates every field.
 * Returns an object keyed by field id -> error message.
 * An empty object means the form is valid.
 */
function validateForm() {
  const errors = {};

  Object.entries(FIELD_RULES).forEach(([id, rule]) => {
    const input = document.getElementById(id);
    const raw = input.value.trim();

    if (raw === "") {
      errors[id] = `${rule.label} is required.`;
      return;
    }

    const value = Number(raw);
    if (Number.isNaN(value)) {
      errors[id] = `${rule.label} must be a number.`;
      return;
    }

    if (value < rule.min || value > rule.max) {
      errors[id] = `${rule.label} should be between ${rule.min} and ${rule.max}.`;
    }
  });

  return errors;
}

function showValidationErrors(errors) {
  // Clear all first, then apply the current set.
  Object.keys(FIELD_RULES).forEach(clearFieldError);

  Object.entries(errors).forEach(([id, message]) => {
    const input = document.getElementById(id);
    const errorEl = document.getElementById(`${id}-error`);
    input.classList.add("invalid");
    input.setAttribute("aria-invalid", "true");
    if (errorEl) errorEl.textContent = message;
  });

  const firstInvalidId = Object.keys(errors)[0];
  document.getElementById(firstInvalidId)?.focus();
}

function clearFieldError(id) {
  const input = document.getElementById(id);
  const errorEl = document.getElementById(`${id}-error`);
  input.classList.remove("invalid");
  input.removeAttribute("aria-invalid");
  if (errorEl) errorEl.textContent = "";
}

/** Collects the current form values into a plain object. */
function getFormData() {
  const data = {};
  Object.keys(FIELD_RULES).forEach((id) => {
    data[id] = Number(document.getElementById(id).value);
  });
  return data;
}

/**
 * Returns a prediction for the given form data.
 *
 * TEMPORARY FRONTEND DEMO — this calls mockPrediction() below. The function
 * is kept separate and async on purpose so it's a drop-in swap later, once
 * there's somewhere to send the request. For example, if a lightweight
 * server ever sits in front of the trained model:
 *
 * async function getPrediction(formData) {
 *   const response = await fetch("/predict", {
 *     method: "POST",
 *     headers: { "Content-Type": "application/json" },
 *     body: JSON.stringify(formData),
 *   });
 *   if (!response.ok) throw new Error("Prediction request failed.");
 *   return await response.json();
 *   // Expected shape: { crop: "rice", confidence: 72, probabilities: {...} }
 * }
 *
 * For now, training and prediction live in a separate Python script that
 * runs on its own — this frontend and that script aren't wired together yet.
 */
async function getPrediction(formData) {
  await simulateNetworkDelay(1100);
  return mockPrediction(formData);
}

function simulateNetworkDelay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Lightweight, rule-of-thumb heuristic used ONLY to make the frontend demo
 * feel responsive to the inputs. This is not the real model — the actual
 * Multinomial Logistic Regression prediction will come from the backend.
 */
function mockPrediction(formData) {
  const { temperature, humidity, rainfall, ph, nitrogen } = formData;
  let candidates;

  if (rainfall > 180 && humidity > 70 && temperature > 20) {
    candidates = ["rice", "jute", "coffee"];
  } else if (nitrogen > 80 && temperature >= 18 && temperature <= 30) {
    candidates = ["maize", "cotton", "banana"];
  } else if (ph < 6 && rainfall < 120) {
    candidates = ["chickpea", "lentil", "watermelon"];
  } else if (temperature > 28 && humidity < 60) {
    candidates = ["cotton", "mango", "watermelon"];
  } else {
    candidates = ["maize", "rice", "lentil"];
  }

  const topCrop = candidates[0];

  // Build a plausible-looking probability distribution centered on topCrop.
  const others = Object.keys(CROP_INFO).filter((c) => c !== topCrop);
  shuffleArray(others);

  const topConfidence = 62 + Math.round(Math.random() * 22); // 62–84%
  let remaining = 100 - topConfidence;

  const probabilities = { [topCrop]: topConfidence };
  const supportCrops = others.slice(0, 3);
  supportCrops.forEach((crop, index) => {
    const isLast = index === supportCrops.length - 1;
    const share = isLast ? remaining : Math.round(remaining * (0.5 - index * 0.15));
    probabilities[crop] = Math.max(1, share);
    remaining -= probabilities[crop];
  });
  if (remaining > 0) probabilities.others = remaining;

  return {
    crop: topCrop,
    confidence: topConfidence,
    probabilities,
  };
}

function shuffleArray(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}

/** Renders the main result card (crop name, emoji, confidence ring). */
function displayPrediction(prediction) {
  const info = CROP_INFO[prediction.crop] || { emoji: "🌱", name: prediction.crop };

  document.getElementById("resultEmoji").textContent = info.emoji;
  document.getElementById("resultName").textContent = info.name.toUpperCase();
  document.getElementById("resultNote").textContent =
    `Based on the conditions you provided, ${info.name} has the highest predicted probability.`;

  const ring = document.getElementById("confidenceRing");
  const num = document.getElementById("confidenceNum");

  // Animate the ring fill and the number counting up together.
  ring.style.setProperty("--pct", 0);
  num.textContent = "0%";
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      ring.style.setProperty("--pct", prediction.confidence);
      animateCountUp(num, prediction.confidence, { suffix: "%", duration: 1000 });
    });
  });
}

/** Dynamically builds the animated probability bars from a {crop: pct} object. */
function displayProbabilities(probabilities, topCrop) {
  const container = document.getElementById("probBars");

  const rows = Object.entries(probabilities).sort((a, b) => b[1] - a[1]);

  container.innerHTML = rows
    .map(([crop, pct]) => {
      const label = crop === "others" ? "Others" : (CROP_INFO[crop]?.name || crop);
      const isTop = crop === topCrop;
      return `
        <div class="prob-row ${isTop ? "is-top" : ""}">
          <div class="prob-row-top">
            <span class="prob-crop">${label}</span>
            <span class="prob-pct">${pct}%</span>
          </div>
          <div class="prob-track">
            <div class="prob-fill" data-width="${pct}"></div>
          </div>
        </div>`;
    })
    .join("");

  // Animate bars in after they've been inserted into the DOM.
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      container.querySelectorAll(".prob-fill").forEach((bar) => {
        bar.style.width = `${bar.getAttribute("data-width")}%`;
      });
    });
  });
}

/** Renders a read-only summary of exactly what the user entered. */
function displayInputSummary(formData) {
  const list = document.getElementById("summaryList");
  const rows = [
    { label: "Nitrogen", value: `${formData.nitrogen} kg/ha` },
    { label: "Phosphorus", value: `${formData.phosphorus} kg/ha` },
    { label: "Potassium", value: `${formData.potassium} kg/ha` },
    { label: "Temperature", value: `${formData.temperature} °C` },
    { label: "Humidity", value: `${formData.humidity} %` },
    { label: "Soil pH", value: `${formData.ph}` },
    { label: "Rainfall", value: `${formData.rainfall} mm` },
  ];

  list.innerHTML = rows
    .map((row) => `<div><dt>${row.label}</dt><dd>${row.value}</dd></div>`)
    .join("");
}

/** Clears the form and hides the result area so the user can try again. */
function resetRecommendation() {
  const form = document.getElementById("cropForm");
  form.reset();
  Object.keys(FIELD_RULES).forEach(clearFieldError);

  document.getElementById("resultArea").hidden = true;
  document.getElementById("cropForm").scrollIntoView({ behavior: "smooth", block: "start" });
  document.getElementById("nitrogen").focus();
}
