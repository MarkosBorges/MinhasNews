import streamlit as st
import feedparser
from deep_translator import GoogleTranslator

# 1. Configuração de Página e Identidade Visual
st.set_page_config(page_title="Radar | Minimal News", layout="centered")

# Função para tradução automática em tempo real
def traduzir_manchete(texto):
    if not texto:
        return ""
    try:
        # Detecta o idioma original e traduz de forma limpa para o português
        return GoogleTranslator(source='auto', target='pt').translate(texto)
    except Exception:
        return texto  # Caso falhe por timeout, mantém o original para não quebrar a página

# Busca e processamento cacheado para performance imediata
@st.cache_data(ttl=1800)  # Atualiza o cache a cada 30 minutos
def buscar_e_traduzir_noticias(urls, limite=4):
    noticias = []
    for url in urls:
        feed = feedparser.parse(url)
        # Extrai um nome amigável para a fonte
        nome_fonte = feed.feed.get('title', 'Portal').split(' - ')[0].split(' | ')[0]
        
        for entry in feed.entries[:limite]: 
            titulo_pt = traduzir_manchete(entry.title)
            
            noticias.append({
                'titulo': titulo_pt,
                'link': entry.link,
                'data': entry.get('published', 'Recent'),
                'fonte': nome_fonte
            })
    return noticias

# 2. Injeção de CSS Customizado - Estética Minimalista & Tons de Roxo
st.markdown("""
    <link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap'>
    <style>
        /* Fundo Geral e Tipografia Inter */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0B0813 !important; /* Roxo extremamente escuro, quase preto */
            font-family: 'Inter', -apple-system, sans-serif;
            color: #E2DBEB;
        }
        
        /* Limpeza de elementos padrão do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .block-container {
            padding-top: 4rem;
            max-width: 680px;
        }
        
        /* Cabeçalho */
        .main-title {
            color: #F3EEF6;
            font-weight: 600;
            font-size: 2rem;
            letter-spacing: -0.03em;
            margin-bottom: 5px;
        }
        .subtitle {
            color: #8C7E9C; 
            font-size: 0.95rem;
            margin-bottom: 35px;
        }
        
        /* Estilização dos Blocos de Notícias (Cards Estilo Jornal) */
        .news-card {
            background-color: #141021; /* Bloco roxo escuro contrastante */
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 16px;
            border: 1px solid #221B35;
            transition: all 0.25s ease-in-out;
        }
        
        /* Efeito Hover nos Blocos */
        .news-card:hover {
            transform: translateY(-2px);
            border-color: #6A1B9A; /* Borda se ilumina em roxo médio */
            box-shadow: 0 4px 20px rgba(106, 27, 154, 0.15);
        }
        
        .news-title a {
            color: #F3EEF6;
            text-decoration: none;
            font-size: 1.1rem;
            font-weight: 500;
            line-height: 1.45;
            transition: color 0.2s ease;
        }
        
        .news-title a:hover {
            color: #B388FF; /* Roxo neon suave ao passar o mouse na escrita */
        }
        
        .news-meta {
            font-size: 0.8rem;
            color: #796B8E;
            margin-top: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Tag de Identificação da Fonte */
        .source-tag {
            background-color: #261743;
            color: #D1B3FF;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        
        /* Customização Elegante das Abas (Tabs) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            border-bottom: 1px solid #221B35;
        }
        .stTabs [data-baseweb="tab"] {
            height: 45px;
            background-color: transparent !important;
            color: #796B8E !important;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            font-size: 0.95rem;
            transition: color 0.2s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #B388FF !important;
        }
        .stTabs [aria-selected="true"] {
            color: #D1B3FF !important;
            border-bottom: 2px solid #8E24AA !important;
        }
    </style>
""", unsafe_allow_html=True)

# Interface Estruturada
st.markdown('<div class="main-title">Radar Pessoal</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Agregador Minimalista • InfoSec & Astronomia</div>', unsafe_allow_html=True)

# Fontes Selecionadas
fontes_sec = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://hackaday.com/blog/feed/",
    "https://tecnoblog.net/categoria/seguranca/feed/",
    "https://mundohacker.com.br/feed/"
]

fontes_astro = [
    "https://www.space.com/feeds/all",
    "https://www.universetoday.com/feed/",
    "https://canaltech.com.br/espaco/rss/"
]


# Abas de Navegação
aba1, aba2 = st.tabs(["Segurança & Hacking", "Astronomia"])

with aba1:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner("Coletando e traduzindo inteligência cibernética..."):
        noticias_sec = buscar_e_traduzir_noticias(fontes_sec)
    
    for n in noticias_sec:
        st.markdown(f"""
            <div class="news-card">
                <div class="news-title"><a href="{n['link']}" target="_blank">{n['titulo']}</a></div>
                <div class="news-meta">
                    <span class="source-tag">{n['fonte']}</span>
                    <span>•</span>
                    <span>{n['data']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

with aba2:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner("Mapeando o cosmos..."):
        noticias_astro = buscar_e_traduzir_noticias(fontes_astro)
    
    for n in noticias_astro:
        st.markdown(f"""
            <div class="news-card">
                <div class="news-title"><a href="{n['link']}" target="_blank">{n['titulo']}</a></div>
                <div class="news-meta">
                    <span class="source-tag">{n['fonte']}</span>
                    <span>•</span>
                    <span>{n['data']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
