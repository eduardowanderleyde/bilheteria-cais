"""
Sistema de Bilheteria - Museu (Versão Web)
Deploy gratuito no Streamlit Cloud
"""

import streamlit as st
import sqlite3
from datetime import datetime, date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Sistema de Bilheteria - Museu",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

class BilheteriaWeb:
    def __init__(self):
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados"""
        conn = sqlite3.connect("bilheteria_web.db")
        cursor = conn.cursor()
        
        # Tabela de vendas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tipo_ingresso TEXT NOT NULL,
                preco REAL NOT NULL,
                nome_cliente TEXT,
                estado TEXT,
                cidade TEXT
            )
        ''')
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        ''')
        
        # Usuário padrão
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO usuarios (username, senha) VALUES (?, ?)', 
                          ('admin', '123456'))
        
        conn.commit()
        conn.close()
    
    def autenticar_usuario(self, username, senha):
        """Autentica usuário"""
        conn = sqlite3.connect("bilheteria_web.db")
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE username = ? AND senha = ?', 
                      (username, senha))
        resultado = cursor.fetchone()
        
        conn.close()
        return resultado is not None
    
    def registrar_venda(self, tipo_ingresso, preco, nome_cliente=None, estado=None, cidade=None):
        """Registra uma nova venda"""
        conn = sqlite3.connect("bilheteria_web.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO vendas (tipo_ingresso, preco, nome_cliente, estado, cidade)
            VALUES (?, ?, ?, ?, ?)
        ''', (tipo_ingresso, preco, nome_cliente, estado, cidade))
        
        conn.commit()
        venda_id = cursor.lastrowid
        conn.close()
        return venda_id
    
    def obter_vendas(self):
        """Obtém todas as vendas"""
        conn = sqlite3.connect("bilheteria_web.db")
        df = pd.read_sql_query("SELECT * FROM vendas ORDER BY data_venda DESC", conn)
        conn.close()
        return df
    
    def obter_relatorio(self, data_inicio=None, data_fim=None):
        """Obtém relatório de vendas"""
        conn = sqlite3.connect("bilheteria_web.db")
        
        if data_inicio and data_fim:
            query = '''
                SELECT 
                    DATE(data_venda) as data,
                    tipo_ingresso,
                    COUNT(*) as quantidade,
                    SUM(preco) as total
                FROM vendas 
                WHERE DATE(data_venda) BETWEEN ? AND ?
                GROUP BY DATE(data_venda), tipo_ingresso
                ORDER BY data DESC, tipo_ingresso
            '''
            df = pd.read_sql_query(query, conn, params=[data_inicio, data_fim])
        else:
            query = '''
                SELECT 
                    DATE(data_venda) as data,
                    tipo_ingresso,
                    COUNT(*) as quantidade,
                    SUM(preco) as total
                FROM vendas 
                GROUP BY DATE(data_venda), tipo_ingresso
                ORDER BY data DESC, tipo_ingresso
            '''
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        return df
    
    def obter_estatisticas(self):
        """Obtém estatísticas gerais"""
        conn = sqlite3.connect("bilheteria_web.db")
        
        # Total de vendas
        total_vendas = pd.read_sql_query("SELECT COUNT(*) as total FROM vendas", conn).iloc[0]['total']
        
        # Total arrecadado
        total_arrecadado = pd.read_sql_query("SELECT SUM(preco) as total FROM vendas", conn).iloc[0]['total'] or 0
        
        # Vendas por tipo
        vendas_tipo = pd.read_sql_query('''
            SELECT tipo_ingresso, COUNT(*) as quantidade, SUM(preco) as total
            FROM vendas 
            GROUP BY tipo_ingresso
        ''', conn)
        
        conn.close()
        return total_vendas, total_arrecadado, vendas_tipo

# Inicializar aplicação
@st.cache_resource
def get_app():
    return BilheteriaWeb()

app = get_app()

# Sistema de autenticação
def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login()
    else:
        show_main_app()

def show_login():
    """Mostra tela de login"""
    st.markdown("""
    <div style='text-align: center; padding: 50px 0;'>
        <h1>🎫 Sistema de Bilheteria</h1>
        <h2>Museu</h2>
        <p>Faça login para acessar o sistema</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.subheader("🔐 Login")
            username = st.text_input("Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                if app.autenticar_usuario(username, senha):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos!")
        
        st.info("👤 **Usuário padrão:** admin\n\n🔑 **Senha padrão:** 123456")

def show_main_app():
    """Mostra aplicação principal"""
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🎫 Sistema de Bilheteria - Museu")
    with col2:
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    # Menu principal
    tab1, tab2, tab3 = st.tabs(["💰 Vendas", "📊 Relatórios", "🗄️ Dados"])
    
    with tab1:
        show_vendas_tab()
    
    with tab2:
        show_relatorios_tab()
    
    with tab3:
        show_dados_tab()

