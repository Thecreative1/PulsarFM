# -*- coding: utf-8 -*-
import os, json

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GENRES = {
 "radios-rock": {
  "genre":"rock","emoji":"\U0001F3B8","nome":"Rock / Alternativo",
  "title":"Rádios Rock Online Grátis — Ouvir ao Vivo | Pulsar FM",
  "desc":"Ouve rádios rock e alternativo ao vivo, grátis e sem instalar nada. Radio Paradise, Rock Antenne, KEXP e mais — em direto, com visualizador retro estilo Winamp.",
  "h1":"Rádios Rock Online",
  "intro":"Do rock clássico ao alternativo de agora: oito estações escolhidas a dedo, todas em direto. Carrega no play, sobe o volume e deixa o Milkdrop tratar da parte visual.",
  "stations":[
   ("Radio Paradise - Rock Mix","Rock eclético escolhido por pessoas, não por um algoritmo. Direto da Califórnia."),
   ("Rock Antenne","A grande rádio rock alemã. Do clássico ao moderno, sem pausas."),
   ("KEXP Seattle","A lendária rádio independente de Seattle. Se uma banda nova vale a pena, há boas hipóteses de passar aqui primeiro."),
   ("Virgin Radio Italy","Rock clássico e moderno, com sotaque italiano."),
   ("M80 Rádio","Os clássicos que marcaram gerações, direto de Portugal. Como a cassete do carro, mas sem a fita enrolar."),
   ("Radio BOB!","Rock alemão sem parar, do classic rock ao metal. Não é sítio para pedir baladas."),
   ("FM4","A rádio alternativa da pública austríaca ORF: indie, eletrónica e muito do que ainda não chegou às playlists. Fala sobretudo em inglês."),
   ("Radio X UK","Rock e indie britânico, direto de Londres. Muito Oasis, muito Arctic Monkeys e nenhuma vergonha disso.")],
  "faq":[
   ("Como ouvir rádio rock online grátis?","Abre o Pulsar FM no navegador, escolhe uma estação rock e carrega em play. É em direto (ao vivo), grátis e não precisas de instalar nada. Nem de criar conta."),
   ("Qual é a melhor rádio rock online?","Depende do que procuras. A Radio Paradise tem curadoria humana e eclética, a Rock Antenne é rock alemão sem pausas e a KEXP Seattle é a referência do rock independente. Se não sabes por onde começar, começa pela KEXP."),
   ("Posso ouvir rádio rock no telemóvel ou no celular?","Sim, em qualquer navegador moderno, no computador, no telemóvel ou no celular. Se não sabes qual escolher, carrega em SCAN e o Pulsar FM escolhe uma estação por ti.")]},
 "radios-jazz": {
  "genre":"jazz","emoji":"\U0001F3B7","nome":"Jazz",
  "title":"Rádios Jazz Online Grátis — Ao Vivo de Paris e do Mundo | Pulsar FM",
  "desc":"Ouve rádios jazz ao vivo e grátis: TSF Jazz de Paris, FIP Jazz e Radio Swiss Jazz. Em direto no browser, com visualizador retro estilo Winamp.",
  "h1":"Rádios Jazz Online",
  "intro":"De Paris à Suíça, jazz 24 horas por dia, em direto. Serve para jantar, para trabalhar ou para fingir que se percebe de contrabaixo.",
  "stations":[
   ("TSF Jazz","A rádio de referência do jazz em Paris, a emitir 24 horas por dia."),
   ("Smooth Jazz","Smooth jazz a 320 kbps, para relaxar. Na era do 56k, um MP3 nesta qualidade levava quase uma hora a descarregar."),
   ("Radio Swiss Jazz","Jazz selecionado e sem publicidade, da rádio pública suíça."),
   ("Jazz Radio France","A grande rede francesa de jazz, do swing ao soul."),
   ("SomaFM Sonic Universe","Jazz de vanguarda e sons experimentais, para quando os standards já não chegam."),
   ("FIP Jazz","O jazz eclético da rádio pública francesa, sem publicidade."),
   ("WWOZ New Orleans","A rádio comunitária de Nova Orleães: jazz, blues e funk, da cidade onde o jazz nasceu."),
   ("KCSM Jazz 91","Jazz 24 horas por dia, da Bay Area de São Francisco.")],
  "faq":[
   ("Qual é a melhor rádio de jazz de Paris?","A TSF Jazz é a rádio de referência do jazz em Paris, a emitir 24 horas por dia. No Pulsar FM também tens a Jazz Radio France, do swing ao soul, e a FIP Jazz, mais eclética."),
   ("Como ouvir rádio jazz online grátis?","Abre o Pulsar FM no navegador, escolhe uma estação de jazz e carrega em play. Em direto (ao vivo), grátis e sem registos."),
   ("Posso ouvir jazz no telemóvel ou no celular?","Sim, em qualquer navegador, no computador ou no celular. Carrega na estrela da TSF Jazz e ela fica guardada nos teus favoritos para a próxima vez.")]},
 "radios-chill": {
  "genre":"chill","emoji":"\U0001F33F","nome":"Chill / Ambiente",
  "title":"Rádios Chill e Ambient Online Grátis — Ao Vivo | Pulsar FM",
  "desc":"Rádios chill e ambient ao vivo: SomaFM Drone Zone, Nightwave Plaza e Ibiza Global Radio. Grátis, em direto, no browser, com visuais psicadélicos.",
  "h1":"Rádios Chill Online",
  "intro":"Ambient, drones espaciais e vaporwave: oito estações para desligar do mundo. Fecha os olhos, ou deixa o visualizador fazer o trabalho por ti.",
  "stations":[
   ("SomaFM Drone Zone","Ambient e drones espaciais, sem batida nem pressa."),
   ("Chillout-style Jazz","Chill com comunicações espaciais da NASA à mistura. Houston, está tudo calmo."),
   ("Nightwave Plaza","Vaporwave e estética retro: a internet dos anos 90 em forma de som, sem os pop-ups."),
   ("SomaFM Lush","Vozes suaves sobre eletrónica de sonho."),
   ("Ibiza Global Radio","Balearic chill e house, direto de Ibiza, a qualquer hora do dia."),
   ("Ambient Sleeping Pill","Ambient puro para dormir ou flutuar, sem interrupções."),
   ("Radio Paradise Mellow Mix","O lado calmo da Radio Paradise: canções suaves escolhidas por pessoas, sem pressa de acabar o dia."),
   ("Radio Paradise Serenity","Ambient e sons da natureza, sem voz nem batida.")],
  "faq":[
   ("Que tipo de música tocam as rádios chill?","Ambient, drones espaciais, vaporwave, downtempo e balearic. Música para relaxar, dormir ou trabalhar sem nada a puxar pela tua atenção."),
   ("Como ouvir rádio chill online grátis?","Abre o Pulsar FM, escolhe uma estação chill e carrega em play. Em direto (ao vivo), grátis e sem instalar nada."),
   ("Posso ouvir música chill no telemóvel ou no celular?","Sim, em qualquer navegador, no telemóvel ou no celular. Para adormecer com ambient, o botão SLEEP pausa a rádio ao fim de 15, 30 ou 60 minutos.")]},
 "radios-pop": {
  "genre":"pop","emoji":"\U0001F3B6","nome":"Pop",
  "title":"Rádios Pop Online Grátis — Hits ao Vivo | Pulsar FM",
  "desc":"Ouve os hits do momento ao vivo: RFM, Rádio Comercial, Capital FM de Londres e NRJ. Em direto, grátis e sem instalar nada.",
  "h1":"Rádios Pop Online",
  "intro":"Os hits do momento, de Portugal a Londres, Paris e à Baviera. Oito estações pop em direto, para quando o dia pede refrões.",
  "stations":[
   ("RFM Pop Rock","Os êxitos pop rock de Portugal, pela RFM."),
   ("Rádio Comercial","A rádio mais ouvida de Portugal: hits e boa disposição."),
   ("Capital FM UK","Os hits do momento, direto de Londres."),
   ("NRJ France","Hit music only, como diz o slogan. Os êxitos, direto de França."),
   ("I Love Radio DE","Charts e hits para a geração do streaming, da Alemanha."),
   ("Antenne Bayern","Os grandes hits da maior rádio privada da Baviera."),
   ("Cidade FM","Os hits do momento para um público mais novo, direto de Portugal."),
   ("Heart UK","Os êxitos pop que se cantam no carro, direto do Reino Unido.")],
  "faq":[
   ("Que rádios pop portuguesas posso ouvir?","A RFM e a Rádio Comercial, as mais ouvidas de Portugal, em direto, lado a lado com a Capital FM de Londres e a NRJ de França."),
   ("Como ouvir rádio pop online grátis?","Abre o Pulsar FM no navegador, escolhe uma estação pop e carrega em play. Emissão ao vivo, grátis e sem instalar nada."),
   ("Posso ouvir os hits no telemóvel ou no celular?","Sim, em qualquer navegador moderno, no computador ou no celular. Se ouvires um refrão que um amigo tem de ouvir, o botão SHARE envia-lhe a estação que está a tocar.")]},
 "radios-study": {
  "genre":"study","emoji":"\U0001F4BB","nome":"Study / Lo-Fi",
  "title":"Rádios para Estudar — Lo-Fi e Clássica ao Vivo | Pulsar FM",
  "desc":"Música para estudar e trabalhar: SomaFM Groove Salad, clássica sem interrupções e chillhop lo-fi. Grátis, ao vivo, no browser.",
  "h1":"Rádios para Estudar",
  "intro":"Lo-fi, downtempo e clássica: oito estações escolhidas para sessões longas de estudo ou trabalho a sério. Pouca letra, pouca conversa e nenhuma desculpa para não começar.",
  "stations":[
   ("SomaFM Groove Salad","Downtempo e chill para manter o foco horas a fio. Uma instituição da rádio online."),
   ("Radio Swiss Classic","Música clássica sem interrupções nem publicidade."),
   ("I Love Chillhop","Lo-fi e chillhop, o clássico do estudo, em versão rádio."),
   ("SomaFM Deep Space One","Ambient espacial profundo, para quando o foco tem de ir longe."),
   ("Venice Classic Radio","Clássica intemporal, de Itália com amor."),
   ("Lofi Radio","Lo-fi beats 24 horas por dia, num loop que não pede atenção."),
   ("Classic FM UK","A rádio de clássica mais ouvida do Reino Unido: peças conhecidas, sem pretensões."),
   ("France Musique","A clássica da rádio pública francesa, com concertos e gravações de referência.")],
  "faq":[
   ("Qual é a melhor música para estudar?","Lo-fi, chillhop, downtempo e clássica: música sem letra, que não compete com o que estás a ler. As oito estações desta página foram escolhidas exatamente para isso."),
   ("Como ouvir rádio lo-fi online grátis?","Abre o Pulsar FM no navegador, escolhe a I Love Chillhop ou a SomaFM Groove Salad e carrega em play. Grátis e sem distrações."),
   ("Posso estudar com o Pulsar FM no telemóvel ou no celular?","Sim, em qualquer navegador, no telemóvel ou no celular. Adiciona o Pulsar FM ao ecrã principal e passa a abrir como uma app, sem passar pela loja de aplicações.")]},
 "radios-electronica": {
  "genre":"electro","emoji":"⚡","nome":"Eletrónica / Dance",
  "title":"Rádio de Música Eletrónica Online Grátis — Ao Vivo | Pulsar FM",
  "desc":"Rádios de música eletrónica e dance ao vivo: TechnoBase.FM, Radio FG de Paris e HouseTime.FM. Techno, house e progressive em direto, grátis no browser.",
  "h1":"Rádios de Música Eletrónica Online",
  "intro":"Techno, house e progressive em direto, 24 horas por dia. Sobe o volume, liga o Milkdrop e o quarto passa a pista. Os vizinhos que se adaptem.",
  "stations":[
   ("TechnoBase.FM DE","Techno e hands up direto da Alemanha, com uma comunidade enorme."),
   ("HouseTime.FM","House 24 horas por dia, da mesma família do TechnoBase."),
   ("Frisky Radio EUA","Deep house e progressive com DJs residentes, direto dos EUA."),
   ("Sunshine Live","A maior rádio de eletrónica da Alemanha: sets, festivais e pouca conversa."),
   ("Hirschmilch Electronic","Eletrónica alemã sem interrupções."),
   ("Radio FG Paris","House e electro direto de Paris: a rádio dos clubes."),
   ("TranceBase.FM","Trance e uplifting da família TechnoBase, para quando o techno pede melodia."),
   ("1.FM Deep House","Deep house sem parar, da rede 1.FM. Para aquecer antes de sair, ou para não sair de todo.")],
  "faq":[
   ("Como ouvir música eletrónica online grátis?","Abre o Pulsar FM no navegador, escolhe uma estação e carrega em play. Techno, house e progressive em direto (ao vivo), 100% grátis."),
   ("Que estilos de eletrónica posso ouvir?","Techno e hands up na TechnoBase.FM, house 24 horas na HouseTime.FM, deep e progressive na Frisky Radio e sets de festivais na Sunshine Live."),
   ("Posso ouvir rádio eletrônica no celular?","Sim, em qualquer navegador, no computador ou no celular (telemóvel). Da próxima vez que abrires o Pulsar FM, o botão Continuar a ouvir leva-te de volta à última estação.")]},
 "radios-psytrance": {
  "genre":"psy","emoji":"\U0001F500","nome":"Goa / Psytrance",
  "title":"Rádio Psytrance e Goa Trance Online — Ao Vivo Grátis | Pulsar FM",
  "desc":"Psytrance e goa trance ao vivo: Goa-Base, Hirschmilch Psy e BOM Psytrance. Em direto, grátis, no browser, com visuais psicadélicos Milkdrop.",
  "h1":"Rádios Psytrance Online",
  "intro":"Goa old school e psytrance moderno, em direto. Combina com o modo TRIP do Pulsar FM, o visualizador em ecrã inteiro. Quem já viu o sol nascer numa pista percebe a ideia.",
  "stations":[
   ("Goa-Base Trance","Goa trance old school, direto da Alemanha. Melodias orientais e 303 a borbulhar."),
   ("Hirschmilch Psy","Psytrance em alta qualidade, sem interrupções."),
   ("BOM Psytrance","Psytrance sem parar, da rede 1.FM."),
   ("Psyndora Psytrance","Psytrance e progressive da cena grega."),
   ("Hirschmilch Progressive","Progressive psy hipnótico, horas a fio."),
   ("Hirschmilch Chillout","Psychill e ambient goa, para aterrar depois da viagem."),
   ("Radio Ozora","A rádio do Ozora, o festival psicadélico húngaro: psytrance e goa como se ouve no vale."),
   ("Goanight","Goa e psytrance noturno, da comunidade laut.fm.")],
  "faq":[
   ("Qual é a diferença entre goa trance e psytrance?","O goa trance é o som original dos anos 90: melódico, oriental e hipnótico. O psytrance é a evolução moderna, mais rápida e mais pesada. Na Goa-Base ouves o clássico; na Hirschmilch Psy, o som de agora."),
   ("Como ouvir psytrance online grátis?","Abre o Pulsar FM, escolhe uma estação psy e carrega em play. Em direto (ao vivo), grátis e sem instalar nada. Ativa o modo TRIP para o visualizador em ecrã inteiro."),
   ("Posso ouvir goa trance no telemóvel ou no celular?","Sim, em qualquer navegador moderno, no computador ou no celular. De preferência com auscultadores: o psytrance perde metade dos graves no altifalante do telemóvel.")]},
 "radios-synthwave": {
  "genre":"synthwave","emoji":"\U0001F306","nome":"Synthwave / Retrowave",
  "title":"Rádios Synthwave e Retrowave Online Grátis — Ao Vivo | Pulsar FM",
  "desc":"Synthwave e retrowave ao vivo: Nightride FM, ChillSynth FM e SomaFM Underground 80s. Neon, nostalgia e visualizador Winamp, em direto no browser.",
  "h1":"Rádios Synthwave Online",
  "intro":"Neon, sintetizadores e a nostalgia de uns anos 80 que nunca foram bem assim. É o género que define a vibe do Pulsar FM, em oito estações.",
  "stations":[
   ("Nightride FM","Synthwave e retrowave para conduzir à noite (mesmo sem carro)."),
   ("ChillSynth FM","Chillsynth suave: neon em modo calmo."),
   ("SomaFM Digitalis","Eletrónica indie com alma digital."),
   ("Nightride Datawave","Datawave: sintetizadores para navegar a noite digital."),
   ("SomaFM Underground 80s","Synthpop e new wave underground dos anos 80. Os lados B que a rádio da altura deixava de fora."),
   ("SomaFM Synphaera","Space synth e eletrónica atmosférica."),
   ("Nightride Darksynth","Darksynth: o synthwave em modo pesadelo. Mais distorção, menos pôr do sol."),
   ("laut.fm Synthwave","Synthwave e retrowave sem parar, da comunidade laut.fm.")],
  "faq":[
   ("O que é synthwave?","Um género eletrónico inspirado nas bandas sonoras e nos sintetizadores dos anos 80: neon, nostalgia e noites que não acabam. Para começar: Kavinsky, The Midnight e Perturbator."),
   ("Como ouvir synthwave online grátis?","Abre o Pulsar FM no navegador, escolhe a Nightride FM ou a ChillSynth FM e carrega em play. Em direto (ao vivo) e grátis."),
   ("Posso ouvir retrowave no telemóvel ou no celular?","Sim, em qualquer navegador, no computador ou no celular. No computador, abre também o SKINS: há skins clássicas do Winamp para o player combinar com o neon.")]},
}

