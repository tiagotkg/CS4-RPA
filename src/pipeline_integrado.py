import pandas as pd
import numpy as np
from datetime import datetime
import logging
import os
import json
from amazon_webscraping import AmazonScraperV2
from classificador_ia import PiracyDetectionClassifier
from gerador_relatorio_tecnico import GeradorRelatorioTecnico
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import warnings
warnings.filterwarnings('ignore')

class IntegratedPiracyDetectionPipeline:
    def __init__(self, config_file="config.json"):
        """
        Inicializa o pipeline integrado de detecção de pirataria
        """
        self.setup_logging()
        self.load_config(config_file)
        self.scraper = None
        self.classifier = None
        self.setup_components()
        
    def setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/pipeline.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self, config_file):
        """Carrega configurações do arquivo JSON"""
        default_config = {
            "scraping": {
                "search_terms": [
                    "cartucho HP 667",
                    "cartucho HP 667XL",
                    "cartucho HP 664",
                    "cartucho HP 662"
                ],
                "max_pages": 2,
                "headless": True
            },
            "ai": {
                "model_file": "resultados/modelo_deteccao_pirataria.pkl",
                "confidence_threshold": 0.7
            },
            "risk_analysis": {
                "high_risk_threshold": 4,
                "medium_risk_threshold": 2
            },
            "output": {
                "results_file": "resultados/resultados_deteccao_pirataria.csv",
                "report_file": "resultados/relatorio_pirataria.html"
            }
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Configurações carregadas de {config_file}")
    
    def setup_components(self):
        """Configura os componentes do pipeline"""
        try:
            # Inicializar scraper
            self.scraper = AmazonScraperV2(
                headless=self.config['scraping']['headless'],
                debug=True
            )
            
            # Inicializar classificador
            self.classifier = PiracyDetectionClassifier()
            
            # Tentar carregar modelo existente
            if os.path.exists(self.config['ai']['model_file']):
                self.classifier.load_model(self.config['ai']['model_file'])
                self.logger.info("Modelo de IA carregado com sucesso")
            else:
                self.logger.info("Modelo de IA não encontrado, será treinado com dados existentes")
            
            self.logger.info("Componentes do pipeline configurados com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar componentes: {e}")
            raise
    
    def executar_pipeline_completo(self):
        """
        Executa o pipeline completo de detecção de pirataria
        """
        self.logger.info("=== INICIANDO PIPELINE DE DETECÇÃO DE PIRATARIA ===")
        
        try:
            # Etapa 1: Coletar dados existentes
            existing_data = self.load_existing_data()
            
            # Etapa 2: Treinar modelo se necessário
            if not self.classifier.is_trained:
                self.train_model_with_existing_data(existing_data)
            
            # Etapa 3: Scraping de novos dados
            new_products = self.scrape_new_products()
            if not new_products:
                self.logger.warning("Nenhum produto coletado no scraping. Encerrando pipeline.")
                return pd.DataFrame()
            
            # Etapa 4: Análise com IA
            analyzed_products = self.analyze_products_with_ai(new_products)
            
            # Etapa 5: Análise de risco
            risk_analyzed_products = self.analisar_niveis_risco(analyzed_products)
            
            # Etapa 6: Salvar resultados
            self.save_results(risk_analyzed_products)
            
            # Etapa 7: Gerar relatório (HTML e PDF)
            self.generate_report(risk_analyzed_products)
            self.generate_pdf_report(risk_analyzed_products)
            
            # Etapa 8: Gerar relatório técnico
            self.generate_technical_report(risk_analyzed_products)
            
            # Etapa 9: Alertas
            self.send_alerts(risk_analyzed_products)
            
            self.logger.info("=== PIPELINE CONCLUÍDO COM SUCESSO ===")
            
            return risk_analyzed_products
            
        except Exception as e:
            self.logger.error(f"Erro durante execução do pipeline: {e}")
            raise
    
    def load_existing_data(self):
        """Carrega dados existentes para treinamento"""
        try:
            # Preferir dataset em data/
            default_path = 'data/base_dados.csv'
            alt_path = 'base_dados.csv'
            dataset_path = default_path if os.path.exists(default_path) else alt_path

            if os.path.exists(dataset_path):
                df = pd.read_csv(dataset_path)
                self.logger.info(f"Dados existentes carregados: {len(df)} registros")
                return df
            else:
                self.logger.warning("Arquivo base_dados.csv não encontrado")
                return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados existentes: {e}")
            return pd.DataFrame()
    
    def train_model_with_existing_data(self, existing_data):
        """Treina o modelo com dados existentes"""
        if len(existing_data) > 0:
            self.logger.info("Treinando modelo com dados existentes...")
            accuracy = self.classifier.treinar_modelo(existing_data)
            # Garantir diretório antes de salvar
            model_path = self.config['ai']['model_file']
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            self.classifier.save_model(model_path)
            self.logger.info(f"Modelo treinado com acurácia: {accuracy:.3f}")
        else:
            self.logger.warning("Sem dados para treinamento")
    
    def scrape_new_products(self):
        """Executa scraping de novos produtos"""
        self.logger.info("Iniciando scraping de novos produtos...")
        
        all_products = []
        search_terms = self.config['scraping']['search_terms']
        max_pages = self.config['scraping']['max_pages']
        
        for term in search_terms:
            self.logger.info(f"Buscando: {term}")
            try:
                # Usar o novo método de scraping completo
                search_url = f"https://www.amazon.com.br/s?k={term.replace(' ', '+')}"
                products = self.scraper.scrape_complete_products(search_url, max_pages)
                all_products.extend(products)
                self.logger.info(f"Encontrados {len(products)} produtos para '{term}'")
            except Exception as e:
                self.logger.error(f"Erro ao buscar '{term}': {e}")
                continue
        
        self.logger.info(f"Total de produtos coletados: {len(all_products)}")
        return all_products
    
    def analyze_products_with_ai(self, products):
        """Analisa produtos com IA, filtrando produtos sem vendedor"""
        if not products:
            self.logger.warning("Nenhum produto para analisar")
            return pd.DataFrame()
        
        self.logger.info("Analisando produtos com IA...")
        
        # Filtrar produtos sem vendedor antes da análise
        products_with_seller = []
        for product in products:
            # Verificar se tem vendedor válido
            has_seller = (
                (product.get('seller_detailed') and 
                 str(product.get('seller_detailed')).strip() and 
                 str(product.get('seller_detailed')).lower() not in ['nan', 'none', 'null', '']) or
                (product.get('seller') and 
                 str(product.get('seller')).strip() and 
                 str(product.get('seller')).lower() not in ['nan', 'none', 'null', ''])
            )
            
            if has_seller:
                products_with_seller.append(product)
            else:
                self.logger.info(f"Produto sem vendedor filtrado: {product.get('title', 'N/A')[:50]}")
        
        if not products_with_seller:
            self.logger.warning("Nenhum produto com vendedor para analisar")
            return pd.DataFrame()
        
        self.logger.info(f"Produtos com vendedor para análise: {len(products_with_seller)}/{len(products)}")
        
        # Converter para DataFrame
        df = pd.DataFrame(products_with_seller)
        
        # Mapear seller_detailed para seller se disponível
        if 'seller_detailed' in df.columns:
            self.logger.info(f"Campo seller_detailed encontrado com {df['seller_detailed'].notna().sum()} valores")
            df['seller'] = df['seller_detailed'].fillna(df.get('seller', ''))
            self.logger.info(f"Vendedores mapeados: {df['seller'].notna().sum()}/{len(df)}")
        else:
            self.logger.warning("Campo seller_detailed não encontrado nos dados")
            self.logger.info(f"Colunas disponíveis: {list(df.columns)}")
        
        # Mapear price_detailed para price se disponível
        if 'price_detailed' in df.columns:
            self.logger.info(f"Campo price_detailed encontrado com {df['price_detailed'].notna().sum()} valores")
            df['price'] = df['price_detailed'].fillna(df.get('price', ''))
            self.logger.info(f"Preços mapeados: {df['price'].notna().sum()}/{len(df)}")
        else:
            self.logger.warning("Campo price_detailed não encontrado nos dados")
        
        # Fazer predições
        if self.classifier.is_trained:
            df = self.classifier.prever(df)
        else:
            self.logger.warning("Modelo não treinado, usando regras heurísticas")
            df['ai_prediction'] = df.apply(self.classifier.apply_heuristic_rules, axis=1)
            df['ai_confidence'] = 0.5  # Confiança padrão
        
        return df
    def analisar_niveis_risco(self, df):
        """Analisa níveis de risco dos produtos"""
        if len(df) == 0:
            return df
        
        self.logger.info("Analisando níveis de risco...")
        
        # Aplicar análise de risco
        df = self.classifier.analyze_risk_level(df)
        
        # Adicionar timestamp
        df['analysis_timestamp'] = datetime.now().isoformat()
        
        return df
    
    def save_results(self, df):
        """Salva resultados em CSV"""
        if len(df) == 0:
            self.logger.warning("Nenhum resultado para salvar")
            return
        
        filename = self.config['output']['results_file']
        # Criar diretório de saída, se necessário
        out_dir = os.path.dirname(filename)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        df.to_csv(filename, index=False, encoding='utf-8')
        self.logger.info(f"Resultados salvos em {filename}")
        
        # Estatísticas
        total_products = len(df)
        suspicious_products = len(df[df['ai_prediction'] == 'SUSPEITO'])
        high_risk_products = len(df[df['risk_level'] == 'ALTO'])
        
        self.logger.info(f"Estatísticas:")
        self.logger.info(f"  Total de produtos: {total_products}")
        self.logger.info(f"  Produtos suspeitos: {suspicious_products}")
        self.logger.info(f"  Produtos de alto risco: {high_risk_products}")
    
    def generate_report(self, df):
        """Gera relatório HTML"""
        if len(df) == 0:
            self.logger.warning("Nenhum dado para gerar relatório")
            return
        
        self.logger.info("Gerando relatório HTML...")
        
        # Estatísticas gerais
        total_products = len(df)
        suspicious_products = len(df[df['ai_prediction'] == 'SUSPEITO'])
        high_risk_products = len(df[df['risk_level'] == 'ALTO'])
        medium_risk_products = len(df[df['risk_level'] == 'MÉDIO'])
        low_risk_products = len(df[df['risk_level'] == 'BAIXO'])
        
        # Produtos de alto risco
        high_risk_df = df[df['risk_level'] == 'ALTO']
        
        # Gerar HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relatório de Detecção de Pirataria</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat-box {{ background-color: #e8f4f8; padding: 15px; border-radius: 5px; text-align: center; }}
                .high-risk {{ background-color: #ffebee; }}
                .medium-risk {{ background-color: #fff3e0; }}
                .low-risk {{ background-color: #e8f5e8; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .alert {{ background-color: #ffcdd2; padding: 10px; border-radius: 5px; margin: 10px 0; }}
                .product-link {{ 
                    background-color: #007bff; 
                    color: white; 
                    padding: 5px 10px; 
                    text-decoration: none; 
                    border-radius: 3px; 
                    font-size: 12px;
                    display: inline-block;
                    transition: background-color 0.3s;
                }}
                .product-link:hover {{ 
                    background-color: #0056b3; 
                    color: white;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Relatório de Detecção de Pirataria</h1>
                <p>Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <h3>{total_products}</h3>
                    <p>Total de Produtos</p>
                </div>
                <div class="stat-box high-risk">
                    <h3>{high_risk_products}</h3>
                    <p>Alto Risco</p>
                </div>
                <div class="stat-box medium-risk">
                    <h3>{medium_risk_products}</h3>
                    <p>Médio Risco</p>
                </div>
                <div class="stat-box low-risk">
                    <h3>{low_risk_products}</h3>
                    <p>Baixo Risco</p>
                </div>
            </div>
            
            <h2>Produtos de Alto Risco</h2>
            {self.generate_high_risk_table(high_risk_df)}
            
            <h2>Resumo por Predição da IA</h2>
            {self.generate_prediction_summary(df)}
            
            <h2>Todos os Produtos Analisados</h2>
            {self.generate_full_table(df)}
        </body>
        </html>
        """
        
        # Salvar arquivo
        filename = self.config['output']['report_file']
        # Criar diretório de saída, se necessário
        out_dir = os.path.dirname(filename)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.logger.info(f"Relatório salvo em {filename}")
    
    def generate_high_risk_table(self, df):
        """Gera tabela de produtos de alto risco"""
        if len(df) == 0:
            return "<p>Nenhum produto de alto risco encontrado.</p>"
        
        html = "<table><tr><th>Título</th><th>Preço</th><th>Vendedor</th><th>Predição IA</th><th>Score de Risco</th><th>Ação</th></tr>"
        
        for _, row in df.iterrows():
            product_url = row.get('url', '')
            link_button = f'<a href="{product_url}" target="_blank" class="product-link">Ver Produto</a>' if product_url else 'N/A'
            
            html += f"""
            <tr>
                <td>{row.get('title', 'N/A')}</td>
                <td>R$ {row.get('price', 'N/A')}</td>
                <td>{row.get('seller', 'N/A')}</td>
                <td>{row.get('ai_prediction', 'N/A')}</td>
                <td>{row.get('risk_score', 'N/A')}</td>
                <td>{link_button}</td>
            </tr>
            """
        
        html += "</table>"
        return html
    
    def generate_prediction_summary(self, df):
        """Gera resumo das predições"""
        summary = df['ai_prediction'].value_counts()
        
        html = "<table><tr><th>Predição</th><th>Quantidade</th><th>Percentual</th></tr>"
        
        for prediction, count in summary.items():
            percentage = (count / len(df)) * 100
            html += f"<tr><td>{prediction}</td><td>{count}</td><td>{percentage:.1f}%</td></tr>"
        
        html += "</table>"
        return html
    
    def generate_full_table(self, df):
        """Gera tabela completa de produtos"""
        if len(df) == 0:
            return "<p>Nenhum produto encontrado.</p>"
        
        html = "<table><tr><th>Título</th><th>Preço</th><th>Vendedor</th><th>Predição IA</th><th>Nível de Risco</th><th>Ação</th></tr>"
        
        for _, row in df.iterrows():
            risk_class = row.get('risk_level', 'N/A')
            product_url = row.get('url', '')
            link_button = f'<a href="{product_url}" target="_blank" class="product-link">Ver Produto</a>' if product_url else 'N/A'
            
            html += f"""
            <tr class="{risk_class.lower().replace('é', 'e')}-risk">
                <td>{row.get('title', 'N/A')}</td>
                <td>R$ {row.get('price', 'N/A')}</td>
                <td>{row.get('seller', 'N/A')}</td>
                <td>{row.get('ai_prediction', 'N/A')}</td>
                <td>{risk_class}</td>
                <td>{link_button}</td>
            </tr>
            """
        
        html += "</table>"
        return html
    
    def generate_pdf_report(self, df):
        """Gera relatório em PDF"""
        if len(df) == 0:
            self.logger.warning("Nenhum dado para gerar relatório PDF")
            return
        
        self.logger.info("Gerando relatório PDF...")
        
        # Nome do arquivo PDF
        pdf_filename = self.config['output']['report_file'].replace('.html', '.pdf')
        out_dir = os.path.dirname(pdf_filename)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        
        # Criar documento PDF
        doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3949ab'),
            spaceAfter=12
        )
        
        # Título
        elements.append(Paragraph("Relatório de Detecção de Pirataria", title_style))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Estatísticas gerais
        total_products = len(df)
        suspicious_products = len(df[df['ai_prediction'] == 'SUSPEITO'])
        original_products = len(df[df['ai_prediction'] == 'ORIGINAL'])
        compatible_products = len(df[df['ai_prediction'] == 'COMPATIVEL'])
        high_risk_products = len(df[df['risk_level'] == 'ALTO'])
        medium_risk_products = len(df[df['risk_level'] == 'MÉDIO'])
        low_risk_products = len(df[df['risk_level'] == 'BAIXO'])
        
        elements.append(Paragraph("Estatísticas Gerais", heading_style))
        
        # Tabela de estatísticas
        stats_data = [
            ['Métrica', 'Quantidade', 'Percentual'],
            ['Total de Produtos', str(total_products), '100%'],
            ['Produtos Suspeitos', str(suspicious_products), f'{(suspicious_products/total_products*100):.1f}%'],
            ['Produtos Originais', str(original_products), f'{(original_products/total_products*100):.1f}%'],
            ['Produtos Compatíveis', str(compatible_products), f'{(compatible_products/total_products*100):.1f}%'],
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Níveis de risco
        elements.append(Paragraph("Análise de Níveis de Risco", heading_style))
        
        risk_data = [
            ['Nível de Risco', 'Quantidade', 'Percentual'],
            ['Alto Risco', str(high_risk_products), f'{(high_risk_products/total_products*100):.1f}%'],
            ['Médio Risco', str(medium_risk_products), f'{(medium_risk_products/total_products*100):.1f}%'],
            ['Baixo Risco', str(low_risk_products), f'{(low_risk_products/total_products*100):.1f}%'],
        ]
        
        risk_table = Table(risk_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d32f2f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(risk_table)
        elements.append(PageBreak())
        
        # Produtos de alto risco
        high_risk_df = df[df['risk_level'] == 'ALTO'].head(20)  # Limitar a 20 produtos
        
        if len(high_risk_df) > 0:
            elements.append(Paragraph("Produtos de Alto Risco", heading_style))
            
            # Preparar dados da tabela
            high_risk_data = [['Título', 'Preço', 'Vendedor', 'Predição IA', 'Score']]
            for _, row in high_risk_df.iterrows():
                title = str(row.get('title', 'N/A'))[:60] + '...' if len(str(row.get('title', ''))) > 60 else str(row.get('title', 'N/A'))
                price = f"R$ {row.get('price', 'N/A')}"
                seller = str(row.get('seller', 'N/A'))[:30]
                prediction = str(row.get('ai_prediction', 'N/A'))
                score = str(row.get('risk_score', 'N/A'))
                high_risk_data.append([title, price, seller, prediction, score])
            
            high_risk_table = Table(high_risk_data, colWidths=[2.5*inch, 1*inch, 1.2*inch, 1*inch, 0.8*inch])
            high_risk_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d32f2f')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ffebee')])
            ]))
            elements.append(high_risk_table)
        
        # Construir PDF
        doc.build(elements)
        self.logger.info(f"Relatório PDF gerado em {pdf_filename}")
    
    def generate_technical_report(self, df):
        """Gera relatório técnico descrevendo o fluxo RPA + IA"""
        if len(df) == 0:
            self.logger.warning("Nenhum dado para gerar relatório técnico")
            return
        
        self.logger.info("Gerando relatório técnico...")
        
        try:
            gerador = GeradorRelatorioTecnico()
            output_file = gerador.gerar_relatorio(
                output_file="resultados/relatorio_tecnico.pdf",
                dados_resultados=df
            )
            self.logger.info(f"Relatório técnico gerado em {output_file}")
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório técnico: {e}")
    
    def send_alerts(self, df):
        """Envia alertas para produtos de alto risco (simulação mockada)"""
        if len(df) == 0 or 'risk_level' not in df.columns:
            self.logger.info("Sem dados de risco para alertar")
            return
        
        high_risk_products = df[df['risk_level'] == 'ALTO']
        
        if len(high_risk_products) > 0:
            self.logger.warning(f"🚨 ALERTA: {len(high_risk_products)} produtos de alto risco detectados!")
            
            # Simular envio de alerta por email (mockado)
            alert_file = os.path.join('resultados', 'alertas.txt')
            os.makedirs(os.path.dirname(alert_file), exist_ok=True)
            
            with open(alert_file, 'w', encoding='utf-8') as f:
                f.write(f"=== ALERTAS DE PIRATARIA - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ===\n\n")
                f.write(f"Total de produtos de alto risco: {len(high_risk_products)}\n\n")
                
                for idx, (_, product) in enumerate(high_risk_products.iterrows(), 1):
                    f.write(f"ALERTA #{idx}:\n")
                    f.write(f"  Título: {product.get('title', 'N/A')}\n")
                    f.write(f"  Preço: R$ {product.get('price', 'N/A')}\n")
                    f.write(f"  Vendedor: {product.get('seller', 'N/A')}\n")
                    f.write(f"  Predição IA: {product.get('ai_prediction', 'N/A')}\n")
                    f.write(f"  Score de Risco: {product.get('risk_score', 'N/A')}\n")
                    f.write(f"  URL: {product.get('url', 'N/A')}\n")
                    f.write("-" * 80 + "\n\n")
            
            self.logger.info(f"Alertas salvos em {alert_file}")
            
            # Simular envio de alerta (mockado - em produção seria email/SMS/webhook)
            self.logger.info("📧 [MOCK] Simulando envio de alerta por email...")
            self.logger.info(f"   Para: equipe-compliance@empresa.com")
            self.logger.info(f"   Assunto: ALERTA: {len(high_risk_products)} produtos de alto risco detectados")
            self.logger.info("   Status: ✓ Alerta mockado enviado com sucesso")
            
            # Log detalhado no console
            for idx, (_, product) in enumerate(high_risk_products.head(5).iterrows(), 1):
                self.logger.warning(f"  [{idx}] PRODUTO SUSPEITO: {product.get('title', 'N/A')[:60]}... - R$ {product.get('price', 'N/A')}")
            
            if len(high_risk_products) > 5:
                self.logger.warning(f"  ... e mais {len(high_risk_products) - 5} produtos (ver arquivo de alertas)")
        else:
            self.logger.info("✓ Nenhum produto de alto risco detectado - Sistema operando normalmente")
    
    def cleanup(self):
        """Limpa recursos"""
        if self.scraper:
            self.scraper.close()
        self.logger.info("Recursos limpos")

def main():
    """
    Função principal para executar o pipeline
    """
    pipeline = IntegratedPiracyDetectionPipeline()
    
    try:
        # Executar pipeline completo
        results = pipeline.executar_pipeline_completo()
        
        print(f"\n=== PIPELINE EXECUTADO COM SUCESSO ===")
        print(f"Total de produtos analisados: {len(results)}")
        
        if len(results) > 0:
            print(f"Produtos suspeitos: {len(results[results['ai_prediction'] == 'SUSPEITO'])}")
            print(f"Produtos de alto risco: {len(results[results['risk_level'] == 'ALTO'])}")
            print(f"Relatório gerado: {pipeline.config['output']['report_file']}")
        
    except Exception as e:
        print(f"Erro durante execução do pipeline: {e}")
    
    finally:
        pipeline.cleanup()

if __name__ == "__main__":
    main()
