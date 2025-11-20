"""async function fetchAlerts(page=1, per=20){
  const res = await fetch(`/api/alerts?page=${page}&per=${per}`);
  return res.json();
}

async function render(){
  const data = await fetchAlerts();
  const table = document.querySelector('#alerts-table tbody');
  table.innerHTML = '';
  const counts = {Critical:0, High:0, Medium:0, Low:0, Unknown:0};
  data.items.forEach(it=>{
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${it.published_date||''}</td><td>${it.source}</td><td>${it.severity}</td><td>${it.summary}</td>`;
    table.appendChild(tr);
    if(counts[it.severity]===undefined) counts.Unknown++;
    else counts[it.severity]++;
  });

  // render chart
  const ctx = document.getElementById('severityChart').getContext('2d');
  if(window._chart) window._chart.destroy();
  window._chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(counts),
      datasets: [{ label: 'Alerts by severity', data: Object.values(counts), backgroundColor:['#8B0000','#FF4500','#FFA500','#FFD700','#6c757d'] }]
    }
  });
}

window.addEventListener('DOMContentLoaded', render);
"""