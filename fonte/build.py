#!/usr/bin/env python3
"""Gera o site estático da Clínica Zelo na raiz do repositório
Uso: python3 fonte/build.py
Todos os dados da clínica ficam no bloco DADOS, logo abaixo. Ao preencher um
campo, troque o valor None pelo texto e rode o script de novo."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

OUT = Path(__file__).parent.parent   # raiz do repositório: é o que a Vercel publica

# ───────────────────────────── DADOS ─────────────────────────────
DOMINIO = "https://clinica-zelo.vercel.app"   # trocar quando houver domínio próprio
NOME = "Clínica Zelo"
NOME_COMPLETO = "Clínica Zelo | Fisioterapia e Pilates"
FONE_EXIBE = "(85) 99944-6666"
FONE_TEL = "+5585999446666"
WHATS = "5585999446666"                  # PREENCHER: confirmar se este número é o WhatsApp
RUA = "Av. Godofredo Maciel, 2540, 2º andar"
BAIRRO = "Maraponga, Fortaleza - CE"
CEP = "60710-684"
REFERENCIA = "2º andar do prédio do supermercado Frangolândia"
NOTA, N_AVAL = "5,0", 30
MAPS_Q = "Clínica Zelo Fisioterapia e Pilates, Av. Godofredo Maciel, 2540 - Maraponga, Fortaleza - CE, 60710-684"
MAPS_ROTA = "https://www.google.com/maps/dir/?api=1&destination=" + quote(MAPS_Q)
MAPS_VER = "https://www.google.com/maps/search/?api=1&query=" + quote(MAPS_Q)
MAPS_EMBED = "https://www.google.com/maps?q=" + quote(MAPS_Q) + "&z=16&output=embed"
# ─────────────────────────────────────────────────────────────────


# O site publicado não mostra pendências. Para ver todas as etiquetas [PREENCHER]
# e os espaços reservados para fotos: python3 fonte/build.py --rascunho
RASCUNHO = "--rascunho" in sys.argv


def fill(txt):
    return f'<span class="fill">[PREENCHER: {txt}]</span>' if RASCUNHO else ""


def so(html):
    """Trecho que só existe no rascunho (depende de informação ainda não fornecida)."""
    return html if RASCUNHO else ""


def wa(msg):
    return f"https://wa.me/{WHATS}?text={quote(msg)}"


WA_ICON = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2a9.9 9.9 0 0 0-8.46 15.03L2 22l5.1-1.54A9.9 9.9 0 1 0 12.04 2Zm0 1.8a8.1 8.1 0 1 1-4.3 14.96l-.3-.19-3.03.92.94-2.94-.2-.31A8.1 8.1 0 0 1 12.04 3.8Zm-3.4 3.9c-.2 0-.5.07-.76.36-.26.28-1 .98-1 2.38 0 1.4 1.02 2.76 1.17 2.95.14.19 2 3.06 4.86 4.29 2.38 1.02 2.87.82 3.39.77.51-.05 1.66-.68 1.9-1.33.23-.66.23-1.22.16-1.34-.07-.12-.26-.19-.54-.33-.29-.14-1.67-.82-1.93-.92-.26-.09-.45-.14-.64.14-.19.29-.73.92-.9 1.11-.16.19-.33.21-.61.07-.29-.14-1.2-.44-2.29-1.41a8.6 8.6 0 0 1-1.58-1.97c-.17-.28-.02-.44.12-.58.13-.12.29-.33.43-.49.14-.17.19-.29.28-.48.1-.19.05-.35-.02-.5-.07-.13-.63-1.55-.88-2.12-.22-.52-.45-.53-.64-.54l-.52-.06Z"/></svg>')


def pic(name, alt, shape, eager=False, sizes=None):
    """shape: 'l' = 3:2 (1080x720) | 'p' = 4:5 (720x900)"""
    w, h = (1080, 720) if shape == "l" else (720, 900)
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source srcset="assets/img/{name}.webp" type="image/webp">'
            f'<img src="assets/img/{name}.jpg" alt="{alt}" width="{w}" height="{h}" {load} decoding="async"></picture>')


def figure(name, alt, shape, caption=None, eager=False, cls=""):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="figure ratio-{shape} {cls}">{pic(name, alt, shape, eager)}{cap}</figure>'


def ph(shape, desc):
    return f'<div class="ph ph--{shape}" role="img" aria-label="Espaço reservado para foto"><b>Foto a providenciar</b><span>{desc}</span></div>'


NAV = [("index.html", "Início"), ("fisioterapia.html", "Fisioterapia"), ("pilates.html", "Pilates"),
       ("terapias-manuais.html", "Terapias manuais"), ("a-clinica.html", "A clínica"), ("contato.html", "Contato")]


def nav_items(current, skip_home=False):
    out = []
    for href, label in NAV:
        if skip_home and href == "index.html":
            continue
        cur = ' aria-current="page"' if href == current else ""
        out.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return "".join(out)


def json_ld():
    data = {
        "@context": "https://schema.org",
        "@type": "Physiotherapy",
        "name": NOME_COMPLETO,
        "image": f"{DOMINIO}/assets/img/pilates-orientado.jpg",
        "url": DOMINIO + "/",
        "telephone": FONE_TEL,
        "address": {"@type": "PostalAddress", "streetAddress": RUA, "addressLocality": "Fortaleza",
                    "addressRegion": "CE", "postalCode": CEP, "addressCountry": "BR"},
        "areaServed": "Maraponga, Fortaleza",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": N_AVAL},
        "hasMap": MAPS_VER,
        # PREENCHER: "openingHoursSpecification" (horários) e "geo" (latitude/longitude) quando confirmados.
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def layout(page, title, desc, body, wa_msg, og="pilates-orientado"):
    w = wa(wa_msg)
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#f6f1e9">
<link rel="canonical" href="{DOMINIO}/{'' if page == 'index.html' else page}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{NOME_COMPLETO}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMINIO}/{'' if page == 'index.html' else page}">
<meta property="og:image" content="{DOMINIO}/assets/img/{og}.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/fraunces-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/figtree-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.add("js")</script>
<script type="application/ld+json">
{json_ld()}
</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header" data-header>
  <div class="wrap header-in">
    <a class="brand" href="index.html" aria-label="Zelo Fisioterapia e Pilates, página inicial">
      <span class="brand-mark">Zelo</span><span class="brand-sub">Fisioterapia e Pilates</span>
    </a>
    <nav class="nav" aria-label="Principal"><ul>{nav_items(page, skip_home=True)}</ul></nav>
    <a class="btn btn--accent btn--sm header-cta" href="{w}" target="_blank" rel="noopener">Agendar avaliação</a>
    <button class="menu-btn" type="button" data-menu-btn aria-expanded="false" aria-controls="menu"><span data-menu-label>Menu</span><i aria-hidden="true"></i></button>
  </div>
</header>

<div class="menu" id="menu">
  <nav aria-label="Menu"><ul class="menu-links">{nav_items(page)}</ul></nav>
  <div class="menu-foot">
    <a class="btn btn--accent" href="{w}" target="_blank" rel="noopener">{WA_ICON}Agendar pelo WhatsApp</a>
    <p>{RUA}<br>{BAIRRO}<br><a href="tel:{FONE_TEL}">{FONE_EXIBE}</a></p>
  </div>
</div>

<main id="conteudo">
{body}
</main>

<footer class="site-footer">
  <div class="wrap grid">
    <div class="footer-brand">
      <span class="brand-mark">Zelo</span>
      <p>Fisioterapia e Pilates na Maraponga, em Fortaleza.</p>
    </div>
    <div class="footer-col">
      <h2>Onde estamos</h2>
      <address>{RUA}<br>{BAIRRO}<br>CEP {CEP}<br>{REFERENCIA[0].upper() + REFERENCIA[1:]}</address>
      <p style="margin-top:.75rem"><a href="{MAPS_ROTA}" target="_blank" rel="noopener">Abrir rota no mapa</a></p>
    </div>
    <div class="footer-col">
      <h2>Contato</h2>
      <ul>
        <li><a href="tel:{FONE_TEL}">{FONE_EXIBE}</a></li>
        <li><a href="{w}" target="_blank" rel="noopener">WhatsApp</a></li>
        {so('<li><span>' + fill('Instagram da clínica') + '</span></li><li><span>' + fill('horários; fecha às 21h') + '</span></li>')}
      </ul>
    </div>
    <div class="footer-col">
      <h2>Páginas</h2>
      <ul>{nav_items(page)}</ul>
    </div>
  </div>
  <div class="wrap"><div class="footer-legal">
    <p>{NOME_COMPLETO}{so(' · CNPJ ' + fill('CNPJ') + '<br>Responsável técnica: ' + fill('nome e CREFITO'))}</p>
    <p>© 2026 {NOME}. Todos os direitos reservados.</p>
  </div></div>
</footer>

<div class="dock" data-dock>
  <a class="btn btn--accent" href="{w}" target="_blank" rel="noopener">{WA_ICON}WhatsApp</a>
  <a class="btn btn--ghost" href="tel:{FONE_TEL}">Ligar</a>
</div>

<script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    head, rest = html.split("</head>", 1)
    # evita quebras ruins em endereço e CEP, mexendo apenas no texto visível (nunca em atributos)
    def tidy(m):
        t = m.group(0)
        return t.replace("2º andar", "2º&nbsp;andar").replace("Fortaleza - CE", "Fortaleza&nbsp;-&nbsp;CE").replace(CEP, f'<span class="nw">{CEP}</span>')
    rest = re.sub(r">[^<]+<", tidy, rest)
    return head + "</head>" + rest


# ───────────────────────── blocos reutilizados ─────────────────────────
def cta(titulo, texto, msg, botao="Agendar pelo WhatsApp"):
    return f"""
