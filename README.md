# Site Oxyn Group

Site institucional da Oxyn Group, holding das frentes Oxyn Comercial, Oxyn Pessoas, Oxyn IA, Naia (GEO e SEO), FQDTV e Oxyn Estúdio.

Site estático (HTML, CSS e JS puros), pronto para a Vercel. Estrutura baseada no template "Corporate Navy", com a identidade do **Manual de Marca Oxyn Group v1.0** (set/2026).

## Rodar localmente

```bash
python3 scripts/dev-server.py
```

Abra http://localhost:4173. O servidor imita as URLs limpas da Vercel (`/solucoes/comercial` serve `solucoes/comercial.html`).

## Editar conteúdo

Os textos das 7 páginas ficam em `scripts/build.py` (lista `UNITS`, `LEADERS`, `SECTORS` e as funções `home()` e `unit_page()`). Depois de editar:

```bash
python3 scripts/build.py
```

O script sobrescreve `index.html`, `solucoes/*.html` e `sitemap.xml`. Não edite esses HTML direto: a próxima geração apaga a mudança.

## Estrutura

| Caminho | O que é |
|---|---|
| `index.html` | Home da holding |
| `solucoes/*.html` | Uma página por empresa do grupo |
| `assets/css/styles.css` | Design system: tokens da marca em `:root` (seção 1) e elementos do manual (seção 10) |
| `assets/js/main.js` | Nav, menu mobile, contadores, animações de entrada, cookies |
| `assets/img/` | Logos oficiais, anel, fotos do manual e favicon |
| `scripts/build.py` | Gerador das páginas (conteúdo) |
| `scripts/sprite.svg` | Ícones (estilo Lucide) |
| `_design/` | Template original de referência (não vai para produção) |

## Regras de marca aplicadas

- Paleta: Azul Oxyn `#1A82A2`, Céu, Névoa, Cinza Claro, Preto; Âmbar só em um botão por página.
- Montserrat para tudo; Barlow Light para números e dados. Títulos em caixa alta.
- Sem degradês entre cores da marca. Anel como marca d'água (8% a 16%), fios finos na composição assinatura.
- Vocabulário: evitar "previsibilidade", "performance", "garantido", superlativos. Todo número com fonte.
- Não usar travessão nos textos.

## Deploy (Vercel)

Importar o repositório na Vercel como projeto estático (sem build). `vercel.json` liga `cleanUrls`; `.vercelignore` tira `_design/` e `scripts/` do deploy.
