"""
Backlog GDS-1 — app Streamlit
Upload dos exports do SIGA -> dashboard consolidado com histórico semanal.

Persistência: como o Streamlit Community Cloud não garante disco entre
reinicializações, o estado (histórico semanal + mapeamento núcleo) é mantido
em st.session_state durante o uso e pode ser salvo/recuperado manualmente
pelos botões de Backup / Restore (arquivo .zip).
"""
import io
import json
import zipfile
import datetime
import streamlit as st

import data_processing as dp
import dashboard_template as db

st.set_page_config(page_title="Backlog GDS-1", page_icon="📊", layout="wide")

# ---------------------------------------------------------------------------
# Autenticação simples (senha em st.secrets)
# ---------------------------------------------------------------------------

def check_password():
    if st.session_state.get("auth_ok"):
        return True
    st.title("🔒 Backlog GDS-1")
    pwd = st.text_input("Senha de acesso", type="password")
    if st.button("Entrar"):
        expected = st.secrets.get("APP_PASSWORD", None)
        if expected is None:
            st.error("APP_PASSWORD não configurada em st.secrets. Veja o README.")
            return False
        if pwd == expected:
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    return False


if not check_password():
    st.stop()

# ---------------------------------------------------------------------------
# Estado inicial
# ---------------------------------------------------------------------------

DEFAULT_MAPPING = {
    'SH0768': 'NSS1', 'SH0865': 'NSS1', 'SH0866': 'NSS1', 'SH0879': 'NSS1', 'SH0876': 'NSS1',
    'HM0615': 'NSS2', 'HM0618': 'NSS2', 'SH0743': 'NSS2',
    'PS0101': 'NSS3', 'SH0712': 'NSS3', 'SH0758': 'NSS3', 'SH0763': 'NSS3', 'SH0765': 'NSS3',
    'SH0774': 'NSS3', 'SH0835': 'NSS3', 'SH0839': 'NSS3', 'SH0841': 'NSS3',
    'SH0887': 'NSS3', 'SH0888': 'NSS3', 'SH0896': 'NSS3', 'SH1505': 'NSS3',
    'SJ2223': 'NSS3', 'SS0404': 'NSS3', 'SS0405': 'NSS3',
    'CI0102': 'NC', 'DE0101': 'NC', 'SB0807': 'NC', 'SB0811': 'NC', 'SB1401': 'NC', 'SB1404': 'NC',
    'SB1408': 'NC', 'SB1423': 'NC', 'SB1424': 'NC', 'SC0132': 'NC', 'SN1407': 'NC', 'SU0107': 'NC',
}

if "nucleo_mapping" not in st.session_state:
    st.session_state.nucleo_mapping = dict(DEFAULT_MAPPING)
if "history_rows" not in st.session_state:
    st.session_state.history_rows = []
if "dataset" not in st.session_state:
    st.session_state.dataset = None
if "avisos" not in st.session_state:
    st.session_state.avisos = []

st.title("📊 Backlog GDS-1")