# English versions (/en/<slug>/), keyed by the PT page. Station names stay the same as in the
# player; descriptions, FAQs and SEO copy are written for English searches (docs/VOZ.md applies).
GENRES_EN = {
 "radios-rock": {
  "slug":"rock-radio","nome":"Rock / Alternative",
  "title":"Rock Radio Online — Listen Live for Free | Pulsar FM",
  "desc":"Listen to rock and alternative radio live and free, nothing to install. Radio Paradise, Rock Antenne, KEXP and more, with a retro Winamp-style visualizer.",
  "h1":"Rock Radio Online",
  "intro":"From classic rock to today's alternative: eight hand-picked stations, all live. Hit play, turn it up and let Milkdrop handle the visuals.",
  "stations":[
   ("Radio Paradise - Rock Mix","Eclectic rock picked by humans, not by an algorithm. Live from California."),
   ("Rock Antenne","Germany's big rock station. Classic to modern, no breaks."),
   ("KEXP Seattle","Seattle's legendary independent station. If a new band is worth hearing, there's a good chance it played here first."),
   ("Virgin Radio Italy","Classic and modern rock with an Italian accent."),
   ("M80 Rádio","The classics that defined generations, live from Portugal. Like the car tape deck, minus the chewed-up tape."),
   ("Radio BOB!","Non-stop German rock, from classic rock to metal. Not the place to request ballads."),
   ("FM4","The alternative station of Austrian public broadcaster ORF: indie, electronica and plenty that hasn't reached the playlists yet. Mostly in English."),
   ("Radio X UK","British rock and indie, live from London. Plenty of Oasis, plenty of Arctic Monkeys and no shame about it.")],
  "faq":[
   ("How can I listen to rock radio online for free?","Open Pulsar FM in your browser, pick a rock station and press play. It's live, free and there's nothing to install. No account either."),
   ("What is the best rock radio station online?","Depends on what you're after. Radio Paradise is human-curated and eclectic, Rock Antenne is non-stop German rock and KEXP Seattle is the reference for indie rock. Not sure where to start? Start with KEXP."),
   ("Can I listen to rock radio on my phone?","Yes, in any modern browser, on desktop or phone. Not sure which station to pick? Press SCAN and Pulsar FM picks one for you.")]},
 "radios-jazz": {
  "slug":"jazz-radio","nome":"Jazz",
  "title":"Jazz Radio Online — Live from Paris and Beyond | Pulsar FM",
  "desc":"Listen to live jazz radio for free: TSF Jazz from Paris, FIP Jazz and Radio Swiss Jazz. Streaming in your browser, with a retro Winamp-style visualizer.",
  "h1":"Jazz Radio Online",
  "intro":"From Paris to Switzerland, jazz around the clock, live. Good for dinner, for work, or for pretending you understand the double bass.",
  "stations":[
   ("TSF Jazz","The reference jazz station in Paris, on air 24 hours a day."),
   ("Smooth Jazz","Smooth jazz at 320 kbps, for unwinding. On a 56k modem, an MP3 at this quality took almost an hour to download."),
   ("Radio Swiss Jazz","Hand-picked, ad-free jazz from Swiss public radio."),
   ("Jazz Radio France","France's big jazz network, from swing to soul."),
   ("SomaFM Sonic Universe","Avant-garde jazz and experimental sounds, for when the standards aren't enough."),
   ("FIP Jazz","Eclectic, ad-free jazz from French public radio."),
   ("WWOZ New Orleans","New Orleans' community radio: jazz, blues and funk from the city where jazz was born."),
   ("KCSM Jazz 91","Jazz around the clock, from the San Francisco Bay Area.")],
  "faq":[
   ("What is the best jazz radio station in Paris?","TSF Jazz is the reference jazz station in Paris, on air 24 hours a day. Pulsar FM also has Jazz Radio France, from swing to soul, and the more eclectic FIP Jazz."),
   ("How can I listen to jazz radio online for free?","Open Pulsar FM in your browser, pick a jazz station and press play. Live, free and no sign-up."),
   ("Can I listen to jazz radio on my phone?","Yes, in any browser, on desktop or phone. Tap the star on TSF Jazz and it stays in your favourites for next time.")]},
 "radios-chill": {
  "slug":"chill-radio","nome":"Chill / Ambient",
  "title":"Chill and Ambient Radio Online — Listen Live | Pulsar FM",
  "desc":"Live chill and ambient radio: SomaFM Drone Zone, Nightwave Plaza and Ibiza Global Radio. Free, streaming in your browser, with psychedelic visuals.",
  "h1":"Chill Radio Online",
  "intro":"Ambient, space drones and vaporwave: eight stations to switch off from the world. Close your eyes, or let the visualizer do the work.",
  "stations":[
   ("SomaFM Drone Zone","Ambient and space drones, no beat and no hurry."),
   ("Chillout-style Jazz","Chill with NASA space chatter in the mix. Houston, all is calm."),
   ("Nightwave Plaza","Vaporwave and retro aesthetics: the 90s internet as sound, minus the pop-ups."),
   ("SomaFM Lush","Soft vocals over dreamy electronica."),
   ("Ibiza Global Radio","Balearic chill and house, live from Ibiza, any time of day."),
   ("Ambient Sleeping Pill","Pure ambient for sleeping or drifting, uninterrupted."),
   ("Radio Paradise Mellow Mix","Radio Paradise's calm side: gentle songs picked by people, in no hurry to end the day."),
   ("Radio Paradise Serenity","Ambient and nature sounds, no vocals and no beat.")],
  "faq":[
   ("What kind of music do chill radio stations play?","Ambient, space drones, vaporwave, downtempo and Balearic. Music for relaxing, sleeping or working without anything tugging at your attention."),
   ("How can I listen to chill radio online for free?","Open Pulsar FM, pick a chill station and press play. Live, free and nothing to install."),
   ("Can I listen to chill music on my phone?","Yes, in any browser on your phone. To fall asleep to ambient, the SLEEP button pauses the radio after 15, 30 or 60 minutes.")]},
 "radios-pop": {
  "slug":"pop-radio","nome":"Pop",
  "title":"Pop Radio Online — Today's Hits Live for Free | Pulsar FM",
  "desc":"Listen to today's hits live: Capital FM London, NRJ France and Portugal's RFM and Rádio Comercial. Free, streaming in your browser, nothing to install.",
  "h1":"Pop Radio Online",
  "intro":"Today's hits, from Portugal to London, Paris and Bavaria. Eight live pop stations for days that call for choruses.",
  "stations":[
   ("RFM Pop Rock","Portugal's pop rock hits, from RFM."),
   ("Rádio Comercial","Portugal's most listened-to station: hits and good mood."),
   ("Capital FM UK","Today's hits, live from London."),
   ("NRJ France","Hit music only, as the slogan says. The hits, live from France."),
   ("I Love Radio DE","Charts and hits for the streaming generation, from Germany."),
   ("Antenne Bayern","The big hits from Bavaria's largest private station."),
   ("Cidade FM","Today's hits for a younger crowd, live from Portugal."),
   ("Heart UK","The pop hits you sing along to in the car, live from the UK.")],
  "faq":[
   ("Which pop radio stations can I listen to?","Capital FM from London, NRJ from France, I Love Radio and Antenne Bayern from Germany, plus RFM and Rádio Comercial, Portugal's most listened-to stations. All live."),
   ("How can I listen to pop radio online for free?","Open Pulsar FM in your browser, pick a pop station and press play. Live, free and nothing to install."),
   ("Can I listen to the hits on my phone?","Yes, in any modern browser, on desktop or phone. Heard a chorus a friend needs to hear? The SHARE button sends them the station that's playing.")]},
 "radios-study": {
  "slug":"study-radio","nome":"Study / Lo-Fi",
  "title":"Lo-Fi and Study Music Radio — Listen Live for Free | Pulsar FM",
  "desc":"Music to study and work to: SomaFM Groove Salad, non-stop classical and lo-fi chillhop. Free, live, right in your browser.",
  "h1":"Study Music Radio",
  "intro":"Lo-fi, downtempo and classical: eight stations picked for long study or deep-work sessions. Few lyrics, little chatter and no excuse not to start.",
  "stations":[
   ("SomaFM Groove Salad","Downtempo and chill to keep you focused for hours. An internet radio institution."),
   ("Radio Swiss Classic","Classical music with no interruptions or ads."),
   ("I Love Chillhop","Lo-fi and chillhop, the study classic, as a radio station."),
   ("SomaFM Deep Space One","Deep space ambient, for when your focus has to go far."),
   ("Venice Classic Radio","Timeless classical, from Italy with love."),
   ("Lofi Radio","Lo-fi beats 24/7, on a loop that doesn't ask for attention."),
   ("Classic FM UK","The UK's most listened-to classical station: well-known pieces, no pretension."),
   ("France Musique","Classical music from French public radio, with concerts and reference recordings.")],
  "faq":[
   ("What is the best music to study to?","Lo-fi, chillhop, downtempo and classical: music without lyrics that doesn't compete with what you're reading. The eight stations on this page were picked for exactly that."),
   ("How can I listen to lo-fi radio online for free?","Open Pulsar FM in your browser, pick I Love Chillhop or SomaFM Groove Salad and press play. Free and distraction-free."),
   ("Can I study with Pulsar FM on my phone?","Yes, in any browser on your phone. Add Pulsar FM to your home screen and it opens like an app, no app store involved.")]},
 "radios-electronica": {
  "slug":"electronic-radio","nome":"Electronic / Dance",
  "title":"Electronic Music Radio Online — Techno and House Live | Pulsar FM",
  "desc":"Live electronic and dance radio: TechnoBase.FM, Radio FG Paris and HouseTime.FM. Techno, house and progressive, free in your browser.",
  "h1":"Electronic Music Radio Online",
  "intro":"Techno, house and progressive, live around the clock. Turn it up, fire up Milkdrop and your room becomes a dancefloor. The neighbours will adapt.",
  "stations":[
   ("TechnoBase.FM DE","Techno and hands up live from Germany, with a huge community."),
   ("HouseTime.FM","House 24/7, from the TechnoBase family."),
   ("Frisky Radio USA","Deep house and progressive with resident DJs, live from the US."),
   ("Sunshine Live","Germany's biggest electronic station: sets, festivals and little talk."),
   ("Hirschmilch Electronic","German electronica, uninterrupted."),
   ("Radio FG Paris","House and electro live from Paris: the club station."),
   ("TranceBase.FM","Trance and uplifting from the TechnoBase family, for when techno needs a melody."),
   ("1.FM Deep House","Non-stop deep house from the 1.FM network. For warming up before going out, or for not going out at all.")],
  "faq":[
   ("How can I listen to electronic music radio for free?","Open Pulsar FM in your browser, pick a station and press play. Techno, house and progressive, live and 100% free."),
   ("Which electronic music styles can I listen to?","Techno and hands up on TechnoBase.FM, 24/7 house on HouseTime.FM, deep and progressive on Frisky Radio and festival sets on Sunshine Live."),
   ("Can I listen to electronic radio on my phone?","Yes, in any browser, on desktop or phone. Next time you open Pulsar FM, the Continue listening button takes you back to your last station.")]},
 "radios-psytrance": {
  "slug":"psytrance-radio","nome":"Goa / Psytrance",
  "title":"Psytrance and Goa Trance Radio Online — Live, Free | Pulsar FM",
  "desc":"Live psytrance and goa trance radio: Goa-Base, Hirschmilch Psy and BOM Psytrance. Free in your browser, with psychedelic Milkdrop visuals.",
  "h1":"Psytrance Radio Online",
  "intro":"Old-school goa and modern psytrance, live. Pairs well with Pulsar FM's TRIP mode, the full-screen visualizer. Anyone who has watched the sun rise on a dancefloor gets the idea.",
  "stations":[
   ("Goa-Base Trance","Old-school goa trance, live from Germany. Eastern melodies and bubbling 303s."),
   ("Hirschmilch Psy","High-quality psytrance, uninterrupted."),
   ("BOM Psytrance","Non-stop psytrance from the 1.FM network."),
   ("Psyndora Psytrance","Psytrance and progressive from the Greek scene."),
   ("Hirschmilch Progressive","Hypnotic progressive psy, for hours on end."),
   ("Hirschmilch Chillout","Psychill and goa ambient, for landing after the trip."),
   ("Radio Ozora","The radio of Ozora, the Hungarian psychedelic festival: psytrance and goa as heard in the valley."),
   ("Goanight","Night-time goa and psytrance, from the laut.fm community.")],
  "faq":[
   ("What is the difference between goa trance and psytrance?","Goa trance is the original 90s sound: melodic, eastern and hypnotic. Psytrance is its modern evolution, faster and heavier. Goa-Base plays the classic; Hirschmilch Psy plays today's sound."),
   ("How can I listen to psytrance radio online for free?","Open Pulsar FM, pick a psy station and press play. Live, free and nothing to install. Switch on TRIP mode for the full-screen visualizer."),
   ("Can I listen to goa trance on my phone?","Yes, in any modern browser, on desktop or phone. Ideally with headphones: psytrance loses half its bass on a phone speaker.")]},
 "radios-synthwave": {
  "slug":"synthwave-radio","nome":"Synthwave / Retrowave",
  "title":"Synthwave and Retrowave Radio Online — Listen Live | Pulsar FM",
  "desc":"Live synthwave and retrowave radio: Nightride FM, ChillSynth FM and SomaFM Underground 80s. Neon, nostalgia and a Winamp visualizer in your browser.",
  "h1":"Synthwave Radio Online",
  "intro":"Neon, synths and nostalgia for an 80s that never quite looked like this. It's the genre that defines Pulsar FM's vibe, in eight stations.",
  "stations":[
   ("Nightride FM","Synthwave and retrowave for night driving (car optional)."),
   ("ChillSynth FM","Soft chillsynth: neon on low."),
   ("SomaFM Digitalis","Indie electronica with a digital soul."),
   ("Nightride Datawave","Datawave: synths for surfing the digital night."),
   ("SomaFM Underground 80s","Underground 80s synthpop and new wave. The B-sides the radio of the time left out."),
   ("SomaFM Synphaera","Space synth and atmospheric electronica."),
   ("Nightride Darksynth","Darksynth: synthwave in nightmare mode. More distortion, fewer sunsets."),
   ("laut.fm Synthwave","Non-stop synthwave and retrowave, from the laut.fm community.")],
  "faq":[
   ("What is synthwave?","An electronic genre inspired by 80s film scores and synthesizers: neon, nostalgia and nights that never end. Where to start: Kavinsky, The Midnight and Perturbator."),
   ("How can I listen to synthwave radio online for free?","Open Pulsar FM in your browser, pick Nightride FM or ChillSynth FM and press play. Live and free."),
   ("Can I listen to retrowave on my phone?","Yes, in any browser, on desktop or phone. On desktop, open SKINS too: there are classic Winamp skins to match the neon.")]},
}

