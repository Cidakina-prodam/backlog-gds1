"""
Templates do dashboard (HTML + JS) embutidos como strings — assim o
projeto inteiro fica em arquivos soltos na raiz do repositório, sem
depender de nenhuma subpasta (evita o problema de upload de pasta no
GitHub pelo navegador).
"""
import json

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SIGA Saúde SH0768 · Backlog Aberto</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0b0e13;
  --bg-panel:#12171f;
  --bg-panel-2:#171d26;
  --bg-raised:#1c2430;
  --border:#252e3a;
  --border-soft:#1a222c;
  --text:#eaeef3;
  --text-dim:#a7b2c2;
  --text-mute:#7d8b9c;
  --accent:#4f8cf7;
  --accent-dim:#2c4a7c;
  --amber:#e8a23c;
  --amber-dim:#4a3a1e;
  --red:#e2523d;
  --red-dim:#4a231e;
  --teal:#31b596;
  --teal-dim:#1c4038;
  --font-display:'Space Grotesk',sans-serif;
  --font-body:'IBM Plex Sans',sans-serif;
  --font-mono:'IBM Plex Mono',monospace;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{
  background:var(--bg);
  color:var(--text);
  font-family:var(--font-body);
  line-height:1.5;
  -webkit-font-smoothing:antialiased;
  background-image:
    radial-gradient(circle at 15% 0%, rgba(79,140,247,0.06), transparent 40%),
    radial-gradient(circle at 85% 10%, rgba(226,82,61,0.05), transparent 35%);
}
.wrap{max-width:1180px;margin:0 auto;padding:0 28px 80px;}

/* ---------- HEADER ---------- */
header.top{
  display:flex;justify-content:space-between;align-items:flex-end;
  padding:36px 0 22px;border-bottom:1px solid var(--border-soft);margin-bottom:36px;
  flex-wrap:wrap;gap:16px;
}
.top-id{
  font-family:var(--font-mono);font-size:12px;letter-spacing:.12em;color:var(--accent);
  text-transform:uppercase;margin-bottom:8px;display:flex;align-items:center;gap:8px;
}
.top-id .dot{width:6px;height:6px;border-radius:50%;background:var(--accent);display:inline-block;box-shadow:0 0 8px var(--accent);}
h1{font-family:var(--font-display);font-weight:600;font-size:30px;letter-spacing:-0.01em;color:var(--text);}
.top-sub{color:var(--text-dim);font-size:14px;margin-top:6px;max-width:520px;}
.top-meta{text-align:right;font-family:var(--font-mono);font-size:12px;color:var(--text-mute);line-height:1.7;}
.top-meta b{color:var(--text-dim);font-weight:500;}

/* ---------- HERO ---------- */
.hero{
  display:grid;grid-template-columns:1.15fr 0.85fr;gap:0;
  border:1px solid var(--border);border-radius:14px;overflow:hidden;
  background:var(--bg-panel);margin-bottom:20px;
}
.hero-left{padding:34px 36px;border-right:1px solid var(--border);}
.hero-eyebrow{font-family:var(--font-mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--red);margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.hero-eyebrow::before{content:'';width:8px;height:8px;background:var(--red);border-radius:2px;transform:rotate(45deg);}
.hero-stat{font-family:var(--font-display);font-weight:700;font-size:64px;line-height:1;letter-spacing:-0.02em;color:var(--text);margin-bottom:4px;}
.hero-stat span{color:var(--amber);}
.hero-stat-label{font-size:15px;color:var(--text-dim);margin-bottom:20px;max-width:460px;}
.hero-desc{font-size:13.5px;color:var(--text-dim);line-height:1.65;max-width:480px;border-top:1px solid var(--border-soft);padding-top:16px;}
.hero-desc b{color:var(--text);font-weight:600;}

.hero-right{padding:34px 30px;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;background:var(--bg-panel-2);}
.gauge-wrap{position:relative;width:100%;max-width:260px;}
.gauge-caption{text-align:center;margin-top:2px;font-family:var(--font-mono);font-size:12px;color:var(--text-mute);letter-spacing:.06em;}
.gauge-legend{display:flex;justify-content:center;gap:16px;margin-top:14px;font-size:12px;color:var(--text-mute);font-family:var(--font-mono);}
.gauge-legend span{display:flex;align-items:center;gap:5px;}
.gauge-legend i{width:7px;height:7px;border-radius:2px;display:inline-block;}

/* ---------- KPI STRIP ---------- */
.kpi-strip{
  display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
  background:var(--border);border:1px solid var(--border);border-radius:14px;overflow:hidden;
  margin-bottom:56px;
}
.kpi{background:var(--bg-panel);padding:20px 22px;}
.kpi-label{font-size:12px;color:var(--text-mute);text-transform:uppercase;letter-spacing:.08em;font-family:var(--font-mono);margin-bottom:10px;}
.kpi-value{font-family:var(--font-display);font-size:26px;font-weight:600;color:var(--text);}
.kpi-value small{font-size:13px;color:var(--text-dim);font-weight:500;font-family:var(--font-body);}
.kpi-sub{font-size:11.5px;color:var(--text-mute);margin-top:4px;}
.kpi.warn .kpi-value{color:var(--amber);}
.kpi.crit .kpi-value{color:var(--red);}

/* ---------- SECTIONS ---------- */
section.block{margin-bottom:56px;}
.block-head{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:20px;flex-wrap:wrap;gap:8px;}
.block-num{font-family:var(--font-mono);font-size:12px;color:var(--text-mute);letter-spacing:.1em;}
.block-title{font-family:var(--font-display);font-size:19px;font-weight:600;color:var(--text);margin-top:4px;}
.block-note{font-size:12.5px;color:var(--text-mute);max-width:420px;text-align:right;}
.panel{background:var(--bg-panel);border:1px solid var(--border);border-radius:14px;padding:26px 28px;}

/* funil */
.funil-row{display:grid;grid-template-columns:150px 1fr 60px;align-items:center;gap:14px;padding:9px 0;}
.funil-row .lbl{font-size:13px;color:var(--text-dim);font-family:var(--font-mono);}
.funil-track{height:22px;background:var(--bg-raised);border-radius:5px;overflow:hidden;position:relative;}
.funil-fill{height:100%;border-radius:5px;background:linear-gradient(90deg,var(--accent-dim),var(--accent));transition:width .6s ease;}
.funil-count{font-family:var(--font-mono);font-size:13px;color:var(--text);text-align:right;font-weight:600;}

/* risk grid */
.risk-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;}
.risk-col-title{font-size:12px;color:var(--text-mute);font-family:var(--font-mono);text-transform:uppercase;letter-spacing:.08em;margin-bottom:16px;}
.risk-item{margin-bottom:16px;}
.risk-item:last-child{margin-bottom:0;}
.risk-top{display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:6px;}
.risk-name{color:var(--text-dim);max-width:210px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.risk-pct{font-family:var(--font-mono);font-weight:600;}
.risk-track{height:8px;background:var(--bg-raised);border-radius:4px;overflow:hidden;display:flex;}
.risk-fill{height:100%;}
.risk-meta{font-family:var(--font-mono);font-size:11.5px;color:var(--text-mute);margin-top:4px;}

/* aging */
.aging-chart{display:flex;align-items:flex-end;gap:16px;height:190px;padding-top:10px;}
.aging-bar-wrap{flex:1;display:flex;flex-direction:column;align-items:center;height:100%;justify-content:flex-end;}
.aging-count{font-family:var(--font-mono);font-size:15px;font-weight:600;margin-bottom:8px;}
.aging-bar{width:100%;border-radius:6px 6px 0 0;min-height:26px;position:relative;display:flex;align-items:flex-start;justify-content:center;padding-top:8px;}
.aging-bar .aging-pct{font-family:var(--font-mono);font-size:12px;font-weight:600;color:rgba(11,14,19,.78);}
.aging-label{margin-top:10px;font-size:11.5px;color:var(--text-mute);font-family:var(--font-mono);text-align:center;}
.aging-flag{font-size:12px;color:var(--red);background:var(--red-dim);border:1px solid rgba(226,82,61,.3);padding:12px 16px;border-radius:8px;margin-top:20px;}

/* evolução */
.evol-legend{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:18px;}
.evol-legend .li{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--text-dim);font-family:var(--font-mono);cursor:pointer;user-select:none;opacity:1;transition:opacity .15s;}
.evol-legend .li.off{opacity:.35;}
.evol-legend .li i{width:16px;height:3px;border-radius:2px;display:inline-block;}
.evol-chart-wrap{width:100%;}
.evol-empty{text-align:center;padding:30px 10px;color:var(--text-mute);font-size:13px;line-height:1.7;}
.evol-empty b{color:var(--text-dim);}

