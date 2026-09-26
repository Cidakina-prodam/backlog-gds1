"""
Templates do dashboard (HTML + JS) embutidos como strings — assim o
projeto inteiro fica em arquivos soltos na raiz do repositório, sem
depender de nenhuma subpasta (evita o problema de upload de pasta no
GitHub pelo navegador).

Painel simplificado (set/2026), pensado para a Dani e os coordenadores:
  1. veredito da semana (o backlog caiu ou subiu?)
  2. Legado (antes do ano corrente) x Atuais (ano corrente)
  3. evolução semanal
  4. status: barras + matriz colorida status x núcleo (clique abre as demandas)
  5. listagem completa + exportação CSV (mantidas como antes)
Um único filtro de núcleo, no topo, vale para o painel inteiro.
"""
import json

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Backlog GDS-1</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#eef1f5; --surface:#ffffff; --ink:#1b2430; --muted:#566273; --line:#dbe1e8; --line-soft:#e8ecf1;
  --legado:#4a5668; --atuais:#a9b5c5; --total:#8793a4;
  --down:#1d7a55; --down-bg:#e4f3ec; --up:#a95400; --up-bg:#fcefe2;
  --NSS1:#2f6fd8; --NSS2:#1d8a70; --NSS3:#b06d0a; --NC:#9a3fcc; --GDS:#1b2430; --OUTRO:#6b7686;
  --font-display:'Space Grotesk','IBM Plex Sans',system-ui,sans-serif;
  --font-body:'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-body);font-variant-numeric:tabular-nums;line-height:1.45}
.wrap{max-width:1240px;margin:0 auto;padding:32px 24px 48px;display:flex;flex-direction:column;gap:20px}
h1,h2,h3,.num{font-family:var(--font-display)}
button{font:inherit}
button:focus-visible,[tabindex]:focus-visible{outline:3px solid #2f6fd8;outline-offset:2px}

header.top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:16px}
h1{margin:0;font-size:34px;font-weight:700;letter-spacing:-0.01em}
.sub{color:var(--muted);font-size:15px}
.top-meta{text-align:right;font-size:14px;color:var(--muted);line-height:1.6}
.top-meta b{color:var(--ink);font-weight:600}