# Interface text per language. PT pages keep their exact original wording.
LABELS = {
 "pt": {"html_lang": "pt", "og_locale": '<meta property="og:locale" content="pt_PT" />\n  <meta property="og:locale:alternate" content="pt_BR" />',
        "play": "\U0001F3A7 Ouvir no player", "all": "▶ OUVIR TUDO NO PULSAR FM", "faq": "Perguntas frequentes",
        "others": "Outros géneros", "alt_label": "English", "lang_q": "",
        "footer": "Pulsar FM — rádio online grátis com visualizador retro estilo Winamp · <a href=\"/privacidade.html\">Privacidade &amp; Cookies</a>"},
 "en": {"html_lang": "en", "og_locale": '<meta property="og:locale" content="en_GB" />\n  <meta property="og:locale:alternate" content="en_US" />',
        "play": "\U0001F3A7 Play in the player", "all": "▶ LISTEN ON PULSAR FM", "faq": "Frequently asked questions",
        "others": "Other genres", "alt_label": "Português", "lang_q": "&amp;lang=en",
        "footer": "Pulsar FM — free online radio with a retro Winamp-style visualizer · <a href=\"/privacidade.html\">Privacy &amp; Cookies</a>"},
}

GA = '''  <!-- Google tag (gtag.js) with Consent Mode v2 - default: everything denied -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-YRD1BYXB78"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('consent', 'default', {
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
      analytics_storage: 'denied',
      wait_for_update: 500
    });
    if (localStorage.getItem('pulsarfm-consent') === 'granted') {
      gtag('consent', 'update', {
        ad_storage: 'granted',
        ad_user_data: 'granted',
        ad_personalization: 'granted',
        analytics_storage: 'granted'
      });
    }
    gtag('js', new Date());
    gtag('config', 'G-YRD1BYXB78');
  </script>'''

