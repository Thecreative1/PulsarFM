# Afiliados Awin na PulsarFM

## Estado e integração

Catálogo inicial com quatro produtos da Worten e links diretos não remunerados: Sony WH-CH520, JBL Go 4, JBL Bar 2.0 All-In-One e Audio-Technica AT-LP60XUSBGM. Os links e imagens vêm das páginas indicadas em `source.referenceUrl`. Não mostramos preços nem apresentamos estes produtos como testes da redação. A disponibilidade e o vendedor, incluindo ofertas Marketplace, devem ser confirmados na loja.

Cada produto tem `linkType: "direct"` ou `"affiliate"`. Os atuais usam `direct`: abrem `destinationUrl` com `rel="noopener"`, sem exigir IDs Awin e sem evento `affiliate_click`, `data-affiliate-link` ou divulgação de comissão. A nota junto dos produtos explica que não há comissão.

Para ativar a Awin depois, preencher o link/IDs e mudar explicitamente o produto para `linkType: "affiliate"`. Configurar IDs, por si só, não monetiza produtos diretos. Produtos sem `linkType` mantêm o comportamento de afiliado por compatibilidade. O template de produto e os feeds destinam-se à futura integração de afiliados.

O site continua estático e compatível com GitHub Pages. A homepage recebeu apenas um link no rodapé, com tradução PT/EN e abertura noutra aba para preservar a reprodução. Não foram alterados o player, as estações nem a navegação principal.

`/recomendacoes/` reúne seis guias em português: auscultadores, colunas Bluetooth, soundbars, gira-discos, home studio e tecnologia/acessórios. Os guias contêm critérios de escolha e estão prontos para receber produtos reais. O HTML é gerado antes da publicação: conteúdo, imagens, links e divulgação continuam disponíveis sem JavaScript.

## Ficheiros

| Ficheiro | Função |
| --- | --- |
| `index.html` | Entrada discreta no rodapé e texto PT/EN |
| `privacidade.html` | Divulgação da relação de afiliado e explicação do evento |
| `sitemap.xml` | Inclui a secção e os seis guias |
| `data/affiliates.json` | Anunciantes, IDs da Awin e catálogo central de produtos |
| `data/recommendations.json` | Conteúdo e produtos selecionados para cada guia |
| `templates/product.json`, `templates/article.json` | Exemplos para novas entradas, não publicados automaticamente |
| `templates/recommendations/page.html` | Estrutura comum das páginas e controlos de consentimento |
| `templates/recommendations/article.html` | Template editorial reutilizável |
| `templates/recommendations/product.html` | Componente de recomendação com imagem, descrição, preço opcional e CTA |
| `templates/recommendations/disclosure.html` | Divulgação de afiliados reutilizável |
| `assets/recommendations.css` | Estilos responsivos isolados das páginas da rádio |
| `assets/affiliate-analytics.js` | Consentimento, evento, fallback de imagem e validade de preços |
| `img/gear-editorial.svg` | Ilustração editorial local e fallback identificado de imagem |
| `tools/gen_recommendations.py` | Validação e geração das sete páginas estáticas e sitemap |
| `tools/import_awin_feed.py` | Adaptador CSV da Awin para rascunhos normalizados |
| `tools/preview_recommendations.py` | Demonstração local com produto fictício e analytics simulado |
| `tests/test_affiliates.py`, `tests/affiliate-analytics.test.cjs` | Validação de links, HTML, importação e tracking |
| `recomendacoes/index.html`, `recomendacoes/*/index.html` | HTML gerado, a incluir no commit; não editar diretamente |
| `docs/PRODUCT.md`, `docs/DESIGN.md` | Contexto da marca e do design preservado |
| `.gitignore` | Exclui caches Python e a pasta local de feeds |

## Onde colocar os links

Em `data/affiliates.json`, dentro de `products`. Há duas opções:

1. **Link pronto:** colocar o URL completo gerado pelo Link Builder da Awin em `affiliateUrl`. Também aceita `aw_deep_link` dos feeds. É a opção mais simples e mantém os parâmetros originais, incluindo `clickref`. Aceita `awin1.com/cread.php`, `awin1.com/pclick.php` e links curtos `tidd.ly`. Outros formatos precisam de validação antes de alargar a lista.
2. **Gerar um deep link:** preencher `awin.publisherId`, `merchants.worten-pt.advertiserId` e o URL real do produto em `destinationUrl`; deixar `affiliateUrl` vazio. O gerador constrói `cread.php` com `awinmid`, `awinaffid`, `ued` e um `clickref` baseado no ID do produto.