<section class="cta on-green" aria-labelledby="cta-t">
  <div class="wrap grid">
    <div class="cta-main reveal">
      <h2 id="cta-t">{titulo}</h2>
      <p>{texto}</p>
      <div class="cta-actions">
        <a class="btn btn--accent" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}{botao}</a>
        <a class="btn btn--ghost" href="tel:{FONE_TEL}">Ligar para {FONE_EXIBE}</a>
      </div>
    </div>
    <div class="cta-side reveal">
      <strong>{RUA}</strong>
      {BAIRRO}. Fica no {REFERENCIA}.
    </div>
  </div>
</section>"""


def crumbs(label):
    return f'<nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a><span aria-hidden="true">/</span><span aria-current="page">{label}</span></nav>'


def mod(n, id_, titulo, resumo, oque, quem, sessao, msg):
    return f"""
    <article class="mod grid" id="{id_}">
      <header class="mod-head reveal">
        <span class="mod-n">{n:02d}</span>
        <h2>{titulo}</h2>
        <p>{resumo}</p>
        <a class="link" href="{wa(msg)}" target="_blank" rel="noopener">Agendar avaliação</a>
      </header>
      <div class="mod-body reveal">
        <dl class="mod-dl">
          <div><dt>O que é</dt><dd>{oque}</dd></div>
          <div><dt>Para quem</dt><dd>{quem}</dd></div>
          <div><dt>Como é a sessão</dt><dd>{sessao}</dd></div>
        </dl>
      </div>
    </article>"""


def toc(items):
    lis = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items)
    return f'<nav class="toc" aria-label="Nesta página"><div class="wrap"><ul>{lis}</ul></div></nav>'


def luanna():
    return f"""
    <div class="person grid">
      <div class="person-media reveal">
        {figure("luanna-carvalho", "Luanna Carvalho, fisioterapeuta, sentada à mesa do consultório ao lado de um modelo anatômico de joelho", "p")}
      </div>
      <div class="person-body reveal">
        <h3>Luanna Carvalho</h3>
        <p class="person-role">Fisioterapeuta e proprietária da Clínica Zelo</p>
        <p style="margin-top:1.25rem">Especialista no tratamento da dor. {fill('duas ou três frases da Luanna, na voz dela: por que escolheu a fisioterapia e como gosta de atender')}</p>
        <dl class="person-meta">
          {so('<div><dt>Registro</dt><dd>' + fill('CREFITO') + '</dd></div><div><dt>Formação</dt><dd>' + fill('graduação, especializações e cursos') + '</dd></div>')}
          <div><dt>Instagram</dt><dd><a href="https://www.instagram.com/luannacarvalhor/" target="_blank" rel="noopener">@luannacarvalhor</a></dd></div>
        </dl>
      </div>
    </div>
    {so('<p class="team-more reveal">' + fill('demais profissionais da equipe: nome, CREFITO, especialidade, foto e uma frase de cada') + '</p>')}"""


def onde(alt=False):
    return f"""