# Genre → matching /recomendacoes/ guide (contextual GEAR block on each page).
# (guide slug, headline, one-line pitch)
GEAR = {
 "radios-rock":      ("soundbars", "Concertos ao vivo na sala",
                      "Riffs e baterias pedem espaço. Vê o que conta numa soundbar antes de te deixares levar pelos watts."),
 "radios-jazz":      ("gira-discos", "Jazz soa ainda melhor em vinil",
                      "Do disco às colunas: o que precisas para montar o teu primeiro gira-discos."),
 "radios-chill":     ("colunas-bluetooth", "Chill em qualquer lado",
                      "Da cozinha ao fim de tarde no jardim: como escolher uma coluna Bluetooth."),
 "radios-pop":       ("tecnologia-acessorios", "Os hits em qualquer aparelho",
                      "Um adaptador, um recetor Bluetooth ou o cabo certo põem a rádio a tocar na aparelhagem que já tens."),
 "radios-study":     ("melhores-auscultadores", "Foco total para estudar",
                      "Auscultadores para sessões longas de estudo ou trabalho: conforto primeiro, o resto depois."),
 "radios-electronica": ("home-studio", "Da pista ao estúdio",
                      "Queres passar de ouvir a produzir? Começa por um home studio pequeno que faça sentido."),
 "radios-psytrance":  ("melhores-auscultadores", "Graves a sério, sem incomodar ninguém",
                      "Como escolher auscultadores para ouvir psytrance como deve ser, sem acordar o prédio."),
 "radios-synthwave": ("gira-discos", "Retro até ao fim",
                      "Synthwave em vinil é outro ritual: prepara o teu primeiro lado A."),
}

