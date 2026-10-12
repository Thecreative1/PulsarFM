# Expansão PulsarFM para Espanha

Implementação local concluída em 12/10/2026, por fases. Não houve push nem deploy. O único commit criado foi o checkpoint de segurança d86ac94, antes da implementação (árvore inicial limpa). As alterações finais ficam na working tree para revisão.

## Auditoria e arquitetura

Site estático em GitHub Pages, sem framework, package.json ou TypeScript. index.html contém a rádio, 64 streams, Webamp 2.3.1, Butterchurn 2.6.7, presets 2.4.7, favoritos, skins, dock/float, sleep, trip e PT/EN. Os guias PT são gerados de data/affiliates.json e data/recommendations.json; os géneros por tools/gen_genre_pages.py. Domínio canónico https://pulsarfm.eu. GA4 G-YRD1BYXB78 reutilizado com pulsarfm-consent.

A edição ES reutiliza o HTML da rádio e os componentes/CSS editoriais. A homepage ES é gerada a partir da original: uma única implementação do player para manutenção, com dois outputs estáticos completos para SEO. Não existe serviço de tradução automática ou redirecionamento por IP. Todas as URLs antigas, a edição inglesa, a infraestrutura da rádio e os dados PT são mantidos.

Comparação direta com d86ac94: radios, skins, playStation(), layoutPlayerWindows(), playRandom(), createStationCard() e toggleFavorite() ficaram idênticos. Os 313 links Amazon existentes nos guias PT mantêm exatamente os mesmos destinos e parâmetros; prova em qa-es/legacy-links.json.

## Fase 1: idiomas

PT permanece nas URLs atuais; ES em /es/. Seletor discreto PT | ES na rádio e nas páginas editoriais; EN existente conservado. Na rádio, mudar PT/ES não recria Webamp nem interrompe a instância. Idioma explícito da URL, preferência local no dispositivo e links coerentes no portal, géneros e privacidade. As traduções ES incluem navegação, filtros, botões da rádio, dock, overlay e instruções de Trip, consentimento, SEO e rodapé. Nomes de marca, emissores, skins e comandos nativos Winamp mantêm-se.

O base href=/ preserva as URLs originais de skins, manifesto e imagens quando a língua muda em memória. /?lang=en continua suportado; os filtros conservam o idioma nos URLs.

## Fase 2: SEO

26 páginas ES indexáveis: homepage, oito géneros, portal, sete categorias, oito artigos e privacidade. Sitemap inclui as 58 páginas PT/EN/ES e atualiza lastmod para os ficheiros alterados. Metadados e Open Graph ES próprios; canonical autorreferencial e hreflang pt-PT/es-ES recíproco apenas nos equivalentes revistos em data/locale-routes.json. x-default continua nas páginas de género existentes como destino PT; não foi acrescentado indiscriminadamente.

Breadcrumbs visíveis e BreadcrumbList em artigos/categorias. Article e CollectionPage onde aplicável, sem avaliações, estrelas, testes ou ofertas inventadas. Conteúdo e links existem sem JavaScript. As ligações de verificação Bing, IndexNow e robots.txt permanecem intactas.

## Fase 3: conteúdo comercial

/es/recomendaciones/ tem sete categorias e oito guias: auriculares Bluetooth qualidade-preço 2026; ANC para trabalhar; altavoces Bluetooth para casa; tocadiscos para começar; home studio económico; micrófonos USB para podcast/streaming; primeiro Hi-Fi; acessórios de áudio.

16 produtos reutilizam a identidade e ASIN do catálogo existente. Texto ES escrito editorialmente, critérios objetivos, escolhas por perfil, comparação, vantagens/limitações visíveis, links relacionados, data de atualização e fontes oficiais junto de cada produto. Fotografias Amazon e preços estáticos não são usados; as imagens são ilustrações próprias existentes. Não alegamos testes da redação, rankings de desempenho medido, disponibilidade atual ou descontos.

## Fase 4: afiliação

Configuração central data/affiliate-markets.json: PT = pulsarfm-21 (preservado), ES = pulsarfmes-21 (confirmado por ti neste chat). tools/market_config.py recusa substituição do ID PT, placeholders e IDs sem validação. A ausência de ID ES produz apenas links diretos sem copiar o ID PT.

