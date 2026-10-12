# Revisão linguística ES-ES — 12/10/2026

Revisão cirúrgica das 39 páginas espanholas: homepage, privacidade, oito géneros, hub, 13 categorias e 15 guias. Foram revistos também os textos de 73 produtos. Há 58 alterações editoriais nas fontes; 36 páginas HTML tiveram diferenças após regeneração. As três páginas já corretas foram mantidas.

## Principais correções

| Antes | Depois |
|---|---|
| 8 géneros. | 8 géneros musicales. |
| 🎧 EQUIPO | 🎧 GUÍAS |
| ⚡ AZAR | ⚡ AL AZAR |
| 🔓 LIBRE | 🔓 FLOTANTE |
| Logótipo Pulsar FM | Logotipo Pulsar FM |
| Frisky Radio EUA | Frisky Radio (EE. UU.) — apenas apresentação ES |
| Escuchar en el player | Escuchar en el reproductor |
| La disponibilidad de cada stream depende de la estación. | La disponibilidad de cada emisión depende de la emisora. |
| Gear / Tecnología | Equipo y tecnología |
| Auriculares y Cascos | Auriculares y cascos |
| Un ordenador puede sonar fuera de su carcasa sin convertirse en un cine. | No necesitas montar un cine en casa para mejorar el sonido de tu ordenador. |
| Esta selección distingue oído abierto, puntas intraaurales y conducción ósea. | En esta selección encontrarás auriculares de diseño abierto, modelos intraaurales y opciones de conducción ósea. |
| Esta selección mantiene cinco caminos, desde la escucha casual hasta los viajes y la grabación con cable. Empieza por dónde, cuánto tiempo y conectados a qué. | Hemos seleccionado cinco modelos para diferentes formas de escuchar música: desde el uso diario hasta los viajes y la grabación con cable. Antes de elegir, piensa dónde los utilizarás, durante cuánto tiempo y a qué dispositivos los conectarás. |

O parágrafo inicial de SEO passou a: «Pulsar FM reúne emisoras seleccionadas a mano de todo el mundo. Escucha radio en directo con un reproductor inspirado en 1999 y disfruta de las visualizaciones de MilkDrop que reaccionan al ritmo de la música.» A continuação correta foi mantida. O slogan, TRIP, SKINS, nomes comerciais e termos técnicos foram preservados. Não foram acrescentadas alegações de testes ou experiência pessoal.

O registo completo de frases antes/depois está em [linguistic-changes.json](qa-es/linguistic-changes.json).

## Ficheiros de implementação

- data/radio.es.json — dicionário e controlos espanhóis.
- data/genres.es.json — instruções e FAQ dos oito géneros.
- data/recommendations.es.json — categorias, guias e descrições editoriais de produtos.
- tools/gen_spain.py e tools/gen_genre_pages.py — apresentação estática ES.
- assets/radio-locales.js — dicionário gerado.
- assets/radio-i18n.js — alt do logótipo e indicação geográfica apenas na apresentação ES, sem modificar a identidade/URL da estação.
- assets/radio-es.css — ajuste necessário de tipografia do botão FLOTANTE abaixo de 560 px; a ficha permite CSS quando necessário. O seletor só se aplica a es-ES, inclusive ao mudar manualmente de idioma. Sem redesign nem alteração do CSS PT/EN.
- tools/smoke_live.cjs — smoke test inclui o novo CSS ES.
- tools/check-spanish-copy.cjs — QA integrada de texto, apresentação e preservação de identidade.

HTML espanhol regenerado com diferenças:

