## 1. Nomes dos membros

* Luiz Fernando Gonçalves Rocha
* José Eduardo Duarte Massucato
* Lucas Almeida Amaral
* Vinicius Leite Censi Faria

## 2. Explicação do sistema

Ferramenta de linha de comando voltada para a identificação de problemas de manutenção em repositórios de software. Seu principal objetivo é analisar a evolução do código ao longo do tempo, utilizando, principalmente, o histórico de commits de um repositório do Github, de modo a detectar padrões que indiquem baixa manutenibilidade. A ferramenta deve receber como entrada um repositório local ou remoto e então executar automaticamente um processo de mineração de dados sobre seu histórico e seus arquivos de código-fonte. 

O funcionamento do sistema será organizado em etapas bem definidas:
1. Coleta dos dados, na qual o repositório é acessado e seu histórico de commits é percorrido.
2. Extração das informações relevantes, como arquivos modificados em cada commit, quantidade de linhas adicionadas e removidas, frequência de alterações por arquivo e autoria das modificações.
3. O código-fonte de cada arquivo é analisado para extrair métricas estruturais, como complexidade ciclomática e tamanho dos arquivos.

A partir desses dados, o sistema realiza uma etapa de análise, na qual são identificados possíveis indicadores de problemas de manutenção. Entre eles, destacam-se os hotspots, commits excessivamente grandes e arquivos com crescimento contínuo ao longo do tempo.

Os resultados serão apresentados ao usuário de forma clara e objetiva diretamente no terminal, podendo também ser exportados em formatos estruturados, como JSON ou CSV. A saída inclui rankings de arquivos críticos, identificação de commits suspeitos e métricas resumidas do repositório, permitindo ao desenvolvedor compreender rapidamente os principais pontos de atenção do sistema analisado.


## 3. Explicação das possíveis tecnologias utilizadas

Explicação das possíveis tecnologias utilizadas

* pydriller: Para iterar sobre os commits, iterar sobre os arquivos modificados em cada commit, pegar a quantidade de linhas adicionadas/removidas (churn), identificar o autor e a data. Permite caminhos de diretórios locais e URLs de repositórios remotos do GitHub

* lizard: Será o motor da sua análise de código-fonte, para obter métricas como complexidade ciclomática

* Pandas: Para pegar os dados brutos extraídos pelo Pydriller e transformá-los em um DataFrame para realizar a análise e exportar os dados
