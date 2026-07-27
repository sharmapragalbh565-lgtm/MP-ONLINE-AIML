/**
 * static/js/app.js
 * Handles form submission, unit conversions (km/mi, INR/USD), API calls,
 * and animated result display.
 */

'use strict';

// ── Conversion Constants ──────────────────────────────────────────────────────
const MILES_TO_KM          = 1.60934;
const USD_TO_INR           = 84;        // 1 USD ≈ 84 INR (fixed rate)
const INR_LAKH             = 100_000;   // 1 Lakh = 100,000 INR

// ── State ─────────────────────────────────────────────────────────────────────
let selectedCurrency = 'INR'; // 'INR' | 'USD'
let selectedDistance = 'km';  // 'km'  | 'mi'

// ── DOM References ────────────────────────────────────────────────────────────
const form         = document.getElementById('predict-form');
const submitBtn    = document.getElementById('submit-btn');
const btnText      = document.getElementById('btn-text');
const btnSpinner   = document.getElementById('btn-spinner');

const resultPanel  = document.getElementById('result-panel');
const predictedEl  = document.getElementById('predicted-price');
const lowerEl      = document.getElementById('lower-bound');
const upperEl      = document.getElementById('upper-bound');
const rangeBar     = document.getElementById('range-bar');

// Result panel dynamic labels
const resultCurrencySymbol = document.getElementById('result-currency-symbol');
const resultPriceUnit      = document.getElementById('result-price-unit');
const rangeUnitEl          = document.getElementById('range-unit');
const rangeUnitLabels      = document.querySelectorAll('.range-unit-label');

const errorPanel   = document.getElementById('error-panel');
const errorMessage = document.getElementById('error-message');
const resetBtn     = document.getElementById('reset-btn');

// Toggle UI refs
const currencyToggle  = document.getElementById('currency-toggle');
const distanceToggle  = document.getElementById('distance-toggle');
const currencyIcon    = document.getElementById('currency-icon');
const distanceIcon    = document.getElementById('distance-icon');
const distanceLabel   = document.getElementById('distance-label');
const priceHint       = document.getElementById('price-hint');
const distanceHint    = document.getElementById('distance-hint');
const priceInput      = document.getElementById('present_price');
const kmsInput        = document.getElementById('kms_driven');

// Unit badge refs (glowing right-side labels)
const priceUnitBadge = document.getElementById('price-unit-badge');
const distUnitBadge  = document.getElementById('distance-unit-badge');


// ── Toggle Helpers ────────────────────────────────────────────────────────────

function activateBtn(group, value) {
  group.querySelectorAll('.unit-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.value === value);
  });
}

/** Update all UI labels when the currency toggle changes. */
function applyCurrencyUI(currency) {
  selectedCurrency = currency;
  activateBtn(currencyToggle, currency);

  if (currency === 'USD') {
    currencyIcon.textContent     = '$';
    priceInput.placeholder       = 'e.g. 10000';
    priceInput.step              = '1';
    priceHint.textContent        = 'Enter amount in US Dollars (USD)';
    if (priceUnitBadge) priceUnitBadge.textContent = 'USD';
  } else {
    currencyIcon.textContent     = 'Rs';
    priceInput.placeholder       = 'e.g. 8.5';
    priceInput.step              = '0.01';
    priceHint.textContent        = 'Enter amount in Lakhs (INR)';
    if (priceUnitBadge) priceUnitBadge.textContent = 'Lakhs';
  }
  priceInput.value = '';
}

/** Update all UI labels when the distance toggle changes. */
function applyDistanceUI(distance) {
  selectedDistance = distance;
  activateBtn(distanceToggle, distance);

  if (distance === 'mi') {
    distanceIcon.textContent  = 'Mi';
    distanceLabel.textContent = 'Miles Driven';
    kmsInput.placeholder      = 'e.g. 28000';
    distanceHint.textContent  = 'Enter distance in miles — will be converted to km';
    if (distUnitBadge) distUnitBadge.textContent = 'mi';
  } else {
    distanceIcon.textContent  = 'Km';
    distanceLabel.textContent = 'Kilometres Driven';
    kmsInput.placeholder      = 'e.g. 45000';
    distanceHint.textContent  = 'Enter distance in kilometres';
    if (distUnitBadge) distUnitBadge.textContent = 'km';
  }
  kmsInput.value = '';
}


// ── Toggle Event Listeners ────────────────────────────────────────────────────

currencyToggle.addEventListener('click', (e) => {
  const btn = e.target.closest('.unit-btn');
  if (btn && btn.dataset.value !== selectedCurrency) {
    applyCurrencyUI(btn.dataset.value);
  }
});

distanceToggle.addEventListener('click', (e) => {
  const btn = e.target.closest('.unit-btn');
  if (btn && btn.dataset.value !== selectedDistance) {
    applyDistanceUI(btn.dataset.value);
  }
});


// ── Unit Conversion ───────────────────────────────────────────────────────────

/** Convert user-entered price to Lakhs INR (what the model expects). */
function toInrLakhs(value, currency) {
  if (currency === 'USD') {
    // USD → INR → Lakhs
    return (value * USD_TO_INR) / INR_LAKH;
  }
  return value; // already in Lakhs
}

/** Convert raw km input to km (handling miles input). */
function toKm(value, unit) {
  if (unit === 'mi') return Math.round(value * MILES_TO_KM);
  return Math.round(value);
}

