"""Gera as artes dos posts 07 a 09 reaproveitando o estilo de gerar.py.
Uso: python3 gerar_07-09.py <caminho-do-repo>"""
import pathlib, sys

src = (pathlib.Path(__file__).parent / "gerar.py").read_text()
exec(src.split("posts = {}")[0])  # CSS, render() e shot() de gerar.py
TMP.mkdir(parents=True, exist_ok=True)

# 7 — Dica: checklist do site de pequeno negócio
itens = [("Botão de WhatsApp à vista", "Cliente com pressa não procura contato. Ele chama na hora."),
         ("Endereço e horário", "E o perfil no Google Maps configurado, pra quem procura achar você."),
         ("Fotos reais do seu negócio", "Seu espaço, sua equipe, seus produtos. Passa confiança."),
         ("Rápido no celular", "A maioria dos clientes abre pelo celular. Se demora, ele fecha."),
         ("Cadeado do HTTPS", "Site seguro, sem aviso de “não seguro” no navegador.")]
cards = "".join(f'<div class="card" style="padding:24px 34px;font-size:34px"><div class="num">✓</div><div><b>{t}</b><br>{d}</div></div>' for t, d in itens)
s = [render("07-1", "dark", '<div class="center"><div class="eyebrow">Checklist</div><h1>5 coisas que o site do seu negócio <span class="hl">precisa ter</span></h1><p>Confere se o seu tem todas.</p></div>', "1/3", True),
     render("07-2", "light", f'<div class="eyebrow">Salve pra conferir</div><div class="row" style="margin-top:0;gap:20px">{cards}</div>', "2/3"),
     render("07-3", "amber", '<div class="center"><h1>Faltou algum? A gente resolve.</h1><p style="color:#163A2C">Todo site da PineWeb sai com HTTPS, pensado pro celular e pronto pro Google.</p><div><span class="cta">Link na bio →</span></div></div>', "3/3")]

# 8 — Perguntas frequentes (do index.html)
faq = [("Quanto tempo leva?", "Site simples: <b>7 dias</b>. Com sistema: <b>15 dias</b>. O prazo conta a partir de quando chegam fotos e textos, e vem escrito no orçamento."),
       ("O domínio fica no meu nome?", "<b>Sim.</b> O endereço do site, tipo seunegocio.com.br, é registrado no seu nome."),
       ("Tem mensalidade?", "<b>Não.</b> A hospedagem é por nossa conta. Você paga só a renovação anual do domínio."),
       ("Atendem fora do Brasil?", "<b>Sim.</b> Brasil e Estados Unidos, em português ou inglês.")]
s8 = [render("08-1", "dark", '<div class="center"><div class="eyebrow">Perguntas frequentes</div><h1>O que todo mundo <span class="hl">pergunta</span> antes de fazer o site</h1></div>', "1/6", True)]
for i, (q, a) in enumerate(faq, start=2):
    s8.append(render(f"08-{i}", "light", f'<div class="center"><span class="tag" style="margin:0 0 40px;align-self:flex-start">Pergunta {i-1}</span><h2>{q}</h2><p>{a}</p></div>', f"{i}/6"))
s8.append(render("08-6", "amber", '<div class="center"><h1>Ficou alguma dúvida? Pergunta pra gente.</h1><p style="color:#163A2C">Orçamento por escrito em até 24 horas.</p><div><span class="cta">Link na bio →</span></div></div>', "6/6"))

# 9 — Case Nora Pinho Estética (imagem única)
s9 = [render("09-1", "dark", f'<div class="eyebrow">Case · Depilação a laser</div><h2>Escolha as áreas <span class="hl">no mapa do corpo.</span></h2>{shot("nora-pinho.webp")}<span class="tag">Agendamento direto no WhatsApp</span>')]

print(s + s8 + s9)
