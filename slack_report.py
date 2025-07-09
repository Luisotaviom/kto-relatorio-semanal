
from jira import JIRA
from datetime import datetime, timedelta
import os

# Variáveis de ambiente
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")

# Conecta ao Jira
jira = JIRA(server='https://SEUJIRA.atlassian.net', basic_auth=(JIRA_EMAIL, JIRA_TOKEN))

# Define o período (últimos 7 dias)
inicio = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
query = f'project = TEC AND created >= \"{inicio}\" ORDER BY created DESC'
issues = jira.search_issues(query, maxResults=50)

# KPIs
total = len(issues)
resolvidos = sum(1 for i in issues if 'done' in i.fields.status.name.lower() or 'complete' in i.fields.status.name.lower())
abertos = total - resolvidos

# Destaques
destaques = []
for i in issues[:3]:
    status = i.fields.status.name.lower()
    emoji = '🟢' if 'done' in status or 'complete' in status else ('🟡' if 'progress' in status else '🔴')
    destaques.append(f"[{i.key}] {i.fields.summary} → {emoji} {i.fields.status.name}")

# Temas
keywords = ['circuit', 'game', 'payment', 'deposit', 'access', 'error']
resumos = [i.fields.summary.lower() for i in issues]
frequencia = {k: sum(k in r for r in resumos) for k in keywords if sum(k in r for r in resumos) > 0}

# Mensagem final
mensagem = f\"\"\"\n📊 Relatório Semanal – Plataforma iGaming ({inicio} a {datetime.now().strftime('%Y-%m-%d')})\n\n• Tickets Criados: {total}\n• Tickets Resolvidos: {resolvidos}\n• Em Aberto: {abertos}\n\n🔥 Destaques da Semana:\n\"\"\"
mensagem += '\\n'.join([f\"• {d}\" for d in destaques])
mensagem += \"\\n\\n🔁 Temas Repetidos:\\n\" + '\\n'.join([f\"• {k.title()} ({v})\" for k, v in frequencia.items()])
mensagem += \"\\n\\n📌 Observação: Seguimos monitorando os sistemas.\"

# Salva no repositório
with open(\"relatorio.txt\", \"w\", encoding=\"utf-8\") as f:
    f.write(mensagem.strip())

print(\"✅ Relatório salvo como relatorio.txt\")
