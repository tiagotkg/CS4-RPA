# Integrantes:
- **555183** - Danilo Ramalho Silva
- **554668** - Israel Dalcin Alves Diniz
- **556213** - João Vitor Pires da Silva
- **555677** - Matheus Hungaro Fidelis
- **556389** - Pablo Menezes Barreto
- **556984** - Tiago Toshio Kumagai Gibo


# Sistema de Hiperautomação para Detecção de 

Este projeto implementa um sistema de hiperautomação que combina RPA (Robotic Process Automation) e técnicas de IA leve para identificar automaticamente indícios de pirataria em produtos de cartuchos HP.

## 📁 Link do Github
https://github.com/tiagotkg/CS3-RPA.git

## 🎯 Objetivos

- **Automação RPA**: Coletar dados de produtos em tempo real da Amazon.com.br
- **Inteligência Artificial**: Classificar produtos como Original/Suspeito/Compatível
- **Análise de Risco**: Identificar produtos de alto, médio e baixo risco
- **Relatórios Automáticos**: Gerar relatórios em HTML, PDF e dashboard interativo
- **Alertas Automáticos**: Sistema de alertas mockado para produtos de alto risco
- **Relatório Técnico**: Documentação completa do fluxo RPA + IA

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   RPA Scraper   │───▶│  AI Classifier  │───▶│ Risk Analyzer   │
│   (Amazon)      │    │   (ML Model)    │    │  (Heuristics)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Storage  │    │  Model Training │    │  Report Gen.    │
│     (CSV)       │    │   (Pickle)      │    │ (HTML/PDF/Dash) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                                           │
         └───────────────────┬───────────────────────┘
                             ▼
                    ┌─────────────────┐
                    │  Alert System   │
                    │    (Mock)       │
                    └─────────────────┘