<section class="section {'section--alt' if alt else 'section--line'}" id="como-chegar" aria-labelledby="onde-t">
  <div class="wrap grid">
    <div class="where-map reveal">
      <div class="map"><a class="map-alt" href="{MAPS_VER}" target="_blank" rel="noopener">Ver a localização no Google Maps</a>
        <iframe src="{MAPS_EMBED}" title="Mapa com a localização da Clínica Zelo na Av. Godofredo Maciel, Maraponga" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
    </div>
    <div class="where-body reveal">
      <span class="eyebrow">Como chegar</span>
      <h2 id="onde-t">Na Godofredo Maciel, em cima do Frangolândia.</h2>
      <p class="where-ref">Entre no prédio do supermercado Frangolândia e suba ao 2º andar.</p>
      <dl class="info">
        <div><dt>Endereço</dt><dd><address>{RUA}<br>{BAIRRO}, {CEP}</address></dd></div>
        {so('<div><dt>Horário</dt><dd>' + fill('dias e horários completos; fecha às 21h') + '</dd></div>')}
        <div><dt>Telefone</dt><dd><a href="tel:{FONE_TEL}">{FONE_EXIBE}</a></dd></div>
        {so('<div><dt>Acesso</dt><dd>' + fill('estacionamento, elevador e acessibilidade') + '</dd></div>')}
      </dl>
      <div class="where-actions">
        <a class="btn btn--ghost" href="{MAPS_ROTA}" target="_blank" rel="noopener">Abrir rota</a>
        <a class="btn btn--ghost" href="tel:{FONE_TEL}">Ligar</a>
      </div>
    </div>
  </div>
</section>"""


# ───────────────────────────── INÍCIO ─────────────────────────────
def page_index():
    msg = "Olá! Vi o site da Clínica Zelo e gostaria de agendar uma avaliação."
    reasons = [
        ("Coluna e lombar", "A dor que volta depois de um dia inteiro sentado, ou que trava na hora de levantar da cama.", "fisioterapia.html#dor-lombar", "Fisioterapia"),
        ("Joelho", "Dor para subir escada, agachar ou voltar a correr.", "fisioterapia.html#joelho", "Fisioterapia"),
        ("Depois de uma cirurgia", "Recuperar movimento e força, no tempo certo de cada fase.", "fisioterapia.html#pos-cirurgica", "Reabilitação"),
        ("Gestação", "Acompanhar as mudanças do corpo durante a gravidez, com exercício e alívio das dores.", "pilates.html#gestantes", "Pilates"),
        ("Envelhecer com autonomia", "Força e equilíbrio para continuar fazendo as próprias coisas.", "fisioterapia.html#idosos", "Fisioterapia"),
        ("Esporte", "Tratar uma lesão e voltar ao treino de forma gradual.", "fisioterapia.html#esportiva", "Fisioterapia"),
        ("Tensão muscular", "Pescoço, ombros e costas sempre duros, com sensação de peso.", "terapias-manuais.html", "Terapias manuais"),
        ("Quero fazer Pilates", "Exercício orientado e adaptado ao seu corpo, com ou sem dor.", "pilates.html", "Pilates"),
    ]
    reasons_html = "".join(
        f'<li class="reason"><a href="{h}"><h3>{t}</h3><p>{d}</p><span class="to">{to}</span></a></li>'
        for t, d, h, to in reasons)

    def front(n, titulo, texto, tags, href, rotulo):
        lis = "".join(f"<li>{t}</li>" for t in tags)
        return (f'<article class="front reveal"><span class="front-n">{n:02d}</span><h3>{titulo}</h3><p>{texto}</p>'
                f'<ul class="tags">{lis}</ul><a class="link" href="{href}">{rotulo}</a></article>')

    body = f"""
<section class="hero on-green" aria-labelledby="hero-t">
  <div class="wrap grid">
    <div class="hero-text">
      <span class="eyebrow">Clínica de fisioterapia · Maraponga, Fortaleza</span>
      <h1 id="hero-t">Fisioterapia e Pilates com tempo para olhar <em>o seu caso.</em></h1>
      <p class="lead">Na Maraponga. Você passa por uma avaliação, entende o que está acontecendo com o seu corpo e segue um plano de tratamento feito para a sua rotina.</p>
      <div class="hero-actions">
        <a class="btn btn--accent" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Agendar avaliação pelo WhatsApp</a>
        <a class="link" href="#como-chegar">Como chegar</a>
      </div>
    </div>
    <div class="hero-media">
      <div class="hero-photo hero-photo--a ratio-p figure">{pic("pilates-orientado", "Fisioterapeuta de uniforme azul orienta uma aluna que ergue uma bola vermelha sentada em um aparelho de Pilates", "p", eager=True)}</div>
      <div class="hero-photo hero-photo--b ratio-p figure">{pic("pilates-aluna", "Aluna sentada em um aparelho de Pilates puxa alças com os braços estendidos à frente", "p", eager=True)}</div>
    </div>
  </div>
  <div class="wrap">
    <dl class="hero-facts">
      <div><dt>No Google</dt><dd>{NOTA} · {N_AVAL} avaliações</dd></div>
      <div><dt>Onde</dt><dd>Maraponga, Fortaleza</dd></div>
      <div><dt>Referência</dt><dd>2º andar, prédio do Frangolândia</dd></div>
    </dl>
  </div>
</section>

<section class="section" aria-labelledby="motivos-t">
  <div class="wrap grid">
    <div class="reasons-head reveal">
      <span class="eyebrow">Por onde começar</span>
      <h2 id="motivos-t">O que traz você aqui?</h2>
      <p>Escolha o que mais se parece com a sua situação. Se não encontrar, chame no WhatsApp e conte o que está sentindo.</p>
    </div>
    <ul class="reasons-list reveal">{reasons_html}</ul>
  </div>
</section>

