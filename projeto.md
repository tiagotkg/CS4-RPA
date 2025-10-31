# Sprint 4 – Encerramento e Integração Inteligente

## Introdução

Com os robôs de RPA e a camada inicial de inteligência já testados na Sprint 3, esta sprint finaliza o projeto, trazendo integração completa entre automação e inteligência artificial.  
O objetivo é consolidar o fluxo de hiperautomação como uma solução que:

- **Executa ponta a ponta:** coleta, análise e geração de alertas.  
- **Aproveita IA leve** para apoiar as regras de negócio.  
- **Entrega resultados claros** para uso imediato em contexto de RPA corporativo.

---

## Objetivos

- Integrar robôs de RPA e heurísticas de IA em um fluxo único.  
- Demonstrar a aplicação prática da IA leve em conjunto com automação.  
- Criar relatórios/alertas simples que simulem uso corporativo.  
- Consolidar documentação do processo, descrevendo a interação entre RPA e IA.

---

## Requisitos Técnicos

### Pipeline Integrado
- Robô que colete e processe dados em uma fonte real ou simulada.  
- Comparação automática com base consolidada.  
- Classificação simples (*Original / Suspeito / Compatível*).

### Camada de Inteligência
- Aplicação de regras de negócio (palavras-chave, atributos suspeitos).  
- Algoritmo simples de classificação (*Naïve Bayes, regressão logística ou equivalente*).  
- Indicador de risco por produto/vendedor.

### Relatórios e Alertas
- Geração de saída em **CSV** e relatório em **PDF** ou **dashboard básico** (*Streamlit, Excel, etc.*).  
- Simulação de envio de alerta automático (*pode ser mockado*).

### Documentação
- **README** com instruções para execução.  
- **Relatório técnico curto** descrevendo o fluxo RPA + IA e exemplos de detecção.

---

## Entregáveis

- Código em repositório (scripts de RPA + IA).  
- Base consolidada atualizada com rótulos de risco.  
- Relatório final em PDF (fluxo, regras, exemplos).  
- README com instruções de execução.