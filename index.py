import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

# 1. Configuração de Página e Layout
st.set_page_config(page_title="Markos News - Site Pessoal", layout="wide", initial_sidebar_state="collapsed")

def traduzir_texto(texto):
    if not texto: return ""
    try:
        return GoogleTranslator(source='auto', target='pt').translate(texto)
    except: return texto 

def extrair_imagem(entry, categoria):
    if 'media_content' in entry and len(entry.media_content) > 0:
        return entry.media_content[0]['url']
    if 'enclosures' in entry and len(entry.enclosures) > 0:
        if 'image' in entry.enclosures[0].get('type', ''):
            return entry.enclosures[0]['href']
            
    if 'summary' in entry:
        soup = BeautifulSoup(entry.summary, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            return img['src']
            
    fallbacks = {
        "SEGURANÇA": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&q=80",
        "HARDWARE": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&q=80",
        "ASTRONOMIA": "https://images.unsplash.com/photo-1464802686167-b939a6910659?w=600&q=80"
    }
    return fallbacks.get(categoria)

# ATUALIZAÇÃO TRAVADA EM 1 HORA (3600 segundos)
@st.cache_data(ttl=3600)
def buscar_e_traduzir(urls, categoria, limite=12): # Limite ajustado para preencher bem a tela
    noticias = []
    for url in urls:
        feed = feedparser.parse(url)
        nome_fonte = feed.feed.get('title', 'Portal').split(' - ')[0].split(' | ')[0]
        
        for entry in feed.entries[:limite]: 
            titulo_pt = traduzir_texto(entry.title)
            imagem_url = extrair_imagem(entry, categoria)
            
            noticias.append({
                'titulo': titulo_pt, 
                'link': entry.link,
                'imagem': imagem_url,
                'fonte': nome_fonte
            })
    return noticias

# 2. CSS AVANÇADO: Transformando as Abas Nativas no Header Fixo
st.markdown("""
    <link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'>
    <style>
        [data-testid="stAppViewContainer"] { background-color: #0F0A18; font-family: 'Inter', sans-serif; }
        #MainMenu, footer, header {visibility: hidden;}

        /* Empurra o conteúdo para baixo para não ficar escondido pelo novo header */
        .block-container {
            padding-top: 90px !important; 
            max-width: 1400px;
        }

        /* TRUQUE: Transforma a lista de abas nativa do Streamlit em uma barra fixa no topo */
        div[data-testid="stTabs"] {
            width: 100%;
        }
        div[data-baseweb="tab-list"] {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background-color: #161124; /* Fundo do Header */
            border-bottom: 1px solid #251B3D;
            display: flex;
            justify-content: center; /* Centraliza os botões como na sua imagem */
            gap: 50px;
            z-index: 999999;
            padding: 0;
            margin: 0;
        }
        
        /* Estilo dos textos do Header (Inativo) */
        div[data-baseweb="tab"] {
            background: transparent !important;
            border: none !important;
            color: #A99BBF !important;
            font-weight: 600 !important;
            font-size: 1.85rem !important;
            letter-spacing: 1px;
            text-transform: uppercase;
            height: 100%;
            padding: 0 20px;
            transition: color 0.2s;
        }
        div[data-baseweb="tab"]:hover {
            color: #E2DBEB !important;
        }
        
        /* Estilo da aba Selecionada/Ativa */
        div[aria-selected="true"] {
            color: #FFFFFF !important;
            border-bottom: 2px solid #B388FF !important; /* Linha roxa indicando onde o usuário está */
        }
        
        /* Oculta as decorações originais que o Streamlit coloca nas abas */
        div[data-baseweb="tab-highlight"] { display: none; }
        div[data-baseweb="tab-borders"] { display: none; }

        /* GRADE ESTILO JORNAL (Acumulando blocos) */
        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 24px;
            padding: 10px 0;
        }

        /* CARDS COMPACTOS */
        .card {
            background-color: transparent;
            transition: transform 0.2s ease;
            display: flex;
            flex-direction: column;
            cursor: pointer;
        }
        .card:hover {
            transform: translateY(-3px);
        }
        .card:hover .card-title a {
            color: #B388FF;
        }
        
        .card-image {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 6px;
            margin-bottom: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }

        .card-title a {
            color: #F8F5FA; 
            text-decoration: none;
            font-size: 1.05rem;
            font-weight: 700; 
            line-height: 1.3;
            display: block; 
            margin-bottom: 8px;
            transition: color 0.2s;
        }
        
        .card-meta {
            font-size: 0.75rem; color: #8C7E9C;
            display: flex; align-items: center; gap: 8px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Configuração de Fontes
fontes = {
    "SEGURANÇA": [
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.bleepingcomputer.com/feed/",
        "https://krebsonsecurity.com/feed/",
        "https://tecnoblog.net/categoria/seguranca/feed/",
        "https://mundohacker.com.br/feed/",
        "https://www.helpnetsecurity.com/feed/",          # Novo: Help Net Security
        "https://www.cisoadvisor.com.br/feed/",           # Novo: CISO Advisor (BR)
        "https://cybernews.com/feed/",                    # Novo: CyberNews
        "https://www.exploit-db.com/rss.xml"              # Novo: Exploit Database
    ],
    "HARDWARE": [
        "https://hackaday.com/blog/feed/",
        "https://www.tomshardware.com/feeds/all", # Gigante global de análises de hardware
        "https://www.raspberrypi.com/news/feed/", # Novidades do mundo Raspberry e microcontroladores
        "https://www.hackster.io/projects.rss"    # Focado 100% em projetos práticos de IoT e embarcados
    ],
    "ASTRONOMIA": [
        "https://www.space.com/feeds/all",
        "https://www.universetoday.com/feed/",
        "https://canaltech.com.br/espaco/rss/"
    ]
}

# 4. Função para renderizar o grid de notícias limpo
# 4. Função para renderizar o grid de notícias limpo (Corrigida)
def renderizar_grade(noticias):
    html = '<div class="news-grid">'
    for n in noticias:
        # Escrevendo o HTML em linha reta para evitar que o Markdown crie blocos de código
        html += f"<div class='card' onclick=\"window.open('{n['link']}', '_blank')\">"
        html += f"<img src='{n['imagem']}' class='card-image' alt='Capa'>"
        html += f"<div class='card-title'><a href='{n['link']}' target='_blank'>{n['titulo']}</a></div>"
        html += f"<div class='card-meta'><span>{n['fonte']}</span></div>"
        html += "</div>"
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)
# 5. ABAS NATIVAS COMO HEADER
aba1, aba2, aba3 = st.tabs(["SEGURANÇA", "HARDWARE", "ASTRONOMIA"])

with aba1:
    with st.spinner("Carregando relatórios de Segurança..."):
        noticias_sec = buscar_e_traduzir(fontes["SEGURANÇA"], "SEGURANÇA")
        renderizar_grade(noticias_sec)

with aba2:
    with st.spinner("Atualizando novidades de Hardware..."):
        noticias_hard = buscar_e_traduzir(fontes["HARDWARE"], "HARDWARE")
        renderizar_grade(noticias_hard)

with aba3:
    with st.spinner("Mapeando o Cosmos..."):
        noticias_astro = buscar_e_traduzir(fontes["ASTRONOMIA"], "ASTRONOMIA")
        renderizar_grade(noticias_astro)