<section class="section section--alt" aria-labelledby="frentes-t">
  <div class="wrap">
    <div class="head2 grid reveal">
      <div class="head2-a">
        <span class="eyebrow">O que fazemos</span>
        <h2 id="frentes-t">Três frentes de cuidado, um mesmo plano.</h2>
      </div>
      <p class="head2-b lead">O tratamento pode usar uma delas ou combinar as três. Quem decide é a avaliação, e não um pacote pronto.</p>
    </div>
    <div class="fronts">
      {front(1, "Fisioterapia", "Para tratar dor, recuperar movimento depois de uma lesão ou cirurgia e voltar às atividades com segurança.", ["Ortopédica", "Esportiva", "Pós-cirúrgica", "Para gestantes", "Para idosos"], "fisioterapia.html", "Conhecer a fisioterapia")}
      {front(2, "Pilates", "Pilates clínico parte de uma avaliação e respeita dores, lesões e limites. Para quem está em tratamento e para quem quer se exercitar com orientação.", ["Clínico", "Personalizado", "Para idosos", "Para gestantes"], "pilates.html", "Conhecer o Pilates")}
      {front(3, "Terapias manuais", "Técnicas feitas com as mãos para trabalhar articulações, músculos e tensões, quando a avaliação mostra que fazem sentido.", ["Quiropraxia", "Osteopatia", "Liberação miofascial", "Liberação muscular", "Ventosaterapia"], "terapias-manuais.html", "Conhecer as terapias manuais")}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="visita-t">
  <div class="wrap">
    <div class="reveal">
      <span class="eyebrow">A primeira visita</span>
      <h2 id="visita-t" style="max-width:18ch">Como funciona, do primeiro contato em diante.</h2>
    </div>
    <ol class="steps">
      <li class="step reveal"><h3>Você chama no WhatsApp</h3><p>Conte em poucas palavras o que está sentindo. A gente tira as dúvidas e combina o horário da avaliação.</p></li>
      <li class="step reveal"><h3>Avaliação</h3><p>Uma conversa sobre a sua história e a sua rotina, seguida de testes de movimento, força e postura. Se tiver exames, traga. {fill('duração da avaliação e o que levar')}</p></li>
      <li class="step reveal"><h3>Plano de tratamento</h3><p>Você sai sabendo o que foi encontrado, o que vamos fazer e por quê, explicado sem termos difíceis.</p></li>
      <li class="step reveal"><h3>Acompanhamento</h3><p>A cada sessão observamos como o corpo respondeu e ajustamos o plano, com orientações para o dia a dia.</p></li>
    </ol>
  </div>
</section>

<section class="section section--alt" aria-labelledby="espaco-t">
  <div class="wrap">
    <div class="head2 grid reveal">
      <div class="head2-a">
        <span class="eyebrow">O espaço</span>
        <h2 id="espaco-t">Um lugar tranquilo para se cuidar.</h2>
      </div>
      <p class="head2-b"><a class="link" href="a-clinica.html">Ver a clínica por dentro</a></p>
    </div>
    <div class="pair">
      <div class="reveal">{figure("estudio-pilates", "Estúdio de Pilates com piso de madeira, aparelhos cinza, coluna de jardim vertical e iluminação quente no teto", "l", "O estúdio de Pilates.")}</div>
      <div class="reveal">{figure("sala-avaliacao", "Sala de atendimento com maca, armário branco e mesa de vidro", "l", "Sala de avaliação e atendimento individual.")}</div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="equipe-t">
  <div class="wrap">
    <div class="team-head reveal">
      <span class="eyebrow">Equipe</span>
      <h2 id="equipe-t">Quem cuida de você.</h2>
    </div>
    {luanna()}
  </div>
</section>

<section class="section section--alt" aria-labelledby="aval-t">
  <div class="wrap grid">
    <div class="reviews-head reveal">
      <span class="eyebrow">Avaliações</span>
      <h2 id="aval-t" class="vh">Avaliações no Google</h2>
      <p class="score" aria-hidden="true">{NOTA}</p>
      <p class="score-label">Nota {NOTA} no Google, com {N_AVAL} avaliações de pacientes.</p>
      <a class="link" href="{MAPS_VER}" target="_blank" rel="noopener">Ver todas no Google</a>
    </div>
    <ul class="reviews-list reveal">
      <li><blockquote><p class="quote">Lugar agradável, bons equipamentos e equipe preparada e atenciosa.</p></blockquote></li>
      <li><blockquote><p class="quote">Bem agradável, ótimo espaço!</p></blockquote></li>
    </ul>
  </div>
</section>

{onde()}

<section class="section section--line" aria-labelledby="faq-t">
  <div class="wrap grid">
    <div class="faq-head reveal">
      <span class="eyebrow">Dúvidas</span>
      <h2 id="faq-t">Perguntas frequentes.</h2>
    </div>
    <div class="faq-list reveal">
      <details><summary>Preciso de encaminhamento médico?</summary><div class="answer"><p>Para o atendimento particular, você pode agendar a avaliação diretamente com a fisioterapeuta. Se tiver pedido médico, laudos ou exames, traga no primeiro dia: eles ajudam na avaliação.</p>{so('<p>' + fill('confirmar a regra para convênios') + '</p>')}</div></details>
      {so('<details><summary>Vocês atendem por convênio?</summary><div class="answer"><p>' + fill('convênios aceitos e formas de pagamento') + '</p></div></details>')}
      {so('<details><summary>Quanto tempo dura a sessão?</summary><div class="answer"><p>' + fill('duração das sessões de fisioterapia e das aulas de Pilates') + '</p></div></details>')}
      <details><summary>Qual a diferença entre Pilates clínico e Pilates de academia?</summary><div class="answer"><p>No Pilates clínico, os exercícios são escolhidos depois de uma avaliação e levam em conta dores, lesões e limitações de cada pessoa. Ele pode fazer parte de um tratamento. Na academia, a aula costuma seguir uma sequência geral, voltada ao condicionamento.</p></div></details>
      <details><summary>Gestante pode fazer Pilates em qualquer fase?</summary><div class="answer"><p>Em geral sim, desde que o obstetra tenha liberado a atividade física. Os exercícios e as posições mudam a cada trimestre, e a avaliação define o que é adequado para o seu momento.</p></div></details>
      <details><summary>Como eu agendo?</summary><div class="answer"><p>Pelo WhatsApp ou por telefone, no {FONE_EXIBE}. Conte o que está sentindo e combinamos o horário da sua avaliação.</p></div></details>
      {so('<details><summary>Tem estacionamento?</summary><div class="answer"><p>' + fill('onde estacionar e como é o acesso ao 2º andar') + '</p></div></details>')}
    </div>
  </div>
</section>

