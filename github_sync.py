"""
Persistência automática no GitHub — evita depender de Backup/Restore manual.

Como funciona: usa a API de "Contents" do GitHub (repos/{repo}/contents/{path})
para ler e gravar dois arquivos pequenos direto no repositório:
  - historico_backlog.csv  (série semanal usada no gráfico de evolução)
  - nucleo_mapping.json    (mapeamento sigla -> núcleo)

Cada gravação vira um commit no repositório (autor = o token configurado).
Requer dois secrets no Streamlit Cloud:
  GITHUB_TOKEN = personal access token com permissão de escrita no repo
  GITHUB_REPO  = "usuario/nome-do-repo"  (ex: "Cidakina-prodam/backlog-gds1")

Se esses secrets não estiverem configurados, is_configured() retorna False e
o app volta a depender só do Backup/Restore manual (nada quebra).
"""
import base64
import json
import requests
import streamlit as st

API_BASE = "https://api.github.com"
HIST_PATH = "historico_backlog.csv"
MAP_PATH = "nucleo_mapping.json"


def is_configured():
    try:
        return bool(st.secrets.get("GITHUB_TOKEN") and st.secrets.get("GITHUB_REPO"))
    except Exception:
        return False


def _headers():
    return {
        "Authorization": f"Bearer {st.secrets['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
    }


def _branch():
    return st.secrets.get("GITHUB_BRANCH", "main")


def _get_file(path):
    """Retorna (conteudo_texto, sha) ou (None, None) se o arquivo não existir."""
    repo = st.secrets["GITHUB_REPO"]
    url = f"{API_BASE}/repos/{repo}/contents/{path}"
    resp = requests.get(url, headers=_headers(), params={"ref": _branch()}, timeout=15)
    if resp.status_code == 404:
        return None, None
    resp.raise_for_status()
    data = resp.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content, data["sha"]


def _put_file(path, content_text, message, sha=None):
    repo = st.secrets["GITHUB_REPO"]
    url = f"{API_BASE}/repos/{repo}/contents/{path}"
    payload = {
        "message": message,
        "content": base64.b64encode(content_text.encode("utf-8")).decode("ascii"),
        "branch": _branch(),
    }
    if sha:
        payload["sha"] = sha
    resp = requests.put(url, headers=_headers(), data=json.dumps(payload), timeout=15)
    resp.raise_for_status()
    return resp.json()["content"]["sha"]


def load_state():
    """Carrega histórico + mapeamento do repositório. Retorna dict com
    'history_csv_text' e 'mapping' (ou None em cada campo se não existir ainda)."""
    hist_text, _ = _get_file(HIST_PATH)
    map_text, _ = _get_file(MAP_PATH)
    mapping = json.loads(map_text) if map_text else None
    return hist_text, mapping


def save_state(history_csv_bytes, mapping_dict, commit_message):
    """Grava histórico + mapeamento no repositório (cria ou atualiza)."""
    _, hist_sha = _get_file(HIST_PATH)
    _, map_sha = _get_file(MAP_PATH)
    _put_file(HIST_PATH, history_csv_bytes.decode("utf-8"), commit_message, sha=hist_sha)
    _put_file(MAP_PATH, json.dumps(mapping_dict, ensure_ascii=False, indent=2),
              commit_message, sha=map_sha)
