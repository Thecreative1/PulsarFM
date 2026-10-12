# Navegação PT/ES/EN e deteção inicial de Espanha

Implementação de 12/10/2026.

## Comportamento

- O idioma explícito na query vence: lang=pt, lang=es e lang=en. A URL /es/ abre ES sem consulta ao país, salvo escolha explícita diferente na query.
- No endereço principal, uma preferência válida já guardada vence a deteção. Uma primeira visita sem preferência consulta Country.is; ES abre /es/, outros países mantêm PT.
- EN regressa à versão PT ou ES de origem. O contexto é guardado em pulsarfm-market e, no caso ES em inglês, em return_lang=es na URL.
- Géneros, privacidade e equipamento mantêm o mercado durante o percurso em inglês. A escolha PT é explícita nos links de regresso ao player.
- Seleção manual cria uma entrada no histórico. Voltar/avançar restaura idioma, mercado e filtro, sem criar outro Webamp.
- Falhas, respostas desconhecidas, JSON inválido ou demora superior a dois segundos não bloqueiam a rádio. Uma resposta tardia não sobrepõe a escolha manual.
- Armazenamento bloqueado já não interrompe as preferências da rádio: a navegação por URL continua disponível.

## Country.is e autorização

O serviço usado é https://api.country.is/. A documentação oficial é https://country.is/. O navegador faz GET / com credentials=omit e referrerPolicy=no-referrer, sem enviar cookies nem o endereço da página como referer. O serviço recebe necessariamente o IP ao responder. A PulsarFM lê apenas country; não persiste o IP, não pede coordenadas/GPS e não acrescenta o IP ao Analytics. A informação consta das políticas PT e ES.

O proprietário pediu a abertura automática por IP de Espanha e autorizou expressamente o destino: «Sim, autorizo Country.is para este fim». A primeira revisão automática bloqueou a ativação por falta de autorização específica para o destinatário; essa autorização foi obtida antes da ativação e dos pedidos reais.

## Validação local

A matriz tools/check-language-navigation.cjs passou 42 cenários em Chrome, nas larguras 1440 e 390: Espanha, Portugal, outro país, falhas de rede/serviço, resposta inválida, timeout, URL explícita, preferência guardada, conflito de idioma, armazenamento bloqueado, resposta tardia, ES → EN → ES, PT → EN → PT, recarregamento, voltar/avançar, filtro rock, género inglês e guias espanhóis.

As respostas de países nesses cenários são interceptadas e simuladas, não visitas feitas com uma VPN espanhola. Um pedido real separado confirmou HTTP 200, CORS legível e um código de país válido, sem registar o IP retornado.

O teste complementar da rádio cobre áudio real com CORS, 64 estações, skins, consentimento e os 13 guias em desktop/mobile. O projeto passou 38 testes Python com 1134 subtestes, 8 testes Analytics, 37 scripts na verificação de sintaxe e lint estático de 71 páginas/1936 ligações internas.

As evidências locais estão em docs/qa-es/language-navigation.json e browser-results.json. Após deploy, a mesma matriz e o smoke test são executados em produção, com evidência em docs/qa-es/live/.
