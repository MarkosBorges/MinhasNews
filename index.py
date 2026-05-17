import streamlit as st
import feedparser
from deep_translator import GoogleTranslator

# 1. Configuração de Página
st.set_page_config(page_title="Mark Newa - Minhas notícias pessoais", layout="centered", initial_sidebar_state="collapsed")

def traduzir_manchete(texto):
    if not texto:
        return ""
    try:
        return GoogleTranslator(source='auto', target='pt').translate(texto)
    except Exception:
        return texto 

@st.cache_data(ttl=1800)
def buscar_e_traduzir_noticias(urls, limite=5):
    noticias = []
    for url in urls:
        feed = feedparser.parse(url)
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

# 2. Injeção de CSS (Header Estilo Tecnoblog + Tons de Roxo) e FontAwesome para Ícones
st.markdown("""
    <link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        /* Fundo Geral e Tipografia Inter */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0B0813 !important; 
            font-family: 'Inter', sans-serif;
            color: #E2DBEB;
        }
        
        /* Limpeza do Streamlit */
        #MainMenu, footer, header {visibility: hidden;}
        
        /* HEADER CUSTOMIZADO (ESTILO PORTAL) */
        .top-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background-color: #1A142A; /* Roxo ligeiramente mais claro que o fundo */
            border-bottom: 1px solid #2A2145;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 4%;
            z-index: 999999;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        /* Logo esquerda */
        .header-logo {
            font-weight: 700;
            font-size: 1.4rem;
            color: #FFFFFF;
            text-decoration: none;
            font-style: italic;
            letter-spacing: -0.5px;
        }
        .header-logo span { color: #B388FF; }
        
        /* Menus centrais (meramente visuais para estética) */
        .header-nav {
            display: flex;
            gap: 25px;
        }
        .header-nav a {
            color: #A99BBF;
            text-decoration: none;
            font-size: 0.75rem;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: color 0.2s;
        }
        .header-nav a:hover { color: #FFFFFF; }
        
        /* Ícones direita */
        .header-icons {
            display: flex;
            gap: 20px;
            color: #A99BBF;
            font-size: 1.1rem;
        }
        .header-icons i { cursor: pointer; transition: color 0.2s; }
        .header-icons i:hover { color: #B388FF; }

        /* Ajuste do container para não ficar atrás do header fixo */
        .block-container {
            padding-top: 6rem;
            max-width: 700px;
        }
        
        /* Estilização dos Blocos de Notícias */
        .news-card {
            background-color: #141021; 
            padding: 22px;
            border-radius: 8px;
            margin-bottom: 16px;
            border: 1px solid #221B35;
            transition: all 0.2s ease-in-out;
            border-left: 4px solid #221B35; /* Detalhe lateral de portal de notícias */
        }
        .news-card:hover {
            transform: translateX(4px); /* Animação sutil para a direita */
            border-left-color: #B388FF;
            box-shadow: 0 4px 15px rgba(179, 136, 255, 0.08);
        }
        .news-title a {
            color: #F3EEF6;
            text-decoration: none;
            font-size: 1.15rem;
            font-weight: 600;
            line-height: 1.4;
        }
        .news-title a:hover { color: #D1B3FF; }
        
        .news-meta {
            font-size: 0.75rem;
            color: #796B8E;
            margin-top: 12px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .source-tag {
            background-color: #261743;
            color: #D1B3FF;
            padding: 4px 10px;
            border-radius: 4px;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        /* Customização Elegante das Abas (Tabs) */
        .stTabs [data-baseweb="tab-list"] { gap: 10px; border-bottom: 1px solid #2A2145; }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            color: #796B8E !important;
            font-weight: 600;
            font-size: 0.9rem;
        }
        .stTabs [aria-selected="true"] {
            color: #D1B3FF !important;
            border-bottom: 2px solid #B388FF !important;
        }
    </style>
    
    <div class="top-header">
        <a href="#" class="header-logo">radar<span>.tech</span></a>
        <div class="header-nav">
            <a href="#">Segurança</a>
            <a href="#">Hardware</a>
            <a href="#">Astronomia</a>
        </div>
        <div class="header-icons">
            <i class="fas fa-search"></i>
            <i class="fab fa-github"></i>
            <i class="fas fa-sun"></i>
        </div>
    </div>
""", unsafe_allow_html=True)


# 3. Listas de Fontes Separadas
fontes_sec = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://tecnoblog.net/categoria/seguranca/feed/",
    "https://mundohacker.com.br/feed/"
]

fontes_hard_iot = [
    "https://hackaday.com/blog/feed/",
    "https://www.tomshardware.com/feeds/all", # Gigante global de análises de hardware
    "https://www.raspberrypi.com/news/feed/", # Novidades do mundo Raspberry e microcontroladores
    "https://www.hackster.io/projects.rss"    # Focado 100% em projetos práticos de IoT e embarcados
]

fontes_astro = [
    "https://www.space.com/feeds/all",
    "https://www.universetoday.com/feed/",
    "https://canaltech.com.br/espaco/rss/"
]

# 4. As 3 Abas
aba1, aba2, aba3 = st.tabs(["🔒 Segurança & Hacking", "⚙️ Hardware & IoTs", "🔭 Astronomia"])

def renderizar_noticias(noticias):
    for n in noticias:
        st.markdown(f"""
            <div class="news-card">
                <div class="news-title"><a href="{n['link']}" target="_blank">{n['titulo']}</a></div>
                <div class="news-meta">
                    <span class="source-tag">{n['fonte']}</span>
                    <span>•</span>
                    <span><i class="far fa-clock"></i> {n['data']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

with aba1:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner("Buscando relatórios de segurança..."):
        renderizar_noticias(buscar_e_traduzir_noticias(fontes_sec))

with aba2:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner("Verificando novidades de hardware..."):
        renderizar_noticias(buscar_e_traduzir_noticias(fontes_hard_iot))

with aba3:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner("Sintonizando frequências espaciais..."):
        renderizar_noticias(buscar_e_traduzir_noticias(fontes_astro))
