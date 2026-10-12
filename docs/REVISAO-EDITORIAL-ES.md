# Revisão editorial da edição espanhola

Concluída em 12/10/2026. Foram revistos os oito guias, as descrições dos 16 produtos, as sete categorias, homepage, oito géneros, avisos comerciais e texto de privacidade/consentimento. As correções estão nos dados e no gerador; o HTML foi regenerado. Não houve publicação.

A revisão seguiu docs/VOZ.md: informação útil primeiro, frases claras, espanhol de Espanha e afirmações apoiadas em documentação. Não acrescentou experiências pessoais, testes de produtos, preços ou disponibilidade.

## Alterações aplicadas

| Área | Correção |
| --- | --- |
| Títulos dos guias | As seleções de poucos modelos deixaram de se apresentar como rankings dos «melhores». Mantêm as palavras de pesquisa e indicam a decisão concreta: formato, ANC, portátil/estéreo ou USB. URLs conservadas. |
| Espanhol | Corrigidos «watts» para «vatios», «en un manual» para «en un modelo manual» e as descrições de entradas de micrófono e instrumento. Explicados on-ear, over-ear, ANC e antiskating quando ajudam a escolher. |
| Auriculares | Melhor distinção entre formato e utilização; WH-CH720N/XM5 comparados por peso, autonomia declarada e códecs, sem atribuir desempenho medido. |
| Altavoces / Hi-Fi | Explicitado o custo do conjunto e a diferença entre par ativo e amplificador para caixas passivas. A tabela não promete que produtos diferentes sejam equivalentes em som ou potência. |
| Tocadiscos | Clarificados os ajustes de modelos manuais, a cadeia PHONO/LINE e a função de digitalização USB. |
| Home studio | Interface descrita como equipamento de áudio, sem tratar XLR como tipo de sinal. Orçamento dividido por necessidades, com suporte e cabos incluídos. |
| Micrófonos | Limitações mais úteis; diferenciadas a ligação XLR analógica e as funções do software RØDE por USB. |
| Accesorios | Eliminada a oposição ambígua «adaptador vs DAC». Explicada a conversão e a limitação do microfone no KA11, sem prometer ganho sonoro. |
| Fontes | Sony WH-CH520 passa a ligar também à página que sustenta as 50 horas anunciadas. RØDE passa a ter documentação complementar sobre XLR/software. |
| Rádio e géneros | Redação mais natural e oito respostas de mobile diferentes, usando funções reais existentes. Reduzida repetição de avisos e afirmações defensivas. |
| Consentimento | Texto espanhol deixa de afirmar que Google só é ativado após aceitar na rádio. O aviso passa a mencionar análise e opções de publicidade, que já são autorizadas em conjunto pela implementação. Corrigida a promessa de atualização instantânea de todas as páginas abertas. |

A transparência de afiliação e a indicação de que os produtos não foram testados pela redação permanecem visíveis. Não alterámos permissões, analytics ou a implementação do player nesta revisão.

## Equivalências PT/ES

Retiradas três associações de hreflang cuja intenção principal é diferente:

- Auriculares PT apenas de formato compacto vs seleção ES com diadema.
- Colunas PT para levar vs guia ES de portátil ou sistema fixo para casa.
- Acessórios PT gerais vs guia ES centrado em adaptadores/DAC.

Mantêm-se canonical próprio e ligações normais para escolher o outro mercado. A decisão editorial é conservadora: temas relacionados não foram apresentados como traduções equivalentes. A documentação [Google sobre versões localizadas](https://developers.google.com/search/docs/specialty/international/localized-versions) explica o uso de hreflang para variantes do mesmo conteúdo.

## Fontes consultadas nas correções

- [Sony WH-CH520](https://www.sony.es/headphones/products/wh-ch520) e [especificações](https://www.sony.es/electronics/support/wireless-headphones-bluetooth-headphones/wh-ch520/specifications): autonomia anunciada e ausência de entrada de áudio.
- [Sony WH-CH720N](https://www.sony.es/electronics/support/wireless-headphones-bluetooth-headphones/wh-ch720n/specifications): peso, autonomia com ANC e códecs.
- [RØDE: ligação XLR e software](https://help.rode.com/hc/en-us/articles/16702089296783-Why-Won-t-R%C3%98DE-Software-Detect-My-XLR-Connected-R%C3%98DE-Microphone): funções acessíveis por USB.
- [FiiO KA11](https://www.fiio.com/newsinfo/895480.html): micrófono do cabo não suportado.
- [Apple: auriculares e adaptadores](https://support.apple.com/es-es/108042): ligação USB-C / 3,5 mm.
- [Focusrite Scarlett Solo](https://focusrite.com/products/scarlett-solo), [Soundcore P20i](https://www.soundcore.com/products/p20i), [JBL Flip 7](https://www.jbl.com/FLIP-7.html), [Edifier R1280DB](https://us.edifier.com/products/r1280db) e manuais Audio-Technica já associados aos produtos: ligações e características usadas nas comparações.
- [Google Consent Mode](https://developers.google.com/tag-platform/security/concepts/consent-mode): distinção entre carregamento condicionado e sinais sem cookies. A redação foi comparada com o código local.

## Validação

Build completo PT/EN/ES; lint de 58 páginas e 1.346 ligações internas; 36 scripts com sintaxe válida; 37 testes Python e 492 subtestes; oito testes Node de analytics; git diff --check. Tudo passou. A verificação Chrome cobre desktop/mobile, navegação, rádio, conteúdo sem JavaScript e consentimento. As evidências atuais ficam em docs/qa-es.

Dados PT, ASINs, produtos selecionados e IDs pulsarfm-21 / pulsarfmes-21 preservados. Registo dos campos alterados em qa-es/editorial-changes.json e resultados em qa-es/editorial-checks.json.

## Estado antes de publicar

A revisão editorial pedida está concluída. Continua pendente a confirmação operacional de variantes, vendedores e stock Amazon, separada desta revisão; a data anterior das fichas não foi renovada. As validações da conta Amazon, GA4/Search Console e a revisão jurídica previstas no relatório de expansão também não foram substituídas por esta revisão de texto.