{cta("Conte o que você está sentindo. <span>A gente começa por aí.</span>", "A conversa pelo WhatsApp é com a equipe da clínica. Você tira as dúvidas e marca a sua avaliação.", msg)}
"""
    return layout("index.html",
                  "Clínica Zelo | Fisioterapia e Pilates na Maraponga, Fortaleza",
                  "Fisioterapia, Pilates clínico e terapias manuais na Maraponga, em Fortaleza. Nota 5,0 no Google. Agende sua avaliação pelo WhatsApp.",
                  body, msg)


# ─────────────────────────── FISIOTERAPIA ───────────────────────────
def page_fisio():
    msg = "Olá! Vi o site da Clínica Zelo e gostaria de agendar uma avaliação de fisioterapia."
    m = lambda s: f"Olá! Vi o site da Clínica Zelo e gostaria de agendar uma avaliação de {s}."
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs("Fisioterapia")}
    <div class="grid page-hero--l">
      <div class="page-hero-text">
        <h1>Fisioterapia para tratar a dor e recuperar <em>o movimento.</em></h1>
        <p class="lead">Dor na coluna, no joelho, uma lesão no treino ou a recuperação de uma cirurgia. O tratamento começa por entender o que está causando o problema.</p>
        <a class="btn btn--accent" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Agendar avaliação</a>
      </div>
      <div class="page-hero-media">
        {figure("sala-avaliacao", "Sala de atendimento com maca, armário branco, mesa de vidro e parede cinza texturizada", "l", "Uma das salas de atendimento.", eager=True)}
      </div>
    </div>
  </div>
</section>

{toc([("ortopedica", "Ortopédica"), ("esportiva", "Esportiva"), ("pos-cirurgica", "Pós-cirúrgica"), ("gestantes", "Para gestantes"), ("idosos", "Para idosos"), ("condicoes", "O que tratamos"), ("recursos", "Recursos")])}

<section aria-label="Modalidades de fisioterapia">
  <div class="wrap">
    {mod(1, "ortopedica", "Fisioterapia ortopédica", "Para dores e lesões em articulações, músculos, tendões e coluna.",
         "O tratamento das dores e das limitações de movimento que vêm de ossos, articulações, músculos e tendões. Aqui entram a dor lombar, a dor no joelho, a escoliose e a artrite.",
         "Para quem sente dor ao sentar, levantar, subir escada ou dormir, e para quem recebeu um diagnóstico e quer entender o que fazer com ele.",
         "Conversamos sobre a sua rotina, testamos movimento e força e examinamos a região da dor. O plano combina exercícios, técnicas manuais e recursos como o laser, conforme o seu caso.",
         m("fisioterapia ortopédica"))}
    {mod(2, "esportiva", "Fisioterapia esportiva", "Para tratar lesões do treino e preparar a volta ao esporte.",
         "O tratamento de lesões ligadas ao treino e ao esporte, como entorses, tendinites e lesões musculares, e o preparo do corpo para voltar à atividade.",
         "Para quem corre, pedala, joga bola ou faz musculação, seja atleta ou praticante de fim de semana.",
         "Avaliamos o gesto do esporte, a força e a mobilidade. O tratamento avança por etapas, do controle da dor ao retorno gradual ao treino.",
         m("fisioterapia esportiva"))}
    {mod(3, "pos-cirurgica", "Reabilitação pós-cirúrgica", "Para recuperar movimento, força e confiança depois de operar.",
         "A reabilitação depois de uma cirurgia ortopédica, como as de joelho, ombro, quadril ou coluna.",
         "Para quem operou e precisa voltar às atividades do dia a dia, ao trabalho ou ao esporte.",
         "Seguimos as orientações do seu cirurgião e respeitamos o tempo de cicatrização. Cada fase tem objetivos claros, e você sabe em qual delas está.",
         m("reabilitação pós-cirúrgica"))}
    {mod(4, "gestantes", "Fisioterapia para gestantes", "Para as dores e os desconfortos que aparecem com a gravidez.",
         "O cuidado com as dores que surgem com as mudanças do corpo na gestação, como a dor lombar e a dor na região do quadril.",
         "Para gestantes com liberação do obstetra para a atividade.",
         "Posições confortáveis, exercícios leves e técnicas manuais suaves, adaptados a cada fase da gestação.",
         m("fisioterapia para gestantes"))}
    {mod(5, "idosos", "Fisioterapia para idosos", "Para manter força, equilíbrio e independência.",
         "Um trabalho de força, equilíbrio e mobilidade voltado para as atividades do dia a dia: caminhar, levantar da cadeira, subir degraus.",
         "Para quem sente que perdeu firmeza nos movimentos e para quem convive com artrose, artrite ou dores antigas.",
         "Ritmo tranquilo, exercícios seguros e progressão gradual. Explicamos cada exercício e para que ele serve.",
         m("fisioterapia para idosos"))}
  </div>
</section>

<section class="section section--alt" id="condicoes" aria-labelledby="cond-t">
  <div class="wrap grid">
    <div class="conds-head reveal">
      <span class="eyebrow">O que tratamos</span>
      <h2 id="cond-t">As queixas que mais chegam até nós.</h2>
    </div>
    <div class="conds reveal">
      <div class="cond" id="dor-lombar"><h3>Dor lombar e coluna</h3><p>A dor na parte baixa das costas pode aparecer depois de muito tempo sentado, de um esforço ou sem motivo claro. A avaliação identifica o que piora e o que alivia. O tratamento costuma combinar exercício, terapia manual e orientação para a rotina.</p></div>
      <div class="cond" id="joelho"><h3>Dor no joelho</h3><p>Dor ao subir escada, agachar, correr ou depois de ficar muito tempo sentado. Avaliamos o joelho junto com o quadril e o tornozelo, porque muitas vezes a sobrecarga começa nos vizinhos.</p></div>
      <div class="cond" id="escoliose"><h3>Escoliose</h3><p>A escoliose é uma curvatura lateral da coluna. O acompanhamento trabalha postura, força e consciência corporal, com exercícios específicos para o tipo de curva de cada pessoa.</p></div>
      <div class="cond" id="artrite"><h3>Artrite</h3><p>Na artrite, as articulações inflamam e doem. A fisioterapia trabalha movimento e força com exercícios dosados para os períodos de crise e para os de calmaria, em conjunto com o tratamento médico.</p></div>
    </div>
  </div>
</section>

<section class="section" id="recursos" aria-labelledby="rec-t">
  <div class="wrap grid">
    <div class="res-head reveal">
      <span class="eyebrow">Recursos</span>
      <h2 id="rec-t">Equipamentos que complementam o tratamento.</h2>
    </div>
    <div class="res reveal">
      {figure("laserterapia", "Aparelho de laser terapêutico aplicado no pescoço de um paciente", "l")}
      <h3>Laserterapia</h3>
      <p>Aplicação de laser de baixa intensidade sobre a região tratada. É indolor e entra como complemento no plano de tratamento. {fill('confirmar em quais casos a clínica indica')}</p>
    </div>
    <div class="res reveal">
      {figure("bota-pneumatica", "Paciente sentado na maca com botas pneumáticas de compressão nas duas pernas", "l")}
      <h3>Bota pneumática</h3>
      <p>Um equipamento que envolve as pernas e faz compressão com ar, em sequência. {fill('confirmar em quais casos a clínica indica')}</p>
    </div>
  </div>
</section>

{cta("Vamos entender a sua dor antes de tratar.", "Chame no WhatsApp, conte o que está sentindo e agende a sua avaliação de fisioterapia.", msg)}
"""
    return layout("fisioterapia.html",
                  "Fisioterapia na Maraponga, Fortaleza | Clínica Zelo",
                  "Fisioterapia ortopédica, esportiva, pós-cirúrgica, para gestantes e para idosos na Maraponga, Fortaleza. Dor lombar, joelho, coluna, escoliose e artrite.",
                  body, msg, og="sala-avaliacao")


