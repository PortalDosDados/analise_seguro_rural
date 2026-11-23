# 03 - Qualidade de Dados, Testes e Checklist

## Testes de Código e Dados
- `OBSERVADO`: Nenhum teste automatizado existe no repositório atualmente (`NÃO IDENTIFICADO`).
- `DIRETRIZ` (confirmado): Adotar `ruff` (lint/format) e `pytest` para testes unitários e de transformação com dados sintéticos/fixtures (sem depender de CSVs reais em `data/`).
- `DIRETRIZ` para camada `silver`:
  - Validar unicidade e não-nulidade de `id_proposta` (`PRIMARY KEY`).
  - Validar contagem de linhas carregadas vs. linhas lidas e registrar linhas descartadas (evitar `on_bad_lines='skip'` silencioso).
- `SUGESTÃO (confirmar)`: Adicionar validação de schema (ex.: `pandera` ou checks SQL pós-carga) para intervalos de datas e valores não negativos.

## Checklist Obrigatório Antes de Concluir Tarefas
- [ ] Rodar `ruff check` / `pytest` se estiverem configurados e aplicáveis ao escopo alterado (somente comandos confirmados).
- [ ] Avaliar impacto downstream (`bronze` → `silver` → `gold`) ao renomear, tipar ou remover colunas.
- [ ] `NUNCA` executar `DROP`, `TRUNCATE`, `DELETE`, `--full-refresh` ou backfill destrutivo no PostgreSQL sem autorização explícita do usuário.
- [ ] `NUNCA` commitar arquivos de `data/`, outputs de notebooks (`*.ipynb`), artefatos ou `.env`.
- [ ] `NUNCA` adicionar dependências em `[requirements.txt]` ou alterar arquivos fora do escopo sem aprovação.
- [ ] Atualizar `[README.md]` se novos scripts ou comandos de execução forem adicionados.
