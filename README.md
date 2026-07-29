# Backlog GDS-1 — app Streamlit

App para consolidar os exports do SIGA (ExportacaoDemanda, .csv ou .xlsx) de
todos os núcleos (NSS1, NSS2, NSS3, NC) num dashboard único, com série
histórica semanal e geração do HTML para distribuição.

**Estrutura propositalmente plana** — todos os arquivos ficam soltos na raiz
do repositório, sem subpastas. Isso evita o problema comum de arrastar uma
pasta pro GitHub pelo navegador (ele só pega arquivos soltos, não pastas).

## Arquivos deste projeto

```
app.py                      # app Streamlit (upload, backup/restore, distribuição)
data_processing.py          # parsing dos exports SIGA + agregações
dashboard_template.py       # o dashboard (HTML/JS) embutido como texto Python
requirements.txt
historico_backlog_seed.csv  # ponto de partida do histórico (opcional)
nucleo_mapping_seed.json    # ponto de partida do mapeamento (opcional)
README.md
```

## Como subir pro GitHub (repositório vazio)

1. Crie um repositório novo no GitHub (pode ser privado).
2. Na página do repositório → **Add file → Upload files**.
3. **Arraste todos os arquivos soltos de uma vez** (app.py, data_processing.py,
   dashboard_template.py, requirements.txt, os dois .csv/.json e o README) —
   como são todos arquivos e não pastas, o GitHub aceita sem problema.
4. Commit direto na branch `main`.

## Deploy no Streamlit Community Cloud

1. Em https://share.streamlit.io → **New app** → selecione o repositório,
   branch `main` e arquivo principal `app.py`.
2. Antes de publicar, vá em **Advanced settings → Secrets** e cole:
   ```toml
   APP_PASSWORD = "sua-senha-aqui"
   ```
3. Deploy. O app fica num link público (`*.streamlit.app`) — **só quem tem
   a senha consegue ver os dados**, mas o link em si não é secreto. Trate a
   senha como você trataria a senha de um sistema interno.

## Como rodar localmente (opcional)

```bash
pip install -r requirements.txt
mkdir .streamlit
echo 'APP_PASSWORD = "teste123"' > .streamlit/secrets.toml
streamlit run app.py
```

## Como usar

1. **Upload**: na barra lateral, suba os `.csv`/`.xlsx` do SIGA — pode ser
   um núcleo por vez ou todos juntos, como preferir.
2. **Núcleos novos**: se aparecer uma sigla de projeto que o app não conhece,
   ele pede pra você classificar (NSS1/NSS2/NSS3/NC) antes de processar.
3. **Processar upload**: roda o pipeline e monta o dashboard.
4. **Distribuição**: baixa o HTML autocontido pra mandar por e-mail/Drive —
   é o mesmo formato usado até aqui, sem depender do app pra ser aberto.
5. **Backup**: baixa um `.zip` pequeno com o histórico semanal (pro gráfico
   de evolução) e o mapeamento de núcleos. **Baixe esse backup depois de
   cada atualização** — é o que garante a continuidade do histórico entre
   sessões, já que o Streamlit Community Cloud não garante disco persistente.
6. **Restore**: no início de uma sessão nova (ou se o app reiniciar/redeployar
   e perder o estado em memória), suba o último `.zip` de backup pra
   continuar de onde parou.

### Por que backup/restore manual em vez de salvar tudo automaticamente?

O plano gratuito do Streamlit Community Cloud não garante que o disco do
app sobreviva a reinicializações (o container pode dormir e reiniciar do
zero). Os dados de origem (os CSVs do SIGA) você já reexporta toda semana
de qualquer forma — o que precisa sobreviver entre sessões é só o
**histórico agregado** (pequeno, poucas linhas por semana) e o
**mapeamento de núcleos**. Por isso o backup guarda só isso, não o dataset
detalhado inteiro.

Se no futuro quiser persistência automática (sem precisar clicar em
backup toda vez), dá pra evoluir isso escrevendo o histórico direto no
repositório GitHub via API (token em `st.secrets`) a cada processamento —
é um passo a mais que pode ser adicionado depois.