# ───────────────────────────── PILATES ─────────────────────────────
def page_pilates():
    msg = "Olá! Vi o site da Clínica Zelo e gostaria de agendar uma avaliação de Pilates."
    m = lambda s: f"Olá! Vi o site da Clínica Zelo e gostaria de saber mais sobre o {s}."
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs("Pilates")}
    <div class="grid page-hero--p">
      <div class="page-hero-text">
        <h1>Pilates clínico na Maraponga, adaptado <em>ao seu corpo.</em></h1>
        <p class="lead">Os exercícios são escolhidos a partir de uma avaliação. Vale para quem tem dor, para quem está voltando de uma lesão e para quem só quer se movimentar melhor.</p>
        <a class="btn btn--accent" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Agendar avaliação de Pilates</a>
      </div>
      <div class="page-hero-media">
        {figure("pilates-aluna", "Aluna sentada em um aparelho de Pilates puxa alças com os braços estendidos à frente", "p", "Exercício de braços com molas.", eager=True)}
      </div>
    </div>
  </div>
</section>

{toc([("clinico", "Pilates clínico"), ("personalizado", "Personalizado"), ("idosos", "Para idosos"), ("gestantes", "Para gestantes"), ("diferenca", "Clínico ou de academia"), ("estudio", "O estúdio")])}

<section aria-label="Modalidades de Pilates">
  <div class="wrap">
    {mod(1, "clinico", "Pilates clínico", "O Pilates como parte de um tratamento.",
         "Pilates orientado por uma avaliação. Os exercícios levam em conta as suas dores, lesões e limitações.",
         "Para quem tem dor na coluna, está saindo de uma reabilitação ou quer se exercitar com segurança tendo algum problema ortopédico.",
         "Exercícios nos aparelhos e no solo, com molas que ajudam ou desafiam o movimento. A carga e a dificuldade mudam conforme você evolui.",
         m("Pilates clínico"))}
    {mod(2, "personalizado", "Pilates personalizado", "Um programa montado para o seu objetivo.",
         "Aulas planejadas para o que você busca: ganhar força, melhorar a postura, ter mais flexibilidade ou complementar outro esporte.",
         "Para quem quer um programa sob medida e atenção aos detalhes de cada movimento.",
         f"A aula segue um programa só seu, revisto de tempos em tempos. {fill('formato das aulas: individual, dupla ou turma, e duração')}",
         m("Pilates personalizado"))}
    {mod(3, "idosos", "Pilates para idosos", "Movimento seguro para manter a autonomia.",
         "Exercícios de força, equilíbrio e mobilidade em um ritmo confortável, com apoio dos aparelhos.",
         "Para quem quer continuar ativo e independente, inclusive quem nunca fez Pilates ou está há muito tempo parado.",
         "Começamos devagar, com exercícios simples, e avançamos aos poucos. Dores e limitações de cada pessoa são respeitadas.",
         m("Pilates para idosos"))}
    {mod(4, "gestantes", "Pilates para gestantes", "Exercício adaptado a cada fase da gravidez.",
         "Pilates adaptado para a gestação, com foco em postura, respiração e fortalecimento.",
         "Para gestantes com liberação do obstetra para a atividade física.",
         "As posições e os exercícios mudam a cada trimestre. A aula acompanha como você está se sentindo no dia.",
         m("Pilates para gestantes"))}
  </div>
</section>

<section class="section on-green versus" id="diferenca" aria-labelledby="dif-t">
  <div class="wrap grid">
    <div class="versus-head reveal">
      <span class="eyebrow">Uma dúvida comum</span>
      <h2 id="dif-t">Pilates clínico ou Pilates de academia?</h2>
    </div>
    <div class="versus-cols reveal">
      <div><h3>Clínico</h3><p>Começa com uma avaliação. Os exercícios são escolhidos para o seu corpo e podem fazer parte de um tratamento. A progressão acompanha a sua evolução.</p></div>
      <div><h3>De academia</h3><p>Costuma seguir uma sequência geral de aula, voltada ao condicionamento. Funciona bem para quem não tem dor nem restrição de movimento.</p></div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="orient-t">
  <div class="wrap grid duo">
    <div class="duo-a reveal">{figure("pilates-orientado", "Fisioterapeuta orienta uma aluna que ergue uma bola vermelha sentada em um aparelho de Pilates", "p")}</div>
    <div class="duo-text reveal">
      <span class="eyebrow">Na prática</span>
      <h2 id="orient-t">Orientação de perto, do começo ao fim.</h2>
      <p>A profissional acompanha a execução, corrige a postura e ajusta a carga na hora. É isso que torna o exercício seguro para quem tem dor.</p>
    </div>
  </div>
</section>

<section class="section section--alt" id="estudio" aria-labelledby="est-t">
  <div class="wrap grid">
    <div class="band-media reveal">{figure("estudio-pilates", "Estúdio de Pilates com piso de madeira, aparelhos cinza, coluna de jardim vertical e iluminação quente", "l")}</div>
    <div class="band-body reveal">
      <span class="eyebrow">O estúdio</span>
      <h2 id="est-t">Aparelhos completos em um ambiente calmo.</h2>
      <p>O estúdio tem aparelhos de Pilates com molas, barris, bolas e acessórios. Fica no mesmo andar das salas de fisioterapia.</p>
      <p><a class="link" href="a-clinica.html">Ver a clínica por dentro</a></p>
    </div>
  </div>
</section>

