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
git clone https://github.com/<usuario>/jamal.git
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
