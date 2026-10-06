# Afiliados na PulsarFM (Amazon.es)

## Estado e integração

A secção `/recomendacoes/` é monetizada pelo Programa de Afiliados da Amazon.es, com o tracking ID **`pulsarfm-21`**. É o único ID permitido em toda a PulsarFM: o gerador recusa qualquer outro, incluindo o de outros sites do mesmo dono.

O catálogo tem 30 produtos em seis guias, todos com `linkType: "affiliate"` e `merchant: "amazon-es"`. Cada guia cobre várias gamas de preço (económico, médio, premium). Cada ASIN foi confirmado na Amazon.es a 06/10/2026: o produto existe, está em stock e tem botão de compra, sem ser apenas em segunda mão. Os modelos que existiam antes e não estavam disponíveis na Amazon.es foram substituídos:

| Antes | Agora | Motivo |
| --- | --- | --- |
| JBL Tune 770NC | Soundcore Space One | Só em revendedores externos |
| Marshall Emberton II | Marshall Emberton III | Revendedor externo, envio lento; o III é o modelo atual |
| Sony HT-SF150 | Samsung HW-B400F | Só em segunda mão |
| LG S40T | Samsung HW-B46CF | Só em segunda mão |
| HyperX QuadCast 2 | Samson Q2U | Só em segunda mão |
| Fonestar Bluetooth 2 em 1 | UGREEN Bluetooth 2 em 1 | Indisponível |
| Trust GXT 260 | New Bee suporte de auscultadores | Não está à venda na Amazon.es |

Não mostramos preços: mudam constantemente e não há integração automática (PA-API). O CTA é «Ver preço na Amazon». Não apresentamos produtos como testes da redação.

**Imagens:** as regras do programa só permitem imagens da Amazon obtidas pela PA-API ou por links fornecidos pela própria Amazon, alojadas nos servidores dela. Não descarregar nem copiar fotografias da Amazon. Enquanto não houver acesso à PA-API (exige vendas qualificadas), os cartões usam a ilustração animada da categoria (`img/gear/*.svg`, mapeada em `categoryImages` no `data/affiliates.json` pelo campo `category` do produto), sem campo `image` no produto. Uma categoria sem ilustração cai para `img/gear-editorial.svg`. Se um dia houver uma imagem autorizada, basta preencher `image` e `imageAlt`. Atenção: uma imagem servida pela Amazon liga o browser do visitante aos servidores dela; atualizar a política de privacidade nesse momento.

O site continua estático e compatível com GitHub Pages. O HTML é gerado antes da publicação: conteúdo, links e divulgação existem sem JavaScript.

## Ficheiros

| Ficheiro | Função |
| --- | --- |
| `index.html` | Entrada discreta no rodapé e texto PT/EN |
| `privacidade.html` | Divulgação de afiliados da Amazon e explicação do evento |
| `sitemap.xml` | Inclui a secção e os seis guias |
| `data/affiliates.json` | Lojas (`amazon-es`) e catálogo central de produtos |
| `data/recommendations.json` | Conteúdo e produtos selecionados para cada guia |
| `templates/product.json`, `templates/article.json` | Exemplos para novas entradas, não publicados automaticamente |
| `templates/recommendations/page.html` | Estrutura comum das páginas e controlos de consentimento |
| `templates/recommendations/article.html` | Template editorial reutilizável |
| `templates/recommendations/product.html` | Componente de recomendação com imagem, descrição, preço opcional e CTA |
| `templates/recommendations/disclosure.html` | Divulgação de afiliados reutilizável (a frase da Amazon entra automaticamente) |
| `assets/recommendations.css` | Estilos responsivos isolados das páginas da rádio |
| `assets/affiliate-analytics.js` | Consentimento, evento `affiliate_click`, fallback de imagem e validade de preços |
| `img/gear-editorial.svg` | Ilustração editorial local, usada nos cartões |
| `tools/gen_recommendations.py` | Validação e geração das sete páginas estáticas e sitemap |
| `tools/import_awin_feed.py` | Adaptador CSV da Awin (inativo, ver abaixo) |
| `tools/preview_recommendations.py` | Demonstração local com produto fictício e analytics simulado |
| `tests/test_affiliates.py`, `tests/affiliate-analytics.test.cjs` | Validação de links, HTML, importação e tracking |
| `recomendacoes/index.html`, `recomendacoes/*/index.html` | HTML gerado, a incluir no commit; não editar diretamente |
| `docs/PRODUCT.md`, `docs/DESIGN.md`, `docs/VOZ.md` | Marca, design e voz editorial |

## Estrutura de um produto

Em `data/affiliates.json`, dentro de `products`:

```json
{
  "id": "sony-wh-ch520",
  "status": "published",
  "linkType": "affiliate",
  "merchant": "amazon-es",
  "asin": "B0BTJD6LCL",
  "name": "Sony WH-CH520",
  "category": "Auscultadores",
  "description": "Texto editorial: para quem serve, porque foi escolhido, principal limitação.",
  "bestFor": "Primeira compra sem fios, uso casual em casa",
  "pros": ["Leves", "Até 50 h de autonomia segundo a Sony"],
  "cons": ["Sem cancelamento de ruído"],
  "price": null,
  "source": { "type": "manual", "checkedAt": "2026-10-06", "referenceUrl": "https://www.amazon.es/dp/B0BTJD6LCL/" }
}
```

- **O link não se escreve à mão.** O gerador constrói `https://www.amazon.es/dp/<ASIN>/?tag=pulsarfm-21` a partir de `asin` e do `trackingId` da loja `amazon-es`. Um ASIN inválido ou outro tracking ID faz a geração falhar.
- `category` é obrigatória e vai para o evento GA4 (`product_category`).
- `bestFor`, `pros` e `cons` ficam **só nos dados**, para escolhas editoriais e futuras trocas. Não aparecem na página. A justificação visível está em `description`.
- `price` fica `null`. O suporte a preço datado continua no gerador (desaparece após sete dias), mas não deve ser usado sem uma fonte automática.

## Adicionar ou trocar um produto

1. Na Amazon.es, confirmar o modelo exato, a cor, o stock e o vendedor. Rejeitar ofertas só em segunda mão («Segunda mano») e preferir produtos vendidos ou enviados pela Amazon ou pela loja oficial da marca.
2. Copiar `templates/product.json` para `products`, com um `id` único (minúsculas, números, hífen) e o ASIN da página `/dp/<ASIN>`.
3. Escrever `description` segundo `docs/VOZ.md`: factos com a fonte («segundo a Sony»), sem preços, descontos, «testámos» ou superlativos de folheto.
4. Mudar `status` para `published` e acrescentar o ID a `productIds` do artigo em `data/recommendations.json` (a ordem do array é a ordem dos cartões). Rever etiquetas, tabela comparativa e FAQ que mencionem o produto antigo.
5. Atualizar `updatedAt` do artigo e da secção e executar:

   ```powershell
   python tools/gen_recommendations.py
   ```

Um produto em rascunho não aparece no HTML. Referências a IDs inexistentes fazem a geração falhar, em vez de desaparecerem em silêncio.

Os links de afiliado têm `target="_blank"`, `rel="sponsored nofollow noopener noreferrer"` e indicação acessível de link de afiliado em nova aba. A divulgação aparece automaticamente no topo dos artigos com links de afiliado, com a frase exigida pelo programa: «Como Afiliado da Amazon, a PulsarFM recebe por compras elegíveis.» Não há componente de loja, carrinho, urgência artificial nem preços riscados. Evitar CTAs como «Comprar já», «Melhor preço» ou «Mais barato».

## Links no texto de um artigo

Dentro de uma entrada de `sections`, usar referências ao mesmo catálogo:

```json
"productLinks": [
  { "productId": "sony-wh-ch720n", "label": "Ver os Sony WH-CH720N na Amazon" }
]
```

O gerador renderiza os links em parágrafos do artigo e aplica os mesmos atributos, tracking e divulgação. Os parágrafos são texto simples e escapado, não HTML livre.

## Etiquetas, tabela comparativa e FAQ

Campos opcionais de cada artigo em `data/recommendations.json` (texto simples, sempre escapado):

```json
"badges": { "sony-wh-ch520": "Económico" },
"comparison": {
  "heading": "Comparação rápida",
  "caption": "Descrição da tabela para leitores de ecrã",
  "columns": ["Modelo", "Formato", "..."],
  "rows": [["Sony WH-CH520", "On-ear", "..."]],
  "note": "Valores indicados pelos fabricantes."
},
"faq": [{ "q": "Pergunta?", "a": "Resposta." }]
```

`badges` só aceita IDs presentes em `productIds` do mesmo artigo; cada linha de `rows` tem de ter uma célula por coluna (a primeira é o cabeçalho da linha). A FAQ gera a secção visível e o JSON-LD `FAQPage` a partir do mesmo texto. As etiquetas indicam a gama (Económico, Gama média, Premium), nunca valores em euros.

## SEO e conversão (campos do artigo)