{cta("Quer começar o Pilates do jeito certo para o seu corpo?", "Chame no WhatsApp e agende a sua avaliação. A partir dela, montamos as suas aulas.", msg)}
"""
    return layout("pilates.html",
                  "Pilates clínico na Maraponga, Fortaleza | Clínica Zelo",
                  "Pilates clínico, personalizado, para idosos e para gestantes na Maraponga, Fortaleza. Exercícios escolhidos a partir de uma avaliação.",
                  body, msg, og="pilates-aluna")


# ──────────────────────── TERAPIAS MANUAIS ────────────────────────
def page_terapias():
    msg = "Olá! Vi o site da Clínica Zelo e gostaria de agendar uma avaliação de terapia manual."
    m = lambda s: f"Olá! Vi o site da Clínica Zelo e gostaria de saber mais sobre {s}."
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs("Terapias manuais")}
    <div class="grid page-hero--text">
      <div class="page-hero-text">
        <h1>Terapias manuais: o tratamento feito <em>com as mãos.</em></h1>
        <p class="lead">Técnicas que trabalham articulações, músculos e pontos de tensão. Podem ser o centro do tratamento ou entrar como parte de um plano de fisioterapia.</p>
        <a class="btn btn--accent" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Agendar avaliação</a>
      </div>
      <p class="page-hero-aside">Nem toda técnica serve para todo mundo. A avaliação define qual é indicada para você e qual não é.</p>
    </div>
  </div>
</section>

{toc([("quiropraxia", "Quiropraxia"), ("osteopatia", "Osteopatia"), ("liberacao-miofascial", "Liberação miofascial"), ("liberacao-muscular", "Liberação muscular"), ("ventosaterapia", "Ventosaterapia")])}

<section aria-label="Técnicas de terapia manual">
  <div class="wrap">
    {mod(1, "quiropraxia", "Quiropraxia", "Ajustes manuais na coluna e nas articulações.",
         "Uma técnica manual voltada para a coluna e as articulações. Usa ajustes rápidos e precisos para trabalhar a mobilidade.",
         "Para quem sente a coluna travada ou tem rigidez no pescoço e na lombar. A avaliação confirma se a técnica é indicada.",
         "Depois dos testes de movimento, o ajuste é feito com as mãos, em posições específicas. É comum ouvir um estalo, que é só gás se deslocando dentro da articulação.",
         m("quiropraxia"))}
    {mod(2, "osteopatia", "Osteopatia", "Um olhar para o corpo como um conjunto.",
         "Uma abordagem manual que procura restrições de movimento em articulações, músculos e outros tecidos que possam estar ligadas à sua queixa.",
         "Para quem tem dores que vão e voltam ou que mudam de lugar, e ainda não encontrou uma explicação clara.",
         "Avaliação detalhada e manobras suaves, feitas com as mãos e sem aparelhos.",
         m("osteopatia"))}
    {mod(3, "liberacao-miofascial", "Liberação miofascial", "Para a sensação de músculo preso e encurtado.",
         "Pressão e deslizamento sobre a fáscia, o tecido que envolve os músculos, para trabalhar pontos de tensão.",
         "Para quem treina com frequência, passa muitas horas na mesma posição ou sente o corpo sempre rígido.",
         "É feita com as mãos ou com instrumentos próprios. Os pontos mais tensos podem incomodar um pouco, e a pressão fica sempre dentro do seu limite.",
         m("liberação miofascial"))}
    {mod(4, "liberacao-muscular", "Liberação muscular", "Para músculos tensos e doloridos.",
         "Um trabalho manual direto sobre os músculos, com pressão e alongamento, voltado para áreas de tensão.",
         "Para quem carrega tensão no pescoço, nos ombros ou nas costas, por esforço, postura ou estresse.",
         "A fisioterapeuta localiza os pontos de tensão e trabalha cada região com calma. Pode ser combinada com exercícios e alongamentos.",
         m("liberação muscular"))}
    {mod(5, "ventosaterapia", "Ventosaterapia", "Sucção sobre a pele, como complemento ao tratamento.",
         "Copos aplicados sobre a pele criam sucção e levantam levemente os tecidos da região.",
         "Costuma entrar como complemento em quadros de tensão muscular. A avaliação define se faz sentido para você.",
         "As ventosas ficam alguns minutos sobre a pele ou são deslizadas pela região. Podem deixar marcas arroxeadas, que somem em alguns dias.",
         m("ventosaterapia"))}
  </div>
</section>

<section class="section section--alt prose" aria-labelledby="tm-t">
  <div class="wrap grid">
    <div class="prose-head reveal">
      <span class="eyebrow">No plano de tratamento</span>
      <h2 id="tm-t">A técnica certa na hora certa.</h2>
    </div>
    <div class="prose-body reveal">
      <p>A terapia manual costuma vir junto com exercícios. As mãos trabalham a tensão e a mobilidade, e o exercício ajuda o corpo a manter o que foi conquistado.</p>
      <p><a class="link" href="fisioterapia.html">Ver a fisioterapia</a></p>
      {so(ph("l", "Foto horizontal, de perto: mãos da fisioterapeuta em um atendimento de terapia manual nas costas ou no ombro de um paciente, com luz suave."))}
    </div>
  </div>
</section>

{cta("Não sabe qual técnica é para você? <span>A avaliação responde.</span>", "Chame no WhatsApp, conte o que está sentindo e agende um horário.", msg)}
"""
    return layout("terapias-manuais.html",
                  "Quiropraxia, osteopatia e liberação miofascial na Maraponga | Clínica Zelo",
                  "Terapias manuais na Maraponga, Fortaleza: quiropraxia, osteopatia, liberação miofascial, liberação muscular e ventosaterapia, indicadas a partir de uma avaliação.",
                  body, msg, og="sala-avaliacao")


# ───────────────────────────── A CLÍNICA ─────────────────────────────
def page_clinica():
    msg = "Olá! Vi o site da Clínica Zelo e gostaria de agendar uma avaliação."
    historia = so(f"""<section class="section section--line prose" aria-labelledby="hist-t">
  <div class="wrap grid">
    <div class="prose-head reveal">
      <span class="eyebrow">Nossa história</span>
      <h2 id="hist-t">Como a clínica começou.</h2>
    </div>
    <div class="prose-body reveal">
      <p>{fill('história da clínica: quando e por que foi fundada, o que mudou desde então e o que o nome Zelo representa para a equipe')}</p>
    </div>
  </div>
</section>""")
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs("A clínica")}
    <div class="grid page-hero--l">
      <div class="page-hero-text">
        <h1>Zelo quer dizer cuidado atento. <em>É o que fazemos aqui.</em></h1>
        <p class="lead">Uma clínica de fisioterapia e Pilates na Maraponga, com estúdio de aparelhos e salas de atendimento individual.</p>
      </div>
      <div class="page-hero-media">
        {figure("estudio-pilates", "Estúdio de Pilates com piso de madeira, aparelhos cinza, coluna de jardim vertical e iluminação quente", "l", "O estúdio de Pilates.", eager=True)}
      </div>
    </div>
  </div>
</section>

{historia}

