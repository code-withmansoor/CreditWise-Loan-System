const form = document.getElementById('prediction-form');
const resultsCard = document.getElementById('results-card');
const resultPill = document.getElementById('result-pill');
const probabilityValue = document.getElementById('probability-value');
const riskValue = document.getElementById('risk-value');
const confidenceValue = document.getElementById('confidence-value');
const emiValue = document.getElementById('emi-value');
const recommendationBox = document.getElementById('recommendation-box');
const historyList = document.getElementById('history-list');

window.addEventListener('load', () => {
  document.querySelector('.loader').classList.add('hidden');
});

const cursorGlow = document.querySelector('.cursor-glow');
const cursorTrail = document.querySelector('.cursor-trail');
window.addEventListener('mousemove', (event) => {
  cursorGlow.style.left = `${event.clientX}px`;
  cursorGlow.style.top = `${event.clientY}px`;
  cursorTrail.style.left = `${event.clientX}px`;
  cursorTrail.style.top = `${event.clientY}px`;
});

document.querySelectorAll('.tilt-card, .info-card, .primary-btn, .secondary-btn, .ghost-btn, .submit-btn').forEach((el) => {
  el.addEventListener('mousemove', (event) => {
    const rect = el.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    el.style.transform = `perspective(800px) rotateX(${((rect.height / 2 - y) / rect.height) * 6}deg) rotateY(${((x - rect.width / 2) / rect.width) * 6}deg)`;
  });
  el.addEventListener('mouseleave', () => {
    el.style.transform = '';
  });
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());
  payload.Applicant_Income = Number(payload.Applicant_Income);
  payload.Coapplicant_Income = Number(payload.Coapplicant_Income);
  payload.Loan_Amount = Number(payload.Loan_Amount);
  payload.Credit_Score = Number(payload.Credit_Score);
  payload.DTI_Ratio = Number(payload.DTI_Ratio);
  payload.Savings = Number(payload.Savings);
  payload.Age = Number(payload.Age);
  payload.Dependents = Number(payload.Dependents);
  payload.Existing_Loans = Number(payload.Existing_Loans);

  const response = await fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await response.json();

  resultPill.textContent = `${data.result} • ${data.risk_level}`;
  resultPill.style.background = data.result === 'Approved' ? 'rgba(93,255,176,0.16)' : 'rgba(255,107,138,0.16)';
  probabilityValue.textContent = `${(data.probability * 100).toFixed(1)}%`;
  riskValue.textContent = `${data.risk_score}`;
  confidenceValue.textContent = `${data.confidence}`;
  emiValue.textContent = `₹${data.emi}`;
  recommendationBox.textContent = data.recommendation;

  if (data.result === 'Approved') {
    document.getElementById('hero-probability').textContent = `${(data.probability * 100).toFixed(1)}%`;
    document.getElementById('hero-risk').textContent = `${data.risk_score}`;
  }

  const historyResponse = await fetch('/history');
  const history = await historyResponse.json();
  historyList.innerHTML = history.slice(0, 5).map((item) => `<div><strong>${item.applicant_name}</strong><br/>${item.result} • ${Number(item.probability).toFixed(2)} probability</div>`).join('');
});