Confirmar na conta Awin a adesão ao programa e o suporte a deep links. Os IDs são os da tua conta e do anunciante, não devem ser copiados dos exemplos de testes. Não colocar API keys no catálogo ou no JavaScript. Os links e IDs públicos de afiliado não são chaves de acesso.

## Adicionar um produto

1. Copiar o objeto de `templates/product.json` para o array `products` em `data/affiliates.json`.
2. Escolher um `id` único (letras minúsculas, números e hífen) e `merchant: "worten-pt"`.
3. Preencher `name`, `description`, `image`, `imageAlt` e o link conforme uma das opções anteriores. Usar uma fotografia autorizada, local em `/img/` ou com URL HTTPS. A ilustração do template é apenas um exemplo, não uma fotografia de produto.
4. Manter `price: null` para não mostrar preço. Para o mostrar:

   ```json
   "price": { "amount": "129.99", "currency": "EUR", "checkedAt": "2026-09-29" }
   ```

   Este valor é apenas exemplo de formato. Usar preço e data realmente verificados. Os preços têm uma nota de atualização e deixam de ser mostrados pelo gerador após sete dias. O JavaScript também oculta preços antigos em páginas já publicadas; sem JavaScript, um HTML antigo mantém o preço datado até à próxima geração. Para evitar manutenção de preços, deixar `null`.

5. Rever a descrição, imagem, preço, disponibilidade, vendedor e destino; mudar `status` de `draft` para `published`.
6. No artigo escolhido em `data/recommendations.json`, acrescentar o ID a `productIds`. A ordem do array determina a ordem dos componentes.
7. Atualizar `updatedAt` do artigo e da secção, e executar:

   ```powershell
   python tools/gen_recommendations.py
   ```

Um produto em rascunho não aparece no HTML. Um produto publicado com dados obrigatórios ou link inválidos faz a geração falhar. Referências a IDs inexistentes também falham, em vez de desaparecerem silenciosamente.

Os links de afiliado têm `target="_blank"`, `rel="sponsored nofollow noopener"` e indicação acessível de nova aba. A divulgação é acrescentada automaticamente quando há links de afiliado no artigo ou seleção. Os links diretos usam apenas `rel="noopener"`. Não há componente de loja, carrinho, urgência artificial nem preços riscados.

## Links no texto de um artigo

Dentro de uma entrada de `sections`, usar referências ao mesmo catálogo:

```json
"productLinks": [
  { "productId": "id-do-produto-real", "label": "Consultar este modelo na Worten" }
]
```

O gerador renderiza os links em parágrafos do artigo e aplica os mesmos atributos, tracking e divulgação. Os parágrafos são texto simples e escapado, não HTML livre.

## Novos anunciantes e artigos

Para outro anunciante Awin, acrescentar uma entrada em `merchants` com um ID próprio, `name`, `network: "awin"`, `advertiserId`, `allowedDestinationHosts` e `cta`. Exemplo de CTA: `Ver oferta`. O `publisherId` é partilhado. Associar os produtos pelo campo `merchant`. Não é necessário editar componentes.

Os domínios de destino são uma lista exata: incluir apenas os domínios reais do anunciante. O gerador rejeita protocolos inseguros, credenciais em URLs, IDs duplicados e deep links que não correspondam ao anunciante ou publisher configurados. Links curtos precisam de verificação manual do destino na Awin.

Para um novo artigo, copiar `templates/article.json` para `articles` em `data/recommendations.json`, preencher o conteúdo, escolher um `slug` único e executar o gerador. Os seis guias iniciais servem de exemplos por categoria. O índice e o sitemap são atualizados automaticamente. Ao remover ou mudar um slug, remover também o respetivo HTML antigo ou preparar o redirecionamento: o gerador não apaga diretórios.

## Preparação para feeds

