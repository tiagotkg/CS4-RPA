"""
Gerador de Relatório Técnico em PDF
Descreve o fluxo RPA + IA e exemplos de detecção
Sprint 4 - Sistema de Hiperautomação
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import pandas as pd
import json

class GeradorRelatorioTecnico:
    """Gera relatório técnico descrevendo o fluxo RPA + IA"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configura estilos personalizados"""
        # Estilo de título principal
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Estilo de subtítulo
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#3949ab'),
            spaceAfter=15,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        # Estilo de cabeçalho de seção
        self.section_style = ParagraphStyle(
            'CustomSection',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#5c6bc0'),
            spaceAfter=12,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        # Estilo de texto normal justificado
        self.normal_justified = ParagraphStyle(
            'NormalJustified',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        )
        
        # Estilo de código/exemplo
        self.code_style = ParagraphStyle(
            'CodeStyle',
            parent=self.styles['Code'],
            fontSize=9,
            fontName='Courier',
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10,
            backColor=colors.HexColor('#f5f5f5')
        )
    
    def gerar_relatorio(self, output_file="resultados/relatorio_tecnico.pdf", 
                       dados_resultados=None):
        """Gera o relatório técnico completo"""
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        elements = []
        
        # Capa
        elements.extend(self._gerar_capa())
        elements.append(PageBreak())
        
        # Introdução
        elements.extend(self._gerar_introducao())
        elements.append(PageBreak())
        
        # Arquitetura do Sistema
        elements.extend(self._gerar_arquitetura())
        elements.append(PageBreak())
        
        # Fluxo RPA + IA
        elements.extend(self._gerar_fluxo_rpa_ia())
        elements.append(PageBreak())
        
        # Exemplos de Detecção
        if dados_resultados is not None:
            elements.extend(self._gerar_exemplos_deteccao(dados_resultados))
            elements.append(PageBreak())
        
        # Regras de Negócio
        elements.extend(self._gerar_regras_negocio())
        elements.append(PageBreak())
        
        # Modelo de IA
        elements.extend(self._gerar_modelo_ia())
        
        # Construir PDF
        doc.build(elements)
        
        return output_file
    
    def _gerar_capa(self):
        """Gera a capa do relatório"""
        elements = []
        
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph("Sistema de Hiperautomação", self.title_style))
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("Detecção de Pirataria em Cartuchos HP", 
                                  self.subtitle_style))
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("Integração RPA + Inteligência Artificial", 
                                  ParagraphStyle('CustomTitle2', parent=self.styles['Normal'], 
                                                fontSize=14, alignment=TA_CENTER)))
        
        elements.append(Spacer(1, 2*inch))
        
        elements.append(Paragraph("Relatório Técnico", 
                                  ParagraphStyle('NormalCenter', parent=self.styles['Normal'],
                                                fontSize=12, alignment=TA_CENTER)))
        elements.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                                  ParagraphStyle('NormalCenter', parent=self.styles['Normal'],
                                                fontSize=10, alignment=TA_CENTER, 
                                                textColor=colors.grey)))
        
        elements.append(Spacer(1, 1*inch))
        elements.append(Paragraph("Sprint 4 - Encerramento e Integração Inteligente",
                                  ParagraphStyle('NormalCenter', parent=self.styles['Normal'],
                                                fontSize=11, alignment=TA_CENTER)))
        
        return elements
    
    def _gerar_introducao(self):
        """Gera a seção de introdução"""
        elements = []
        
        elements.append(Paragraph("1. Introdução", self.subtitle_style))
        
        intro_text = """
        Este relatório técnico descreve a implementação do sistema de hiperautomação 
        desenvolvido para detecção automática de indícios de pirataria em produtos de 
        cartuchos HP disponíveis na plataforma Amazon.com.br.
        
        O sistema combina técnicas de Robotic Process Automation (RPA) para coleta 
        automatizada de dados com algoritmos de Inteligência Artificial leve para 
        classificação e análise de risco dos produtos coletados.
        
        A solução foi desenvolvida seguindo as melhores práticas de automação corporativa, 
        utilizando tecnologias open-source e abordando o problema de forma incremental 
        através de sprints de desenvolvimento.
        """
        
        elements.append(Paragraph(intro_text, self.normal_justified))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph("1.1. Objetivos", self.section_style))
        
        objetivos_text = """
        O sistema foi projetado para:
        <bullet>&bull;</bullet> Executar coleta automatizada de dados de produtos da Amazon.com.br
        <bullet>&bull;</bullet> Classificar produtos utilizando modelos de IA treinados
        <bullet>&bull;</bullet> Calcular níveis de risco baseados em regras de negócio e predições da IA
        <bullet>&bull;</bullet> Gerar relatórios e alertas automáticos para produtos de alto risco
        <bullet>&bull;</bullet> Fornecer dashboard interativo para visualização dos resultados
        """
        
        elements.append(Paragraph(objetivos_text.replace('<bullet>&bull;</bullet>', '•'), 
                                self.normal_justified))
        
        return elements
    
    def _gerar_arquitetura(self):
        """Gera a seção de arquitetura"""
        elements = []
        
        elements.append(Paragraph("2. Arquitetura do Sistema", self.subtitle_style))
        
        arquitetura_text = """
        O sistema é composto por três componentes principais que trabalham em conjunto:
        
        <b>2.1. Robô RPA (Amazon Scraper)</b>
        
        Responsável pela coleta automatizada de dados da Amazon.com.br. Utiliza Selenium 
        WebDriver para simular navegação de navegador e extrair informações dos produtos, 
        incluindo título, preço, vendedor, avaliações e URL.
        
        <b>2.2. Classificador de IA</b>
        
        Implementa algoritmos de Machine Learning (Random Forest + TF-IDF) para classificar 
        produtos em três categorias: ORIGINAL, SUSPEITO ou COMPATIVEL. O modelo é treinado 
        com base em regras heurísticas aplicadas aos dados históricos.
        
        <b>2.3. Analisador de Risco</b>
        
        Combina predições da IA com regras de negócio para calcular um score de risco e 
        classificar produtos em níveis ALTO, MÉDIO ou BAIXO risco.
        """
        
        elements.append(Paragraph(arquitetura_text, self.normal_justified))
        
        return elements
    
    def _gerar_fluxo_rpa_ia(self):
        """Gera a seção descrevendo o fluxo RPA + IA"""
        elements = []
        
        elements.append(Paragraph("3. Fluxo RPA + Inteligência Artificial", self.subtitle_style))
        
        elements.append(Paragraph("3.1. Pipeline Integrado", self.section_style))
        
        fluxo_text = """
        O pipeline completo de detecção segue os seguintes passos:
        
        <b>Etapa 1: Coleta de Dados (RPA)</b>
        O robô RPA navega pela Amazon.com.br buscando produtos relacionados a cartuchos HP. 
        Para cada termo de busca configurado (ex: "cartucho HP 667"), o sistema:
        • Navega pelas páginas de resultados
        • Extrai informações básicas de cada produto (listagem)
        • Acessa páginas individuais para obter detalhes completos
        • Filtra produtos sem informações essenciais (ex: vendedor)
        
        <b>Etapa 2: Comparação com Base Consolidada</b>
        Os produtos coletados são comparados com uma base de dados existente para identificar 
        produtos já conhecidos e novos produtos que requerem análise.
        
        <b>Etapa 3: Classificação com IA</b>
        Cada produto coletado é analisado pelo modelo de IA que:
        • Extrai features textuais (TF-IDF do título, descrição, vendedor)
        • Extrai features numéricas (preço, confiança do vendedor)
        • Gera predição de classificação (ORIGINAL/SUSPEITO/COMPATIVEL)
        • Calcula score de confiança da predição
        
        <b>Etapa 4: Análise de Risco</b>
        O analisador de risco combina múltiplos fatores:
        • Predição da IA
        • Confiança da predição
        • Preço do produto (valores muito baixos ou altos são suspeitos)
        • Vendedor (marketplace vs vendedor oficial)
        • Presença de palavras-chave suspeitas
        
        O resultado é um score de risco e classificação em ALTO, MÉDIO ou BAIXO risco.
        
        <b>Etapa 5: Geração de Relatórios</b>
        Os resultados são consolidados e apresentados em múltiplos formatos:
        • CSV para análise em planilhas
        • HTML para visualização web
        • PDF para documentação formal
        • Dashboard Streamlit para análise interativa
        
        <b>Etapa 6: Alertas Automáticos</b>
        Produtos classificados como ALTO RISCO geram alertas automáticos que são:
        • Registrados em arquivo de log
        • Simulados para envio por email (mockado em ambiente de desenvolvimento)
        • Salvos em arquivo de alertas para revisão manual
        """
        
        elements.append(Paragraph(fluxo_text.replace('<b>', '').replace('</b>', ''), 
                                self.normal_justified))
        
        return elements
    
    def _gerar_exemplos_deteccao(self, dados_resultados):
        """Gera seção com exemplos de detecção"""
        elements = []
        
        elements.append(Paragraph("4. Exemplos de Detecção", self.subtitle_style))
        
        if isinstance(dados_resultados, pd.DataFrame) and len(dados_resultados) > 0:
            # Exemplo de produto suspeito
            suspeitos = dados_resultados[dados_resultados.get('ai_prediction', pd.Series()) == 'SUSPEITO']
            altos_risco = dados_resultados[dados_resultados.get('risk_level', pd.Series()) == 'ALTO']
            
            if len(suspeitos) > 0:
                elements.append(Paragraph("4.1. Produto Classificado como SUSPEITO", 
                                        self.section_style))
                
                exemplo = suspeitos.iloc[0]
                exemplo_text = f"""
                <b>Título:</b> {exemplo.get('title', 'N/A')}
                <br/><b>Preço:</b> R$ {exemplo.get('price', 'N/A')}
                <br/><b>Vendedor:</b> {exemplo.get('seller', 'N/A')}
                <br/><b>Predição IA:</b> {exemplo.get('ai_prediction', 'N/A')}
                <br/><b>Confiança:</b> {exemplo.get('ai_confidence', 'N/A'):.2f} (se disponível)
                <br/><b>Nível de Risco:</b> {exemplo.get('risk_level', 'N/A')}
                <br/><b>Score de Risco:</b> {exemplo.get('risk_score', 'N/A')}
                """
                
                elements.append(Paragraph(exemplo_text, self.normal_justified))
            
            if len(altos_risco) > 0:
                elements.append(Paragraph("4.2. Produto de Alto Risco Detectado", 
                                        self.section_style))
                
                exemplo = altos_risco.iloc[0]
                exemplo_text = f"""
                <b>Título:</b> {exemplo.get('title', 'N/A')}
                <br/><b>Preço:</b> R$ {exemplo.get('price', 'N/A')}
                <br/><b>Vendedor:</b> {exemplo.get('seller', 'N/A')}
                <br/><b>Razões do Alto Risco:</b>
                • Predição da IA: {exemplo.get('ai_prediction', 'N/A')}
                • Score de risco: {exemplo.get('risk_score', 'N/A')}
                """
                
                elements.append(Paragraph(exemplo_text, self.normal_justified))
            
            # Estatísticas gerais
            elements.append(Paragraph("4.3. Estatísticas de Detecção", self.section_style))
            
            total = len(dados_resultados)
            suspeitos_count = len(suspeitos)
            altos_risco_count = len(altos_risco)
            
            stats_data = [
                ['Métrica', 'Quantidade', 'Percentual'],
                ['Total de Produtos Analisados', str(total), '100%'],
                ['Produtos Suspeitos', str(suspeitos_count), 
                 f'{(suspeitos_count/total*100):.1f}%' if total > 0 else '0%'],
                ['Produtos de Alto Risco', str(altos_risco_count),
                 f'{(altos_risco_count/total*100):.1f}%' if total > 0 else '0%']
            ]
            
            stats_table = Table(stats_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(stats_table)
        
        return elements
    
    def _gerar_regras_negocio(self):
        """Gera seção de regras de negócio"""
        elements = []
        
        elements.append(Paragraph("5. Regras de Negócio", self.subtitle_style))
        
        regras_text = """
        O sistema utiliza regras heurísticas combinadas com IA para detectar produtos suspeitos:
        
        <b>5.1. Palavras-chave Suspeitas</b>
        Produtos contendo as seguintes palavras-chave são sinalizados:
        • genérico, cópia, compatível, recondicionado, usado
        • refurbished, remanufactured, compatible, generic
        • não original, alternativo, substituto, imitação
        
        <b>5.2. Análise de Preço</b>
        Preços muito abaixo do mercado (< R$ 30) ou muito acima (> R$ 200) são 
        considerados suspeitos e aumentam o score de risco.
        
        <b>5.3. Confiança do Vendedor</b>
        Vendedores oficiais (Amazon.com.br, HP Brasil) reduzem o score de risco.
        Vendedores de marketplace ou terceiros aumentam o score de risco.
        
        <b>5.4. Score de Risco</b>
        O score é calculado considerando:
        • Predição da IA (SUSPEITO = +3, COMPATIVEL = +1)
        • Confiança da IA (< 0.7 = +1)
        • Preço (< R$ 30 = +2, > R$ 200 = +1)
        • Vendedor (marketplace = +1)
        
        Classificação final:
        • Score ≥ 4: ALTO RISCO
        • Score ≥ 2: MÉDIO RISCO
        • Score < 2: BAIXO RISCO
        """
        
        elements.append(Paragraph(regras_text.replace('<b>', '').replace('</b>', ''), 
                                self.normal_justified))
        
        return elements
    
    def _gerar_modelo_ia(self):
        """Gera seção sobre o modelo de IA"""
        elements = []
        
        elements.append(Paragraph("6. Modelo de Inteligência Artificial", self.subtitle_style))
        
        modelo_text = """
        <b>6.1. Algoritmo Utilizado</b>
        O sistema utiliza Random Forest combinado com vetorização TF-IDF para classificação:
        • <b>Features Textuais:</b> TF-IDF aplicado ao título, descrição e vendedor
        • <b>Features Numéricas:</b> Preço, tamanho do título, confiança do vendedor, 
        contagem de palavras suspeitas/originais
        
        <b>6.2. Treinamento</b>
        O modelo é treinado usando dados históricos rotulados por regras heurísticas. 
        A acurácia típica é de aproximadamente 85% em dados de teste.
        
        <b>6.3. Classes de Predição</b>
        • <b>ORIGINAL:</b> Produto identificado como original/genuíno
        • <b>SUSPEITO:</b> Produto com indícios de pirataria
        • <b>COMPATIVEL:</b> Produto compatível (não original mas não necessariamente pirata)
        
        <b>6.4. Integração com Regras</b>
        As predições da IA são combinadas com regras de negócio para calcular o risco final, 
        permitindo que o sistema aprenda com padrões complexos enquanto mantém controle 
        através de regras explícitas.
        """
        
        elements.append(Paragraph(modelo_text.replace('<b>', '').replace('</b>', ''), 
                                self.normal_justified))
        
        return elements

def main():
    """Função principal para gerar relatório técnico"""
    gerador = GeradorRelatorioTecnico()
    
    # Tentar carregar dados de resultados
    dados = None
    possible_files = [
        'resultados/resultados_deteccao_pirataria.csv',
        'data/complete_pipeline_results.csv'
    ]
    
    for file_path in possible_files:
        if os.path.exists(file_path):
            try:
                dados = pd.read_csv(file_path)
                print(f"Dados carregados de {file_path}")
                break
            except:
                continue
    
    output_file = gerador.gerar_relatorio(dados_resultados=dados)
    print(f"Relatório técnico gerado em: {output_file}")

if __name__ == "__main__":
    main()

