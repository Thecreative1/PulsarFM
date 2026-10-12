# Conversão da estrutura editorial PT para ES — 12/10/2026

O portal espanhol passa a usar o mesmo menu de 13 guias e a mesma ordem, hierarquia visual e ilustrações da edição portuguesa. O menu liga diretamente aos guias; as páginas de categoria anteriormente publicadas continuam disponíveis.

- 13 guias principais: Regalos, Cascos, Auriculares, Para niños, Altavoces Bluetooth, Altavoces para PC, Barras de sonido, Para la TV, Tocadiscos, Amplificación, Home Studio, Micrófonos e Accesorios.
- Os 73 produtos e as escolhas rápidas de cada guia português estão presentes na edição espanhola, com descrições, vantagens, limites, tabelas, FAQs e ligações entre guias em espanhol.
- Os dois guias espanhóis específicos de ANC no trabalho e de iniciação Hi-Fi continuam como leituras complementares. Nenhuma URL espanhola anterior foi removida.
- Os 13 pares de guias têm navegação PT/ES e hreflang recíproco.
- Amazon ES usa pulsarfmes-21. Os 313 hrefs Amazon portugueses são idênticos à versão publicada 88edad4 e continuam com pulsarfm-21.

## Revisão editorial e fontes

A adaptação preserva os temas e a seleção, mas corrige afirmações que não devem ser transpostas literalmente: ANC de escuta versus chamadas, Bluetooth de receção versus transmissão, USB para energia versus áudio, ligações phono versus linha, configurações DJI/FIFINE e variantes Philips SHC5200. O guia infantil usa a fonte primária da OMS e explica que um limite anunciado de 85 dB não garante segurança independentemente do tempo de escuta.

As fontes estão registadas em data/recommendations.es.json e apresentadas nos produtos. A data de verificação dos anúncios do catálogo mantém-se em 06/10/2026: não houve nova confirmação de stock, preço ou vendedor. EarFun com fio conserva a referência do catálogo, identificada como tal, sem afirmar consulta recente de um manual ainda não identificado. FIFINE, Americanflat e o cabo UGREEN têm notas explícitas de confirmação da variante, para não atribuir características de outra referência.

Não existem preços estáticos, fotografias da Amazon, experiências pessoais inventadas nem classificações de testes.

## Validação antes de publicar

- Build estático concluído; 71 URLs no sitemap, 39 espanholas e 1936 ligações internas válidas.
- Pytest: 38 testes e 1134 subtestes aprovados.
- Analytics: 8 testes aprovados; 36 scripts da aplicação passaram a verificação de sintaxe.
- Navegador: todos os 13 botões e guias abertos em desktop e mobile, com seleção, tabela, escolhas rápidas, idioma correspondente e largura verificados. Sem erros JavaScript.
- Rádio: player pronto, 64 estações, PT/ES/EN, persistência, filtros, skins e descodificação de áudio CORS aprovados.
- Consentimento: um evento de afiliado simulado com consentimento, nenhum após revogação; pedidos Google Analytics e Amazon bloqueados durante o teste.
- Páginas sem JavaScript, rotas PT/EN e hrefs portugueses preservados.

Evidência: docs/qa-es/browser-results.json, parity-checks.json e screenshots. O smoke test em produção fica em docs/qa-es/live/.
