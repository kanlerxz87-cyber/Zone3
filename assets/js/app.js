// Zone3 — Amazon Affiliate Platform
// Renders featured product cards on the landing page from data/products.json.
// Falls back gracefully if the data file is unavailable.

(async function () {
  const grid = document.getElementById('featured-grid');
  if (!grid) return;

  let products = [];
  try {
    const res = await fetch('data/products.json', { cache: 'no-cache' });
    if (!res.ok) throw new Error('data file unavailable');
    const data = await res.json();
    products = data.products || [];
  } catch (err) {
    console.warn('Could not load data/products.json:', err);
    grid.innerHTML = '<p style="color:var(--text-muted);">Product data could not be loaded. Visit the Products page for the full table.</p>';
    return;
  }

  grid.innerHTML = products.map(p => `
    <article class="card">
      <h3>${escapeHtml(p.title)}</h3>
      <div class="meta">
        <span class="cat-badge">${escapeHtml(p.categoryLabel)}</span>
        <span style="float:right">ASIN: ${escapeHtml(p.asin)}</span>
      </div>
      <p>${escapeHtml(p.analysis)}</p>
      <div class="meta">
        Commission rate: <span class="blank">${p.commissionRate || 'unverified'}</span>
      </div>
      <a href="${p.officialSource}" target="_blank" rel="noopener" class="btn" style="margin-top:auto;width:100%;justify-content:center;">Official source &rarr;</a>
      <a href="${p.affiliateLink}" target="_blank" rel="nofollow noopener" style="margin-top:0.5rem;width:100%;text-align:center;color:var(--text-muted);font-size:0.8rem;">Affiliate link (Amazon) &rarr;</a>
    </article>
  `).join('');
})();

function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
