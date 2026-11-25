"""Gera as artes do Instagram da PineWeb (1080x1350, JPEG) com Chrome headless."""
import json, subprocess, sys, pathlib
from PIL import Image

REPO = pathlib.Path(sys.argv[1])
OUT = REPO / "social"
TMP = pathlib.Path("/home/claude/social-build/tmp")
OUT.mkdir(exist_ok=True); TMP.mkdir(parents=True, exist_ok=True)
# Símbolo desenhado inline (mesmo do cabeçalho do site). Nunca aplicar filter no logo:
# o brightness() escurecia a janela clara e o pinheiro virava um borrão escuro.
def logo_svg(borda):
    return ('<svg viewBox="0 0 120 120" aria-hidden="true">'
            f'<rect x="7" y="11" width="106" height="98" rx="20" fill="#F4F6F1" stroke="{borda}" stroke-width="6"/>'
            '<path d="M7 36 H113" stroke="#163A2C" stroke-width="4"/>'
            '<circle cx="23" cy="24" r="4" fill="#163A2C"/><circle cx="35" cy="24" r="4" fill="#163A2C"/><circle cx="47" cy="24" r="4" fill="#163A2C"/>'
            '<polygon points="60,42 74,58 46,58" fill="#2E7D5B"/><polygon points="60,51 81,75 39,75" fill="#2E7D5B"/>'
            '<polygon points="60,63 88,94 32,94" fill="#2E7D5B"/><rect x="55" y="94" width="10" height="9" fill="#163A2C"/></svg>')

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:'Inter Display','Inter',sans-serif;position:relative;padding:96px 88px}
.dark{background:#163A2C;color:#F4F6F1}
.light{background:#F4F6F1;color:#1C2420}
.amber{background:#F2A541;color:#163A2C}
.brand{position:absolute;left:88px;bottom:72px;display:flex;align-items:center;gap:16px;font-weight:700;font-size:30px;letter-spacing:-.5px}
.brand svg{width:56px;height:56px;flex:none}
.page{position:absolute;right:88px;bottom:80px;font-size:26px;opacity:.6;font-weight:500}
.eyebrow{font-size:28px;font-weight:600;letter-spacing:3px;text-transform:uppercase;margin-bottom:36px}
.dark .eyebrow{color:#8FD694} .light .eyebrow{color:#2E7D5B}
h1{font-size:104px;line-height:1.02;font-weight:800;letter-spacing:-3px}
h2{font-size:78px;line-height:1.06;font-weight:800;letter-spacing:-2px}
p{font-size:40px;line-height:1.35;margin-top:40px;font-weight:400}
.dark p{color:#C9D6CC} .light p{color:#4E5C54}
.hl{color:#F2A541} .light .hl{color:#2E7D5B}
.big{font-size:230px;font-weight:800;letter-spacing:-8px;line-height:1;color:#8FD694}
.row{display:flex;gap:28px;margin-top:56px;flex-direction:column}
.card{background:rgba(255,255,255,.07);border-radius:28px;padding:34px 40px;font-size:38px;line-height:1.3;display:flex;gap:28px;align-items:flex-start}
.light .card{background:#fff;border:2px solid #D9E0D8}
.card b{font-weight:700}
.num{min-width:64px;height:64px;border-radius:50%;background:#8FD694;color:#163A2C;font-weight:800;font-size:32px;display:flex;align-items:center;justify-content:center}
.light .num{background:#2E7D5B;color:#fff}
.frame{margin-top:56px;border-radius:24px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.35);background:#fff}
.bar{height:46px;background:#E6EEE5;display:flex;gap:12px;align-items:center;padding:0 22px}
.bar i{width:16px;height:16px;border-radius:50%;background:#B9C6BB;display:block}
.frame img{width:100%;display:block}
.tag{display:inline-block;margin-top:44px;padding:14px 28px;border-radius:999px;background:#8FD694;color:#163A2C;font-size:30px;font-weight:700}
.light .tag{background:#163A2C;color:#F4F6F1}
.cta{display:inline-block;margin-top:60px;padding:30px 48px;border-radius:999px;background:#F2A541;color:#163A2C;font-size:40px;font-weight:800}
.amber .cta{background:#163A2C;color:#F4F6F1}
.center{display:flex;flex-direction:column;justify-content:center;height:100%;padding-bottom:120px}
.swipe{position:absolute;right:88px;top:96px;font-size:28px;font-weight:600;opacity:.75}
"""

def brand(theme):
    # Fundo escuro: borda verde-broto (como no site). Fundos claros/âmbar: borda floresta.
    logo = logo_svg("#8FD694" if theme == "dark" else "#163A2C")
    return f'<div class="brand">{logo}PineWeb</div>'

def render(name, theme, body, page=None, swipe=False):
    pg = f'<div class="page">{page}</div>' if page else ""
    sw = '<div class="swipe">arraste →</div>' if swipe else ""
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{theme}">{sw}{body}{brand(theme)}{pg}</body></html>'
    h = TMP / f"{name}.html"; h.write_text(html)
    png = TMP / f"{name}.png"
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1080,1350",
                    f"--screenshot={png}", h.as_uri()], check=True, capture_output=True)
    Image.open(png).convert("RGB").resize((1080, 1350)).save(OUT / f"{name}.jpg", "JPEG", quality=90)
    return f"social/{name}.jpg"

def shot(p):
    return f'<div class="frame"><div class="bar"><i></i><i></i><i></i></div><img src="{(REPO/"portfolio"/p).as_uri()}"></div>'

posts = {}

# 1 — Apresentação
s = []
s.append(render("01-1", "dark", '<div class="center"><div class="eyebrow">Brasil · USA</div><h1>Seu negócio <span class="hl">ainda não tem site?</span></h1><p>A PineWeb cria sites profissionais para pequenos negócios. Sem mensalidade.</p></div>', "1/4", True))
s.append(render("01-2", "light", '<div class="eyebrow">O que a gente faz</div><h2>Tudo pra você aparecer na internet</h2><div class="row"><div class="card"><div class="num">1</div><div><b>Site sob medida</b><br>suas cores, fotos e textos</div></div><div class="card"><div class="num">2</div><div><b>Pensado pro celular</b><br>rápido em qualquer tela</div></div><div class="card"><div class="num">3</div><div><b>Encontrado no Google</b><br>e no Google Maps</div></div></div>', "2/4"))
s.append(render("01-3", "dark", '<div class="eyebrow">Em números</div><div class="big">7</div><h2>dias pra ficar pronto</h2><p><span class="hl">2</span> rodadas de revisão · <span class="hl">R$ 0</span> de mensalidade · domínio <span class="hl">no seu nome</span></p>', "3/4"))
s.append(render("01-4", "amber", '<div class="center"><h1>Vamos colocar seu negócio na internet?</h1><p style="color:#163A2C">Orçamento por escrito em até 24 horas.</p><div><span class="cta">Link na bio →</span></div></div>', "4/4"))
posts["01"] = s

# 2 — Portfólio
proj = [("gc-trend.webp", "Loja de importados", "Catálogo com sacola que fecha o pedido no WhatsApp."),
        ("glassmaster.webp", "Limpeza de vidros · Flórida", "Site em inglês com orçamento guiado por serviço."),
        ("maja-kids.webp", "Locação de brinquedos", "Catálogo animado e festa montada direto no WhatsApp."),
        ("atual-ensino.webp", "Escola de Ensino Médio", "Visual de caderno e perguntas que viram mensagem."),
        ("nora-pinho.webp", "Depilação a laser", "Mapa do corpo pra escolher as áreas e agendar.")]
s = [render("02-1", "dark", '<div class="center"><div class="eyebrow">Portfólio</div><h1>5 negócios, <span class="hl">5 sites</span> feitos sob medida</h1><p>Nada de modelo genérico. Arraste e veja.</p></div>', "1/7", True)]
for i, (img, t, d) in enumerate(proj, start=2):
    s.append(render(f"02-{i}", "light", f'<div class="eyebrow">Projeto {i-1} de 5</div><h2>{t}</h2>{shot(img)}<p>{d}</p>', f"{i}/7"))
s.append(render("02-7", "amber", '<div class="center"><h1>O próximo pode ser o seu.</h1><div><span class="cta">Peça seu orçamento →</span></div></div>', "7/7"))
posts["02"] = s

# 3 — Instagram não é site
itens = [("Quem procura no Google não acha seu Instagram", "Site aparece nas buscas e no Google Maps."),
         ("O Instagram não é seu", "Se a conta cair, você perde tudo. O site e o domínio ficam no seu nome."),
         ("Passa mais confiança", "Cliente novo pesquisa antes de comprar. Site profissional fecha negócio."),
         ("Tudo num lugar só", "Serviços, preços, fotos e o botão do WhatsApp, sem rolar 200 posts.")]
s = [render("03-1", "dark", '<div class="center"><div class="eyebrow">Dica</div><h1>Instagram <span class="hl">não é</span> site.</h1><p>4 motivos pra seu negócio ter os dois.</p></div>', "1/6", True)]
for i, (t, d) in enumerate(itens, start=2):
    s.append(render(f"03-{i}", "light", f'<div class="center"><div class="num" style="width:110px;height:110px;font-size:54px;margin-bottom:48px">{i-1}</div><h2>{t}</h2><p>{d}</p></div>', f"{i}/6"))
s.append(render("03-6", "amber", '<div class="center"><h1>Salve esse post e mande pra quem precisa.</h1><div><span class="cta">Site na bio →</span></div></div>', "6/6"))
posts["03"] = s

# 4 — Como funciona
passos = [("Conversa", "Você conta sobre o seu negócio."), ("Formulário", "Você recebe uma pasta só sua pra mandar fotos e textos."),
          ("Orçamento", "Valor, prazo e o que está incluso, por escrito, em até 24h."), ("Criação", "7 dias (15 se tiver sistema), com 2 revisões."),
          ("Publicação", "No seu domínio, com hospedagem grátis."), ("No ar", "Sem mensalidade.")]
cards = "".join(f'<div class="card" style="padding:24px 34px;font-size:34px"><div class="num">{i}</div><div><b>{t}</b> · {d}</div></div>' for i, (t, d) in enumerate(passos, 1))
s = [render("04-1", "dark", '<div class="center"><div class="eyebrow">Como funciona</div><h1>Do primeiro “oi” ao site no ar em <span class="hl">6 passos</span></h1></div>', "1/3", True),
     render("04-2", "light", f'<div class="eyebrow">Passo a passo</div><div class="row" style="margin-top:0;gap:20px">{cards}</div>', "2/3"),
     render("04-3", "amber", '<div class="center"><h1>Tudo combinado por escrito. Sem surpresa.</h1><div><span class="cta">Comece pelo link na bio →</span></div></div>', "3/3")]
posts["04"] = s

# 5 — Case EUA (imagem única)
posts["05"] = [render("05-1", "dark", f'<div class="eyebrow">Case · Florida, USA</div><h2>Clean glass. <span class="hl">Clear results.</span></h2>{shot("glassmaster.webp")}<span class="tag">Website in English · Quotes by SMS or WhatsApp</span>')]

# 6 — Mitos
mitos = [("“Site é caro de manter”", "Na PineWeb não tem mensalidade. Você paga só a renovação anual do domínio."),
         ("“Demora meses”", "Site simples fica pronto em 7 dias depois que chega o material."),
         ("“Preciso entender de tecnologia”", "Você manda fotos e textos. A gente cuida do resto.")]
s = [render("06-1", "dark", '<div class="center"><div class="eyebrow">Mitos</div><h1>3 mitos que <span class="hl">travam</span> seu site</h1></div>', "1/5", True)]
for i, (t, d) in enumerate(mitos, start=2):
    s.append(render(f"06-{i}", "light", f'<div class="center"><span class="tag" style="margin:0 0 40px;align-self:flex-start">Mito {i-1}</span><h2>{t}</h2><p><b style="color:#2E7D5B">Verdade:</b> {d}</p></div>', f"{i}/5"))
s.append(render("06-5", "amber", '<div class="center"><h1>Sem desculpa: bora tirar seu site do papel?</h1><div><span class="cta">Link na bio →</span></div></div>', "5/5"))
posts["06"] = s

json.dump(posts, open("/home/claude/social-build/arquivos.json", "w"), indent=1)
print({k: len(v) for k, v in posts.items()})