| Campo | Para quê |
| --- | --- |
| `seoTitle` | `<title>` e `og:title` pensados para pesquisa ("Melhores … 2026"), com pt-PT e pt-BR (caixa de som, toca-discos, barra de som, fones). O H1 continua a ser `title`. |
| `metaDescription` | Meta description com 140–155 caracteres, a nomear 2–4 modelos. Sem ela usa-se `summary`. |
| `publishedAt` | Data de publicação para o JSON-LD `Article` (`updatedAt` é a `dateModified`). |
| `related` | Os dois guias de "Mais para a tua próxima sessão", escolhidos por tema. Um slug inexistente falha a geração. Garantir que todos os guias recebem pelo menos um link. |
| `quickPicks` | Caixa "Escolhas rápidas" logo após a divulgação: `[{ "label": "Económico", "productId": "…", "note": "Frase curta." }]`. O produto tem de estar em `productIds`. Cada escolha liga ao cartão (`#product-<id>`) e à Amazon (posição GA4 `quick-N`). |
| `comparison.rowProducts` | Um ID de produto (ou `null`) por linha da tabela: põe "Ver na Amazon" por baixo do nome do modelo (posição `table-N`). |

O gerador acrescenta automaticamente o JSON-LD `BreadcrumbList`, `Article` e `ItemList` (produtos) a cada guia, e `BreadcrumbList` + `ItemList` (guias) ao hub, além do `FAQPage` já existente. Não usamos `Product` com ofertas: sem preço nem avaliações, seria marcação inválida.

As páginas de género também levam aos guias pela caixa GEAR (`GEAR` em `tools/gen_genre_pages.py`). Desde 06/10/2026, a página Pop liga a Tecnologia e acessórios.

## Novos artigos

Copiar `templates/article.json` para `articles` em `data/recommendations.json`, preencher o conteúdo seguindo `docs/VOZ.md`, escolher um `slug` único e executar o gerador. O índice e o sitemap são atualizados automaticamente. Ao remover ou mudar um slug, remover também o HTML antigo ou preparar o redirecionamento: o gerador não apaga diretórios.

## Analytics

Com consentimento de análise (chave `pulsarfm-consent`, a mesma da homepage), cada clique num link de afiliado envia ao GA4 existente (`G-YRD1BYXB78`) o evento `affiliate_click`:

| Parâmetro | Exemplo |
| --- | --- |
| `affiliate_platform` | `amazon` |
| `tracking_id` | `pulsarfm-21` |
| `product_name` | `Sony WH-CH520` |
| `product_category` | `Auscultadores` |
| `page_path` | `/recomendacoes/melhores-auscultadores/` (sem query string) |
| `destination_url` | `https://www.amazon.es/dp/B0BTJD6LCL/?tag=pulsarfm-21` |
| `position` | `recommendation-1` (cartão) ou `inline-3-1` (link no texto) |

Sem consentimento não há evento: o link abre na mesma. Não existe nenhum outro analytics nem script da Amazon.

### Validar no GA4

1. Abrir um guia com `?affiliate_debug=1` no endereço.
2. Aceitar analytics no banner ou em «Preferências de cookies».
3. Clicar num link. Na consola aparece `[PulsarFM] affiliate_click`. Para inspecionar a fila:

   ```javascript
   (window.dataLayer || []).filter(item => item[0] === 'event' && item[1] === 'affiliate_click')
   ```

4. No GA4, abrir **Administração → Apresentação de dados → DebugView**. O parâmetro da URL ativa `debug_mode` apenas para os eventos de afiliado dessa visita.
5. Para usar os parâmetros em relatórios, registá-los como dimensões personalizadas de âmbito Evento em **Definições personalizadas**.
6. Recusar nas preferências e clicar outra vez: não deve haver novo evento.

O evento mede cliques; as vendas e comissões são confirmadas no painel de Afiliados da Amazon (relatórios por tracking ID `pulsarfm-21`).

## Testes

```powershell
python -m pytest -q tests
node --test tests/affiliate-analytics.test.cjs
```

Os testes garantem, entre outras coisas, que todos os links de afiliado das páginas publicadas apontam para `www.amazon.es` com `tag=pulsarfm-21` e mais nenhum parâmetro, que outro tracking ID falha a geração, que `pros`/`cons`/`bestFor` não chegam ao HTML e que o texto «sem comissão» não volta a aparecer.

Pré-visualização do site completo: `python -m http.server 4173 --bind 127.0.0.1`, depois abrir `/recomendacoes/`. Não testar cliques com links reais em massa: geram cliques sem compra na conta de afiliado.

## Suporte Awin (inativo)

O gerador mantém o suporte à rede Awin (deep links `cread.php`, links `pclick.php`/`tidd.ly` e o importador de feeds `tools/import_awin_feed.py`), coberto pelos testes. Não há lojas Awin no catálogo. Para reativar, acrescentar em `data/affiliates.json` um bloco `"awin": { "publisherId": "..." }` e uma loja com `network: "awin"`, `advertiserId`, `allowedDestinationHosts` e `cta`; o link pronto vai em `affiliateUrl` ou é gerado a partir de `destinationUrl`. A política de privacidade teria de voltar a mencionar a Awin.

## Publicação

As páginas geradas devem acompanhar os dados, assets e templates no commit. Seguir o fluxo habitual do projeto: rever as alterações e fazer push para `main` quando quiseres publicar.
