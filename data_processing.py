"""
Processamento dos exports do SIGA (ExportacaoDemanda) em .csv ou .xlsx
para o formato consolidado usado pelo dashboard Backlog GDS-1.

Reaproveita a lógica validada manualmente ao longo do desenvolvimento do
dashboard (parsing de datas BR/ISO, números com vírgula decimal, etc.)
"""
import csv
import io
import json
import datetime
from collections import defaultdict, Counter

OPEN_STATUS = ['Execução', 'Homologação', 'Aprovar Planej.', 'Planejamento', 'Aberta']


# ---------------------------------------------------------------------------
# Leitura de arquivos
# ---------------------------------------------------------------------------

def read_csv_bytes(file_bytes, filename=""):
    """Lê um export CSV do SIGA (separador ; , encoding cp1252, com linha SEP= no topo)."""
    text = file_bytes.decode('cp1252', errors='replace')
    raw = list(csv.reader(io.StringIO(text), delimiter=';'))
    # primeira linha pode ser "SEP=;" (padrão de export do Excel/SIGA)
    if raw and raw[0] and raw[0][0].strip().upper().startswith('SEP'):
        header, data = raw[1], raw[2:]
    else:
        header, data = raw[0], raw[1:]
    return header, [dict(zip(header, row)) for row in data if any(row)]


def read_xlsx_bytes(file_bytes, filename=""):
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    header = list(rows[0])
    data = [dict(zip(header, [str(c) if c is not None else '' for c in row])) for row in rows[1:]]
    # xlsx mantém tipos nativos (datas/números) — refaz preservando os originais
    data_native = [dict(zip(header, row)) for row in rows[1:]]
    return header, data_native


def read_upload(file_bytes, filename):
    """Detecta o tipo pelo nome do arquivo e delega para o parser correto."""
    lower = filename.lower()
    if lower.endswith('.xlsx') or lower.endswith('.xls'):
        return read_xlsx_bytes(file_bytes, filename)
    return read_csv_bytes(file_bytes, filename)


# ---------------------------------------------------------------------------
# Normalização de campos
# ---------------------------------------------------------------------------

def norm_num(v):
    if v is None or v == '':
        return 0
    if isinstance(v, (int, float)):
        return v
    s = str(v).strip()
    if s in ('', '-'):
        return 0
    s = s.replace('.', '').replace(',', '.') if ',' in s else s
    try:
        return float(s)
    except ValueError:
        return 0