O adaptador segue as colunas do [feed de produtos da Awin](https://help.awin.com/developers/docs/product-feed-publisher-guide-intro), com os [campos disponibilizados para download](https://help.awin.com/developers/docs/product-feed-list-download).

Mapeamento: `aw_deep_link` → `affiliateUrl`, `merchant_deep_link` → `destinationUrl`, `product_name` → `name`, `merchant_image_url`/`aw_image_url` → `image`, `search_price`/`currency` → `price`, e IDs/data/stock → `source`. A data do preço vem de `last_updated`, não da data de importação. Sem data válida não se apresenta um preço.

Depois de configurar o `advertiserId`, descarregar o CSV da Awin fora da pasta publicada ou para `private-feeds/` (ignorada pelo Git). Não guardar o URL privado de download nem a API key no repositório.

```powershell
python tools/import_awin_feed.py private-feeds/worten.csv --merchant worten-pt --output private-feeds/worten-drafts.json
```

Usar `--delimiter ";"` se o CSV tiver ponto e vírgula. O ficheiro de saída deve ser novo. A importação valida `merchant_id`, exige links da rede e rejeita IDs duplicados. Não altera produtos existentes: cria apenas rascunhos para rever e incorporar no catálogo.

Uma futura tarefa automática deve descarregar no servidor/CI com segredos protegidos, chamar este adaptador, comparar produtos por `source.merchantProductId`/`source.awinProductId` e atualizar os campos comerciais sem substituir descrições ou escolhas editoriais. A descarga periódica e a publicação automática não foram ativadas.

## Testar agora, sem conta Awin

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/affiliate-analytics.test.cjs
python tools/preview_recommendations.py
```

Abrir [a demonstração local](http://127.0.0.1:4174/__preview__/?affiliate_debug=1). O produto e o preço fictícios só existem em memória neste servidor, nunca nas páginas publicadas. O destino dos links é local e o `gtag` é simulado: não há cliques enviados à Awin nem eventos enviados à Google.

- Recusar e clicar num CTA: não deve aparecer nenhum evento no painel da demonstração.
- Abrir «Preferências de cookies», aceitar e clicar: aparece `affiliate_click` com `merchant`, `product_name`, `page` e `position`.
- Experimentar o link de texto: a posição muda de `recommendation-1` para `inline-1-1`.
- Verificar o componente em telemóvel e desktop, com e sem preço.

Pré-visualização do site completo: `python -m http.server 4173 --bind 127.0.0.1`, depois abrir `/recomendacoes/`. Não é preciso instalar pacotes Python nem dependências npm.

## Validar no GA4 quando existirem links reais

1. Abrir um guia com um produto publicado e acrescentar `?affiliate_debug=1` ao endereço.
2. Aceitar analytics no banner ou nas preferências. É usada a mesma chave `pulsarfm-consent` da homepage. Se não houver consentimento, o evento de afiliado não é enviado.
3. Clicar no link. Na consola aparece `[PulsarFM] affiliate_click`. Para inspecionar a fila:

   ```javascript
   (window.dataLayer || []).filter(item => item[0] === 'event' && item[1] === 'affiliate_click')
   ```

4. No GA4 da propriedade `G-YRD1BYXB78`, abrir **Administração → Apresentação de dados → DebugView**. O parâmetro da URL ativa `debug_mode` apenas para os eventos de afiliado dessa visita, de acordo com a [documentação do DebugView](https://support.google.com/analytics/answer/7201382?hl=en).
5. Confirmar os quatro campos: `merchant` é o ID do anunciante no catálogo (por exemplo `worten-pt`), `product_name` é o nome, `page` é apenas o caminho da página, `position` identifica o CTA ou link editorial. Para os usar em relatórios personalizados, registar as quatro dimensões de âmbito Evento em Definições personalizadas.
6. Recusar nas preferências e clicar novamente: não deve haver um novo evento. Bloqueadores de analytics podem impedir o envio mesmo com consentimento; a presença na `dataLayer` confirma a emissão local, o DebugView confirma a receção pela Google.

O evento no GA4 mede cliques; não prova atribuição de vendas na Awin. Com links reais e o programa ativo, verificar o redirecionamento para o produto e o registo de cliques no painel Awin. Essa validação depende da conta e não foi feita nesta implementação.

## Publicação

As páginas geradas devem acompanhar os dados, assets e templates no commit. Seguir o fluxo habitual do projeto: rever as alterações e fazer push para `main` quando quiseres publicar. Esta implementação não faz commit, push nem alterações na conta Awin/GA4.