<section class="section section--alt" aria-labelledby="esp-t">
  <div class="wrap">
    <div class="grid">
      <div class="res-head reveal">
        <span class="eyebrow">O espaço</span>
        <h2 id="esp-t">Por dentro da clínica.</h2>
      </div>
    </div>
    <div class="grid" style="row-gap:var(--gap); align-items:end">
      <div class="reveal" style="grid-column:1/-1" data-g="a">{figure("sala-avaliacao", "Sala de atendimento com maca, armário branco, mesa de vidro e parede cinza texturizada", "l", "Sala de avaliação e atendimento individual.")}</div>
      <div class="reveal" data-g="b">{figure("pilates-aluna", "Aluna em exercício no aparelho de Pilates, com bolas e acessórios organizados ao fundo", "p", "Aparelhos e acessórios do estúdio.")}</div>
      {so('<div class="reveal" data-g="c">' + ph("p", "Foto vertical da recepção, vista de quem chega, sem pessoas posando.") + '</div><div class="reveal" data-g="d">' + ph("l", "Foto horizontal da fachada do prédio ou da entrada que leva ao 2º andar, de dia.") + '</div>')}
    </div>
    <blockquote class="reveal" style="margin-top:clamp(2.5rem,5vw,4.5rem); max-width:44rem">
      <p class="quote">Bem agradável, ótimo espaço!</p>
      <cite class="quote-src" style="font-style:normal">Avaliação no Google</cite>
    </blockquote>
  </div>
</section>

<section class="section" aria-labelledby="equipe-t">
  <div class="wrap">
    <div class="team-head reveal">
      <span class="eyebrow">Equipe</span>
      <h2 id="equipe-t">Quem cuida de você.</h2>
    </div>
    {luanna()}
  </div>
</section>

{onde(alt=True)}

{cta("Venha conhecer a clínica.", "Agende a sua avaliação pelo WhatsApp e veja o espaço de perto.", msg)}
"""
    return layout("a-clinica.html",
                  "A clínica: espaço e equipe | Clínica Zelo, Maraponga",
                  "Conheça o espaço e a equipe da Clínica Zelo, clínica de fisioterapia e Pilates na Av. Godofredo Maciel, Maraponga, Fortaleza.",
                  body, msg, og="estudio-pilates")


# ───────────────────────────── CONTATO ─────────────────────────────
def page_contato():
    msg = "Olá! Vi o site da Clínica Zelo e gostaria de agendar uma avaliação."
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs("Contato")}
    <div class="grid page-hero--text">
      <div class="page-hero-text">
        <h1>Fale com a gente. <em>Responder é parte do cuidado.</em></h1>
        <p class="lead">O caminho mais rápido para agendar é o WhatsApp. Se preferir, ligue ou passe na clínica.</p>
      </div>
      {so('<p class="page-hero-aside">Horário de atendimento: ' + fill('dias e horários completos; fecha às 21h') + '</p>')}
    </div>
  </div>
</section>

<section aria-label="Canais de contato" style="padding-bottom:var(--section)">
  <div class="wrap">
    <ul class="channels reveal">
      <li class="channel"><a href="{wa(msg)}" target="_blank" rel="noopener"><span class="k">WhatsApp</span><span class="big">Agendar uma avaliação</span><span class="note">{FONE_EXIBE}</span></a></li>
      <li class="channel"><a href="tel:{FONE_TEL}"><span class="k">Telefone</span><span class="big">{FONE_EXIBE}</span><span class="note">Toque para ligar</span></a></li>
      <li class="channel"><a href="{MAPS_ROTA}" target="_blank" rel="noopener"><span class="k">Endereço</span><span class="big">{RUA}</span><span class="note">{BAIRRO}<br>CEP {CEP}</span></a></li>
      {so('<li class="channel"><div><span class="k">Instagram</span><span class="big">' + fill('@ da clínica') + '</span><span class="note"></span></div></li>')}
    </ul>
  </div>
</section>

<section class="section section--alt" id="como-chegar" aria-labelledby="rota-t">
  <div class="wrap grid">
    <div class="where-map reveal">
      <div class="map"><a class="map-alt" href="{MAPS_VER}" target="_blank" rel="noopener">Ver a localização no Google Maps</a>
        <iframe src="{MAPS_EMBED}" title="Mapa com a localização da Clínica Zelo na Av. Godofredo Maciel, Maraponga" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
    </div>
    <div class="where-body reveal">
      <span class="eyebrow">Como chegar</span>
      <h2 id="rota-t">Em cima do supermercado Frangolândia.</h2>
      <ol class="route">
        <li><span>Siga pela Av. Godofredo Maciel até o número 2540, na Maraponga.</span></li>
        <li><span>Entre no prédio do supermercado Frangolândia.</span></li>
        <li><span>Suba ao 2º andar. A clínica fica ali. {fill('escada, elevador e onde estacionar')}</span></li>
      </ol>
      <div class="where-actions">
        <a class="btn btn--accent" href="{MAPS_ROTA}" target="_blank" rel="noopener">Abrir rota</a>
        <a class="btn btn--ghost" href="tel:{FONE_TEL}">Ligar</a>
      </div>
    </div>
  </div>
</section>

<section class="section prose" aria-labelledby="fach-t">
  <div class="wrap grid">
    <div class="prose-head reveal">
      <span class="eyebrow">Primeira vez?</span>
      <h2 id="fach-t">O que trazer.</h2>
    </div>
    <div class="prose-body reveal">
      <p>Se tiver exames, laudos ou pedido médico, traga no dia da avaliação. Venha com uma roupa confortável, que permita se movimentar.</p>
      {so('<p>' + fill('documentos necessários e outras orientações da clínica') + '</p>' + ph("l", "Foto horizontal da fachada do prédio, de dia, mostrando a entrada que leva ao 2º andar."))}
    </div>
  </div>
</section>

{cta("Um recado no WhatsApp já resolve.", "Conte o que você está sentindo e a gente combina o melhor horário.", msg)}
"""
    return layout("contato.html",
                  "Contato e como chegar | Clínica Zelo, Maraponga, Fortaleza",
                  "Agende pelo WhatsApp (85) 99944-6666. Av. Godofredo Maciel, 2540, 2º andar, Maraponga, Fortaleza, no prédio do supermercado Frangolândia.",
                  body, msg, og="estudio-pilates")


PAGES = {"index.html": page_index, "fisioterapia.html": page_fisio, "pilates.html": page_pilates,
         "terapias-manuais.html": page_terapias, "a-clinica.html": page_clinica, "contato.html": page_contato}

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="6" fill="#24443a"/>'
           '<text x="32" y="47" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="44" fill="#f6f1e9">Z</text></svg>')

if __name__ == "__main__":
    for name, fn in PAGES.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
    (OUT / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    urls = "".join(f"  <url><loc>{DOMINIO}/{'' if n == 'index.html' else n}</loc></url>\n" for n in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
    print("ok:", ", ".join(PAGES))