/* fluxo semanal */
.flow-filter-bar{display:flex;align-items:center;gap:12px;margin-bottom:22px;}
.flow-filter-bar .fb-label{font-family:var(--font-mono);font-size:12px;color:var(--text-mute);text-transform:uppercase;letter-spacing:.08em;}
.flow-filter-bar select{
  background:var(--bg-raised);border:1px solid var(--border);color:var(--text);
  padding:8px 12px;border-radius:7px;font-family:var(--font-body);font-size:13px;min-width:200px;
}
.flow-empty{text-align:center;padding:30px 10px;color:var(--text-mute);font-size:13px;line-height:1.7;}
.flow-empty b{color:var(--text-dim);}
.flow-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:12px;overflow:hidden;margin-bottom:26px;}
.flow-card{background:var(--bg-panel);padding:18px 20px;}
.flow-card-label{font-size:12px;color:var(--text-mute);text-transform:uppercase;letter-spacing:.08em;font-family:var(--font-mono);margin-bottom:8px;}
.flow-card-value{font-family:var(--font-display);font-size:24px;font-weight:600;color:var(--text);}
.flow-card.novas .flow-card-value{color:var(--amber);}
.flow-card.saidas .flow-card-value{color:var(--teal);}
.flow-card.mudou .flow-card-value{color:var(--accent);}
.flow-card-sub{font-size:12px;color:var(--text-mute);margin-top:4px;}
.flow-subtitle{font-size:12px;color:var(--text-mute);font-family:var(--font-mono);text-transform:uppercase;letter-spacing:.08em;margin:26px 0 14px;}
.flow-subtitle:first-child{margin-top:0;}
.flow-nucleo-table{width:100%;border-collapse:collapse;font-size:12.5px;margin-bottom:8px;}
.flow-nucleo-table th{text-align:left;padding:8px 10px;color:var(--text-mute);font-family:var(--font-mono);font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid var(--border);}
.flow-nucleo-table th:not(:first-child),.flow-nucleo-table td:not(:first-child){text-align:right;}
.flow-nucleo-table td{padding:9px 10px;border-bottom:1px solid var(--border-soft);color:var(--text-dim);}
.flow-nucleo-table td.nuc-name{color:var(--text);font-weight:500;text-align:left;}
.flow-nucleo-table td.saldo-pos{color:var(--red);font-weight:600;}
.flow-nucleo-table td.saldo-neg{color:var(--teal);font-weight:600;}
.flow-nucleo-table td.saldo-zero{color:var(--text-mute);}
.flow-trans-row{display:grid;grid-template-columns:230px 1fr 46px;align-items:center;gap:14px;padding:8px 0;}
.flow-trans-lbl{font-size:12.5px;color:var(--text-dim);font-family:var(--font-mono);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.flow-trans-lbl b{color:var(--text);font-weight:600;}
.flow-trans-track{height:18px;background:var(--bg-raised);border-radius:5px;overflow:hidden;}
.flow-trans-fill{height:100%;border-radius:5px;background:linear-gradient(90deg,var(--teal-dim),var(--teal));}
.flow-trans-fill.backward{background:linear-gradient(90deg,var(--red-dim),var(--red));}
.flow-trans-count{font-family:var(--font-mono);font-size:12.5px;color:var(--text);text-align:right;font-weight:600;}
@media (max-width:820px){
  .flow-cards{grid-template-columns:1fr 1fr;}
  .flow-trans-row{grid-template-columns:1fr;gap:4px;}
  .flow-trans-count{text-align:left;}
}

/* filtro de núcleo local, dentro de uma seção (Pipeline / Aging / Esforço) */
.section-filter-bar{display:flex;align-items:center;gap:10px;margin-bottom:14px;}
.section-filter-bar .fb-label{font-family:var(--font-mono);font-size:12px;color:var(--text-mute);text-transform:uppercase;letter-spacing:.08em;}
.section-filter-bar select{
  background:var(--bg-raised);border:1px solid var(--border);color:var(--text);
  padding:7px 12px;border-radius:7px;font-family:var(--font-body);font-size:13px;min-width:180px;
}

/* global filter bar */
.filter-bar{
  display:flex;align-items:center;gap:12px;flex-wrap:wrap;
  background:var(--bg-panel);border:1px solid var(--border);border-radius:12px;
  padding:14px 18px;margin-bottom:28px;
}
.filter-bar .fb-label{font-family:var(--font-mono);font-size:12px;color:var(--text-mute);text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:center;gap:6px;}
.filter-bar select{
  background:var(--bg-raised);border:1px solid var(--border);color:var(--text);
  padding:8px 12px;border-radius:7px;font-family:var(--font-body);font-size:13px;min-width:200px;
}
.filter-bar .fb-clear{
  font-family:var(--font-mono);font-size:11.5px;color:var(--accent);cursor:pointer;
  background:none;border:1px solid var(--accent-dim);padding:8px 12px;border-radius:7px;
}
.filter-bar .fb-clear:hover{background:var(--accent-dim);}
.filter-bar .fb-count{margin-left:auto;font-family:var(--font-mono);font-size:11.5px;color:var(--text-dim);}
.filter-bar .fb-count b{color:var(--text);}

/* effort table mini */
.effort-list{display:flex;flex-direction:column;gap:0;}
.effort-row{display:grid;grid-template-columns:1fr 110px 110px 90px;gap:12px;align-items:center;padding:10px 0;border-bottom:1px solid var(--border-soft);font-size:12.5px;}
.effort-row:last-child{border-bottom:none;}
.effort-title{color:var(--text-dim);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.effort-bar-mini{height:6px;background:var(--bg-raised);border-radius:3px;overflow:hidden;position:relative;}
.effort-bar-mini .est{position:absolute;top:0;left:0;height:100%;background:var(--text-mute);}
.effort-bar-mini .real{position:absolute;top:0;left:0;height:100%;background:var(--red);}
.effort-num{font-family:var(--font-mono);text-align:right;color:var(--text-dim);}
.effort-delta{font-family:var(--font-mono);text-align:right;color:var(--red);font-weight:600;}
.effort-head{display:grid;grid-template-columns:1fr 110px 110px 90px;gap:12px;font-family:var(--font-mono);font-size:11.5px;color:var(--text-mute);text-transform:uppercase;letter-spacing:.06em;padding-bottom:10px;border-bottom:1px solid var(--border);margin-bottom:2px;}
.effort-head span:not(:first-child){text-align:right;}

/* table */
.table-controls{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;align-items:center;}
.table-controls input[type=text]{
  background:var(--bg-raised);border:1px solid var(--border);color:var(--text);
  padding:9px 12px;border-radius:7px;font-family:var(--font-body);font-size:13px;min-width:220px;
}
.table-controls select{
  background:var(--bg-raised);border:1px solid var(--border);color:var(--text-dim);
  padding:9px 12px;border-radius:7px;font-family:var(--font-body);font-size:13px;
}
.chk-wrap{display:flex;align-items:center;gap:7px;font-size:12.5px;color:var(--text-dim);margin-left:auto;cursor:pointer;user-select:none;}
.chk-wrap input{accent-color:var(--amber);width:14px;height:14px;}
.table-count{font-family:var(--font-mono);font-size:11.5px;color:var(--text-mute);margin-bottom:12px;}
.table-scroll{overflow-x:auto;border:1px solid var(--border);border-radius:12px;}
table{width:100%;border-collapse:collapse;font-size:12.5px;table-layout:fixed;}
thead th{
  text-align:left;padding:10px 8px;background:var(--bg-raised);color:var(--text-mute);
  font-family:var(--font-mono);font-size:11px;text-transform:uppercase;letter-spacing:.03em;
  cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border-bottom:1px solid var(--border);position:sticky;top:0;
  user-select:none;
}
thead th:hover{color:var(--text-dim);}
thead th .arrow{opacity:0;margin-left:2px;}
thead th.sorted .arrow{opacity:1;color:var(--accent);}
tbody td{padding:9px 8px;border-bottom:1px solid var(--border-soft);color:var(--text-dim);white-space:normal;word-break:break-word;overflow:hidden;}
tbody tr:last-child td{border-bottom:none;}
tbody tr:hover{background:rgba(255,255,255,0.02);}
td.titulo{white-space:normal;color:var(--text);font-size:12.5px;}
td.trunc{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}

/* larguras proporcionais das colunas — somam 100% para caber sem scroll */
th:nth-child(1),td:nth-child(1){width:7%;}
th:nth-child(2),td:nth-child(2){width:19%;}
th:nth-child(3),td:nth-child(3){width:6%;}
th:nth-child(4),td:nth-child(4){width:7%;}
th:nth-child(5),td:nth-child(5){width:9%;}
th:nth-child(6),td:nth-child(6){width:14%;}
th:nth-child(7),td:nth-child(7){width:11%;}
th:nth-child(8),td:nth-child(8){width:7%;}
th:nth-child(9),td:nth-child(9){width:8%;}
th:nth-child(10),td:nth-child(10){width:6%;}
th:nth-child(11),td:nth-child(11){width:6%;}
td.mono{font-family:var(--font-mono);color:var(--text-dim);}
.id-sub{font-size:11px;color:var(--text-mute);margin-top:3px;font-family:var(--font-mono);}
.badge{display:inline-block;padding:3px 9px;border-radius:20px;font-size:11.5px;font-family:var(--font-mono);font-weight:600;letter-spacing:.02em;}
.badge.on{background:rgba(226,82,61,.15);color:var(--red);border:1px solid rgba(226,82,61,.3);}
.badge.off{background:rgba(49,181,150,.12);color:var(--teal);border:1px solid rgba(49,181,150,.25);}
.status-pill{display:inline-block;padding:3px 9px;border-radius:6px;font-size:11px;background:var(--bg-raised);color:var(--text-dim);border:1px solid var(--border);}
.dias-cell.old{color:var(--red);font-weight:600;}
.dias-cell.mid{color:var(--amber);}

footer{margin-top:60px;padding-top:20px;border-top:1px solid var(--border-soft);font-size:11.5px;color:var(--text-mute);font-family:var(--font-mono);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;}

@media (max-width:1000px){
  .risk-grid{grid-template-columns:1fr 1fr;}
}
@media (max-width:820px){
  .hero{grid-template-columns:1fr;}
  .hero-left{border-right:none;border-bottom:1px solid var(--border);}
  .kpi-strip{grid-template-columns:1fr 1fr;}
  .risk-grid{grid-template-columns:1fr;}
  .filter-bar select{min-width:150px;flex:1;}
  .filter-bar .fb-count{margin-left:0;width:100%;}
  .aging-chart{gap:8px;}
  .effort-row,.effort-head{grid-template-columns:1fr 70px 70px;}
  .effort-row .effort-delta{display:none;}
  .effort-head span:nth-child(4){display:none;}
}
</style>
</head>
<body>
<div class="wrap">

  <header class="top">
    <div>
      <h1>Backlog GDS-1</h1>
      <div class="top-sub">Consolidado das demandas ativas do núcleo (SMS / PRODAM), extraídas do ExportaçãoDemanda de cada projeto.</div>
    </div>
    <div class="top-meta">
      <div><b id="metaTotalBase">—</b> demandas na base total</div>
      <div><b id="metaTotalBacklog">—</b> em backlog aberto</div>
      <div>Gerado em <span id="metaGeradoEm">—</span></div>
    </div>
  </header>

  <!-- FILTROS GLOBAIS -->
  <div class="filter-bar">
    <span class="fb-label">Filtrar por</span>
    <select id="globalNucleo"></select>
    <select id="globalProjeto"></select>
    <button class="fb-clear" id="clearFilters">Limpar filtros</button>
    <span class="fb-count" id="filterCount"></span>
  </div>

  <!-- HERO -->
  <div class="hero">
    <div class="hero-left">
      <div class="hero-eyebrow">Crítico</div>
      <div class="hero-stat"><span id="heroPct">—</span></div>
      <div class="hero-stat-label" id="heroLabel">do backlog aberto não tem prazo estimado nem data fim prevista cadastrada.</div>
      <div class="hero-desc">Sem prazo, não há como medir atraso, cobrar entrega ou priorizar fila — é a lacuna que mais compromete a gestão do backlog hoje. A concentração desse problema por núcleo, gestor e projeto está detalhada abaixo.</div>
    </div>
    <div class="hero-right">
      <div class="gauge-wrap">
        <svg id="gaugeSvg" viewBox="0 0 260 150" width="100%"></svg>
      </div>
      <div class="gauge-caption">ÍNDICE DE DEMANDAS SEM PRAZO DEFINIDO</div>
      <div class="gauge-legend">
        <span><i style="background:var(--teal)"></i>0–30%</span>
        <span><i style="background:var(--amber)"></i>30–60%</span>
        <span><i style="background:var(--red)"></i>60–100%</span>
      </div>
    </div>
  </div>

  <!-- KPI STRIP -->
  <div class="kpi-strip" id="kpiStrip"></div>

  <!-- EVOLUÇÃO -->
  <section class="block">
    <div class="block-head">
      <div>
        <div class="block-num">00 · SÉRIE HISTÓRICA</div>
        <div class="block-title">Evolução do backlog — GDS-1</div>
      </div>
      <div class="block-note" id="evolNote">Comparativo semanal do volume de backlog aberto, geral e por núcleo.</div>
    </div>
    <div class="panel">
      <div class="evol-legend" id="evolLegend"></div>
      <div class="evol-chart-wrap">
        <svg id="evolSvg" viewBox="0 0 1000 300" width="100%"></svg>
      </div>
    </div>
  </section>

  <!-- FLUXO SEMANAL -->
  <section class="block">
    <div class="block-head">
      <div>
        <div class="block-num">01 · FLUXO SEMANAL</div>
        <div class="block-title">O que mudou desde a coleta anterior</div>
      </div>
      <div class="block-note" id="flowNote">Comparativo item a item entre a coleta anterior e a atual.</div>
    </div>
    <div class="panel">
      <div class="flow-filter-bar" id="flowFilterBar" style="display:none;">
        <span class="fb-label">Núcleo</span>
        <select id="flowNucleoSelect"></select>
      </div>
      <div id="flowPanel"></div>
    </div>
  </section>

  <!-- FUNIL -->
  <section class="block">
    <div class="block-head">
      <div>
        <div class="block-num">02 · PIPELINE</div>
        <div class="block-title">Backlog por status</div>
      </div>
      <div class="block-note">Fluxo do ciclo de vida das demandas abertas, da abertura até homologação.</div>
    </div>
    <div class="section-filter-bar">
      <span class="fb-label">Núcleo</span>
      <select id="funilNucleoSelect"></select>
    </div>
    <div class="panel" id="funilPanel"></div>
  </section>

  <!-- RISCO -->
  <section class="block">
    <div class="block-head">
      <div>
        <div class="block-num">03 · DEMANDAS SEM PRAZO</div>
        <div class="block-title">Onde está concentrado o risco de prazo</div>
      </div>
      <div class="block-note">% de demandas sem prazo definido, por núcleo, gestor e projeto. Núcleo (NSS1/NSS2/NSS3/NC) é atribuído por projeto — a planilha não traz essa informação diretamente.</div>
    </div>
    <div class="panel">
      <div class="risk-grid">
        <div>
          <div class="risk-col-title">Por núcleo</div>
          <div id="riskNucleo"></div>
        </div>
        <div>
          <div class="risk-col-title">Por gestor</div>
          <div id="riskGestor"></div>
        </div>
        <div>
          <div class="risk-col-title">Por projeto</div>
          <div id="riskProjeto"></div>
        </div>
      </div>
    </div>
  </section>

  <!-- AGING -->
  <section class="block">
    <div class="block-head">
      <div>
        <div class="block-num">04 · TEMPO EM ABERTO</div>
        <div class="block-title">Aging do backlog</div>
      </div>
      <div class="block-note">Dias corridos desde a criação da demanda até a data da coleta (<span id="agingRefDate">—</span>).</div>
    </div>
    <div class="section-filter-bar">
      <span class="fb-label">Núcleo</span>
      <select id="agingNucleoSelect"></select>
    </div>
    <div class="panel">
      <div class="aging-chart" id="agingChart"></div>
      <div class="aging-flag" id="agingFlag"></div>
    </div>
  </section>

  <!-- ESFORÇO -->
  <section class="block">
    <div class="block-head">
      <div>
        <div class="block-num">05 · ESFORÇO</div>
        <div class="block-title">Estimado vs. realizado — maiores estouros</div>
      </div>
      <div class="block-note">Demandas abertas em que o esforço já executado (horas) superou o estimado.</div>
    </div>
    <div class="section-filter-bar">
      <span class="fb-label">Núcleo</span>
      <select id="effortNucleoSelect"></select>
    </div>
    <div class="panel">
      <div class="effort-head"><span>Demanda</span><span>Estimado</span><span>Realizado</span><span>Δ</span></div>
      <div class="effort-list" id="effortList"></div>
    </div>
  </section>

  <!-- TABELA -->
  <section class="block">
    <div class="block-head">
      <div>
        <div class="block-num">06 · DETALHAMENTO</div>
        <div class="block-title">Todas as demandas em aberto</div>
      </div>
      <div class="block-note">Clique nos cabeçalhos para ordenar. Ordenado por dias em aberto (decrescente).</div>
    </div>
    <div class="table-controls">
      <input type="text" id="searchInput" placeholder="Buscar por ID ou título…">
      <select id="filterNucleo"></select>
      <select id="filterStatus"></select>
      <label class="chk-wrap"><input type="checkbox" id="filterSemPrazo"> Somente sem prazo</label>
    </div>
    <div class="table-count" id="tableCount"></div>
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th data-key="id">ID<span class="arrow">▾</span></th>
            <th data-key="titulo">Título<span class="arrow">▾</span></th>
            <th data-key="nucleoNegocio">Núcleo<span class="arrow">▾</span></th>
            <th data-key="sigla">Projeto<span class="arrow">▾</span></th>
            <th data-key="status">Status<span class="arrow">▾</span></th>
            <th data-key="gerenciaInterna">Gerência (Prodam)<span class="arrow">▾</span></th>
            <th data-key="gestor">Gestor<span class="arrow">▾</span></th>
            <th data-key="diasAberto">Dias aberto<span class="arrow">▾</span></th>
            <th data-key="semPrazo">Prazo<span class="arrow">▾</span></th>
            <th data-key="esfEst">Esf. est.<span class="arrow">▾</span></th>
            <th data-key="esfReal">Esf. real<span class="arrow">▾</span></th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </section>

  <footer>
    <div>Fontes: SH0768 (SIGA Saúde) · SH0865 (BI Corporativo SMS) · SH0866 (BI GSS) · SH0879 (Agenda Fácil) · SH0876 (BI Corujão)</div>
    <div>Recorte: demandas com status Aberta, Planejamento, Aprovar Planej., Execução ou Homologação</div>
  </footer>

</div>

<script>
const DATA = __DATA_JSON__;
</script>
<script src="dashboard.js"></script>
</body>
</html>
"""

DASHBOARD_JS = r"""// ---------- Helpers ----------
const fmt = n => Math.round(n).toLocaleString('pt-BR');
const fmt1 = n => n.toLocaleString('pt-BR',{maximumFractionDigits:1});
const fmtPct = n => n.toString().replace('.',',');
function severityColor(pct){
  if(pct>=60) return 'var(--red)';
  if(pct>=30) return 'var(--amber)';
  return 'var(--teal)';
}

const ALL_RECORDS = DATA.records;
const status_order=['Aberta','Planejamento','Aprovar Planej.','Planej. Aprovado','Execução','Homologação','Homolog. Expressa','Homolog. Tácita'];
// Nivel de cada status no ciclo de vida -- usado so pra saber se uma transicao
// e avanco ou retorno (regressao) na secao de Fluxo Semanal. Homologacao,
// Homolog. Expressa e Homolog. Tacita ficam no MESMO nivel (sao caminhos
// alternativos equivalentes, nenhum "vem antes" do outro).
const STATUS_TIER={
  'Aberta':0,'Planejamento':1,'Aprovar Planej.':2,'Planej. Aprovado':3,
  'Execução':4,'Homologação':5,'Homolog. Expressa':5,'Homolog. Tácita':5,
  'Concluída':6,'Concluída (integração)':6,
};
function transDirection(de, para){
  const i1 = STATUS_TIER[de], i2 = STATUS_TIER[para];
  if(i1===undefined || i2===undefined) return 'neutral';
  if(i2>i1) return 'forward';
  if(i2<i1) return 'backward';
  return 'neutral';
}

// ---------- Aggregation (recomputed on every filter change) ----------
function computeAggregates(recs){
  const kpis = recs.length ? {
    totalBacklog: recs.length,
    semPrazoCount: recs.filter(r=>r.semPrazo).length,
    esforcoRealAberto: recs.reduce((a,r)=>a+r.esfReal,0),
    esforcoEstAberto: recs.reduce((a,r)=>a+r.esfEst,0),
    itemMaisAntigoDias: Math.max(...recs.map(r=>r.diasAberto||0)),
    over2anos: recs.filter(r=>r.diasAberto>730).length,
    estouroEsforco: recs.filter(r=>r.esfEst>0 && r.esfReal>r.esfEst).length,
  } : {totalBacklog:0,semPrazoCount:0,esforcoRealAberto:0,esforcoEstAberto:0,itemMaisAntigoDias:0,over2anos:0,estouroEsforco:0};
  kpis.semPrazoPct = recs.length ? Math.round((kpis.semPrazoCount/recs.length)*1000)/10 : 0;

  const statusFunil = status_order.map(s=>({status:s, count: recs.filter(r=>r.status===s).length}));

  function riskBy(field){
    const agg = {};
    recs.forEach(r=>{
      const k = r[field];
      if(!agg[k]) agg[k]=[0,0];
      agg[k][1]++;
      if(r.semPrazo) agg[k][0]++;
    });
    return Object.entries(agg).map(([key,[sp,tot]])=>({key,semPrazo:sp,total:tot,pct:Math.round((sp/tot)*1000)/10}))
      .sort((a,b)=>b.total-a.total);
  }
  const nucleoRisk = riskBy('nucleoNegocio');
  const gestorRisk = riskBy('gestor');
  const projetoRisk = riskBy('sigla');

  const bucketDefs=[['0-90',0,90],['91-180',91,180],['181-365',181,365],['366-730',366,730],['>730',731,999999]];
  const agingBuckets = bucketDefs.map(([label,lo,hi])=>({
    label, count: recs.filter(r=>r.diasAberto!=null && r.diasAberto>=lo && r.diasAberto<=hi).length
  }));

  const effortTop = recs.filter(r=>r.esfEst>0 && r.esfReal>r.esfEst)
    .map(r=>({...r, delta:r.esfReal-r.esfEst}))
    .sort((a,b)=>b.delta-a.delta)
    .slice(0,10);

  return {kpis, statusFunil, nucleoRisk, gestorRisk, projetoRisk, agingBuckets, effortTop};
}

// ---------- Gauge (semicircle) ----------
function drawGauge(pct){
  const svg = document.getElementById('gaugeSvg');
  const cx=130, cy=130, r=100;
  function polar(cx,cy,r,angleDeg){
    const a = (angleDeg*Math.PI)/180;
    return [cx + r*Math.cos(a), cy - r*Math.sin(a)];
  }
  function arcPath(r0,a0,a1){
    const [x0,y0]=polar(cx,cy,r0,a0);
    const [x1,y1]=polar(cx,cy,r0,a1);
    const large = (a0-a1)>180 ? 1:0;
    return `M ${x0} ${y0} A ${r0} ${r0} 0 ${large} 1 ${x1} ${y1}`;
  }
  let html='';
  const zones=[[0,30,'#1c4038'],[30,60,'#4a3a1e'],[60,100,'#4a231e']];
  zones.forEach(([lo,hi,bgc])=>{
    const a0 = 180 - (lo/100)*180;
    const a1 = 180 - (hi/100)*180;
    html += `<path d="${arcPath(r,a0,a1)}" stroke="${bgc}" stroke-width="16" fill="none"/>`;
  });
  const progColor = severityColor(pct);
  const a1 = 180 - (pct/100)*180;
  html += `<path d="${arcPath(r,180,a1)}" stroke="${progColor}" stroke-width="16" fill="none" stroke-linecap="round" opacity="0.95"/>`;
  for(let t=0;t<=100;t+=10){
    const ang = 180-(t/100)*180;
    const [x0,y0]=polar(cx,cy,r+12,ang);
    const [x1,y1]=polar(cx,cy,r+2,ang);
    html += `<line x1="${x0}" y1="${y0}" x2="${x1}" y2="${y1}" stroke="#37414f" stroke-width="1.5"/>`;
  }
  const needleAng = 180-(pct/100)*180;
  const [nx,ny]=polar(cx,cy,r-14,needleAng);
  html += `<line x1="${cx}" y1="${cy}" x2="${nx}" y2="${ny}" stroke="#eaeef3" stroke-width="2.5" stroke-linecap="round"/>`;
  html += `<circle cx="${cx}" cy="${cy}" r="6" fill="#eaeef3"/>`;
  html += `<text x="${cx}" y="${cy-24}" text-anchor="middle" font-family="Space Grotesk" font-weight="700" font-size="30" fill="${progColor}">${fmtPct(pct)}%</text>`;
  html += `<text x="18" y="145" font-family="IBM Plex Mono" font-size="10" fill="#546070">0%</text>`;
  html += `<text x="228" y="145" font-family="IBM Plex Mono" font-size="10" fill="#546070">100%</text>`;
  svg.innerHTML = html;
}

// ---------- Render pieces ----------
function renderHero(agg, base){
  document.getElementById('heroPct').textContent = fmtPct(agg.kpis.semPrazoPct)+'%';
  document.getElementById('heroLabel').textContent =
    `do backlog${base.scopeLabel} (${fmt(agg.kpis.semPrazoCount)} de ${fmt(agg.kpis.totalBacklog)} demandas) não tem prazo estimado nem data fim prevista cadastrada.`;
  drawGauge(agg.kpis.semPrazoPct);
}

function renderKpis(agg){
  const k = agg.kpis;
  const items = [
    {label:'Backlog aberto', value: fmt(k.totalBacklog), sub:'demandas ativas em qualquer fase', cls:''},
    {label:'Sem prazo definido', value: fmt(k.semPrazoCount), sub:`${fmtPct(k.semPrazoPct)}% do backlog`, cls:'warn'},
    {label:'Esforço já consumido', value: fmt(k.esforcoRealAberto)+'<small>h</small>', sub:`sem entrega concluída (est.: ${fmt(k.esforcoEstAberto)}h)`, cls:''},
    {label:'Item mais antigo', value: fmt(k.itemMaisAntigoDias)+'<small>d</small>', sub:`${k.over2anos} itens abertos há +2 anos`, cls:'crit'},
  ];
  document.getElementById('kpiStrip').innerHTML = items.map(it=>`
    <div class="kpi ${it.cls}">
      <div class="kpi-label">${it.label}</div>
      <div class="kpi-value">${it.value}</div>
      <div class="kpi-sub">${it.sub}</div>
    </div>`).join('');
}

function renderFunil(agg){
  const max = Math.max(1, ...agg.statusFunil.map(s=>s.count));
  document.getElementById('funilPanel').innerHTML = agg.statusFunil.map(s=>`
    <div class="funil-row">
      <div class="lbl">${s.status}</div>
      <div class="funil-track"><div class="funil-fill" style="width:${(s.count/max*100).toFixed(1)}%"></div></div>
      <div class="funil-count">${s.count}</div>
    </div>`).join('');
}

function renderRisk(containerId, list, maxItems){
  const items = list.slice(0,maxItems);
  if(!items.length){ document.getElementById(containerId).innerHTML = '<div class="risk-meta">Sem dados no recorte atual.</div>'; return; }
  const maxTotal = Math.max(...items.map(d=>d.total));
  document.getElementById(containerId).innerHTML = items.map(d=>{
    const col = severityColor(d.pct);
    const widthPct = (d.total/maxTotal*100).toFixed(1);
    return `
    <div class="risk-item">
      <div class="risk-top">
        <span class="risk-name" title="${d.key}">${d.key}</span>
        <span class="risk-pct" style="color:${col}">${fmtPct(d.pct)}%</span>
      </div>
      <div class="risk-track" style="width:${widthPct}%">
        <div class="risk-fill" style="width:${d.pct}%;background:${col}"></div>
      </div>
      <div class="risk-meta">${d.semPrazo} sem prazo de ${d.total} demandas</div>
    </div>`;
  }).join('');
}

function renderAging(agg){
  const buckets = agg.agingBuckets;
  const total = agg.kpis.totalBacklog || 1;
  const max = Math.max(1, ...buckets.map(b=>b.count));
  const colors = ['#4f8cf7','#4f8cf7','var(--amber)','var(--amber)','var(--red)'];
  document.getElementById('agingChart').innerHTML = buckets.map((b,i)=>{
    const pct = total ? Math.round((b.count/total)*100) : 0;
    return `
    <div class="aging-bar-wrap">
      <div class="aging-count" style="color:${colors[i]}">${b.count}</div>
      <div class="aging-bar" style="height:${Math.max((b.count/max*140),26)}px;background:${colors[i]}">
        <span class="aging-pct">${pct}%</span>
      </div>
      <div class="aging-label">${b.label}<br>dias</div>
    </div>`;
  }).join('');
  const over2 = agg.kpis.over2anos;
  const pct2 = total ? Math.round((over2/total)*100) : 0;
  document.getElementById('agingFlag').innerHTML = over2 ?
    `<b>${over2} demandas (${pct2}%)</b> estão abertas há mais de 2 anos sem conclusão — candidatas prioritárias para triagem: reavaliar se ainda são necessárias, cancelar ou replanejar com prazo formal.`
    : 'Nenhuma demanda com mais de 2 anos em aberto no recorte atual.';
}

function renderEffort(agg){
  const items = agg.effortTop;
  if(!items.length){ document.getElementById('effortList').innerHTML = '<div class="risk-meta">Nenhum estouro de esforço no recorte atual.</div>'; return; }
  const maxVal = Math.max(...items.map(r=>Math.max(r.esfEst,r.esfReal)));
  document.getElementById('effortList').innerHTML = items.map(r=>`
    <div class="effort-row">
      <div>
        <div class="effort-title" title="${r.titulo}">${r.titulo}</div>
        <div class="effort-bar-mini">
          <div class="est" style="width:${(r.esfEst/maxVal*100).toFixed(1)}%"></div>
          <div class="real" style="width:${(r.esfReal/maxVal*100).toFixed(1)}%;opacity:.55"></div>
        </div>
      </div>
      <div class="effort-num">${fmt1(r.esfEst)}h</div>
      <div class="effort-num">${fmt1(r.esfReal)}h</div>
      <div class="effort-delta">+${fmt1(r.delta)}h</div>
    </div>`).join('');
}

// ---------- Fluxo semanal (comparativo item a item) ----------
function renderWeeklyFlow(){
  const wf = DATA.weeklyFlow;
  const filterBar = document.getElementById('flowFilterBar');
  const selectEl = document.getElementById('flowNucleoSelect');

  if(!wf){
    filterBar.style.display = 'none';
    document.getElementById('flowPanel').innerHTML = `<div class="flow-empty"><b>Sem dado de comparação nesta coleta.</b><br>Restaure o HTML da coleta anterior (passo 0 no app) antes de processar, para habilitar o comparativo semana a semana aqui.</div>`;
    document.getElementById('flowNote').textContent = 'Comparativo item a item entre a coleta anterior e a atual.';
    return;
  }

  filterBar.style.display = 'flex';
  if(!selectEl.dataset.populated){
    const nucleos = (wf.porNucleo || []).map(n=>n.nucleo);
    selectEl.innerHTML = '<option value="">Todos os núcleos</option>' +
      nucleos.map(n=>`<option value="${n}">${n}</option>`).join('');
    selectEl.dataset.populated = '1';
    selectEl.addEventListener('change', ()=>renderFlowBody(wf));
  }
  renderFlowBody(wf);
}

function renderFlowBody(wf){
  const selectEl = document.getElementById('flowNucleoSelect');
  const nucleoSel = selectEl.value;
  const fmtDateBR = d => d ? d.split('-').reverse().join('/') : '—';

  let t, transicoes;
  if(nucleoSel){
    const entry = (wf.porNucleo || []).find(n=>n.nucleo===nucleoSel);
    t = entry || {novas:0,retornaram:0,saidas:0,mudancaStatus:0,semAlteracao:0,totalAnterior:0,totalAtual:0,saldoLiquido:0};
    transicoes = (wf.transicoesPorNucleo && wf.transicoesPorNucleo[nucleoSel]) || [];
  } else {
    t = wf.totals;
    transicoes = wf.transicoes || [];
  }

  document.getElementById('flowNote').textContent =
    `De ${fmtDateBR(wf.prevDate)} para ${fmtDateBR(wf.currDate)}${nucleoSel ? ' · '+nucleoSel : ''} — ${fmt(t.totalAnterior)} → ${fmt(t.totalAtual)} demandas em aberto.`;

  const saldoColor = t.saldoLiquido>0 ? 'var(--red)' : (t.saldoLiquido<0 ? 'var(--teal)' : 'var(--text-dim)');
  let html = `
    <div class="flow-cards">
      <div class="flow-card novas">
        <div class="flow-card-label">Novas demandas</div>
        <div class="flow-card-value">+${fmt(t.novas)}</div>
        <div class="flow-card-sub">criadas dentro do período</div>
      </div>
      <div class="flow-card saidas">
        <div class="flow-card-label">Saíram do backlog</div>
        <div class="flow-card-value">-${fmt(t.saidas)}</div>
        <div class="flow-card-sub">concluídas, canceladas ou fechadas</div>
      </div>
      <div class="flow-card mudou">
        <div class="flow-card-label">Mudaram de status</div>
        <div class="flow-card-value">${fmt(t.mudancaStatus)}</div>
        <div class="flow-card-sub">avançaram ou retrocederam na fila</div>
      </div>
      <div class="flow-card">
        <div class="flow-card-label">Saldo líquido</div>
        <div class="flow-card-value" style="color:${saldoColor}">${t.saldoLiquido>0?'+':''}${fmt(t.saldoLiquido)}</div>
        <div class="flow-card-sub">${fmt(t.semAlteracao)} sem nenhuma alteração</div>
      </div>
    </div>`;

  if(!nucleoSel && wf.porNucleo && wf.porNucleo.length){
    html += `<div class="flow-subtitle">Por núcleo</div>
    <table class="flow-nucleo-table">
      <thead><tr><th>Núcleo</th><th>Novas</th><th>Saíram</th><th>Mudaram status</th><th>Anterior → Atual</th></tr></thead>
      <tbody>
      ${wf.porNucleo.map(n=>{
        return `<tr>
          <td class="nuc-name">${n.nucleo}</td>
          <td>+${fmt(n.novas)}</td>
          <td>-${fmt(n.saidas)}</td>
          <td>${fmt(n.mudancaStatus)}</td>
          <td>${fmt(n.totalAnterior)} → ${fmt(n.totalAtual)}</td>
        </tr>`;
      }).join('')}
      </tbody>
    </table>`;
  }

  html += `<div class="flow-subtitle">Transições de status${nucleoSel ? ' — '+nucleoSel : ''}</div>`;
  if(transicoes.length){
    const maxT = Math.max(...transicoes.map(x=>x.count));
    html += transicoes.slice(0,12).map(x=>{
      const dir = transDirection(x.de, x.para);
      const fillCls = dir==='backward' ? 'flow-trans-fill backward' : 'flow-trans-fill';
      const arrow = dir==='backward' ? '↩' : '→';
      const arrowColor = dir==='backward' ? 'var(--red)' : 'var(--text-mute)';
      return `
      <div class="flow-trans-row">
        <div class="flow-trans-lbl">${x.de} <span style="color:${arrowColor}">${arrow}</span> <b>${x.para}</b></div>
        <div class="flow-trans-track"><div class="${fillCls}" style="width:${(x.count/maxT*100).toFixed(1)}%"></div></div>
        <div class="flow-trans-count">${x.count}</div>
      </div>`;
    }).join('');
  } else {
    html += `<div class="risk-meta">Nenhuma demanda mudou de status${nucleoSel ? ' em '+nucleoSel : ''} entre as duas coletas.</div>`;
  }

  document.getElementById('flowPanel').innerHTML = html;
}

// ---------- Evolução (série histórica) ----------
const EVOL_COLORS = {
  'GDS-1': '#eaeef3',
  'NSS1': '#4f8cf7',
  'NSS2': '#31b596',
  'NSS3': '#e8a23c',
  'NC':   '#c26bf0',
};
let evolHidden = new Set();

function groupHistory(){
  const byNucleo = {};
  (DATA.history||[]).forEach(row=>{
    if(!byNucleo[row.nucleo]) byNucleo[row.nucleo] = [];
    byNucleo[row.nucleo].push(row);
  });
  Object.values(byNucleo).forEach(arr=>arr.sort((a,b)=>a.data_snapshot.localeCompare(b.data_snapshot)));
  return byNucleo;
}

function renderEvolLegend(byNucleo){
  const order = ['GDS-1','NSS1','NSS2','NSS3','NC'];
  const keys = order.filter(k=>byNucleo[k]);
  document.getElementById('evolLegend').innerHTML = keys.map(k=>`
    <span class="li ${evolHidden.has(k)?'off':''}" data-k="${k}">
      <i style="background:${EVOL_COLORS[k]||'#888'}"></i>${k}
    </span>`).join('');
  document.querySelectorAll('.evol-legend .li').forEach(el=>{
    el.addEventListener('click',()=>{
      const k = el.dataset.k;
      if(evolHidden.has(k)) evolHidden.delete(k); else evolHidden.add(k);
      renderEvolution();
    });
  });
}

function renderEvolution(){
  const byNucleo = groupHistory();
  const weekCount = Math.max(0, ...Object.values(byNucleo).map(a=>a.length));
  renderEvolLegend(byNucleo);
  const svg = document.getElementById('evolSvg');
  const noteEl = document.getElementById('evolNote');

  if(weekCount<2){
    svg.innerHTML='';
    svg.style.display='none';
    noteEl.textContent = 'Comparativo semanal do volume de backlog aberto, geral e por núcleo.';
    document.querySelector('.evol-chart-wrap').innerHTML =
      `<div class="evol-empty"><b>Primeira coleta registrada${DATA.history && DATA.history[0] ? ' em '+DATA.history[0].data_snapshot.split('-').reverse().join('/') : ''}.</b><br>
      O gráfico de evolução aparece a partir da 2ª atualização semanal — assim que o histórico tiver pelo menos 2 pontos, a tendência é traçada automaticamente aqui.</div>`;
    return;
  }

  const W=1000,H=300,padL=54,padR=46,padT=20,padB=36;
  const plotW = W-padL-padR, plotH = H-padT-padB;
  const order = ['GDS-1','NSS1','NSS2','NSS3','NC'];
  const visible = order.filter(k=>byNucleo[k] && !evolHidden.has(k));
  const allVals = visible.flatMap(k=>byNucleo[k].map(r=>r.backlog_total));
  const maxVal = Math.max(1, ...allVals);
  const dates = byNucleo[order.find(k=>byNucleo[k])] ? byNucleo[order.find(k=>byNucleo[k])].map(r=>r.data_snapshot) : [];

  function x(i){ return padL + (dates.length<=1 ? plotW/2 : (i/(dates.length-1))*plotW); }
  function y(v){ return padT + plotH - (v/maxVal)*plotH; }

  let html='';
  // grid horizontal
  for(let g=0; g<=4; g++){
    const gv = Math.round(maxVal/4*g);
    const gy = y(gv);
    html += `<line x1="${padL}" y1="${gy}" x2="${W-padR}" y2="${gy}" stroke="#1e2630" stroke-width="1"/>`;
    html += `<text x="${padL-8}" y="${gy+4}" text-anchor="end" font-family="IBM Plex Mono" font-size="10" fill="#546070">${gv}</text>`;
  }
  // x labels
  dates.forEach((d,i)=>{
    const label = d.split('-').slice(1).reverse().join('/');
    html += `<text x="${x(i)}" y="${H-10}" text-anchor="middle" font-family="IBM Plex Mono" font-size="10" fill="#546070">${label}</text>`;
  });
  // lines + pontos
  visible.forEach(k=>{
    const rows = byNucleo[k];
    const col = EVOL_COLORS[k]||'#888';
    const pts = rows.map((r,i)=>`${x(i)},${y(r.backlog_total)}`).join(' ');
    const strokeW = k==='GDS-1' ? 3 : 2;
    if(rows.length>1){
      html += `<polyline points="${pts}" fill="none" stroke="${col}" stroke-width="${strokeW}" stroke-linejoin="round" stroke-linecap="round"/>`;
    }
    rows.forEach((r,i)=>{
      html += `<circle cx="${x(i)}" cy="${y(r.backlog_total)}" r="${k==='GDS-1'?4:3}" fill="${col}"/>`;
    });
  });
  // rótulos do último ponto de cada série — com correção de colisão vertical
  function layoutLabels(getVal){
    let items = visible.map(k=>{
      const rows = byNucleo[k];
      const r = getVal(rows);
      return {k, col: EVOL_COLORS[k]||'#888', val: r.backlog_total, yTrue: y(r.backlog_total)};
    });
    items.sort((a,b)=>a.yTrue-b.yTrue);
    const minGap = 13;
    items.forEach(l=>{ l.yLabel = l.yTrue; });
    for(let i=1;i<items.length;i++){
      if(items[i].yLabel - items[i-1].yLabel < minGap){
        items[i].yLabel = items[i-1].yLabel + minGap;
      }
    }
    return items;
  }
  const endLabels = layoutLabels(rows=>rows[rows.length-1]);
  endLabels.forEach(l=>{
    html += `<text x="${x(dates.length-1)+8}" y="${l.yLabel+4}" font-family="IBM Plex Mono" font-size="11" font-weight="600" fill="${l.col}">${l.val}</text>`;
  });
  // rótulos do primeiro ponto (valor da coleta anterior), só quando há 2+ semanas
  if(dates.length>1){
    const startLabels = layoutLabels(rows=>rows[0]);
    startLabels.forEach(l=>{
      html += `<text x="${x(0)-8}" y="${l.yLabel+4}" text-anchor="end" font-family="IBM Plex Mono" font-size="11" font-weight="600" fill="${l.col}" opacity="0.75">${l.val}</text>`;
    });
  }

  svg.style.display='';
  svg.innerHTML = html;

  const first = byNucleo['GDS-1'] ? byNucleo['GDS-1'][0] : null;
  const last = byNucleo['GDS-1'] ? byNucleo['GDS-1'][byNucleo['GDS-1'].length-1] : null;
  if(first && last && first!==last){
    const delta = last.backlog_total - first.backlog_total;
    const sign = delta>0 ? '+' : '';
    noteEl.textContent = `GDS-1: ${sign}${delta} demandas desde ${first.data_snapshot.split('-').reverse().join('/')} (${first.backlog_total} → ${last.backlog_total}).`;
  }
}

// ---------- Global filters ----------
function populateGlobalFilters(){
  const selProjeto = document.getElementById('globalProjeto');
  const selNucleo = document.getElementById('globalNucleo');
  selNucleo.innerHTML = '<option value="">Todos os núcleos</option>' + DATA.nucleosNegocio.map(n=>`<option value="${n}">${n}</option>`).join('');
  refreshProjetoOptions();
}
function refreshProjetoOptions(){
  const selProjeto = document.getElementById('globalProjeto');
  const nucleo = document.getElementById('globalNucleo').value;
  const current = selProjeto.value;
  const options = nucleo ? (DATA.projetoPorNucleo[nucleo]||[]) : DATA.projetos;
  selProjeto.innerHTML = '<option value="">Todos os projetos</option>' + options.map(p=>`<option value="${p}">${p}</option>`).join('');
  if(options.includes(current)) selProjeto.value = current;
}
function getGloballyFiltered(){
  const nucleo = document.getElementById('globalNucleo').value;
  const projeto = document.getElementById('globalProjeto').value;
  return ALL_RECORDS.filter(r=>{
    if(nucleo && r.nucleoNegocio!==nucleo) return false;
    if(projeto && r.projeto!==projeto) return false;
    return true;
  });
}

// ---------- Table ----------
let sortKey='diasAberto', sortDir=-1;
function populateTableFilters(){
  const statuses = status_order;
  const selStatus = document.getElementById('filterStatus');
  selStatus.innerHTML = '<option value="">Todos os status</option>' + statuses.map(s=>`<option value="${s}">${s}</option>`).join('');
  const selNucleo = document.getElementById('filterNucleo');
  selNucleo.innerHTML = '<option value="">Todos os núcleos</option>' + DATA.nucleosNegocio.map(n=>`<option value="${n}">${n}</option>`).join('');
}
function getTableRows(baseRecs){
  const q = document.getElementById('searchInput').value.trim().toLowerCase();
  const nuc = document.getElementById('filterNucleo').value;
  const st = document.getElementById('filterStatus').value;
  const onlySemPrazo = document.getElementById('filterSemPrazo').checked;
  let rows = baseRecs.filter(r=>{
    if(nuc && r.nucleoNegocio!==nuc) return false;
    if(st && r.status!==st) return false;
    if(onlySemPrazo && !r.semPrazo) return false;
    if(q && !(String(r.id).includes(q) || r.titulo.toLowerCase().includes(q))) return false;
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
function renderTable(baseRecs){
  const rows = getTableRows(baseRecs);
  document.getElementById('tableCount').textContent = `${rows.length} de ${baseRecs.length} demandas no recorte atual`;
  document.getElementById('tableBody').innerHTML = rows.map(r=>{
    const diasCls = r.diasAberto>730 ? 'old' : (r.diasAberto>365 ? 'mid':'');
    return `
    <tr>
      <td class="mono">${r.id}<div class="id-sub">${r.dataCriacao || '—'}</div></td>
      <td class="titulo">${r.titulo}</td>
      <td><span class="status-pill">${r.nucleoNegocio}</span></td>
      <td class="mono">${r.sigla}</td>
      <td><span class="status-pill">${r.status}</span></td>
      <td class="trunc" title="${(r.gerenciaInterna||'').replace(/"/g,'&quot;')}">${r.gerenciaInterna}</td>
      <td class="trunc gestor" title="${(r.gestor||'').replace(/"/g,'&quot;')}">${r.gestor}</td>
      <td class="mono dias-cell ${diasCls}">${r.diasAberto ?? '—'}</td>
      <td>${r.semPrazo ? '<span class="badge on">SEM PRAZO</span>' : '<span class="badge off">definido</span>'}</td>
      <td class="mono">${r.esfEst ? fmt1(r.esfEst) : '—'}</td>
      <td class="mono">${r.esfReal ? fmt1(r.esfReal) : '—'}</td>
    </tr>`;
  }).join('');
  document.querySelectorAll('thead th').forEach(th=>{
    th.classList.toggle('sorted', th.dataset.key===sortKey);
    const arrow = th.querySelector('.arrow');
    if(th.dataset.key===sortKey) arrow.textContent = sortDir===1?'▴':'▾';
  });
}

// ---------- Master render ----------
function renderAll(){
  const filtered = getGloballyFiltered();
  const nucleo = document.getElementById('globalNucleo').value;
  const projeto = document.getElementById('globalProjeto').value;
  let scopeLabel = '';
  if(nucleo && projeto) scopeLabel = ` de ${nucleo} / ${projeto.split(' · ')[0]}`;
  else if(nucleo) scopeLabel = ` de ${nucleo}`;
  else if(projeto) scopeLabel = ` de ${projeto.split(' · ')[0]}`;

  const agg = computeAggregates(filtered);
  renderHero(agg, {scopeLabel});
  renderKpis(agg);
  renderRisk('riskNucleo', agg.nucleoRisk, 7);
  renderRisk('riskGestor', agg.gestorRisk, 7);
  renderRisk('riskProjeto', agg.projetoRisk, 7);
  renderTable(filtered);

  document.getElementById('metaTotalBase').textContent = fmt(DATA.totalBaseGeral);
  document.getElementById('metaTotalBacklog').textContent = fmt(ALL_RECORDS.length);
  const dataRef = DATA.snapshotDate || new Date().toISOString().slice(0,10);
  const dataRefBR = dataRef.split('-').reverse().join('/');
  document.getElementById('metaGeradoEm').textContent = dataRefBR;
  const agingRef = document.getElementById('agingRefDate');
  if(agingRef) agingRef.textContent = dataRefBR;
  document.getElementById('filterCount').innerHTML = (projeto||nucleo)
    ? `<b>${filtered.length}</b> de ${ALL_RECORDS.length} demandas no recorte`
    : `<b>${ALL_RECORDS.length}</b> demandas no recorte (sem filtro)`;
}

function initFilters(){
  populateGlobalFilters();
  populateTableFilters();
  populateSectionNucleoFilters();
  document.getElementById('globalNucleo').addEventListener('change', ()=>{
    refreshProjetoOptions();
    renderAll();
  });
  document.getElementById('globalProjeto').addEventListener('change', renderAll);
  document.getElementById('clearFilters').addEventListener('click', ()=>{
    document.getElementById('globalNucleo').value='';
    refreshProjetoOptions();
    document.getElementById('globalProjeto').value='';
    renderAll();
  });
  document.querySelectorAll('thead th').forEach(th=>{
    th.addEventListener('click',()=>{
      const key = th.dataset.key;
      if(sortKey===key){ sortDir*=-1; } else { sortKey=key; sortDir = ['titulo','gerenciaInterna','gestor','status','sigla','nucleoNegocio'].includes(key) ? 1 : -1; }
      renderTable(getGloballyFiltered());
    });
  });
  ['searchInput','filterNucleo','filterStatus','filterSemPrazo'].forEach(id=>{
    document.getElementById(id).addEventListener('input', ()=>renderTable(getGloballyFiltered()));
    document.getElementById(id).addEventListener('change', ()=>renderTable(getGloballyFiltered()));
  });
}

// ---------- Filtros locais de núcleo (independentes do filtro global do topo) ----------
function populateSectionNucleoFilters(){
  const opts = '<option value="">Todos os núcleos</option>' + DATA.nucleosNegocio.map(n=>`<option value="${n}">${n}</option>`).join('');
  ['funilNucleoSelect','agingNucleoSelect','effortNucleoSelect'].forEach(id=>{
    document.getElementById(id).innerHTML = opts;
  });
  document.getElementById('funilNucleoSelect').addEventListener('change', renderFunilSection);
  document.getElementById('agingNucleoSelect').addEventListener('change', renderAgingSection);
  document.getElementById('effortNucleoSelect').addEventListener('change', renderEffortSection);
}
function renderFunilSection(){
  const nuc = document.getElementById('funilNucleoSelect').value;
  const recs = nuc ? ALL_RECORDS.filter(r=>r.nucleoNegocio===nuc) : ALL_RECORDS;
  renderFunil(computeAggregates(recs));
}
function renderAgingSection(){
  const nuc = document.getElementById('agingNucleoSelect').value;
  const recs = nuc ? ALL_RECORDS.filter(r=>r.nucleoNegocio===nuc) : ALL_RECORDS;
  renderAging(computeAggregates(recs));
}
function renderEffortSection(){
  const nuc = document.getElementById('effortNucleoSelect').value;
  const recs = nuc ? ALL_RECORDS.filter(r=>r.nucleoNegocio===nuc) : ALL_RECORDS;
  renderEffort(computeAggregates(recs));
}

// ---------- Init ----------
initFilters();
renderAll();
renderFunilSection();
renderAgingSection();
renderEffortSection();
renderEvolution();
renderWeeklyFlow();
"""


def build_dashboard_html(dataset: dict, history_rows: list, weekly_flow: dict = None) -> str:
    data = dict(dataset)
    data['history'] = history_rows
    data['weeklyFlow'] = weekly_flow
    data_json = json.dumps(data, ensure_ascii=False)

    html = DASHBOARD_HTML.replace("const DATA = __DATA_JSON__;", f"const DATA = {data_json};")
    html = html.replace('<script src="dashboard.js"></script>', f"<script>\n{DASHBOARD_JS}\n</script>")
    return html