Links diretos Amazon.es, rel=sponsored nofollow noopener noreferrer, sem intermediários. Aviso de publicidade antes do primeiro link em cada artigo e declaração Amazon espanhola no portal, artigos e privacidade, conforme a [orientação oficial Amazon](https://afiliados.amazon.es/help/node/topic/GHQNZAU6669EZS98). A contradição histórica sobre comissões já estava corrigida no gerador atual; foi confirmada por regeneração e pelos testes existentes.

## Fase 5: medição

Um emissor de affiliate_click, com market, language, article_slug, product_id, merchant e link_position, mantendo os parâmetros antigos. page_view editorial recebe contexto de mercado, idioma, artigo, categoria e tipo de página. GA4 só carrega após aceitar nas páginas editoriais. Recusa, revogação, alterações entre separadores e localStorage bloqueado são cobertos nos testes de analytics.

País e tráfego orgânico usam dimensões nativas GA4; não foi adicionada geolocalização. Procedimento de dimensões personalizadas, DebugView, análise por categoria/artigo/posição e relatório Amazon em docs/AFILIADOS.md. Cliques não são vendas ou comissões. Caso a medição otimizada GA4 já emita click para saídas, analisar affiliate_click separadamente para evitar dupla contagem.

## Fase 6: experiência

Rádio continua principal. EQUIPO e rodapé abrem guias em nova aba; géneros ES têm chamada contextual para o guia relevante. Mesmo CSS, Share Tech Mono, paleta, ilustrações e hierarquia retro existentes. Tabelas com scroll próprio no telemóvel, links relacionados e CTAs calmos. Sem pop-ups comerciais ou novos banners publicitários.

## Fase 7: testes e evidências

- Build: python -X utf8 tools/build_site.py, gera PT/EN/ES em ordem e valida dados antes de gravar cada edição.
- Lint estático: 58 páginas, 26 ES, 1.346 ligações internas, canonical, hreflang, sitemap, IDs, JSON-LD e metadados próprios.
- Lint JS: 36 scripts externos/inline com sintaxe válida.
- Python: compileall sem erros; 37 testes e 492 subtestes passados.
- Analytics Node: 8 testes passados, incluindo ES, consentimento, revogação, um evento por clique e reutilização de gtag.
- git diff --check: passou.
- Chrome: 1440×1000 e 390×844, rádio/portal/artigo sem overflow ou erros JS; seleção PT/ES/EN, persistência, filtros, instância do Webamp conservada, assets de skins e URLs antigas.
- Áudio: stream existente Radio Paradise descodificado em Chrome com CORS, readyState=4 e tempo de reprodução a avançar. Não revalidámos os 64 streams nem alterámos os seus URLs.
- Sem JS: homepage, portal, artigo, género e privacidade espanhóis devolvem 200 e conteúdo localizado.

Typecheck formal: não aplicável/configurado neste repositório de HTML/JS e Python; não existe TypeScript ou verificador de tipos. As verificações executadas foram sintaxe JS, compilação Python e testes de contratos, sem as apresentar como análise estática de tipos.

Screenshots revistos: qa-es/radio-desktop.png, radio-mobile.png, hub-desktop.png, hub-mobile.png, article-desktop.png e article-mobile.png. Resultados estruturados: qa-es/browser-results.json e qa-es/check-results.json. Inventário completo de ficheiros: qa-es/changed-files.json.

## Problemas encontrados e resolvidos

A substituição inicial de lang podia alterar também hreflang; a alteração foi restringida ao atributo html e a reciprocidade passa no teste. O botão EN precisava de tratamento da nova terceira língua; foi corrigido e testado. Mudar a URL da rádio em memória podia alterar a resolução de skins relativas; o base href e a regressão dedicada resolvem isso sem tocar no catálogo. Um fixture antigo de analytics esperava só os parâmetros anteriores; foi atualizado para o contrato ampliado. Linhas em branco dos templates sem equivalente geravam whitespace; foram corrigidas.

## Confirmações manuais antes de produção

1. Revisão editorial concluída em 12/10/2026, a pedido do dono, em docs/REVISAO-EDITORIAL-ES.md. Os oito guias foram corrigidos; três equivalências demasiado amplas foram retiradas. O conteúdo não é apresentado como testado.
2. Amazon bloqueou a consulta automatizada de algumas fichas; os ASINs e a verificação anterior de 06/10/2026 foram preservados. Confirmar os 16 modelos, variantes, vendedor, produto novo/segunda mão e stock antes de publicar. A data de consulta de especificações oficiais é separada desta verificação.
3. Confirmar no painel Amazon que pulsarfmes-21 está aprovado e o domínio está registado; foi configurado com base na tua confirmação.
4. Configurar as dimensões GA4 e validar um evento real no DebugView com consentimento. Os testes locais bloqueiam pedidos GA4 e Amazon para não fabricar cliques reais.
5. Rever juridicamente as políticas/comunicação comercial e testar fullscreen, audição e skins em dispositivos reais. Os menus internos Webamp continuam os do componente original, preservado por requisito.
6. Depois da revisão, executar novamente build/checks, publicar pelo fluxo habitual e submeter/validar sitemap no Google Search Console. Acesso à consola e indexação real não foram exercidos localmente.

## Ficheiros principais

- index.html
- privacidade.html
- sitemap.xml
- assets/radio-i18n.js
- assets/radio-locales.js
- assets/site-language.js
- assets/affiliate-analytics.js
- assets/recommendations.css
- data/affiliate-markets.json
- data/locale-routes.json
- data/radio.es.json
- data/genres.es.json
- data/recommendations.es.json
- tools/market_config.py
- tools/site_i18n.py
- tools/gen_spain.py
- tools/gen_genre_pages.py
- tools/gen_recommendations.py
- tools/build_site.py
- tools/check_site.py
- tools/check-js.cjs
- tools/browser-check.cjs
- templates/recommendations/page.html
- tests/test_spain.py
- tests/affiliate-analytics.test.cjs
- docs/AFILIADOS.md
- CLAUDE.md

Além destes, foram regeneradas as páginas PT/EN de géneros e as 14 páginas editoriais PT para navegação, equivalências e contexto de medição. Foram adicionadas 26 páginas ES. O catálogo e conteúdo editorial PT (data/affiliates.json e data/recommendations.json), streams, skins, imagens, manifest e infraestrutura de hosting não foram alterados.

Atualização editorial de 12/10/2026: textos e metadados revistos, novas fontes complementares, FAQs de géneros diferenciadas e avisos alinhados com o código. Build, lint e 45 testes passaram após as correções; ver REVISAO-EDITORIAL-ES.md.
