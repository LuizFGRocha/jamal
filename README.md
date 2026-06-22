# Jamal

Ferramenta de linha de comando para identificar problemas de manutenção em repositórios de software. Jamal minera o histórico de commits de um repositório Git (local ou remoto via GitHub) e detecta padrões indicativos de baixa manutenibilidade: hotspots, commits excessivamente grandes, arquivos em crescimento contínuo e acoplamento implícito entre arquivos.

## Membros

- Luiz Fernando Gonçalves Rocha
- José Eduardo Duarte Massucato
- Lucas Almeida Amaral
- Vinicius Leite Censi Faria

## Objetivo

Analisar a evolução de um repositório de software ao longo do tempo, combinando dados do histórico de commits com métricas estáticas de código-fonte, para detectar indicadores concretos de baixa manutenibilidade. A saída inclui rankings de arquivos críticos, identificação de commits suspeitos e métricas resumidas do repositório.

## Tecnologias

| Biblioteca | Uso |
|---|---|
| **pydriller** | Iteração sobre commits, extração de metadados (autoria, data, churn) |
| **lizard** | Análise estática: complexidade ciclomática, LOC, contagem de funções |
| **pandas** | Manipulação de dados tabulares |
| **rich** | Saída formatada e colorida no terminal |
| **click** | Interface de linha de comando |

## Instalação

```bash
git clone https://github.com/LuizFGRocha/jamal.git
cd jamal
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Alternativa com [uv](https://docs.astral.sh/uv/):

```bash
uv venv && uv pip install -e ".[dev]"
```

## Uso

> **Observação:** nos exemplos abaixo, `.` representa o caminho para o repositório a ser analisado (por exemplo, `/caminho/para/repositorio`).

```bash
# Analisar um repositório local
jamal analyze /caminho/para/repositorio

# Analisar um repositório remoto
jamal analyze https://github.com/pallets/flask

# Limitar resultados (padrão: 10 por seção)
jamal analyze . --top 5

# Filtrar por intervalo de datas
jamal analyze . --since 2024-01-01 --until 2024-06-30

# Analisar apenas uma branch
jamal analyze . --branch main

# Exportar para JSON
jamal analyze . --output json --output-file results.json

# Exportar hotspots para CSV
jamal analyze . --output csv --output-file hotspots.csv
```

## Métricas

| Métrica | Módulo | Descrição |
|---|---|---|
| **Cyclomatic Complexity** | extractor | Complexidade média das funções por arquivo |
| **LOC** | extractor | Linhas de código efetivas |
| **Token Count** | extractor | Total de tokens (proxy de tamanho semântico) |
| **Churn** | collector | Linhas adicionadas + removidas por arquivo |
| **Hotspot Score** | analyzer | Frequência de mudanças × complexidade ciclomática |
| **Bus Factor** | analyzer | Número de autores distintos por arquivo |
| **File Coupling** | analyzer | Pares de arquivos frequentemente alterados juntos |
| **Big Commits** | analyzer | Commits com >10 arquivos ou >500 linhas de churn |
| **Continuous Growth** | analyzer | Arquivos com tendência crescente de churn |

## Executando os Testes

```bash
pytest tests/ -v
```

Com relatório de cobertura:

```bash
pytest tests/ -v --cov=jamal --cov-report=term-missing
```

## Exemplo de Saída

```
Analyzing: https://github.com/pallets/flask
Found 2847 commits.

╭─────────────────── Repository Summary ────────────────────╮
│ Total commits:       2847                                  │
│ Unique files:        412                                   │
│ Authors:             183                                   │
│ Avg churn/commit:    38.4                                  │
│                                                            │
│ Top contributors:                                          │
│   David Lord: 812 commits                                  │
│   Armin Ronacher: 523 commits                              │
╰────────────────────────────────────────────────────────────╯

╭─ Top Hotspots ──────────────────────────────────────────────╮
│ File              Changes  Churn  Avg CC  Bus Factor  Score │
│ src/flask/app.py      312  18400     8.2          47  2558  │
│ src/flask/ctx.py      198   9200     6.1          31  1208  │
╰─────────────────────────────────────────────────────────────╯
```

## Estrutura do Projeto

```
jamal/
├── jamal/
│   ├── cli.py        # Ponto de entrada CLI
│   ├── collector.py  # Coleta via pydriller
│   ├── extractor.py  # Métricas via lizard
│   ├── analyzer.py   # Algoritmos de análise
│   ├── reporter.py   # Saída formatada
│   ├── models.py     # Modelos de dados
│   └── config.py     # Constantes
├── tests/
└── .github/workflows/ci.yml
```

## Uso de IA
Utilizamos ferramentas de Inteligência Artificial para apoiar a refatoração de código, a identificação e correção de bugs e a avaliação da qualidade dos testes, como a busca por comportamentos não contemplados pela suíte existente.

As decisões de projeto, implementação e validação final permaneceram sob responsabilidade da equipe. A principal ferramenta utilizada foi o GitHub Copilot, com uso predominante do modelo Claude.