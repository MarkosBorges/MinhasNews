import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

# 1. Configuração de Página e Layout
st.set_page_config(page_title="Radar Tech Pro", layout="wide", initial_sidebar_state="collapsed")

if 'categoria' not in st.session_state:
    st.session_state.categoria = "SEGURANÇA"

def traduzir_texto(texto):
    if not texto: return ""
    try:
        return GoogleTranslator(source='auto', target='pt').translate(texto)
    except: return texto 

# Função para extrair imagem do feed ou usar um Fallback (imagem padrão) de alta qualidade
def extrair_imagem(entry, categoria):
    # Tenta pegar a imagem anexada na mídia do RSS
    if 'media_content' in entry and len(entry.media_content) > 0:
        return entry.media_content[0]['url']
    if 'enclosures' in entry and len(entry.enclosures) > 0:
        if 'image' in entry.enclosures[0].get('type', ''):
            return entry.enclosures[0]['href']
            
    # Tenta "raspar" a imagem de dentro do texto da notícia
    if 'summary' in entry:
        soup = BeautifulSoup(entry.summary, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            return img['src']
            
    # Imagens padrão profissionais caso o site não forneça uma imagem no feed
    fallbacks = {
        "SEGURANÇA": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&q=80",
        "HARDWARE": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&q=80",
        "ASTRONOMIA": "https://images.unsplash.com/photo-1464802686167-b939a6910659?w=600&q=80"
    }
    return fallbacks.get(categoria)

# Função para limpar tags HTML do resumo e limitar o tamanho
def limpar_resumo(html_text):
    if not html_text: return ""
    soup = BeautifulSoup(html_text, 'html.parser')
    texto_limpo = soup.get_text(separator=' ', strip=True)
    return texto_limpo[:140] + "..." if len(texto_limpo) > 140 else texto_limpo

@st.cache_data(ttl=1800)
def buscar_e_traduzir(urls, categoria, limite=6):
    noticias = []
    for url in urls:
        feed = feedparser.parse(url)
        nome_fonte = feed.feed.get('title', 'Portal').split(' - ')[0].split(' | ')[0]
        
        for entry in feed.entries[:limite]: 
            titulo_pt = traduzir_texto(entry.title)
            
            # Limpa e traduz o resumo
            resumo_original = entry.get('summary', '')
            resumo_limpo = limpar_resumo(resumo_original)
            resumo_pt = traduzir_texto(resumo_limpo) if resumo_limpo else ""
            
            imagem_url = extrair_imagem(entry, categoria)
            
            noticias.append({
                'titulo': titulo_pt, 
                'resumo': resumo_pt,
                'link': entry.link,
                'imagem': imagem_url,
                'data': entry.get('published', 'Recent')[:16], # Pega apenas parte da data
                'fonte': nome_fonte
            })
    return noticias

# 2. CSS AVANÇADO (Design de Portal Pro)
st.markdown("""
    <link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap'>
    <style>
        [data-testid="stAppViewContainer"] { background-color: #0A0710; font-family: 'Inter', sans-serif; }
        #MainMenu, footer, header {visibility: hidden;}

        .main-header {
            position: fixed; top: 0; left: 0; width: 100%; height: 75px;
            background-color: #120E1F; border-bottom: 1px solid #221B35;
            display: flex; align-items: center; justify-content: center;
            z-index: 9999; box-shadow: 0 4px 20px rgba(0,0,0,0.6);
        }

        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 30px;
            padding: 10px;
            margin-top: 100px;
        }

        /* CARDS NÍVEL PROFISSIONAL */
        .card {
            background-color: #151124;
            border: 1px solid #2A2145;
            border-radius: 12px;
            overflow: hidden; /* Mantém a imagem dentro do card arredondado */
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .card:hover {
            transform: translateY(-6px);
            border-color: #8E24AA;
            box-shadow: 0 12px 30px rgba(142, 36, 170, 0.15);
        }
        
        .card-image {
            width: 100%;
            height: 200px;
            object-fit: cover; /* Faz a imagem preencher o espaço sem distorcer */
            border-bottom: 1px solid #2A2145;
        }

        .card-content {
            padding: 24px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }

        .card-title a {
            color: #F8F5FA; text-decoration: none;
            font-size: 1.25rem; font-weight: 700; line-height: 1.4;
            display: block; margin-bottom: 12px;
            transition: color 0.2s;
        }
        .card-title a:hover { color: #D1B3FF; }
        
        .card-excerpt {
            color: #9E91B3; font-size: 0.95rem; line-height: 1.5;
            margin-bottom: 20px; flex-grow: 1;
        }

        .card-meta {
            font-size: 0.8rem; color: #796B8E;
            display: flex; align-items: center; gap: 10px;
            border-top: 1px solid #2A2145;
            padding-top: 16px;
        }
        .tag {
            background-color: #2D1B4E; color: #E2DBEB;
            padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 0.7rem;
            text-transform: uppercase; letter-spacing: 0.5px;
        }

        div.row-widget.stRadio > div {
            flex-direction: row; justify-content: center; gap: 50px;
            position: fixed; top: 20px; width: 100%; z-index: 10000;
        }
        div.row-widget.stRadio label {
            background: none !important; color: #796B8E !important;
            font-weight: 700 !important; font-size: 0.95rem !important;
            text-transform: uppercase; cursor: pointer; border: none !important;
        }
        div.row-widget.stRadio [data-testid="stWidgetLabel"] { display: none; }
        div.row-widget.stRadio [data-testid="stMarkdownContainer"] p { color: #8C7E9C; letter-spacing: 1px; }
        div.row-widget.stRadio input:checked + div p { color: #FFFFFF !important; }
    </style>
    <div class="main-header"></div>
""", unsafe_allow_html=True)

# 3. NAVEGAÇÃO
selecionado = st.radio("Menu", ["SEGURANÇA", "HARDWARE", "ASTRONOMIA"], horizontal=True, label_visibility="collapsed")

fontes = {
    "SEGURANÇA": [
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.bleepingcomputer.com/feed/"
    ],
    "HARDWARE": [
        "https://hackaday.com/blog/feed/",
        "https://www.tomshardware.com/feeds/all"
    ],
    "ASTRONOMIA": [
        "https://www.space.com/feeds/all",
        "https://www.universetoday.com/feed/"
    ]
}

# 4. RENDERIZAÇÃO PROFISSIONAL
st.markdown('<div class="news-grid">', unsafe_allow_html=True)

with st.spinner(f"Carregando inteligência de {selecionado}..."):
    noticias = buscar_e_traduzir(fontes[selecionado], selecionado)
    
    for n in noticias:
        st.markdown(f"""
            <div class="card">
                <img src="{n['imagem']}" class="card-image" alt="Capa da Notícia">
                <div class="card-content">
                    <div class="card-title">
                        <a href="{n['link']}" target="_blank">{n['titulo']}</a>
                    </div>
                    <div class="card-excerpt">
                        {n['resumo']}
                    </div>
                    <div class="card-meta">
                        <span class="tag">{n['fonte']}</span>
                        <span>•</span>
                        <span>{n['data']}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
