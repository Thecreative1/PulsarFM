# Smoke test em produção — navegação e deteção por país

Resultado: aprovado.

- Site: https://pulsarfm.eu/
- Versão: 88abe58db95941d9b203b4722f026010d1823f88
- GitHub Pages: built, sem erro.
- Testes concluídos: 2026-10-12T19:10:04.120Z

## Navegação

42 cenários aprovados em desktop (1440 px) e mobile (390 px): ES → EN → ES, PT → EN → PT, recarregamento, histórico voltar/avançar, filtros, géneros, guias, escolha explícita, preferências guardadas, armazenamento bloqueado e deteção inicial de país. A escolha manual não é sobreposta por uma resposta tardia.

As respostas de país foram simuladas por interceção de pedidos no navegador. Não foi usada uma VPN espanhola. Um pedido real separado ao serviço Country.is respondeu HTTP 200, com CORS e código de país válido; o IP retornado não foi registado.

Na primeira visita ao endereço principal sem preferência, país ES abre /es/. A URL explícita e a preferência guardada têm prioridade. EN regressa ao mercado de origem, preservado também nos links de géneros, privacidade e equipamento. Falhas e timeout de dois segundos mantêm PT sem impedir a rádio.

## Site e rádio

71 páginas e oito assets críticos devolvem HTTP 200 e coincidem com a versão local. As URLs normais de /, /es/ e /es/recomendaciones/ também coincidem sem parâmetro de teste.

Os 13 guias espanhóis passaram navegação e layout em desktop/mobile. O player continua com 64 estações, as skins, os filtros e a mesma instância Webamp durante a troca de idioma. O áudio real com CORS foi descodificado e avançou 0.162246 segundos.

Tracking PT e ES corretos. O evento de afiliado foi simulado na fila local: um após consentimento e nenhum após revogação. Pedidos GA4/Amazon bloqueados; sem compras ou eventos reais de teste. Rotas principais também renderizam conteúdo espanhol sem JavaScript. Nenhum erro JavaScript nos dois testes.

Evidência: language-navigation.json, smoke-results.json e screenshots nesta pasta.

IndexNow aceitou 71 URLs alteradas (HTTP 200) após ambos os testes aprovados.