def show_vendas_tab():
    """Aba de vendas"""
    st.header("💰 Registrar Nova Venda")
    
    with st.form("venda_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_ingresso = st.selectbox(
                "Tipo de Ingresso",
                ["Inteira (R$ 10,00)", "Meia (R$ 5,00)", "Gratuito"],
                help="Selecione o tipo de ingresso"
            )
        
        with col2:
            # Determinar preço
            if "Inteira" in tipo_ingresso:
                preco = 10.0
            elif "Meia" in tipo_ingresso:
                preco = 5.0
            else:
                preco = 0.0
            
            st.metric("Preço", f"R$ {preco:.2f}")
        
        st.subheader("📝 Dados do Cliente (Opcional)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            nome_cliente = st.text_input("Nome", placeholder="Nome do cliente")
        with col2:
            estado = st.text_input("Estado", placeholder="Estado")
        with col3:
            cidade = st.text_input("Cidade", placeholder="Cidade")
        
        submitted = st.form_submit_button("💾 Registrar Venda", use_container_width=True)
        
        if submitted:
            if not tipo_ingresso:
                st.error("Selecione um tipo de ingresso!")
            else:
                try:
                    tipo_clean = tipo_ingresso.split(" (")[0]  # Remove preço da string
                    venda_id = app.registrar_venda(
                        tipo_clean, preco, 
                        nome_cliente if nome_cliente else None,
                        estado if estado else None,
                        cidade if cidade else None
                    )
                    st.success(f"✅ Venda registrada com sucesso! ID: {venda_id}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao registrar venda: {str(e)}")
    
    # Informações sobre preços
    st.info("""
    💡 **Informações sobre preços:**
    - **Inteira:** R$ 10,00
    - **Meia:** R$ 5,00  
    - **Gratuito:** Terças-feiras e idosos
    - Todos os campos do cliente são opcionais
    """)

def show_relatorios_tab():
    """Aba de relatórios"""
    st.header("📊 Relatórios de Vendas")
    
    # Filtros
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        data_inicio = st.date_input("Data Início", value=None)
    with col2:
        data_fim = st.date_input("Data Fim", value=None)
    with col3:
        gerar_relatorio = st.button("📈 Gerar Relatório", use_container_width=True)
    
    # Estatísticas gerais
    total_vendas, total_arrecadado, vendas_tipo = app.obter_estatisticas()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Vendas", total_vendas)
    with col2:
        st.metric("Total Arrecadado", f"R$ {total_arrecadado:.2f}")
    with col3:
        st.metric("Média por Venda", f"R$ {total_arrecadado/total_vendas:.2f}" if total_vendas > 0 else "R$ 0,00")
    
    # Gráfico de vendas por tipo
    if not vendas_tipo.empty:
        fig_tipo = px.pie(vendas_tipo, values='quantidade', names='tipo_ingresso', 
                         title="Distribuição por Tipo de Ingresso")
        st.plotly_chart(fig_tipo, use_container_width=True)
    
    # Relatório detalhado
    if gerar_relatorio or st.session_state.get('auto_load', True):
        st.subheader("📋 Relatório Detalhado")
        
        relatorio = app.obter_relatorio(
            data_inicio.strftime('%Y-%m-%d') if data_inicio else None,
            data_fim.strftime('%Y-%m-%d') if data_fim else None
        )
        
        if not relatorio.empty:
            st.dataframe(relatorio, use_container_width=True)
            
            # Gráfico de vendas por data
            fig_data = px.bar(relatorio, x='data', y='total', color='tipo_ingresso',
                             title="Vendas por Data e Tipo")
            st.plotly_chart(fig_data, use_container_width=True)
        else:
            st.warning("Nenhuma venda encontrada no período selecionado.")

def show_dados_tab():
    """Aba de dados"""
    st.header("🗄️ Dados Salvos")
    
    # Filtros
    col1, col2 = st.columns([3, 1])
    with col1:
        filtro_data = st.date_input("Filtrar por data", value=None)
    with col2:
        atualizar = st.button("🔄 Atualizar", use_container_width=True)
    
    # Obter dados
    vendas_df = app.obter_vendas()
    
    if filtro_data:
        vendas_df['data_venda_date'] = pd.to_datetime(vendas_df['data_venda']).dt.date
        vendas_df = vendas_df[vendas_df['data_venda_date'] == filtro_data]
    
    if not vendas_df.empty:
        st.subheader(f"📋 Registros ({len(vendas_df)} vendas)")
        
        # Formatação da data
        vendas_display = vendas_df.copy()
        vendas_display['data_venda'] = pd.to_datetime(vendas_display['data_venda']).dt.strftime('%d/%m/%Y %H:%M')
        vendas_display['preco'] = vendas_display['preco'].apply(lambda x: f"R$ {x:.2f}")
        
        # Renomear colunas
        vendas_display.columns = ['ID', 'Data/Hora', 'Tipo', 'Preço', 'Cliente', 'Estado', 'Cidade']
        
        st.dataframe(vendas_display, use_container_width=True, hide_index=True)
        
        # Download dos dados
        csv = vendas_display.to_csv(index=False)
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name=f"vendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("Nenhuma venda encontrada.")
    
    # Estatísticas
    total_vendas, total_arrecadado, vendas_tipo = app.obter_estatisticas()
    
    st.subheader("📊 Estatísticas Gerais")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Vendas", total_vendas)
        st.metric("Total Arrecadado", f"R$ {total_arrecadado:.2f}")
    
    with col2:
        if not vendas_tipo.empty:
            st.subheader("Vendas por Tipo")
            for _, row in vendas_tipo.iterrows():
                st.write(f"**{row['tipo_ingresso']}:** {row['quantidade']} vendas - R$ {row['total']:.2f}")

if __name__ == "__main__":
    main()