/**
 * Convert a model result (always Lakhs INR) to the display value
 * based on selectedCurrency.
 */
function fromLakhsToDisplay(lakhs, currency) {
  if (currency === 'USD') {
    // Lakhs → INR → USD
    return (lakhs * INR_LAKH) / USD_TO_INR;
  }
  return lakhs;
}

/** Format the display value depending on currency. */
function formatDisplayValue(value, currency) {
  if (currency === 'USD') {
    // Show as whole dollars, comma-separated
    return value.toLocaleString('en-US', { maximumFractionDigits: 0 });
  }
  return value.toFixed(2);
}


// ── Helpers ───────────────────────────────────────────────────────────────────

/** Animate a number counting up from 0 to target over `duration` ms. */
function animateCount(element, target, currency, duration = 1200) {
  const start = performance.now();

  function step(now) {
    const elapsed  = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased    = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current  = eased * target;
    element.textContent = formatDisplayValue(current, currency);
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

/** Show loading state on the submit button. */
function setLoading(loading) {
  submitBtn.disabled = loading;
  btnText.classList.toggle('hidden', loading);
  btnSpinner.classList.toggle('hidden', !loading);
}

/** Show the error panel with a message. */
function showError(msg) {
  errorMessage.textContent = msg;
  errorPanel.classList.remove('hidden');
  resultPanel.classList.add('hidden');
}

/** Hide both result and error panels. */
function hidePanels() {
  resultPanel.classList.add('hidden');
  errorPanel.classList.add('hidden');
}

/** Update result panel currency labels. */
function applyResultLabels(currency) {
  if (currency === 'USD') {
    resultCurrencySymbol.textContent = '$';
    resultPriceUnit.textContent      = 'USD';
    if (rangeUnitEl) rangeUnitEl.textContent = 'USD';
    rangeUnitLabels.forEach(el => { el.textContent = 'USD'; });
  } else {
    resultCurrencySymbol.textContent = 'Rs.';
    resultPriceUnit.textContent      = 'Lakhs';
    if (rangeUnitEl) rangeUnitEl.textContent = 'L';
    rangeUnitLabels.forEach(el => { el.textContent = 'L'; });
  }
}


// ── Form Submission ───────────────────────────────────────────────────────────

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  hidePanels();

  // Client-side sanity checks
  if (!form.owner.value)       { showError('Please select the number of previous owners.'); return; }
  if (!form.fuel_type.value)   { showError('Please select a fuel type.'); return; }
  if (!form.seller_type.value) { showError('Please select a seller type.'); return; }

  const rawPrice    = parseFloat(form.present_price.value);
  const rawDistance = parseFloat(form.kms_driven.value);

  if (isNaN(rawPrice) || rawPrice <= 0) {
    showError('Please enter a valid ex-showroom price.'); return;
  }
  if (isNaN(rawDistance) || rawDistance < 0) {
    showError('Please enter a valid distance.'); return;
  }

  // Convert to model-native units (Lakhs INR, km)
  const priceInLakhs = toInrLakhs(rawPrice, selectedCurrency);
  const kmsDriven    = toKm(rawDistance, selectedDistance);

  const payload = {
    present_price: priceInLakhs,
    car_age:       parseInt(form.car_age.value, 10),
    kms_driven:    kmsDriven,
    owner:         parseInt(form.owner.value, 10),
    fuel_type:     form.fuel_type.value,
    seller_type:   form.seller_type.value,
    transmission:  form.transmission.value,
  };

  setLoading(true);

  try {
    const response = await fetch('/predict', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok || data.error) {
      showError(data.error || `Server error: ${response.status}`);
      return;
    }

    // ── Convert results for display ───────────────────────────────────
    const displayPrice = fromLakhsToDisplay(data.predicted_price, selectedCurrency);
    const displayLower = fromLakhsToDisplay(data.lower_bound,     selectedCurrency);
    const displayUpper = fromLakhsToDisplay(data.upper_bound,     selectedCurrency);

    // ── Update result labels ──────────────────────────────────────────
    applyResultLabels(selectedCurrency);

    // ── Show panel & animate ──────────────────────────────────────────
    resultPanel.classList.remove('hidden');

    animateCount(predictedEl, displayPrice, selectedCurrency, 1200);

    lowerEl.textContent = formatDisplayValue(displayLower, selectedCurrency);
    upperEl.textContent = formatDisplayValue(displayUpper, selectedCurrency);

    // Animate range bar
    const spread    = displayUpper - displayLower;
    const maxSpread = displayPrice * 0.40;
    const fillPct   = Math.min(100, (spread / maxSpread) * 100);

    setTimeout(() => { rangeBar.style.width = `${fillPct}%`; }, 100);

    resultPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  } catch (err) {
    showError('Network error. Is the Flask server running?');
    console.error(err);
  } finally {
    setLoading(false);
  }
});


// ── Reset Button ──────────────────────────────────────────────────────────────

resetBtn.addEventListener('click', () => {
  hidePanels();
  rangeBar.style.width = '0%';
  form.reset();

  // Reset toggles and labels to defaults
  applyCurrencyUI('INR');
  applyDistanceUI('km');
  document.getElementById('trans-manual').checked = true;

  form.scrollIntoView({ behavior: 'smooth', block: 'start' });
});