def norm_date(v):
    if v is None or v == '' or v == '-':
        return None
    if isinstance(v, datetime.datetime):
        return v
    if isinstance(v, datetime.date):
        return datetime.datetime(v.year, v.month, v.day)
    s = str(v).strip()
    if not s:
        return None
    for fmt in ('%Y-%m-%d', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y'):
        try:
            return datetime.datetime.strptime(s[:19] if 'H' in fmt else s[:10], fmt)
        except ValueError:
            continue
    return None


def nn(v, default='Não informado'):
    return v if v else default


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def build_dataset(uploaded_files, nucleo_mapping, today=None):
    """
    uploaded_files: lista de tuplas (filename, bytes)
    nucleo_mapping: dict {sigla: nucleo_negocio}  ex: {'SH0768': 'NSS1'}
    today: datetime.datetime usado como referência para aging (default = agora)

    Retorna (dataset_dict, avisos)
      dataset_dict: estrutura pronta para o dashboard (records, projetos, etc.)
      avisos: lista de strings — duplicatas detectadas, siglas não mapeadas, etc.
    """
    if today is None:
        today = datetime.datetime.now()

    all_rows = []
    total_linhas_base = 0
    avisos = []
    seen_ids_by_sigla = defaultdict(set)

    for filename, file_bytes in uploaded_files:
        header, rows = read_upload(file_bytes, filename)
        total_linhas_base += len(rows)
        all_rows.extend(rows)

    # --- checagem de duplicidade entre arquivos (mesma sigla + mesmos IDs) ---
    by_sigla_ids = defaultdict(set)
    for rd in all_rows:
        sigla = rd.get('SiglaSistema') or '—'
        _id = rd.get('ID_GDP')
        by_sigla_ids[sigla].add(_id)

    records = []
    unmapped = set()

    for rd in all_rows:
        status = rd.get('Status')
        if status not in OPEN_STATUS:
            continue
        sigla = rd.get('SiglaSistema') or '—'
        nome = rd.get('NomeSistema') or ''
        projeto = f"{sigla} · {nome}" if nome else sigla
        dc = norm_date(rd.get('DataCriacao'))
        dtfim = norm_date(rd.get('DtFimPrevisto'))
        prazo = norm_num(rd.get('PrazoEstimado'))
        esf_est = norm_num(rd.get('EsforcoEstimado'))
        esf_real = norm_num(rd.get('EsforcoReal'))
        dias = (today - dc).days if dc else None
        sem_prazo = (prazo == 0 and dtfim is None)
        nuc_neg = nucleo_mapping.get(sigla)
        if nuc_neg is None:
            unmapped.add(sigla)
            nuc_neg = 'Não classificado'
        records.append({
            'id': rd.get('ID_GDP'),
            'titulo': (rd.get('TituloDemanda') or '').strip(),
            'status': status,
            'nucleoNegocio': nuc_neg,
            'nucleoInterno': nn(rd.get('Nucleo')),
            'gerenciaInterna': nn(rd.get('Gerencia')),
            'projeto': projeto,
            'sigla': sigla,
            'tipo': nn(rd.get('Tipo')),
            'categoria': nn(rd.get('Categoria')),
            'gestor': nn(rd.get('Gestor')),
            'prazo': prazo,
            'esfEst': round(esf_est, 1),
            'esfReal': round(esf_real, 1),
            'dataCriacao': dc.strftime('%d/%m/%Y') if dc else None,
            'dtFimPrevisto': dtfim.strftime('%d/%m/%Y') if dtfim else None,
            'diasAberto': dias,
            'semPrazo': sem_prazo,
            'numOS': rd.get('NumeroOS') or None,
            'numContrato': rd.get('NumeroContrato'),
        })

    if unmapped:
        avisos.append(
            "Projetos sem núcleo classificado: " + ", ".join(sorted(unmapped)) +
            " — classifique-os na aba de mapeamento antes de distribuir."
        )

    dataset = {
        'records': sorted(records, key=lambda r: -(r['diasAberto'] or 0)),
        'projetos': sorted(set(r['projeto'] for r in records)),
        'nucleosNegocio': sorted(set(r['nucleoNegocio'] for r in records)),
        'totalBaseGeral': total_linhas_base,
    }
    pn = defaultdict(set)
    for r in records:
        pn[r['nucleoNegocio']].add(r['projeto'])
    dataset['projetoPorNucleo'] = {k: sorted(v) for k, v in pn.items()}

    return dataset, avisos


# ---------------------------------------------------------------------------
# Histórico semanal (série usada no gráfico de evolução)
# ---------------------------------------------------------------------------

def snapshot_row(records, nucleo, snapshot_date):
    recs = [r for r in records if nucleo == 'GDS-1' or r['nucleoNegocio'] == nucleo]
    total = len(recs)
    sem_prazo = sum(1 for r in recs if r['semPrazo'])
    over2 = sum(1 for r in recs if r['diasAberto'] and r['diasAberto'] > 730)
    esf_real = sum(r['esfReal'] for r in recs)
    return {
        'data_snapshot': snapshot_date,
        'nucleo': nucleo,
        'backlog_total': total,
        'sem_prazo_count': sem_prazo,
        'sem_prazo_pct': round(sem_prazo / total * 100, 1) if total else 0,
        'over_2anos': over2,
        'esforco_real_total': round(esf_real, 1),
    }


def build_history_rows(records, snapshot_date):
    nucleos_presentes = sorted(set(r['nucleoNegocio'] for r in records) - {'Não classificado'})
    rows = [snapshot_row(records, n, snapshot_date) for n in nucleos_presentes]
    rows.append(snapshot_row(records, 'GDS-1', snapshot_date))
    return rows


def append_history(history_rows_existing, new_rows, replace_same_date=True):
    """Anexa uma nova coleta ao histórico. Se já existir uma linha com a mesma
    data_snapshot + nucleo, substitui (permite reprocessar o mesmo dia)."""
    key = lambda r: (r['data_snapshot'], r['nucleo'])
    existing = {key(r): r for r in history_rows_existing} if replace_same_date else {}
    for r in new_rows:
        existing[key(r)] = r
    out = list(existing.values())
    out.sort(key=lambda r: (r['data_snapshot'], r['nucleo']))
    return out


HISTORY_FIELDS = ['data_snapshot', 'nucleo', 'backlog_total', 'sem_prazo_count',
                   'sem_prazo_pct', 'over_2anos', 'esforco_real_total']


def history_to_csv_bytes(history_rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=HISTORY_FIELDS, delimiter=';')
    w.writeheader()
    w.writerows(history_rows)
    return buf.getvalue().encode('utf-8')


def history_from_csv_bytes(file_bytes):
    text = file_bytes.decode('utf-8', errors='replace')
    reader = csv.DictReader(io.StringIO(text), delimiter=';')
    rows = []
    for r in reader:
        r['backlog_total'] = int(r['backlog_total'])
        r['sem_prazo_count'] = int(r['sem_prazo_count'])
        r['sem_prazo_pct'] = float(r['sem_prazo_pct'])
        r['over_2anos'] = int(r['over_2anos'])
        r['esforco_real_total'] = float(r['esforco_real_total'])
        rows.append(r)
    return rows
