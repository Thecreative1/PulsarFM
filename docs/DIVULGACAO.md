# Divulgação — textos prontos

Rascunhos para publicar à mão (11/10/2026). Uma comunidade de cada vez, com
alguns dias entre posts, e as regras de cada uma lidas antes. Responde aos
comentários nas primeiras 2–3 horas: é isso que mantém um post vivo.

Links com `?ref=` não são precisos: o GA4 já mostra a origem (hn, reddit…).

---

## 1. Show HN (Hacker News)

Publicar em news.ycombinator.com/submit, terça a quinta, ~15–16h (PT).

**Title** (máx. 80 caracteres):

```
Show HN: PulsarFM – 64 live radio stations in Winamp with a Milkdrop visualizer
```

**URL:** `https://pulsarfm.eu/?lang=en`

**Primeiro comentário** (publicar logo a seguir, no próprio post):

```
PulsarFM is a web radio built around Webamp (the Winamp 2 clone in JS) and
Butterchurn (the WebGL port of Milkdrop). 64 live stations in 8 genres:
rock, jazz, chill, pop, study, electronic, psytrance and synthwave.

Some details that might interest people here:

- It's a single static HTML file on GitHub Pages. No backend, no account,
  no build step.
- The visualizer reacts to the actual stream, which means every station has
  to send CORS headers. Many don't, and some only fail on a redirect hop, so
  every stream is checked in a real browser before it goes in.
- 20 classic .wsz skins from the Winamp Skin Museum, a fullscreen "trip"
  mode, a sleep timer, favourites, and a dock/float toggle if you want to
  drag the windows around like it's 1999.
- Works on phones, although Milkdrop on a phone is more of a party trick.

Webamp was the hard part: it renders straight into <body> and ignores some
of its own layout options, so the windows are placed by dispatching on its
internal store after render. Happy to go into the details.

Feedback welcome, especially stations I should add.
```

---

## 2. Reddit — r/winamp

**Title:**

```
I put Webamp + Milkdrop on top of 64 live radio stations — with 20 skins from the Skin Museum
```

**Body:**

```
PulsarFM: https://pulsarfm.eu/?lang=en

It's Webamp (the browser Winamp 2) with Butterchurn running the Milkdrop
presets, playing live internet radio. 8 genres, 8 stations each.

The SKINS button loads 20 classic .wsz skins from the Winamp Skin Museum,
and your choice is remembered. TRIP puts Milkdrop in fullscreen.

No account, no install. If there's a skin you think belongs in the list,
tell me which one.
```

---

## 3. Reddit — r/synthwave (ou r/outrun)

Ler as regras antes: algumas semanas só aceitam self-promo em threads
próprias. Se for o caso, usar o texto na thread semanal.

**Title:**

```
Synthwave radio with a Winamp player and Milkdrop visuals, free in the browser
```

**Body:**

```
https://pulsarfm.eu/en/synthwave-radio/

Eight live synthwave and retrowave stations in one place: Nightride FM,
Nightride Darksynth, ChillSynth FM, SomaFM Underground 80s, laut.fm
Synthwave and more, playing through Webamp with a Milkdrop visualizer.

Hit TRIP for fullscreen visuals. Pick a skin, turn the lights off.

Which stations am I missing?
```

---

## 4. Reddit — r/InternetIsBeautiful

Regra da comunidade: o título descreve o site, sem "I made" nem hype.

**Title:**

```
A web radio that looks and works like Winamp, with Milkdrop visuals and 64 live stations
```

**URL:** `https://pulsarfm.eu/?lang=en`

(Post de link, sem texto. Se pedirem detalhes, usar o comentário do Show HN.)

---

## 5. Reddit — r/webdev (só ao sábado, "Showoff Saturday")

**Title:**

```
[Showoff Saturday] Winamp-style web radio: Webamp + Butterchurn, one static HTML file on GitHub Pages
```

**Body:**

```
https://pulsarfm.eu/?lang=en

A single index.html, no framework, no backend. Things that were trickier
than expected:

- Webamp ignores the node you pass and mounts on <body>, so the "dock"
  panel is a separate fixed element and the windows are laid out after
  render by dispatching to Webamp's store.
- Webamp's window wrappers use inline transforms, which break
  position: fixed for the fullscreen visualizer. The fix is
  transform: none on the ancestor chain while in fullscreen.
- Milkdrop needs CORS on the audio stream, and a single redirect hop
  without CORS kills the whole chain. Every station is checked in a real
  browser.

Happy to answer questions about any of it.
```

---

## 6. Webamp (GitHub Discussions do projeto)

Em github.com/captbaritone/webamp → Discussions → "Show and tell" (se não
existir, procurar onde o projeto mostra sites feitos com Webamp).

**Title:**

```
PulsarFM: live radio player built on Webamp + Butterchurn
```

**Body:**

```
Hi! Thanks for Webamp, it made this possible.

PulsarFM (https://pulsarfm.eu/?lang=en) uses Webamp 2.3.1 with Butterchurn
to play 64 live internet radio stations, with 20 skins from the Skin Museum
and a fullscreen Milkdrop mode.

A couple of things I worked around, in case they're useful to others:
- windowLayout is ignored for the Milkdrop window, so I lay out the windows
  after render with UPDATE_WINDOW_POSITIONS / WINDOW_SIZE_CHANGED on the store.
- A position: fixed fullscreen canvas needs the inline transforms on the
  window wrappers neutralised.

If you keep a list of projects built with Webamp, I'd be glad to be on it.
```

---

## 7. Email — imprensa tech portuguesa

Para: Pplware, 4gnews, Shifter (procurar o email de "dicas"/"contacto" ou
"enviar notícia" em cada site). Personalizar a primeira linha para cada um.

**Assunto:**

```
Site português põe o Winamp a tocar 64 rádios em direto, no browser
```

**Corpo:**

```
Olá,

Chamo-me Flávio e criei o PulsarFM (https://pulsarfm.eu), uma rádio online
que recupera o visual do Winamp e o visualizador Milkdrop, agora a correr
no browser.

Em poucas linhas:
- 64 rádios em direto, em 8 géneros: rock, jazz, chill, pop, estudo,
  eletrónica, psytrance e synthwave. Inclui portuguesas como a M80, a RFM,
  a Rádio Comercial e a Cidade FM.
- 20 skins clássicas do Winamp, modo de ecrã inteiro com os visuais
  Milkdrop e temporizador para adormecer.
- Gratuito, sem conta, sem instalar nada. Funciona no computador e no
  telemóvel.
- É um projeto independente, feito em Portugal, em português e em inglês.

Quem usou o Winamp nos anos 90 percebe tudo ao primeiro clique. Quem não
usou, fica pelo menos com um visualizador melhor do que o do Spotify.

Se fizer sentido para o vosso público, tenho todo o gosto em responder a
perguntas ou enviar imagens.

Obrigado,
Flávio Martins
PulsarFM — https://pulsarfm.eu
```

---

## 8. Diretórios (formulário, não precisam de texto longo)

Descrição curta, para colar onde pedirem (AlternativeTo, Uneed, Product Hunt):

```
Free web radio with a Winamp player and Milkdrop visualizer. 64 live
stations in 8 genres, 20 classic skins, no account or install.
```

AlternativeTo: listar como alternativa a TuneIn, Radio Garden, myTuner e
Winamp. Tags: radio, internet-radio, winamp, music-visualizer, retro.