def path_for(slug, lang):
    """URL path (no leading slash) of a genre page: PT keeps radios-*/, EN lives under en/."""
    return slug + "/" if lang == "pt" else "en/" + GENRES_EN[slug]["slug"] + "/"


def localized(slug, lang):
    """Genre data for one language; EN overrides the copy and keeps genre/emoji from PT."""
    g = GENRES[slug]
    if lang == "pt":
        return g
    en = GENRES_EN[slug]
    assert len(en["stations"]) == len(g["stations"]), slug  # keep the same number of stations per genre
    return dict(g, **{k: v for k, v in en.items() if k != "slug"})


def page(slug, lang="pt"):
    g = localized(slug, lang)
    L = LABELS[lang]
    path = path_for(slug, lang)
    other_lang = "en" if lang == "pt" else "pt"
    base = "https://pulsarfm.eu/"
    alternates = "\n  ".join(
        '<link rel="alternate" hreflang="{}" href="{}{}" />'.format(code, base, path_for(slug, target))
        for code, target in (("pt", "pt"), ("en", "en"), ("x-default", "pt")))
    lang_alt = '<a class="lang-alt" href="/{}" hreflang="{}" lang="{}">{}</a>'.format(
        path_for(slug, other_lang), other_lang, other_lang, L["alt_label"])
    gear_html = ""
    if lang == "pt":  # The guides are PT-only (and Amazon.es), so EN pages skip the GEAR box.
        gear_slug, gear_h, gear_p = GEAR[slug]
        gear_html = '''    <a class="gear-box" href="/recomendacoes/{}/">
      <span class="gear-tag">\U0001F3A7 GEAR</span>
      <strong>{}</strong>
      <span>{}</span>
      <span class="gear-go">Ler o guia →</span>
    </a>'''.format(gear_slug, gear_h, gear_p)
    others = "\n".join(
        '          <a href="/{}" class="genre-filter-link">{} {}</a>'.format(
            path_for(s, lang), d["emoji"], localized(s, lang)["nome"])
        for s, d in GENRES.items() if s != slug)
    cards = "\n".join('''      <article class="radio-card">
        <h3>{}</h3>
        <p>{}</p>
        <a class="play-cta" href="/?genre={}{}">{}</a>
      </article>'''.format(name, desc, g["genre"], L["lang_q"], L["play"]) for name, desc in g["stations"])
    stations_ld = ",\n      ".join(
        '{{ "@type": "ListItem", "position": {}, "item": {{ "@type": "RadioStation", "name": {}, "description": {} }} }}'.format(
            i + 1, json.dumps(name, ensure_ascii=False), json.dumps(desc, ensure_ascii=False))
        for i, (name, desc) in enumerate(g["stations"]))
    faq_html = "\n".join('''      <div class="faq-item">
        <h3>{}</h3>
        <p>{}</p>
      </div>'''.format(q, a) for q, a in g["faq"])
    faq_ld = ",\n      ".join(
        '{{ "@type": "Question", "name": {}, "acceptedAnswer": {{ "@type": "Answer", "text": {} }} }}'.format(
            json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False))
        for q, a in g["faq"])
    return '''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
{GA}

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="/favicon.ico" type="image/x-icon">

  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="https://pulsarfm.eu/{path}" />
  {alternates}
  <meta name="theme-color" content="#031317" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://pulsarfm.eu/{path}" />
  <meta property="og:title" content="{h1} | Pulsar FM" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://pulsarfm.eu/img/pulsar-og.jpg" />
  <meta property="og:site_name" content="Pulsar FM" />
  {og_locale}

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "{h1}",
    "itemListElement": [
      {stations_ld}
    ]
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Pulsar FM", "item": "https://pulsarfm.eu/" }},
      {{ "@type": "ListItem", "position": 2, "name": "{h1}", "item": "https://pulsarfm.eu/{path}" }}
    ]
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {faq_ld}
    ]
  }}
  </script>

  <style>
    :root {{
      --line-primary: #00ffcc;
      --line-secondary: #00ccff;
      --neon-pink: #ff2d9b;
      --neon-green: #39ff14;
      --text-primary: #ecfffb;
      --text-muted: #9ad9d3;
      --text-dim: rgba(236, 255, 251, 0.72);
    }}

    html {{ color-scheme: dark; }}

    body {{
      min-height: 100vh;
      margin: 0;
      padding: 32px 16px 60px;
      display: flex;
      flex-direction: column;
      align-items: center;
      background:
        radial-gradient(circle at top left,  rgba(192, 68, 255, 0.13), transparent 40%),
        radial-gradient(circle at top right, rgba(255, 45, 155, 0.10), transparent 38%),
        linear-gradient(180deg, #02080b 0%, #031317 48%, #010507 100%);
      color: var(--text-primary);
      font-family: 'Share Tech Mono', 'Courier New', monospace;
    }}

    main {{
      width: min(860px, 100%);
      background-color: rgba(0, 10, 14, 0.78);
      border: 2px solid var(--line-primary);
      border-radius: 24px;
      padding: 36px 28px;
      box-sizing: border-box;
      box-shadow:
        0 0 25px rgba(0, 255, 204, 0.22),
        0 0 28px rgba(255, 45, 155, 0.18);
      backdrop-filter: blur(8px);
    }}

    .breadcrumb {{
      font-size: 0.78rem;
      margin: 0 0 18px;
      color: var(--text-dim);
    }}

    .breadcrumb a {{ color: var(--line-secondary); text-decoration: none; }}
    .breadcrumb {{ display: flex; flex-wrap: wrap; gap: 4px 6px; }}
    .breadcrumb .lang-alt {{ margin-left: auto; color: var(--text-muted); }}
    .breadcrumb a:hover {{ color: var(--line-primary); }}

    h1 {{
      margin: 0 0 10px;
      color: var(--line-primary);
      font-size: clamp(1.5rem, 4vw, 2.3rem);
      text-shadow:
        0 0 18px rgba(0, 255, 204, 0.35),
        0 0 40px rgba(255, 45, 155, 0.20);
    }}

    .intro {{
      color: var(--text-muted);
      line-height: 1.75;
      font-size: 0.95rem;
      margin: 0 0 26px;
    }}

    .station-list {{
      display: grid;
      gap: 16px;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      margin-bottom: 30px;
    }}

    .radio-card {{
      background-color: rgba(0, 0, 0, 0.72);
      border: 1px solid var(--line-secondary);
      border-radius: 16px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 0 16px rgba(0, 204, 255, 0.18);
      transition: transform 0.18s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }}

    .radio-card:hover {{
      transform: translateY(-2px);
      border-color: var(--neon-pink);
      box-shadow: 0 0 18px rgba(255, 45, 155, 0.30);
    }}

    .radio-card h3 {{
      margin: 0 0 8px;
      color: var(--line-secondary);
      font-size: 1.05rem;
    }}

    .radio-card p {{
      margin: 0 0 14px;
      color: var(--text-dim);
      font-size: 0.85rem;
      line-height: 1.6;
      flex: 1;
    }}

    .play-cta {{
      align-self: flex-start;
      background-color: var(--line-secondary);
      color: #001114;
      text-decoration: none;
      padding: 9px 16px;
      border-radius: 999px;
      font-weight: bold;
      font-size: 0.85rem;
      transition: background-color 0.2s ease, transform 0.14s ease, box-shadow 0.2s ease;
    }}

    .play-cta:hover {{
      background-color: var(--neon-green);
      color: #001a00;
      transform: translateY(-1px);
      box-shadow: 0 0 14px rgba(57, 255, 20, 0.5);
    }}

    h2 {{
      color: var(--text-muted);
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin: 30px 0 12px;
    }}

    .genre-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 26px;
    }}

    .genre-filter-link {{
      display: inline-block;
      padding: 8px 14px;
      border-radius: 999px;
      text-decoration: none;
      background: rgba(0, 204, 255, 0.12);
      border: 1px solid rgba(0, 204, 255, 0.25);
      color: var(--line-secondary);
      font-size: 0.82rem;
      transition: all 0.2s ease;
    }}

    .genre-filter-link:hover {{
      background: rgba(255, 45, 155, 0.22);
      border-color: rgba(255, 45, 155, 0.5);
      color: var(--neon-pink);
      transform: translateY(-2px);
    }}

    .home-cta {{
      display: inline-block;
      background: var(--neon-green);
      color: #001a00;
      text-decoration: none;
      font-weight: bold;
      padding: 12px 24px;
      border-radius: 999px;
      font-size: 0.9rem;
      letter-spacing: 0.06em;
      box-shadow: 0 0 16px rgba(57, 255, 20, 0.4);
      transition: box-shadow 0.2s ease, transform 0.14s ease;
    }}

    .home-cta:hover {{
      transform: translateY(-2px);
      box-shadow: 0 0 24px rgba(57, 255, 20, 0.6);
    }}

    .gear-box {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin: 26px 0 8px;
      padding: 16px 18px;
      border-radius: 14px;
      text-decoration: none;
      border: 1px solid rgba(255, 45, 155, 0.35);
      background: linear-gradient(90deg, rgba(0, 255, 204, 0.05), rgba(255, 45, 155, 0.08));
      color: var(--text-dim);
      font-size: 0.87rem;
      line-height: 1.6;
      transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.14s ease;
    }}

    .gear-box:hover {{
      border-color: var(--neon-pink);
      box-shadow: 0 0 16px rgba(255, 45, 155, 0.3);
      transform: translateY(-2px);
    }}

    .gear-box strong {{ color: var(--line-primary); font-size: 1rem; }}
    .gear-tag {{ color: var(--neon-pink); font-size: 0.72rem; letter-spacing: 0.18em; }}
    .gear-go {{ color: var(--neon-pink); font-weight: bold; }}

    .faq {{ margin-bottom: 6px; }}

    .faq-item {{
      border-left: 2px solid rgba(0, 204, 255, 0.35);
      padding: 2px 0 2px 14px;
      margin-bottom: 16px;
    }}

    .faq-item h3 {{
      margin: 0 0 6px;
      color: var(--line-secondary);
      font-size: 0.95rem;
    }}

    .faq-item p {{
      margin: 0;
      color: var(--text-dim);
      font-size: 0.87rem;
      line-height: 1.7;
    }}

    footer {{
      margin-top: 26px;
      font-size: 0.78rem;
      color: rgba(0, 255, 204, 0.6);
    }}

    footer a {{ color: var(--text-muted); }}
  </style>
</head>
<body>
  <main>
    <nav class="breadcrumb"><a href="/">Pulsar FM</a> › {emoji} {nome}{lang_alt}</nav>

    <h1>{emoji} {h1}</h1>
    <p class="intro">{intro}</p>

    <div class="station-list">
{cards}
    </div>

    <a class="home-cta" href="/?genre={genre}{lang_q}">{all_label}</a>

{gear_html}

    <h2>{faq_h}</h2>
    <div class="faq">
{faq_html}
    </div>

    <h2>{others_h}</h2>
    <div class="genre-links">
{others}
    </div>

    <footer>{footer}</footer>
  </main>
</body>
</html>
'''.format(GA=GA, path=path, alternates=alternates, lang_alt=lang_alt, cards=cards, others=others,
           stations_ld=stations_ld, html_lang=L["html_lang"], og_locale=L["og_locale"],
           lang_q=L["lang_q"], all_label=L["all"], faq_h=L["faq"], others_h=L["others"], footer=L["footer"],
           faq_html=faq_html, faq_ld=faq_ld, gear_html=gear_html,
           title=g["title"], desc=g["desc"], h1=g["h1"], intro=g["intro"],
           emoji=g["emoji"], nome=g["nome"], genre=g["genre"])

for slug in GENRES:
    for lang in ("pt", "en"):
        d = os.path.join(OUT, *path_for(slug, lang).strip("/").split("/"))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(slug, lang))
        print("OK", path_for(slug, lang))