- es/index.html
- es/privacidad/index.html
- es/radio-chill/index.html
- es/radio-electronica/index.html
- es/radio-jazz/index.html
- es/radio-para-estudiar/index.html
- es/radio-pop/index.html
- es/radio-psytrance/index.html
- es/radio-rock/index.html
- es/radio-synthwave/index.html
- es/recomendaciones/accesorios-audio/index.html
- es/recomendaciones/altavoces-bluetooth-casa/index.html
- es/recomendaciones/altavoces-para-pc/index.html
- es/recomendaciones/amplificador-para-tocadiscos/index.html
- es/recomendaciones/auriculares-bluetooth-calidad-precio/index.html
- es/recomendaciones/auriculares-cancelacion-ruido-trabajar/index.html
- es/recomendaciones/auriculares-diadema/index.html
- es/recomendaciones/barras-de-sonido/index.html
- es/recomendaciones/categorias/accesorios-audio/index.html
- es/recomendaciones/categorias/altavoces-bluetooth/index.html
- es/recomendaciones/categorias/altavoces-pc/index.html
- es/recomendaciones/categorias/amplificacion/index.html
- es/recomendaciones/categorias/auriculares-cascos/index.html
- es/recomendaciones/categorias/barras-sonido/index.html
- es/recomendaciones/categorias/equipos-hi-fi/index.html
- es/recomendaciones/categorias/home-studio/index.html
- es/recomendaciones/categorias/microfonos/index.html
- es/recomendaciones/categorias/para-ninos/index.html
- es/recomendaciones/categorias/para-tv/index.html
- es/recomendaciones/categorias/regalos/index.html
- es/recomendaciones/categorias/tocadiscos/index.html
- es/recomendaciones/equipos-hi-fi-empezar/index.html
- es/recomendaciones/home-studio-economico/index.html
- es/recomendaciones/index.html
- es/recomendaciones/microfonos-usb-podcast-streaming/index.html
- es/recomendaciones/regalos-para-amantes-musica/index.html

Evidências atualizadas: browser-results.json, language-navigation.json, imagens do navegador em docs/qa-es, linguistic-browser.json, linguistic-invariants.json, linguistic-check-results.json e linguistic-changes.json e linguistic-files.json. A lista integral de ficheiros consta de [linguistic-files.json](qa-es/linguistic-files.json).

## Validação

- python -X utf8 tools/build_site.py: passou.
- python -X utf8 tools/check_site.py: 71 páginas indexáveis, 39 ES e 1936 links internos; passou.
- python -X utf8 -m pytest -q tests: 38 testes e 1135 subtestes passaram.
- node tools/check-js.cjs: 37 scripts passaram.
- node --test tests/affiliate-analytics.test.cjs: oito testes passaram.
- tools/browser-check.cjs: reprodução real do stream Radio Paradise decodificada com tempo avançando, Webamp preservado na mudança de idioma, 13 guias navegados em desktop/mobile, consentimento aceite/revogado e conteúdo sem JavaScript; passou.
- tools/check-language-navigation.cjs: 42 cenários passaram, incluindo ES→EN→ES, preferências manuais, falhas/timeout de geolocalização e armazenamento bloqueado. Respostas de país simuladas; a leitura CORS do serviço aprovado também passou.
- tools/check-spanish-copy.cjs: 39 páginas acessíveis e sem overflow a 320 px; controlos sem colisões a 1440/390/360/320 px; AL AZAR mantém a seleção no catálogo original; Webamp e canvas MilkDrop presentes; nenhuma exceção JavaScript nova.

## Preservação confirmada

Comparação com a versão publicada 88abe58: os 32 ficheiros HTML PT/EN são byte a byte iguais. O index.html original, dicionários de controlos PT/EN, catálogo e guias portugueses, analytics, Consent Mode, chaves/lógica de preferências, geolocalização e navegação não tiveram alterações funcionais.

Os 221 links de afiliado das páginas ES mantêm exatamente os mesmos URLs, tracking IDs e atributos, incluindo os parâmetros de eventos. A declaração obrigatória de afiliado Amazon permanece igual. Todos os destinos de links internos, canonicals, hreflang e hierarquia H1/H2/H3 permanecem iguais. Sitemap e robots.txt não têm diferenças. As estruturas, tipos e URLs Schema.org foram preservados; 27 campos textuais de FAQ/nome de categoria acompanharam as correções linguísticas visíveis. Nomes crus, IDs e ordem das 64 emisoras, URLs de streams e identificadores de produtos foram preservados.

## Limites e validação manual

A QA mobile usa Chrome com emulação de viewport, sem ensaio físico em Safari/iOS ou Android. Uma verificação nesses dispositivos continua recomendada. O modo flutuante anterior permite que janelas Webamp sobreponham o botão de retorno nas larguras 390/360/320 px; o teste reproduziu a mesma sobreposição em PT e ES. A lógica/layout desse modo permanece intacta nesta revisão de texto. A reprodução real foi amostrada em Radio Paradise; não se afirma disponibilidade de todos os streams ou teste dos produtos.

## Publicação

Após o commit/push, o smoke test em produção verifica as 71 páginas do sitemap, os recursos essenciais, áudio, navegação, consentimento e conteúdo publicado. As evidências do resultado final ficam em docs/qa-es/live.