```

## 📁 Estrutura do Projeto

```
CS3-RPA/
├── src/                           # Código principal
│   ├── amazon_webscraping.py     # Robô RPA para scraping da Amazon
│   ├── classificador_ia.py        # Classificador de IA para detecção
│   ├── pipeline_integrado.py      # Pipeline integrado completo
│   ├── analisar_dados.py          # Análise dos dados existentes
│   ├── dashboard.py               # Dashboard Streamlit (Sprint 4)
│   └── gerador_relatorio_tecnico.py # Gerador de relatório técnico (Sprint 4)
├── data/                     # Dados do projeto
│   ├── base_dados.csv        # Base de dados existente
│   ├── catalogo.csv          # Catálogo oficial HP
│   ├── complete_pipeline_results.csv # Resultados do pipeline
│   └── products_with_ai_analysis.csv # Produtos com análise de IA
├── resultados/               # Arquivos de saída
│   ├── modelo_deteccao_pirataria.pkl # Modelo de IA treinado
│   ├── resultados_*.csv      # Resultados das análises
│   └── relatorio_*.html      # Relatórios HTML
├── config.json               # Configurações do sistema
├── requirements.txt          # Dependências Python
├── .gitignore                # Arquivos ignorados pelo Git
└── README.md                 # Este arquivo
```

## 🚀 Instalação e Configuração

### 1. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar ChromeDriver

O sistema usa Selenium com ChromeDriver, que é baixado automaticamente via webdriver-manager.

## 🗂️ Organização do Projeto

O projeto foi organizado seguindo as melhores práticas:

- **`src/`**: Código principal do sistema
- **`tests/`**: Testes organizados com documentação
- **`data/`**: Dados do projeto (CSV, resultados)
- **`.gitignore`**: Configurado para ignorar arquivos desnecessários

## 📊 Como Usar

### 1. Análise dos Dados Existentes

```bash
python src/analisar_dados.py
```

Este comando analisa a estrutura dos dados existentes e identifica padrões suspeitos.


### 2. Executa o pipeline completo, gerando:
- `resultados/resultados_deteccao_pirataria.csv`: Resultados completos
- `resultados/relatorio_pirataria.html`: Relatório HTML
- `resultados/relatorio_pirataria.pdf`: Relatório PDF
- `resultados/relatorio_tecnico.pdf`: Relatório técnico completo
- `resultados/alertas.txt`: Alertas de produtos de alto risco


```bash
python src/pipeline_integrado.py
```

Executa o pipeline completo:
1. **Scraping**: Coleta produtos da Amazon
2. **Classificação IA**: Analisa produtos com modelo treinado
3. **Análise de Risco**: Calcula níveis de risco
4. **Relatórios**: Gera relatórios HTML e PDF
5. **Relatório Técnico**: Documentação do fluxo RPA + IA
6. **Alertas**: Identifica produtos de alto risco (mockado)

### 3. Dashboard Interativo (Streamlit)

```bash
streamlit run src/dashboard.py
```

Abre um dashboard interativo no navegador com:
- Visualizações gráficas dos resultados
- Filtros por predição IA, nível de risco e vendedor
- Tabelas interativas de produtos
- Download de CSV filtrado
- Estatísticas em tempo real

### 4. Scraping Manual da Amazon (caso queira ver o webscraping rodando no navegador)

```bash
python src/amazon_webscraping.py
```

Executa apenas o scraping da Amazon (requer navegador Chrome).

## 🤖 Componentes do Sistema

### 1. Amazon Scraper (`src/amazon_webscraping.py`)

- **Funcionalidade**: Coleta produtos da Amazon.com.br
- **Tecnologia**: Selenium WebDriver
- **Dados Coletados**: Título, preço, vendedor, avaliações, URL
- **Filtros**: Identifica produtos suspeitos em tempo real

### 2. AI Classifier (`src/classificador_ia.py`)

- **Algoritmo**: Random Forest + TF-IDF
- **Features**: Texto (título, descrição) + numéricas (preço, vendedor)
- **Classes**: ORIGINAL, SUSPEITO, COMPATIVEL
- **Acurácia**: ~85.7% nos dados de teste
- **Modelo**: Salvo em `resultados/modelo_deteccao_pirataria.pkl`

### 3. Risk Analyzer

- **Método**: Regras heurísticas + score de risco
- **Fatores**: Preço, vendedor, palavras-chave, confiança da IA
- **Níveis**: ALTO, MÉDIO, BAIXO

### 4. Report Generator (Sprint 4)

- **Formatos**: HTML responsivo, PDF, Dashboard Streamlit
- **Conteúdo**: Estatísticas, produtos de risco, tabelas detalhadas
- **Visualização**: Cores por nível de risco, gráficos interativos
- **Relatório Técnico**: Documentação completa do fluxo RPA + IA em PDF

### 5. Sistema de Alertas (Sprint 4)

- **Funcionalidade**: Detecção automática de produtos de alto risco
- **Formato**: Arquivo de texto + simulação mockada de email
- **Configuração**: Alertas configuráveis por nível de risco


### Palavras-chave Suspeitas Identificadas

- genérico, cópia, compatível, recondicionado, usado
- refurbished, remanufactured, não original, alternativo

### Vendedores de Confiança

- Amazon.com.br, HP Brasil

## ⚙️ Configurações

Edite `config.json` para personalizar:

```json
{
  "scraping": {
    "search_terms": ["cartucho HP 667", "cartucho HP 667XL"],
    "max_pages": 2,
    "headless": true
  },
  "ai": {
    "model_file": "resultados/modelo_deteccao_pirataria.pkl",
    "confidence_threshold": 0.7
  },
  "risk_analysis": {
    "high_risk_threshold": 4,
    "medium_risk_threshold": 2
  }
}
```

## 🔍 Exemplos de Detecção

### Produto Suspeito Detectado
- **Título**: "Cartucho Compatível HP 667 Preto Genérico"
- **Preço**: R$ 25.90 (muito abaixo do mercado)
- **Vendedor**: "Marketplace Vendedor"
- **Razões**: Palavras "compatível" e "genérico" no título
- **Nível de Risco**: ALTO

### Produto Original
- **Título**: "Cartucho HP 667 Original Preto 2ml"
- **Preço**: R$ 69.90 (preço de mercado)
- **Vendedor**: "Amazon.com.br"
- **Nível de Risco**: BAIXO

## 🚨 Alertas e Monitoramento

O sistema gera alertas automáticos para:
- Produtos com score de risco ≥ 4
- Preços muito abaixo do mercado (< R$ 30)
- Vendedores não confiáveis
- Palavras-chave suspeitas

## 📊 Arquivos de Saída

### Dados e Resultados
- `data/complete_pipeline_results.csv`: Dados completos com análises
- `data/products_with_ai_analysis.csv`: Produtos com análise de IA
- `resultados/resultados_deteccao_pirataria.csv`: Resultados do pipeline

### Relatórios (Sprint 4)
- `resultados/relatorio_pirataria.html`: Relatório visual interativo (HTML)
- `resultados/relatorio_pirataria.pdf`: Relatório em PDF
- `resultados/relatorio_tecnico.pdf`: Relatório técnico completo (fluxo RPA + IA)
- `resultados/alertas.txt`: Alertas de produtos de alto risco

### Modelo e Configuração
- `resultados/modelo_deteccao_pirataria.pkl`: Modelo de IA treinado
- `config.json`: Configurações do sistema

## 🆕 Novidades da Sprint 4

### Funcionalidades Implementadas

1. **Geração de Relatórios em PDF**
   - Relatórios formatados profissionalmente
   - Estatísticas e tabelas detalhadas
   - Compatível com ambiente corporativo

2. **Dashboard Interativo (Streamlit)**
   - Visualizações gráficas interativas
   - Filtros dinâmicos por predição, risco e vendedor
   - Download de dados filtrados
   - Estatísticas em tempo real

3. **Sistema de Alertas Melhorado**
   - Alertas automáticos para produtos de alto risco
   - Simulação mockada de envio por email
   - Arquivo de alertas para revisão manual

4. **Relatório Técnico Completo**
   - Documentação do fluxo RPA + IA
   - Exemplos de detecção
   - Regras de negócio documentadas
   - Arquitetura do sistema explicada

5. **Integração Completa**
   - Pipeline ponta a ponta funcional
   - Múltiplos formatos de saída
   - Documentação completa do processo
