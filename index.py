import streamlit as st
import feedparser

# 1. Configuração da página e Injeção de CSS Minimalista
st.set_page_config(page_title="Radar | Minimal News", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        /* Esconde o menu hamburguer e o rodapé padrão do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Ajusta o espaçamento geral para um visual mais limpo */
        .block-container {
            padding-top: 3rem;
            padding-bottom: 2rem;
            max-width: 800px;
        }

        /* Estiliza os links das notícias */
        a {
            text-decoration: none;
            color: #E2E2E2; /* Cor neutra para o título */
            font-weight: 500;
            transition: color 0.2s ease-in-out;
        }
        a:hover {
            color: #4da6ff; /* Azul suave ao passar o mouse */
        }

        /* Estiliza a data e fonte */
        .meta-info {
            font-size: 0.85rem;
            color: #888888;
            margin-bottom: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho Limpo
st.markdown("## Radar Pessoal")
st.markdown(
    "<p style='color: #888; margin-top: -15px; margin-bottom: 30px;'>Agregador automatizado • InfoSec & Astronomia</p>",
    unsafe_allow_html=True)

# 2. Listas de Fontes
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


# 3. Função Otimizada
@st.cache_data(ttl=3600)  # Mantém as notícias salvas por 1 hora para carregar instantaneamente
def buscar_noticias(urls, limite=4):
    noticias = []
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:limite]:
            noticias.append({
                'titulo': entry.title,
                'link': entry.link,
                'data': entry.get('published', 'Data não informada')
            })
    return noticias


# 4. Abas Minimalistas
aba1, aba2 = st.tabs(["Segurança & Hacking", "Astronomia"])

with aba1:
    st.markdown("<br>", unsafe_allow_html=True)  # Espaço extra
    noticias_sec = buscar_noticias(fontes_sec)
    for notic in noticias_sec:
        st.markdown(f"#### <a href='{notic['link']}' target='_blank'>{notic['titulo']}</a>", unsafe_allow_html=True)
        st.markdown(f"<div class='meta-info'>{notic['data']}</div>", unsafe_allow_html=True)

with aba2:
    st.markdown("<br>", unsafe_allow_html=True)
    noticias_astro = buscar_noticias(fontes_astro)
    for notic in noticias_astro:
        st.markdown(f"#### <a href='{notic['link']}' target='_blank'>{notic['titulo']}</a>", unsafe_allow_html=True)
        st.markdown(f"<div class='meta-info'>{notic['data']}</div>", unsafe_allow_html=True)