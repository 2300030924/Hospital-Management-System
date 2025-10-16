const form = document.getElementById('prediction-form');
const resultCard = document.getElementById('result-card');
const resultText = document.getElementById('result-text');
const resultProb = document.getElementById('result-prob');
const tipsList = document.getElementById('tips');

let probChart; // Chart.js instance

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  // Gather form values
  const payload = {
    age:      parseFloat(document.getElementById('age').value),
    gender:   parseFloat(document.getElementById('gender').value),
    impulse:  parseFloat(document.getElementById('impulse').value),
    highbp:   parseFloat(document.getElementById('highbp').value),
    lowbp:    parseFloat(document.getElementById('lowbp').value),
    glucose:  parseFloat(document.getElementById('glucose').value),
    kcm:      parseFloat(document.getElementById('kcm').value),
    troponin: parseFloat(document.getElementById('troponin').value)
  };

  // Quick client-side sanity checks (optional)
  for (const [k,v] of Object.entries(payload)){
    if (Number.isNaN(v)) {
      alert(`Please enter a valid number for "${k}".`);
      return;
    }
  }

  // Call API
  try{
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Prediction failed');

    // Update result card
    const cat = (data.risk_category || '').toLowerCase(); // "low" | "moderate" | "high"
    resultCard.classList.remove('low','moderate','high');
    resultCard.classList.add(cat || 'low');

    resultText.textContent = `Risk: ${data.risk_category}`;
    resultProb.textContent = `Estimated probability of heart disease: ${(data.probability*100).toFixed(1)}%`;

    // Tips
    tipsList.innerHTML = '';
    (data.tips || []).forEach(t => {
      const li = document.createElement('li');
      li.textContent = t;
      tipsList.appendChild(li);
    });

    // Draw / update chart
    const ctx = document.getElementById('probChart');
    const p = data.probability;
    const healthy = 1 - p;

    if (probChart) probChart.destroy();
    probChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Disease probability','Healthy probability'],
        datasets: [{
          data: [p, healthy]
        }]
      },
      options: {
        responsive: true,
        cutout: '65%',
        plugins: {
          legend: { position: 'bottom' },
          tooltip: { enabled: true }
        }
      }
    });

  }catch(err){
    console.error(err);
    resultCard.classList.remove('low','moderate','high');
    resultText.textContent = 'Error getting prediction';
    resultProb.textContent = err.message;
    tipsList.innerHTML = '';
  }
});