# ---------------------------------------------------------------------------
# Sidebar — upload, mapeamento, backup/restore
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("1. Upload dos exports")
    uploaded = st.file_uploader(
        "CSV/XLSX do GDP (Export Demandas)",
        type=["csv", "xlsx"], accept_multiple_files=True,
    )
    snapshot_date = st.date_input("Data desta coleta", value=datetime.date.today(), format="DD/MM/YYYY")

    st.divider()
    st.header("2. Núcleos não classificados")
    novas_siglas = []
    if uploaded:
        # pré-varredura rápida só para detectar siglas novas antes de processar
        for f in uploaded:
            try:
                header, rows = dp.read_upload(f.getvalue(), f.name)
                for r in rows:
                    s = r.get('SiglaSistema')
                    if s and s not in st.session_state.nucleo_mapping:
                        novas_siglas.append(s)
            except Exception:
                pass
    novas_siglas = sorted(set(novas_siglas))
    if novas_siglas:
        st.warning(f"{len(novas_siglas)} sigla(s) nova(s) — classifique antes de processar:")
        for s in novas_siglas:
            col1, col2 = st.columns([2, 2])
            col1.write(s)
            escolha = col2.selectbox(
                " ", ["", "NSS1", "NSS2", "NSS3", "NC"], key=f"map_{s}", label_visibility="collapsed"
            )
            if escolha:
                st.session_state.nucleo_mapping[s] = escolha
    else:
        st.caption("Nenhuma sigla nova detectada.")

    st.divider()
    st.header("3. Processar")
    processar = st.button("🔄 Processar upload", type="primary", disabled=not uploaded)

    st.divider()
    st.header("💾 Backup / ♻️ Restore")
    st.caption("Guarda o histórico semanal + mapeamento de núcleos. Os CSVs de origem você sempre reenvia frescos.")

    def make_backup_zip():
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("historico_backlog.csv", dp.history_to_csv_bytes(st.session_state.history_rows))
            z.writestr("nucleo_mapping.json", json.dumps(st.session_state.nucleo_mapping, ensure_ascii=False, indent=2))
        buf.seek(0)
        return buf.getvalue()

    st.download_button(
        "💾 Baixar backup (.zip)",
        data=make_backup_zip(),
        file_name=f"backup_gds1_{datetime.date.today().isoformat()}.zip",
        mime="application/zip",
        use_container_width=True,
    )

    restore_file = st.file_uploader("Restaurar backup (.zip)", type=["zip"], key="restore_uploader")
    if restore_file is not None:
        if st.button("♻️ Restaurar agora", use_container_width=True):
            try:
                with zipfile.ZipFile(io.BytesIO(restore_file.getvalue())) as z:
                    hist_bytes = z.read("historico_backlog.csv")
                    map_bytes = z.read("nucleo_mapping.json")
                st.session_state.history_rows = dp.history_from_csv_bytes(hist_bytes)
                st.session_state.nucleo_mapping.update(json.loads(map_bytes.decode("utf-8")))
                st.success(f"Restaurado: {len(st.session_state.history_rows)} linhas de histórico.")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao restaurar backup: {e}")

# ---------------------------------------------------------------------------
# Processamento
# ---------------------------------------------------------------------------

if processar and uploaded:
    files = [(f.name, f.getvalue()) for f in uploaded]
    today_dt = datetime.datetime.combine(snapshot_date, datetime.time())
    dataset, avisos = dp.build_dataset(files, st.session_state.nucleo_mapping, today=today_dt)
    st.session_state.dataset = dataset
    st.session_state.avisos = avisos

    new_hist = dp.build_history_rows(dataset['records'], snapshot_date.isoformat())
    st.session_state.history_rows = dp.append_history(st.session_state.history_rows, new_hist)

    st.success(f"Processado: {len(dataset['records'])} demandas em backlog aberto ({len(files)} arquivo(s)).")

# ---------------------------------------------------------------------------
# Corpo principal
# ---------------------------------------------------------------------------

if st.session_state.avisos:
    for a in st.session_state.avisos:
        st.warning(a)

if st.session_state.dataset is None:
    st.info("⬅️ Suba os arquivos do GDP na barra lateral e clique em **Processar upload** para gerar o dashboard.")
else:
    dataset = st.session_state.dataset
    n = len(dataset['records'])
    sem_prazo = sum(1 for r in dataset['records'] if r['semPrazo'])
    c1, c2, c3 = st.columns(3)
    c1.metric("Backlog aberto", n)
    c2.metric("Sem prazo definido", f"{sem_prazo} ({sem_prazo/n*100:.1f}%)" if n else "0")
    c3.metric("Núcleos no recorte", len(dataset['nucleosNegocio']))

    st.divider()
    st.subheader("📤 Distribuição")
    st.caption("Gera o HTML autocontido (mesmo formato já usado) para enviar por e-mail ou subir num Drive/Teams.")
    html = db.build_dashboard_html(dataset, st.session_state.history_rows)
    st.download_button(
        "📤 Gerar HTML para distribuição",
        data=html.encode("utf-8"),
        file_name=f"backlog_gds1_{datetime.date.today().isoformat()}.html",
        mime="text/html",
        type="primary",
    )

    st.divider()
    st.subheader("Prévia do dashboard")
    st.components.v1.html(html, height=2400, scrolling=True)
