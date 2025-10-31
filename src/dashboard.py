"""
Dashboard Streamlit para visualização dos resultados da detecção de pirataria
Sprint 4 - Sistema de Hiperautomação
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Configuração da página
st.set_page_config(
    page_title="Dashboard - Detecção de Pirataria",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1a237e;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3949ab;
    }
    </style>
""", unsafe_allow_html=True)

def load_results():
    """Carrega os resultados do pipeline"""
    # Tentar carregar diferentes arquivos possíveis
    possible_files = [
        'resultados/resultados_deteccao_pirataria.csv',
        'data/complete_pipeline_results.csv',
        'data/products_with_ai_analysis.csv'
    ]
    
    for file_path in possible_files:
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                return df
            except Exception as e:
                continue
    
    return None

def main():
    """Função principal do dashboard"""
    
    # Header
    st.markdown('<h1 class="main-header">🛡️ Dashboard - Detecção de Pirataria</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Carregar dados
    df = load_results()
    
    if df is None or len(df) == 0:
        st.warning("⚠️ Nenhum dado encontrado. Execute o pipeline primeiro usando: `python src/pipeline_integrado.py`")
        
        # Mostrar instruções
        with st.expander("📋 Como usar o dashboard"):
            st.markdown("""
            ### Passos para visualizar os dados:
            
            1. Execute o pipeline completo:
               ```bash
               python src/pipeline_integrado.py
               ```
            
            2. Aguarde a conclusão do pipeline
            
            3. Recarregue esta página
            
            ### Arquivos esperados:
            - `resultados/resultados_deteccao_pirataria.csv`
            - `data/complete_pipeline_results.csv`
            """)
        return
    
    # Sidebar - Filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro por predição IA
    if 'ai_prediction' in df.columns:
        predictions = ['Todos'] + list(df['ai_prediction'].unique())
        selected_prediction = st.sidebar.selectbox("Predição IA", predictions)
        
        if selected_prediction != 'Todos':
            df = df[df['ai_prediction'] == selected_prediction]
    
    # Filtro por nível de risco
    if 'risk_level' in df.columns:
        risk_levels = ['Todos'] + list(df['risk_level'].unique())
        selected_risk = st.sidebar.selectbox("Nível de Risco", risk_levels)
        
        if selected_risk != 'Todos':
            df = df[df['risk_level'] == selected_risk]
    
    # Filtro por vendedor
    if 'seller' in df.columns:
        sellers = ['Todos'] + sorted(list(df['seller'].dropna().unique()))[:20]
        selected_seller = st.sidebar.selectbox("Vendedor", sellers)
        
        if selected_seller != 'Todos':
            df = df[df['seller'] == selected_seller]
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    total_products = len(df)
    suspicious_products = len(df[df.get('ai_prediction', pd.Series()) == 'SUSPEITO']) if 'ai_prediction' in df.columns else 0
    high_risk = len(df[df.get('risk_level', pd.Series()) == 'ALTO']) if 'risk_level' in df.columns else 0
    avg_price = df['price'].mean() if 'price' in df.columns else 0
    
    with col1:
        st.metric("Total de Produtos", total_products)
    
    with col2:
        st.metric("Produtos Suspeitos", suspicious_products, 
                 delta=f"{(suspicious_products/total_products*100):.1f}%" if total_products > 0 else "0%")
    
    with col3:
        st.metric("Alto Risco", high_risk,
                 delta=f"{(high_risk/total_products*100):.1f}%" if total_products > 0 else "0%")
    
    with col4:
        st.metric("Preço Médio", f"R$ {avg_price:.2f}" if avg_price > 0 else "N/A")
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribuição por Predição IA")
        if 'ai_prediction' in df.columns:
            pred_counts = df['ai_prediction'].value_counts()
            fig_pred = px.pie(
                values=pred_counts.values,
                names=pred_counts.index,
                title="Predições da IA",
                color_discrete_map={
                    'SUSPEITO': '#d32f2f',
                    'ORIGINAL': '#388e3c',
                    'COMPATIVEL': '#f57c00'
                }
            )
            st.plotly_chart(fig_pred, use_container_width=True)
        else:
            st.info("Coluna 'ai_prediction' não encontrada nos dados")
    
    with col2:
        st.subheader("⚠️ Distribuição por Nível de Risco")
        if 'risk_level' in df.columns:
            risk_counts = df['risk_level'].value_counts()
            fig_risk = px.bar(
                x=risk_counts.index,
                y=risk_counts.values,
                title="Níveis de Risco",
                color=risk_counts.index,
                color_discrete_map={
                    'ALTO': '#d32f2f',
                    'MÉDIO': '#f57c00',
                    'BAIXO': '#388e3c'
                },
                labels={'x': 'Nível de Risco', 'y': 'Quantidade'}
            )
            st.plotly_chart(fig_risk, use_container_width=True)
        else:
            st.info("Coluna 'risk_level' não encontrada nos dados")
    
    # Gráfico de preços
    if 'price' in df.columns and 'risk_level' in df.columns:
        st.subheader("💰 Distribuição de Preços por Nível de Risco")
        fig_price = px.box(
            df,
            x='risk_level',
            y='price',
            color='risk_level',
            title="Distribuição de Preços",
            labels={'price': 'Preço (R$)', 'risk_level': 'Nível de Risco'},
            color_discrete_map={
                'ALTO': '#d32f2f',
                'MÉDIO': '#f57c00',
                'BAIXO': '#388e3c'
            }
        )
        st.plotly_chart(fig_price, use_container_width=True)
    
    st.markdown("---")
    
    # Tabela de produtos
    st.subheader("📋 Produtos Analisados")
    
    # Selecionar colunas para exibição
    display_columns = []
    if 'title' in df.columns:
        display_columns.append('title')
    if 'price' in df.columns:
        display_columns.append('price')
    if 'seller' in df.columns:
        display_columns.append('seller')
    if 'ai_prediction' in df.columns:
        display_columns.append('ai_prediction')
    if 'risk_level' in df.columns:
        display_columns.append('risk_level')
    if 'risk_score' in df.columns:
        display_columns.append('risk_score')
    if 'url' in df.columns:
        display_columns.append('url')
    
    if display_columns:
        # Filtrar produtos de alto risco primeiro
        if 'risk_level' in df.columns:
            df_display = df.sort_values('risk_level', ascending=False)
        else:
            df_display = df
        
        st.dataframe(
            df_display[display_columns].head(100),
            use_container_width=True,
            height=400
        )
        
        # Download de CSV
        csv = df_display[display_columns].to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"resultados_deteccao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Seção de alertas
    st.markdown("---")
    st.subheader("🚨 Alertas de Alto Risco")
    
    if 'risk_level' in df.columns:
        high_risk_df = df[df['risk_level'] == 'ALTO']
        
        if len(high_risk_df) > 0:
            st.warning(f"⚠️ **{len(high_risk_df)} produtos de alto risco detectados!**")
            
            alert_cols = ['title', 'price', 'seller', 'ai_prediction', 'risk_score']
            available_cols = [col for col in alert_cols if col in high_risk_df.columns]
            
            if available_cols:
                st.dataframe(
                    high_risk_df[available_cols],
                    use_container_width=True,
                    height=300
                )
        else:
            st.success("✅ Nenhum produto de alto risco detectado!")
    
    # Rodapé
    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #666;'>Dashboard gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>", 
                unsafe_allow_html=True)

if __name__ == "__main__":
    main()