.filter{display:flex;flex-wrap:wrap;gap:8px;position:sticky;top:0;z-index:5;background:var(--bg);padding:10px 0}
.chip{height:44px;padding:0 18px;border-radius:99px;border:1.5px solid var(--line);background:var(--surface);color:var(--ink);font-size:15px;font-weight:500;cursor:pointer;display:flex;align-items:center;gap:8px}
.chip .dot{width:10px;height:10px;border-radius:50%}
.chip[aria-pressed="true"]{background:var(--c);border-color:var(--c);color:#fff}
.chip[aria-pressed="true"] .dot{background:#fff !important}
.fhint{flex-basis:100%;font-size:14px;color:var(--muted);padding-left:4px}

.panel{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:22px 24px}
.panel-head{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:12px;margin-bottom:10px}
.panel-head h2{margin:0;font-size:21px;font-weight:600}
.legend{display:flex;gap:18px;font-size:14px;color:var(--muted);flex-wrap:wrap}
.legend span{display:flex;align-items:center;gap:8px}
.sw{width:14px;height:14px;border-radius:4px;display:inline-block;flex-shrink:0}

.verdict{display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.verdict .num{font-size:52px;font-weight:700;line-height:1}
.verdict .t1{font-size:19px;font-weight:600}
.verdict .t2{font-size:15px;color:var(--muted)}
.verdict.good{background:var(--down-bg);border-color:#bfe0cf}
.verdict.bad{background:var(--up-bg);border-color:#f0d2b3}
.good-t{color:var(--down)} .bad-t{color:var(--up)}

.split{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media (max-width:760px){.split{grid-template-columns:1fr}}
.card h2{margin:0 0 14px;font-size:21px;font-weight:600;display:flex;align-items:center;gap:10px}
.card h2 small{font-family:var(--font-body);font-weight:400;font-size:15px;color:var(--muted)}
.ntag{margin-left:auto;font-family:var(--font-body);font-size:13px;font-weight:600;color:#fff;padding:3px 10px;border-radius:99px;display:none}
.stats{display:flex;gap:36px;align-items:flex-end;flex-wrap:wrap}
.stat{display:flex;flex-direction:column}
.stat .big{font-size:46px;font-weight:700;line-height:1}
.stat .mid{font-size:22px;font-weight:600}
.stat .lab{font-size:14px;color:var(--muted);margin-top:4px}
.bar-row{margin-top:18px;display:flex;flex-direction:column;gap:8px}
.bar-lab{display:flex;justify-content:space-between;font-size:14px;color:var(--muted);gap:12px}
.track{height:10px;border-radius:6px;background:#e7ebf0;overflow:hidden;display:flex;gap:3px}
.note{font-size:14px;color:var(--muted)}

.chart-box{overflow-x:auto}
svg text{font-family:var(--font-body)}

.stbars{display:flex;flex-direction:column;gap:4px;margin-top:6px}
.strow{display:grid;grid-template-columns:190px 1fr 60px 64px;align-items:center;gap:14px;width:100%;background:none;border:0;border-radius:8px;padding:6px 8px;font-size:15px;color:inherit;cursor:pointer;text-align:left}
.strow:hover{background:#f3f6fa}
.strow .nm{font-weight:500}
.strow .n{text-align:right;font-weight:600}
.strow .dl{text-align:right;font-weight:600}
.strow .bar{display:flex;height:18px;gap:2px}
.strow .bar span{display:block;height:18px;border-radius:3px}
.strow.susp{border-top:1.5px dashed #c9d1db;border-radius:0;padding-top:12px;margin-top:6px}
.strow.susp .nm small{display:block;font-weight:400;font-size:13px;color:var(--muted)}
@media (max-width:640px){.strow{grid-template-columns:130px 1fr 44px 52px;font-size:14px}}

.mtx-title{font-size:17px;font-weight:600;margin:26px 0 6px}
.tbl-box{overflow-x:auto}
table.mtx{width:100%;border-collapse:collapse;font-size:16px;min-width:640px}
table.mtx th{font-size:14px;font-weight:500;color:var(--muted);padding:10px 12px;border-bottom:1px solid var(--line);text-align:center}
table.mtx td{border-bottom:1px solid var(--line);text-align:center;padding:0}
table.mtx td:first-child,table.mtx th:first-child{text-align:left;padding:12px}
table.mtx td.h{font-weight:600}
table.mtx tr.tot td{font-weight:600;border-top:2px solid #c9d1db;padding:14px 12px}
table.mtx tr.sus td{color:var(--muted)}
table.mtx tr.sus td:first-child small{font-size:13px}
table.mtx .colsel{box-shadow:inset 2px 0 0 var(--c),inset -2px 0 0 var(--c)}
table.mtx th.colsel{color:var(--ink);font-weight:700}
.cellbtn{width:100%;min-height:48px;background:none;border:0;font-size:16px;color:inherit;cursor:pointer}
.cellbtn:hover{text-decoration:underline;text-underline-offset:3px;font-weight:700}
.zero{display:block;min-height:48px;line-height:48px;color:#a3adba}

/* diálogo com a lista de demandas */
dialog{width:min(1180px,96vw);max-height:88vh;border:0;border-radius:16px;padding:22px 24px;box-shadow:0 20px 60px rgba(20,30,45,.3);color:var(--ink)}
dialog::backdrop{background:rgba(20,30,45,.45)}
.dlg-head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap;margin-bottom:10px}
.dlg-head h2{margin:0;font-size:22px}
.dlg-scroll{max-height:62vh;overflow:auto}
table.dtab{width:100%;border-collapse:collapse;min-width:980px;font-size:14px}
table.dtab th{position:sticky;top:0;background:#fff;font-size:13px;font-weight:500;color:var(--muted);text-align:left;padding:10px;border-bottom:1px solid var(--line)}
table.dtab td{padding:9px 10px;border-bottom:1px solid var(--line-soft);vertical-align:top}
table.dtab td.r,table.dtab th.r{text-align:right}
table.dtab td.tt{max-width:340px}
.btn{height:44px;padding:0 18px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink);font-size:15px;cursor:pointer;white-space:nowrap}
.btn.primary{background:var(--ink);color:#fff;border-color:var(--ink);font-weight:600}
.actions{display:flex;gap:10px;flex-wrap:wrap}
.tag{font-size:12.5px;padding:2px 8px;border-radius:99px;white-space:nowrap}
.tag.tl{background:#e3e7ed;color:#3a4556}.tag.ta{background:#e6eefb;color:#2456a8}
.semp{color:#b3261e;font-weight:600;white-space:nowrap}

/* listagem (mesmas colunas e regras de antes, só no tema claro) */
#listagem .table-controls{display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap;align-items:center}
#listagem .table-controls input[type=text],#listagem .table-controls select{border:1px solid var(--line);background:#fff;color:var(--ink);padding:9px 12px;border-radius:8px;font:inherit;font-size:14px;min-height:40px}
#listagem .table-controls input[type=text]{min-width:220px}
#listagem .table-controls select{max-width:340px}
#listagem .chk-wrap{display:flex;align-items:center;gap:7px;font-size:14px;color:var(--muted);margin-left:auto;cursor:pointer;user-select:none}
#listagem .table-count-row{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px;flex-wrap:wrap}
#listagem .table-count{font-size:14px;color:var(--muted)}
#listagem .table-scroll{overflow-x:auto;border:1px solid var(--line);border-radius:12px}
#listagem table{width:100%;border-collapse:collapse;font-size:13px;table-layout:fixed;min-width:1180px}
#listagem thead th{text-align:left;padding:10px 8px;background:#f3f5f8;color:var(--muted);font-size:12.5px;font-weight:500;cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border-bottom:1px solid var(--line);position:sticky;top:0;user-select:none}
#listagem thead th .arrow{opacity:0;margin-left:2px}
#listagem thead th.sorted .arrow{opacity:1;color:var(--NSS1)}
#listagem tbody td{padding:9px 8px;border-bottom:1px solid var(--line-soft);color:#3a4556;white-space:normal;word-break:break-word;overflow:hidden}
#listagem tbody tr:hover{background:#f7f9fb}
#listagem td.titulo{color:var(--ink)}
#listagem td.trunc{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#listagem th:nth-child(1),#listagem td:nth-child(1){width:8%;white-space:nowrap}
#listagem th:nth-child(2),#listagem td:nth-child(2){width:7%}
#listagem th:nth-child(3),#listagem td:nth-child(3){width:20%}
#listagem th:nth-child(4),#listagem td:nth-child(4){width:6%}
#listagem th:nth-child(5),#listagem td:nth-child(5){width:7%}
#listagem th:nth-child(6),#listagem td:nth-child(6){width:11%}
#listagem th:nth-child(7),#listagem td:nth-child(7){width:10%}
#listagem th:nth-child(8),#listagem td:nth-child(8){width:10%}
#listagem th:nth-child(9),#listagem td:nth-child(9){width:5%;white-space:nowrap}
#listagem th:nth-child(10),#listagem td:nth-child(10){width:8%}
#listagem th:nth-child(11),#listagem td:nth-child(11){width:4%}
#listagem th:nth-child(12),#listagem td:nth-child(12){width:4%}
#listagem .status-pill{white-space:nowrap;max-width:100%;overflow:hidden;text-overflow:ellipsis;vertical-align:middle}
.mono{font-variant-numeric:tabular-nums}
.id-sub{font-size:11.5px;color:var(--muted);margin-top:3px;white-space:nowrap}
.badge{display:inline-block;padding:3px 9px;border-radius:20px;font-size:11.5px;font-weight:600;white-space:nowrap}
.badge.on{background:#fbe9e7;color:#b3261e;border:1px solid #f3c5bf}
.badge.off{background:#e4f3ec;color:var(--down);border:1px solid #bfe0cf}
.status-pill{display:inline-block;padding:3px 9px;border-radius:6px;font-size:12px;background:#f0f3f7;color:#3a4556;border:1px solid var(--line)}
.status-pill.suspensa{background:var(--up-bg);color:var(--up);border-color:#f0d2b3;cursor:help}
.dias-cell.old{color:#b3261e;font-weight:600}
.dias-cell.mid{color:var(--up)}
footer.foot{font-size:13px;color:var(--muted);text-align:center}
</style>
</head>
<body>
<div class="wrap">

  <header class="top">
    <div>
      <h1>Backlog GDS-1</h1>
      <div class="sub" id="subColeta">—</div>
    </div>
    <div class="top-meta">
      <div><b id="metaTotalBase">—</b> demandas na base total</div>
      <div><b id="metaTotalBacklog">—</b> em backlog aberto (sem suspensas)</div>
    </div>
  </header>

  <nav class="filter" aria-label="Filtrar por núcleo" id="filter"></nav>

  <section class="panel verdict" id="verdict" aria-live="polite"></section>

  <section class="split">
    <div class="panel card">
      <h2><span class="sw" style="background:var(--legado)"></span>Legado <small id="legSub">abertas antes de 2026</small><span class="ntag" data-ntag></span></h2>
      <div class="stats" id="legStats"></div>
      <div class="bar-row" id="legBar"></div>
    </div>
    <div class="panel card">
      <h2><span class="sw" style="background:var(--atuais)"></span>Atuais <small id="atuSub">abertas em 2026</small><span class="ntag" data-ntag></span></h2>
      <div class="stats" id="atuStats"></div>
      <div class="bar-row" id="atuBar"></div>
    </div>
  </section>

  <section class="panel">
    <div class="panel-head">
      <h2 id="chartTitle">Evolução semanal do backlog aberto</h2>
      <div class="legend" id="chartLegend"></div>
    </div>
    <div class="chart-box" id="chart"></div>
    <div class="note" id="chartNote"></div>
  </section>

  <section class="panel">
    <div class="panel-head">
      <h2 id="stTitle">Por status</h2>
      <div class="legend">
        <span><span class="sw" style="background:var(--legado)"></span>Legado</span>
        <span><span class="sw" style="background:var(--atuais)"></span>Atuais</span>
      </div>
    </div>
    <div class="note" id="stNote"></div>
    <div id="stBars" class="stbars"></div>
    <h3 class="mtx-title">Status por núcleo <span class="sub" style="font-family:var(--font-body);font-weight:400;font-size:14px">(clique num número para ver as demandas)</span></h3>
    <div class="tbl-box"><table class="mtx" id="mtx"></table></div>
  </section>

  <!-- LISTAGEM (mantida) -->
  <section class="panel" id="listagem">
    <div class="panel-head">
      <h2 id="listTitle">Todas as demandas em aberto</h2>
      <div class="note">Clique nos cabeçalhos para ordenar.</div>
    </div>
    <div class="table-controls">
      <input type="text" id="searchInput" placeholder="Buscar por ID ou título…">
      <select id="filterNucleo" aria-label="Núcleo"></select>
      <select id="filterProjeto"></select>
      <select id="filterStatus"></select>
      <label class="chk-wrap"><input type="checkbox" id="filterSemPrazo"> Somente sem prazo</label>
    </div>
    <div class="table-count-row">
      <div class="table-count" id="tableCount"></div>
      <button type="button" class="btn" id="exportCsvBtn">Exportar CSV</button>
    </div>
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th data-key="id">ID<span class="arrow">▾</span></th>
            <th data-key="idNgds">NGDS<span class="arrow">▾</span></th>
            <th data-key="titulo">Título<span class="arrow">▾</span></th>
            <th data-key="nucleoNegocio">Núcleo<span class="arrow">▾</span></th>
            <th data-key="sigla">Projeto<span class="arrow">▾</span></th>
            <th data-key="status">Status<span class="arrow">▾</span></th>
            <th data-key="gerenciaInterna">Gerência (Prodam)<span class="arrow">▾</span></th>
            <th data-key="gestor">Gestor<span class="arrow">▾</span></th>
            <th data-key="diasAberto">Dias<span class="arrow">▾</span></th>
            <th data-key="semPrazo">Prazo<span class="arrow">▾</span></th>
            <th data-key="esfEst">Esf. est.<span class="arrow">▾</span></th>
            <th data-key="esfReal">Esf. real<span class="arrow">▾</span></th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </section>

  <footer class="foot">Recorte: demandas do GDP com status Aberta, Planejamento, Aprovar Planej., Planej. Aprovado, Execução ou Homologação (incluindo expressa e tácita). Suspensas aparecem à parte e não contam no backlog aberto.</footer>
</div>

<dialog id="dlg" aria-labelledby="dlgTitle">
  <div class="dlg-head">
    <div><h2 id="dlgTitle"></h2><div class="sub" id="dlgSub"></div></div>
    <div class="actions">
      <button class="btn" type="button" id="dlgCsv">Exportar CSV desta lista</button>
      <button class="btn primary" type="button" id="dlgClose">Fechar</button>
    </div>
  </div>
  <div class="tbl-box dlg-scroll">
    <table class="dtab">
      <thead><tr><th>ID</th><th>Título</th><th>Núcleo</th><th>Projeto</th><th>Status</th><th>Gestor</th><th class="r">Dias</th><th>Prazo</th><th>Origem</th></tr></thead>
      <tbody id="dlgBody"></tbody>
    </table>
  </div>
</dialog>

<script>
const DATA = __DATA_JSON__;
</script>
<script src="dashboard.js"></script>
</body>
</html>
"""

DASHBOARD_JS = r"""// ---------- Base ----------
const ALL_RECORDS = DATA.records || [];
const HISTORY = DATA.history || [];
const STATUS_HIST = DATA.statusHistory || [];
const WF = (DATA.weeklyFlow && DATA.weeklyFlow.porBloco) ? DATA.weeklyFlow : null;
const status_order = ['Aberta','Planejamento','Aprovar Planej.','Planej. Aprovado','Execução','Homologação','Homolog. Expressa','Homolog. Tácita','Suspensa'];
const STATUS_OPEN = status_order.filter(s=>s!=='Suspensa');
const NUC_ORDER = ['NSS1','NSS2','NSS3','NC'];
const NUCS = NUC_ORDER.filter(n=>(DATA.nucleosNegocio||[]).includes(n))
  .concat((DATA.nucleosNegocio||[]).filter(n=>!NUC_ORDER.includes(n) && n!=='Não classificado'));
const ALL = 'GDS-1';
const colorOf = k => k===ALL ? 'var(--GDS)' : (NUC_ORDER.includes(k) ? `var(--${k})` : 'var(--OUTRO)');
const labelOf = k => k===ALL ? 'GDS-1 (todos)' : k;
const ANO = DATA.anoCorte || new Date().getFullYear();

const fmt = n => Math.round(n).toLocaleString('pt-BR');
const fmt1 = n => n.toLocaleString('pt-BR',{maximumFractionDigits:1});
const fmtD = v => v===null||v===undefined ? '—' : (v===0 ? '= 0' : (v<0 ? '▼ '+fmt(-v) : '▲ '+fmt(v)));
const cls = v => v===null||v===undefined ? '' : (v<0 ? 'good-t' : (v>0 ? 'bad-t' : ''));
const brDate = iso => iso ? String(iso).slice(0,10).split('-').reverse().join('/') : '—';
const shortDate = iso => brDate(iso).slice(0,5);
const esc = s => String(s===null||s===undefined?'':s).replace(/[&<>"]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

let cur = ALL;
try{ const s = localStorage.getItem('gds1-nucleo'); if(s && (s===ALL || NUCS.includes(s))) cur = s; }catch(e){}

const inScope = (r, k) => k===ALL || r.nucleoNegocio===k;
const scopeRecs = k => ALL_RECORDS.filter(r=>inScope(r,k));
const isLeg = r => r.bloco==='passivo';

// ---------- Histórico ----------
function histOf(k){
  return HISTORY.filter(h=>h.nucleo===k)
    .map(h=>({
      date:h.data_snapshot,
      total:+h.backlog_total,
      leg:(h.backlog_legado===undefined||h.backlog_legado===''||h.backlog_legado===null)?null:+h.backlog_legado,
      atu:(h.backlog_atual===undefined||h.backlog_atual===''||h.backlog_atual===null)?null:+h.backlog_atual,
    }))
    .sort((a,b)=>a.date<b.date?-1:1);
}
function streak(vals){
  const L = vals.length-1; if(L<1) return {dir:0,s:0};
  const dir = Math.sign(vals[L]-vals[L-1]); if(!dir) return {dir:0,s:0};
  let s=0; for(let i=L;i>0;i--){ if(Math.sign(vals[i]-vals[i-1])===dir) s++; else break; }
  return {dir,s};
}
// fluxo (entraram/saíram) por bloco — só existe quando a coleta anterior foi restaurada no Passo 0
function flowOf(k, bloco){ return WF && WF.porBloco[k] ? WF.porBloco[k][bloco] : null; }

// ---------- Filtro de núcleo ----------
function renderFilter(){
  const f = document.getElementById('filter'); f.innerHTML='';
  [ALL, ...NUCS].forEach(k=>{
    const b = document.createElement('button'); b.type='button'; b.className='chip';
    b.style.setProperty('--c', colorOf(k)); b.setAttribute('aria-pressed', k===cur);
    b.innerHTML = `<span class="dot" style="background:${colorOf(k)}"></span>${labelOf(k)}`;
    b.onclick = ()=>select(k); f.appendChild(b);
  });
  const hint = document.createElement('span'); hint.className='fhint';
  hint.textContent = cur===ALL
    ? 'Filtra todo o painel e a listagem. A matriz de status mostra sempre todos os núcleos.'
    : `Mostrando só ${cur} no painel e na listagem. Na matriz de status, ${cur} fica destacado.`;
  f.appendChild(hint);
}
function select(k){
  cur = k; try{ localStorage.setItem('gds1-nucleo', k); }catch(e){}
  renderAll();
}

// ---------- Veredito ----------
function renderVerdict(){
  const h = histOf(cur), recs = scopeRecs(cur).filter(r=>!r.suspensa);
  const total = recs.length;
  const L = h.length-1;
  const delta = L>=1 ? h[L].total - h[L-1].total : null;
  const k = streak(h.map(x=>x.total));
  const v = document.getElementById('verdict');
  v.className = 'panel verdict ' + (delta<0 ? 'good' : (delta>0 ? 'bad' : ''));
  let t1;
  if(delta===null) t1 = 'Primeira coleta registrada: a comparação aparece a partir da próxima.';
  else {
    const trend = k.dir<0 ? (k.s>1 ? `backlog diminuindo há ${k.s} semanas seguidas` : 'backlog caiu nesta semana')
                : k.dir>0 ? (k.s>1 ? `backlog crescendo há ${k.s} semanas seguidas` : 'backlog subiu nesta semana')
                : 'backlog estável';
    t1 = `${fmtD(delta)} na semana, ${trend}`;
  }
  let t2;
  const fl = flowOf(cur,'passivo'), fa = flowOf(cur,'corrente');
  if(fl && fa){
    const inn = fl.entraram + fa.entraram, out = fl.sairam + fa.sairam, sus = fl.suspensas + fa.suspensas;
    const dl = fl.atual - fl.anterior, da = fa.atual - fa.anterior;
    const src = (dl===0 && da===0) ? '' : (Math.abs(dl) >= Math.abs(da) ? '; a variação vem principalmente do legado' : '; a variação vem principalmente das demandas de ' + ANO);
    t2 = `${labelOf(cur)}: entraram ${fmt(inn)}, saíram ${fmt(out)}${sus ? ` (${fmt(sus)} por suspensão)` : ''}${src}.`;
  } else {
    t2 = `${labelOf(cur)}: para ver o que entrou e o que saiu, restaure o HTML da coleta anterior no Passo 0 antes de processar.`;
  }
  v.innerHTML = `<div class="num">${fmt(total)}</div><div><div class="t1 ${cls(delta)}">${t1}</div><div class="t2">${t2}</div></div>`;
}

// ---------- Legado x Atuais ----------
function statBlock(n, d, sp){
  return `<div class="stat"><span class="big num">${fmt(n)}</span><span class="lab">em aberto</span></div>`+
         `<div class="stat"><span class="mid ${cls(d)}">${fmtD(d)}</span><span class="lab">${d===null ? 'sem comparação ainda' : 'na semana'}</span></div>`+
         `<div class="stat"><span class="mid">${fmt(sp)}</span><span class="lab">sem prazo</span></div>`;
}
function renderCards(){
  const recs = scopeRecs(cur).filter(r=>!r.suspensa);
  const leg = recs.filter(isLeg), atu = recs.filter(r=>!isLeg(r));
  const h = histOf(cur), L = h.length-1;
  const fl = flowOf(cur,'passivo'), fa = flowOf(cur,'corrente');
  const dLeg = fl ? fl.atual-fl.anterior : (L>=1 && h[L].leg!==null && h[L-1].leg!==null ? h[L].leg-h[L-1].leg : null);
  const dAtu = fa ? fa.atual-fa.anterior : (L>=1 && h[L].atu!==null && h[L-1].atu!==null ? h[L].atu-h[L-1].atu : null);
  document.getElementById('legSub').textContent = `abertas antes de ${ANO}`;
  document.getElementById('atuSub').textContent = `abertas em ${ANO}`;
  document.getElementById('legStats').innerHTML = statBlock(leg.length, dLeg, leg.filter(r=>r.semPrazo).length);
  document.getElementById('atuStats').innerHTML = statBlock(atu.length, dAtu, atu.filter(r=>r.semPrazo).length);

  // limpeza do legado: desde a primeira coleta que já guardou a quebra legado/atual
  const base = h.find(x=>x.leg!==null);
  const lb = document.getElementById('legBar');
  if(base && L>=0 && base.date < h[L].date && base.leg>0){
    const pct = Math.round((base.leg - leg.length)/base.leg*100);
    lb.innerHTML = `<div class="bar-lab"><span>Limpeza do legado desde ${shortDate(base.date)}</span><span>${fmt(base.leg)} → ${fmt(leg.length)} (${pct>=0?'−':'+'}${Math.abs(pct)}%)</span></div>`+
      `<div class="track"><div style="width:${Math.max(0,Math.min(100,pct))}%;background:var(--down);height:10px"></div></div>`;
  } else {
    lb.innerHTML = `<div class="note">A barra de limpeza do legado aparece a partir da próxima coleta.</div>`;
  }
  const ab = document.getElementById('atuBar');
  if(fa){
    ab.innerHTML = `<div class="bar-lab"><span>Fluxo da semana</span><span>entraram ${fmt(fa.entraram)}, saíram ${fmt(fa.sairam)}</span></div>`+
      `<div class="track"><div style="flex-grow:${fa.entraram||0.0001};background:var(--up)"></div><div style="flex-grow:${fa.sairam||0.0001};background:var(--down)"></div></div>`;
  } else {
    ab.innerHTML = `<div class="note">O fluxo da semana aparece quando a coleta anterior é restaurada no Passo 0.</div>`;
  }
  document.querySelectorAll('[data-ntag]').forEach(e=>{
    e.textContent = cur===ALL ? '' : cur; e.style.background = colorOf(cur); e.style.display = cur===ALL ? 'none' : 'inline-block';
  });
}

// ---------- Evolução ----------
function renderChart(){
  const h = histOf(cur).slice(-12);
  document.getElementById('chartTitle').textContent = `Evolução semanal do backlog aberto: ${labelOf(cur)}`;
  const box = document.getElementById('chart');
  const hasSplit = h.some(x=>x.leg!==null), hasTotal = h.some(x=>x.leg===null);
  document.getElementById('chartLegend').innerHTML =
    (hasSplit ? '<span><span class="sw" style="background:var(--legado)"></span>Legado</span><span><span class="sw" style="background:var(--atuais)"></span>Atuais</span>' : '') +
    (hasTotal ? '<span><span class="sw" style="background:var(--total)"></span>Total (antes da divisão)</span>' : '');
  document.getElementById('chartNote').textContent = hasTotal && hasSplit
    ? 'As semanas anteriores ao painel novo guardaram só o total; a divisão legado/atuais vale a partir da primeira coleta processada com ele.' : '';
  if(!h.length){ box.innerHTML = '<div class="note">Ainda não há histórico para este recorte.</div>'; return; }
  const W=1180, H=300, x0=52, x1=W-10, yb=262, top=40;
  const max = Math.max(...h.map(x=>x.total))*1.12 || 1, sc = (yb-top)/max;
  const slot = (x1-x0)/h.length, bw = Math.min(60, slot*0.5);
  const raw = max/4, mag = Math.pow(10, Math.floor(Math.log10(raw))), step = [1,2,2.5,5,10].map(m=>m*mag).find(s=>s>=raw);
  let g='';
  for(let v=0; v<=max; v+=step){
    const y = yb - v*sc;
    g += `<line x1="${x0}" x2="${x1}" y1="${y}" y2="${y}" stroke="#e3e8ee"/><text x="${x0-8}" y="${y+4}" text-anchor="end" font-size="12" fill="#566273">${fmt(v)}</text>`;
  }
  h.forEach((p,i)=>{
    const cx = x0 + slot*i + slot/2, x = cx-bw/2, last = i===h.length-1;
    if(p.leg!==null){
      const hl = p.leg*sc, ha = p.atu*sc;
      g += `<rect x="${x}" y="${yb-hl}" width="${bw}" height="${hl}" rx="3" fill="var(--legado)"><title>Legado: ${p.leg}</title></rect>`;
      g += `<rect x="${x}" y="${yb-hl-ha+2}" width="${bw}" height="${Math.max(ha-2,0)}" rx="3" fill="var(--atuais)"><title>Atuais: ${p.atu}</title></rect>`;
    } else {
      const ht = p.total*sc;
      g += `<rect x="${x}" y="${yb-ht}" width="${bw}" height="${ht}" rx="3" fill="var(--total)"><title>Total: ${p.total}</title></rect>`;
    }
    g += `<text x="${cx}" y="${yb-p.total*sc-8}" text-anchor="middle" font-size="13" font-weight="${last?700:500}" fill="#1b2430">${fmt(p.total)}</text>`;
    g += `<text x="${cx}" y="${yb+20}" text-anchor="middle" font-size="13" fill="${last?'#1b2430':'#566273'}" font-weight="${last?600:400}">${shortDate(p.date)}</text>`;
  });
  box.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="min-width:640px" role="img" aria-label="Backlog aberto por semana, ${labelOf(cur)}">${g}</svg>`;
}

// ---------- Status ----------
function statusPrev(k){
  // contagem por status na coleta anterior (histórico por status); null se ainda não houver
  const snap = DATA.snapshotDate;
  const dates = [...new Set(STATUS_HIST.map(r=>r.data_snapshot))].filter(d=>d<snap).sort();
  if(!dates.length) return null;
  const prevD = dates[dates.length-1], out = {};
  STATUS_HIST.filter(r=>r.data_snapshot===prevD && r.nucleo===k).forEach(r=>out[r.status]=+r.count);
  return out;
}
function renderStatus(){
  document.getElementById('stTitle').textContent = `Por status: ${labelOf(cur)}`;
  const recs = scopeRecs(cur), prev = statusPrev(cur);
  document.getElementById('stNote').textContent = prev ? '' : 'A variação por status na semana aparece a partir da próxima coleta.';
  const rowsData = status_order.map(st=>{
    const rs = recs.filter(r=>r.status===st);
    return {st, leg:rs.filter(isLeg).length, atu:rs.filter(r=>!isLeg(r)).length, n:rs.length, d: prev ? rs.length-(prev[st]||0) : null};
  });
  const mx = Math.max(1, ...rowsData.map(r=>r.n));
  document.getElementById('stBars').innerHTML = rowsData.map(r=>{
    const susp = r.st==='Suspensa';
    return `<button type="button" class="strow${susp?' susp':''}" data-st="${esc(r.st)}">`+
      `<span class="nm">${r.st}${susp?'<small>fora do backlog aberto</small>':''}</span>`+
      (susp
        ? `<span class="bar"><span style="width:${r.n/mx*100}%;background:repeating-linear-gradient(45deg,#8a95a5 0 4px,#c9d1db 4px 8px)"></span></span>`
        : `<span class="bar" title="Legado ${r.leg}, atuais ${r.atu}"><span style="width:${r.leg/mx*100}%;background:var(--legado)"></span><span style="width:${r.atu/mx*100}%;background:var(--atuais)"></span></span>`)+
      `<span class="n">${fmt(r.n)}</span><span class="dl ${susp?'':cls(r.d)}">${fmtD(r.d)}</span></button>`;
  }).join('');
  document.querySelectorAll('#stBars .strow').forEach(b=>b.onclick=()=>openList(cur, b.dataset.st));
  renderMatrix();
}
function renderMatrix(){
  const cols = [...NUCS, ALL];
  const count = (k, st) => ALL_RECORDS.filter(r=>inScope(r,k) && r.status===st).length;
  const cells = []; NUCS.forEach(n=>STATUS_OPEN.forEach(st=>cells.push(count(n,st))));
  const cmax = Math.max(1, ...cells);
  const heat = v => `rgba(47,111,216,${(0.06+0.34*v/cmax).toFixed(2)})`;
  const sel = c => cur!==ALL && c===cur;
  const selAttr = c => sel(c) ? ` class="colsel" style="--c:${colorOf(c)}"` : '';
  const cell = (c, st, bgOn) => {
    const v = count(c, st), bg = (bgOn && c!==ALL) ? `background:${heat(v)};` : '';
    const inner = v ? `<button type="button" class="cellbtn" data-c="${c}" data-st="${esc(st)}" aria-label="Abrir ${v} demandas ${esc(st)} de ${c}">${fmt(v)}</button>` : '<span class="zero">0</span>';
    return `<td class="${c===ALL?'h':''} ${sel(c)?'colsel':''}" style="${bg}${sel(c)?'--c:'+colorOf(c):''}">${inner}</td>`;
  };
  let m = `<thead><tr><th>Status</th>${cols.map(c=>`<th${selAttr(c)}>${c}</th>`).join('')}</tr></thead><tbody>`;
  STATUS_OPEN.forEach(st=>{ m += `<tr><td>${st}</td>${cols.map(c=>cell(c,st,true)).join('')}</tr>`; });
  m += `<tr class="tot"><td>Backlog aberto</td>${cols.map(c=>`<td${selAttr(c)}>${fmt(ALL_RECORDS.filter(r=>inScope(r,c) && !r.suspensa).length)}</td>`).join('')}</tr>`;
  m += `<tr class="sus"><td>Suspensa <small>(fora do backlog)</small></td>${cols.map(c=>cell(c,'Suspensa',false)).join('')}</tr></tbody>`;
  const t = document.getElementById('mtx'); t.innerHTML = m;
  t.querySelectorAll('.cellbtn').forEach(b=>b.onclick=()=>openList(b.dataset.c, b.dataset.st));
}

// ---------- Lista de demandas (diálogo) ----------
let dlgRows = [], dlgTag = '';
function openList(k, st){
  dlgRows = ALL_RECORDS.filter(r=>inScope(r,k) && r.status===st).sort((a,b)=>(b.diasAberto||0)-(a.diasAberto||0));
  dlgTag = `${k}_${st}`;
  document.getElementById('dlgTitle').textContent = `${st}: ${labelOf(k)}`;
  const nl = dlgRows.filter(isLeg).length, ns = dlgRows.filter(r=>r.semPrazo).length;
  document.getElementById('dlgSub').textContent = `${fmt(dlgRows.length)} demandas, ${fmt(nl)} do legado e ${fmt(dlgRows.length-nl)} de ${ANO}; ${fmt(ns)} sem prazo`;
  document.getElementById('dlgBody').innerHTML = dlgRows.map(r=>{
    const stCell = r.suspensa ? `Suspensa<div class="id-sub">real: ${esc(r.statusReal)}</div>` : esc(r.status);
    return `<tr><td class="mono">${esc(r.id)}<div class="id-sub">${esc(r.dataCriacao||'—')}</div></td>`+
      `<td class="tt">${esc(r.titulo)}</td><td>${esc(r.nucleoNegocio)}</td><td>${esc(r.sigla)}</td><td>${stCell}</td>`+
      `<td>${esc(r.gestor)}</td><td class="r">${r.diasAberto ?? '—'}</td>`+
      `<td>${r.semPrazo ? '<span class="semp">sem prazo</span>' : esc(r.dtFimPrevisto || 'definido')}</td>`+
      `<td><span class="tag ${isLeg(r)?'tl':'ta'}">${isLeg(r)?'Legado':ANO}</span></td></tr>`;
  }).join('');
  const d = document.getElementById('dlg');
  if(d.showModal) d.showModal(); else d.setAttribute('open','');
}

// ---------- Listagem (mantida) ----------
function getGloballyFiltered(){ return scopeRecs(cur); }
let sortKey='diasAberto', sortDir=-1;
function populateTableFilters(){
  document.getElementById('filterNucleo').innerHTML = '<option value="">Todos os núcleos</option>' + NUCS.map(n=>`<option value="${n}">${n}</option>`).join('');
  document.getElementById('filterStatus').innerHTML = '<option value="">Todos os status</option>' + status_order.map(s=>`<option value="${s}">${s}</option>`).join('');
  refreshTableProjetos();
}
function refreshTableProjetos(){
  const sel = document.getElementById('filterProjeto'), current = sel.value;
  const opts = cur===ALL ? (DATA.projetos||[]) : ((DATA.projetoPorNucleo||{})[cur] || []);
  sel.innerHTML = '<option value="">Todos os projetos</option>' + opts.map(p=>`<option value="${esc(p)}">${esc(p)}</option>`).join('');
  if(opts.includes(current)) sel.value = current;
}
function getTableRows(baseRecs){
  const q = document.getElementById('searchInput').value.trim().toLowerCase();
  const proj = document.getElementById('filterProjeto').value;
  const st = document.getElementById('filterStatus').value;
  const onlySemPrazo = document.getElementById('filterSemPrazo').checked;
  let rows = baseRecs.filter(r=>{
    if(proj && r.projeto!==proj) return false;
    if(st && r.status!==st) return false;
    if(onlySemPrazo && !r.semPrazo) return false;
    if(q && !(String(r.id).includes(q) || (r.titulo||'').toLowerCase().includes(q))) return false;
    return true;
  });
  rows.sort((a,b)=>{
    let va=a[sortKey], vb=b[sortKey];
    if(va===null||va===undefined) va = typeof vb==='number' ? -Infinity : '';
    if(vb===null||vb===undefined) vb = typeof va==='number' ? -Infinity : '';
    if(typeof va==='string') va=va.toLowerCase();
    if(typeof vb==='string') vb=vb.toLowerCase();
    if(va<vb) return -1*sortDir;
    if(va>vb) return 1*sortDir;
    return 0;
  });
  return rows;
}
function renderTable(){
  document.getElementById('filterNucleo').value = cur===ALL ? '' : cur;
  const baseRecs = getGloballyFiltered();
  const rows = getTableRows(baseRecs);
  document.getElementById('listTitle').textContent = cur===ALL ? 'Todas as demandas em aberto' : `Demandas em aberto: ${cur}`;
  document.getElementById('tableCount').textContent = `${fmt(rows.length)} de ${fmt(baseRecs.length)} demandas no recorte atual`;
  document.getElementById('tableBody').innerHTML = rows.map(r=>{
    const diasCls = r.diasAberto>730 ? 'old' : (r.diasAberto>365 ? 'mid':'');
    const statusCell = r.suspensa
      ? (()=>{
          const partes = [`Status real: ${r.statusReal}`];
          if(r.motivoSuspensao) partes.push(r.motivoSuspensao);
          if(r.dtInicioSuspensao) partes.push(`suspensa desde ${r.dtInicioSuspensao}`);
          return `<span class="status-pill suspensa" title="${esc(partes.join(' — '))}">${esc(r.status)}</span>`;
        })()
      : `<span class="status-pill">${esc(r.status)}</span>`;
    return `
    <tr>
      <td class="mono">${esc(r.id)}<div class="id-sub">${esc(r.dataCriacao || '—')}</div></td>
      <td class="mono">${esc(r.idNgds || '—')}</td>
      <td class="titulo">${esc(r.titulo)}</td>
      <td><span class="status-pill">${esc(r.nucleoNegocio)}</span></td>
      <td class="mono">${esc(r.sigla)}</td>
      <td>${statusCell}</td>
      <td class="trunc" title="${esc(r.gerenciaInterna)}">${esc(r.gerenciaInterna)}</td>
      <td class="trunc" title="${esc(r.gestor)}">${esc(r.gestor)}</td>
      <td class="mono dias-cell ${diasCls}">${r.diasAberto ?? '—'}</td>
      <td>${r.semPrazo ? '<span class="badge on">SEM PRAZO</span>' : '<span class="badge off">definido</span>'}</td>
      <td class="mono">${r.esfEst ? fmt1(r.esfEst) : '—'}</td>
      <td class="mono">${r.esfReal ? fmt1(r.esfReal) : '—'}</td>
    </tr>`;
  }).join('');
  document.querySelectorAll('#listagem thead th').forEach(th=>{
    th.classList.toggle('sorted', th.dataset.key===sortKey);
    const arrow = th.querySelector('.arrow');
    if(th.dataset.key===sortKey) arrow.textContent = sortDir===1?'▴':'▾';
  });
}

// ---------- CSV (mesmo formato de antes) ----------
function csvEscape(v){
  const s = (v===null||v===undefined) ? '' : String(v);
  return /[";\n]/.test(s) ? '"' + s.replace(/"/g,'""') + '"' : s;
}
function exportRowsCSV(rows, sufixo){
  const header = ['ID','NGDS','Data criação','Título','Núcleo','Projeto','Status','Status real','Gerência (Prodam)','Gestor','Dias aberto','Prazo','Esf. estimado','Esf. realizado','Suspensa','Motivo suspensão','Início suspensão'];
  const lines = [header.map(csvEscape).join(';')];
  rows.forEach(r=>{
    lines.push([
      r.id, r.idNgds || '', r.dataCriacao || '', r.titulo, r.nucleoNegocio, r.sigla, r.status, r.statusReal,
      r.gerenciaInterna, r.gestor, r.diasAberto ?? '', r.semPrazo ? 'SEM PRAZO' : 'definido',
      r.esfEst ?? '', r.esfReal ?? '', r.suspensa ? 'Sim' : 'Não', r.motivoSuspensao || '', r.dtInicioSuspensao || ''
    ].map(csvEscape).join(';'));
  });
  const blob = new Blob(['\ufeff' + lines.join('\r\n')], {type:'text/csv;charset=utf-8;'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  const dataRef = (DATA.snapshotDate || new Date().toISOString().slice(0,10));
  a.href = url;
  a.download = `backlog_gds1_${sufixo}_${dataRef}.csv`.replace(/[^\w.\-]+/g,'_');
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
function exportTableCSV(){
  exportRowsCSV(getTableRows(getGloballyFiltered()), cur===ALL ? 'detalhamento' : `detalhamento_${cur}`);
}

// ---------- Master render ----------
function renderHeader(){
  const dates = [...new Set(HISTORY.map(h=>h.data_snapshot))].sort();
  const snap = DATA.snapshotDate;
  const prev = dates.filter(d=>d<snap).pop();
  document.getElementById('subColeta').textContent = prev
    ? `Coleta de ${brDate(snap)}, comparada com ${brDate(prev)}`
    : `Coleta de ${brDate(snap)}`;
  document.getElementById('metaTotalBase').textContent = fmt(DATA.totalBaseGeral || 0);
  document.getElementById('metaTotalBacklog').textContent = fmt(ALL_RECORDS.filter(r=>!r.suspensa).length);
}
function renderAll(){
  renderFilter();
  renderVerdict();
  renderCards();
  renderChart();
  renderStatus();
  refreshTableProjetos();
  renderTable();
}
function init(){
  renderHeader();
  populateTableFilters();
  document.querySelectorAll('#listagem thead th').forEach(th=>{
    th.addEventListener('click',()=>{
      const key = th.dataset.key;
      if(sortKey===key){ sortDir*=-1; } else { sortKey=key; sortDir = ['titulo','gerenciaInterna','gestor','status','sigla','nucleoNegocio'].includes(key) ? 1 : -1; }
      renderTable();
    });
  });
  ['searchInput','filterProjeto','filterStatus','filterSemPrazo'].forEach(id=>{
    document.getElementById(id).addEventListener('input', renderTable);
    document.getElementById(id).addEventListener('change', renderTable);
  });
  document.getElementById('exportCsvBtn').addEventListener('click', exportTableCSV);
  // o núcleo da listagem é o mesmo filtro do topo: mudar aqui muda o painel inteiro
  document.getElementById('filterNucleo').addEventListener('change', e=>select(e.target.value || ALL));
  const d = document.getElementById('dlg');
  document.getElementById('dlgClose').onclick = ()=>{ if(d.close) d.close(); else d.removeAttribute('open'); };
  d.addEventListener('click', e=>{ if(e.target===d && d.close) d.close(); });
  document.getElementById('dlgCsv').onclick = ()=>exportRowsCSV(dlgRows, dlgTag);
  renderAll();
}
init();
"""


def build_dashboard_html(dataset: dict, history_rows: list, weekly_flow=None, status_history_rows: list = None) -> str:
    data = dict(dataset)
    data['history'] = history_rows
    data['statusHistory'] = status_history_rows or []
    # comparativo com a coleta anterior (entraram/saíram por legado x atuais);
    # só existe quando o HTML anterior foi restaurado no Passo 0.
    if weekly_flow:
        data['weeklyFlow'] = weekly_flow
    # '</' escapado para um título de demanda nunca fechar a tag <script> antes da hora
    data_json = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')

    html = DASHBOARD_HTML.replace("const DATA = __DATA_JSON__;", f"const DATA = {data_json};")
    html = html.replace('<script src="dashboard.js"></script>', f"<script>\n{DASHBOARD_JS}\n</script>")
    return html
