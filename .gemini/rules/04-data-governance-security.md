# 04 - Governança, Segurança e Custos

## Privacidade e LGPD
- `DIRETRIZ` (confirmado): Colunas identificadoras `nm_segurado` e `nr_documento_segurado` devem existir **apenas na camada `bronze`**.
- `DIRETRIZ` (confirmado): `NUNCA` expor `nm_segurado` ou `nr_documento_segurado` em texto claro nas camadas `silver` e `gold` (omitir ou mascarar).
- `NUNCA` transcrever valores reais de linhas, documentos ou nomes de segurados em regras, logs, testes ou respostas.

## Segredos e Dados Brutos
- `OBSERVADO` `[.gitignore]`: `.env`, `data/`, `assets/`, `venv/` e `__pycache__/` estão ignorados no Git.
- `NUNCA` ler, imprimir ou transcrever `.env*` ou strings de conexão com senha. Referenciar apenas nomes das variáveis (`DB_USER`, `DB_PASS`, `DB_HOST`, `DB_PORT`, `DB_NAME`) `[database.py]`.
- `NUNCA` abrir arquivos brutos (`data/*.csv`) para leitura de conteúdo completo; inspecionar apenas schema/metadados ou cabeçalho mínimo quando estritamente autorizado.

## Segurança Operacional
- `DIRETRIZ`: Operar em modo **somente leitura** por padrão ao inspecionar o PostgreSQL.
- `SEMPRE` usar `LIMIT` em consultas exploratórias no banco (`SELECT ... LIMIT 10`).
- `NUNCA` executar DDL destrutivo (`DROP TABLE`, `TRUNCATE`) ou carga em massa sem confirmação explícita.
