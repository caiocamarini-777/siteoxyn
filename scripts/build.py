"""Gera as paginas HTML do site Oxyn (home + 6 solucoes) a partir de dados.
Uso (na raiz do repo): python3 scripts/build.py
Edite os textos aqui e rode o script; ele sobrescreve index.html, solucoes/*.html e sitemap.xml.
"""
import json, sys, pathlib, hashlib

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
SITE = "https://oxyngroup.com.br"
WA = "https://wa.me/5511979706449?text=Ol%C3%A1%2C%20quero%20falar%20com%20um%20especialista%20da%20Oxyn."
WA_NUM = "5511979706449"
def wa_oferta(oferta):
    """Link de WhatsApp que ja chega com o nome da oferta, para a equipe saber em qual o cliente clicou."""
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUM}?text=" + quote(f"Olá! Vi no site da Oxyn e quero conversar sobre: {oferta}.")
def slugify(t):
    import unicodedata, re
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")
EMAIL = "comercial@oxyngroup.com.br"
PHONE = "+55 11 97970-6449"
IG = "https://www.instagram.com/oxyn_group/"
LI = "https://www.linkedin.com/company/oxyn-group/"

# --------------------------------------------------------------------------
# O Oxyn Group sao 4 empresas: a Oxyn (frentes Vendas, Pessoas e IA), Naia, FQDTV e FQD Studios.
# Oxyn Vendas (antes "Comercial" no manual) e Oxyn Pessoas seguem o manual de marca;
# o nome "Oxyn IA" e de trabalho: validar com a diretoria.
# --------------------------------------------------------------------------
UNITS = [
  dict(slug="vendas", unit="Oxyn Vendas", short="Vendas", icon="i-trend", color="blue", img="foto-leao.jpg",
       card="Consultoria comercial B2B. Diagnóstico primeiro; depois reestruturamos o time, treinamos a equipe ou assumimos a operação de vendas.",
       tags=["Diagnóstico comercial", "Treinamento", "Operação terceirizada"],
       menu="Consultoria comercial e operação de vendas",
       title="Consultoria comercial B2B e terceirização de vendas",
       eyebrow="Oxyn Vendas · Frente principal",
       h1_thin="Antes de vender mais,", h1="entenda o que trava suas vendas.",
       lead="Começamos pelo diagnóstico e, a partir dele, definimos o caminho: reestruturar o time comercial, treinar a equipe atual ou assumir a operação de vendas como parte da sua empresa.",
       pains_h2="Onde a venda trava na sua empresa?",
       pains=[("i-chart","Resultado instável","Meses bons e meses ruins sem saber por quê. Falta cadência e critério claro de qualificação."),
              ("i-users","Energia no lead errado","Time ocupado com contas de baixo potencial, propostas genéricas e ciclos que se arrastam."),
              ("i-database","Gestão sem dados","CRM desatualizado, funil sem indicadores e decisões tomadas por sensação."),
              ("i-layers","Sem processo e definições claras","Ninguém sabe ao certo quem faz o quê, em qual etapa e com qual critério. Cada vendedor vende do seu jeito.")],
       deliv_eyebrow="", deliv_h2="Como a Oxyn faz você vender mais", deliv_cta="Quero conversar sobre isso",
       deliv=[("i-target","Consultoria de vendas e performance","Diagnóstico de processo, time, carteira e mercado, com plano de ação e acompanhamento dos indicadores comerciais."),
              ("i-layers","Reestruturação de operações","Redesenho de papéis, perfis, metas, remuneração e rituais da área comercial."),
              ("i-users","Treinamento comercial","Capacitação do time em método, prospecção e negociação com a metodologia D.R.I.V.E."),
              ("i-award","Mentoria","Acompanhamento individual de líderes e gestores comerciais para decidir melhor e conduzir o time."),
              ("i-handshake","Terceirização de operação comercial","A Oxyn assume a operação comercial como o time da sua empresa, com metas e rituais compartilhados.")],
       how_eyebrow="Metodologia", how_h2="D.R.I.V.E., de ponta a ponta no processo comercial",
       how_lead="Nosso método para vendas complexas: da escolha das contas certas até o fechamento, com dados em cada etapa.",
       how=["<b>Descoberta:</b> quais empresas, perfis e decisores têm maior potencial de receita e fit operacional",
            "<b>Ranqueamento:</b> a energia do time concentrada nos leads com maior chance de conversão",
            "<b>Investigação:</b> escuta estruturada das motivações, restrições e dependências do comprador",
            "<b>Validação:</b> o diagnóstico vira uma proposta clara, personalizada e financeiramente viável",
            "<b>Execução:</b> acompanhamento até o fechamento, retroalimentando o sistema com dados"],
       connects=["inteligencia-artificial","pessoas","naia-geo-seo"],
       faq=[("Qual a diferença entre reestruturar, treinar e operar?","Reestruturar é redesenhar o time: papéis, perfis, metas e rituais. Treinar é capacitar o time atual em método, prospecção e negociação. Operar é a Oxyn assumir a área comercial como o time da sua empresa."),
            ("Por que começar pelo diagnóstico?","Porque contratar mais vendedores raramente resolve. Na maioria dos casos, o problema está antes: no perfil de cliente mal definido ou em um funil sem critério de priorização. O diagnóstico mostra se o gargalo está no processo, no time ou no mercado."),
            ("A Oxyn representa a minha marca?","Não representamos marcas: vestimos a camisa. Quando faz sentido, assumimos a operação comercial com a sua marca, metas, rituais e indicadores compartilhados.")]),
  dict(slug="inteligencia-artificial", unit="Oxyn IA", short="Inteligência Artificial", icon="i-cpu", color="blue", img="foto-abstrato-escuro.jpg",
       card="Consultoria em IA, treinamento e padronização do uso de IA pelo time e desenvolvimento de soluções personalizadas, para a empresa inteira.",
       tags=["Consultoria em IA", "Treinamento e padronização", "Soluções sob medida"],
       menu="Consultoria, treinamento e soluções de IA",
       title="Consultoria, treinamento e soluções de inteligência artificial para empresas",
       eyebrow="Oxyn IA · Inteligência artificial",
       h1_thin="Inteligência artificial", h1="aplicada à empresa inteira.",
       lead="Fazemos consultoria para identificar onde a IA gera retorno, treinamos e padronizamos o uso de IA pelo seu time e desenvolvemos soluções personalizadas com IA. Em vendas, atendimento, marketing, financeiro, RH e operação: onde houver ganho.",
       pains_h2="A IA já chegou na sua empresa ou só no discurso?",
       pains=[("i-message","IA só no discurso","A empresa sabe que precisa, mas não sabe por onde começar nem como medir o retorno."),
              ("i-zap","Horas em tarefa repetitiva","Relatórios, atendimento, propostas e conferências manuais tomando o tempo de todas as áreas."),
              ("i-layers","Cada um usa de um jeito","Cada área testa uma ferramenta diferente, sem padrão, governança nem segurança de dados.")],
       deliv_h2="Como a Oxyn IA leva a IA para a sua empresa", deliv_cta="Quero conversar sobre isso",
       deliv=[("i-target","Consultoria em IA","Diagnóstico de processos e maturidade, mapa de oportunidades priorizado por retorno e plano de adoção para cada área da empresa."),
              ("i-users","Treinamento e padronização","Capacitação prática por área e padrões de uso: ferramentas aprovadas, prompts, fluxos de trabalho e regras de segurança de dados."),
              ("i-cpu","Soluções personalizadas com IA","Desenvolvimento de agentes, automações e sistemas sob medida, integrados às ferramentas que a sua empresa já usa.")],
       how_eyebrow="Como funciona", how_h2="Pilotos curtos, resultados medidos",
       how_lead="Começamos pequeno, provamos valor com indicadores e só então escalamos para outras áreas.",
       how=["Diagnóstico de processos e maturidade digital em cada área",
            "Priorização de casos de uso por impacto e esforço",
            "Treinamento do time e padronização do uso de IA",
            "Desenvolvimento e integração de soluções personalizadas",
            "Acompanhamento da adoção e dos indicadores de cada piloto"],
       connects=["vendas","pessoas","naia-geo-seo"],
       faq=[("A Oxyn IA atua só em vendas?","Não. Atuamos na empresa inteira: vendas, atendimento, marketing, financeiro, RH e operação. Onde houver tarefa repetitiva ou decisão que se beneficia de dados, a IA pode gerar ganho."),
            ("O que significa padronizar o uso de IA?","É definir quais ferramentas usar, para quê e com quais regras: políticas de uso, proteção de dados, prompts e fluxos de trabalho por área, para que todo o time use IA do mesmo jeito e com segurança."),
            ("Vocês desenvolvem soluções de IA sob medida?","Sim. Desenvolvemos agentes, automações e sistemas com IA personalizados para o seu processo, integrados aos sistemas que você já usa."),
            ("Preciso ter uma equipe de tecnologia?","Não. Conduzimos diagnóstico, desenvolvimento e treinamento. Quando há integração com sistemas internos, trabalhamos junto com o seu time ou fornecedor de TI.")]),
  dict(slug="pessoas", unit="Oxyn Pessoas", short="Pessoas e RH", icon="i-users", color="blue", img="foto-broto.jpg",
       card="Consultoria de RH e formação de lideranças. Estruturamos o RH, formamos líderes e, quando necessário, somos o RH da sua empresa.",
       tags=["Consultoria de RH", "Mentoria de líderes", "RH como serviço"],
       menu="Consultoria de RH, lideranças e RH como serviço",
       title="Consultoria de RH, formação de líderes e RH como serviço",
       eyebrow="Oxyn Pessoas · Consultoria de RH",
       h1_thin="Líderes preparados", h1="sustentam o crescimento.",
       lead="Estruturamos o RH, formamos lideranças e, quando necessário, atuamos como o RH da sua empresa. Pessoas certas, nas funções certas, com rituais de gestão que se mantêm depois que saímos.",
       pains_h2="Pessoas são o gargalo do seu crescimento?",
       pains=[("i-users","Contratação que não vinga","Rotatividade alta, custo de reposição e meses perdidos até o novo profissional produzir."),
              ("i-award","Liderança sem preparo","Gestores promovidos pelo desempenho individual, sem formação para liderar pessoas."),
              ("i-layers","RH sem estrutura","Cargos, carreiras e salários sem critério, e nenhum indicador de pessoas para orientar decisões.")],
       deliv_h2="Estrutura, lideranças e rotina",
       deliv=[("i-layers","Consultoria de RH","Estrutura e governança, papéis e reportes, cargos, carreiras e salários, indicadores de pessoas."),
              ("i-award","Mentoria de líderes","Formação de líderes, mentoria individual, desenvolvimento e handover do time de RH."),
              ("i-message","Rituais de gestão","1:1 e feedback, People Check-in, PDI, pesquisa de clima e reunião de liderança."),
              ("i-handshake","RH como serviço","A Oxyn atua como o RH da empresa, com rituais, clima, PDI e transição planejada.")],
       how_eyebrow="Como implantamos", how_h2="Em 90 dias, a rotina fica com a sua liderança",
       how_lead="A consultoria entra para organizar, colocar em prática e transferir a rotina para os líderes e o time de Pessoas da empresa.",
       how=["<b>Mês 1 · Estruturar:</b> papéis, responsabilidades, indicadores, rituais e alinhamento dos líderes",
            "<b>Mês 2 · Implantar:</b> formação dos líderes e primeira aplicação dos rituais, com acompanhamento",
            "<b>Mês 3 · Sustentar:</b> ajustes finais, co-condução, handover e revisão do ciclo",
            "<b>Ao final:</b> a rotina está com a liderança e com o time de Pessoas da sua empresa"],
       connects=["vendas","inteligencia-artificial","fqd-studios"],
       faq=[("A consultoria de RH é só para a área comercial?","Não. Atendemos toda a estrutura da empresa: governança de RH, cargos e salários, lideranças e rituais de gestão. A experiência comercial do grupo ajuda especialmente em times de vendas."),
            ("O que é RH como serviço?","É quando a Oxyn atua como o RH da sua empresa, conduzindo rituais, clima e PDI, com uma transição planejada para um time interno quando fizer sentido."),
            ("Quanto tempo dura a implantação?","O ciclo padrão é de 90 dias: estruturar, implantar e sustentar. Ao final, a rotina está com a liderança e com o time de Pessoas da empresa.")]),
  dict(slug="naia-geo-seo", unit="Naia", short="GEO e SEO", icon="i-search", color="blue", img="foto-abstrato-capa.jpg",
       card="Implementação e ongoing da Naia, plataforma de GEO, mais SEO para sua marca ser encontrada no Google e recomendada pelas IAs.",
       tags=["GEO", "SEO", "Plataforma Naia"],
       menu="GEO e SEO com a plataforma Naia",
       title="Naia: GEO e SEO para empresas",
       eyebrow="Naia · GEO e SEO",
       h1_thin="Seja encontrado no Google", h1="e recomendado pelas IAs.",
       lead="Seus clientes já pesquisam no ChatGPT, Gemini e Perplexity antes de falar com um vendedor. Com a Naia, plataforma de GEO, e o nosso time de SEO, sua marca aparece nas respostas que influenciam a decisão de compra.",
       pains_h2="Quando seu cliente pergunta, quem aparece?",
       pains=[("i-message","Invisível nas IAs","Quando o comprador pergunta a uma IA quem resolve o problema dele, a resposta cita seus concorrentes."),
              ("i-trend","Orgânico estagnado","O tráfego do Google não cresce e o site não gera oportunidades para o time comercial."),
              ("i-layers","Conteúdo sem estratégia","Publicações que não respondem às perguntas reais do comprador e não geram leads.")],
       deliv_h2="Visibilidade que vira oportunidade",
       deliv=[("i-cpu","Implementação da Naia","Configuração da plataforma, mapeamento das perguntas do seu mercado e linha de base de visibilidade."),
              ("i-chart","Monitoramento contínuo","Acompanhamento de menções, posicionamento e concorrentes nas principais IAs generativas."),
              ("i-search","SEO técnico e de conteúdo","Arquitetura do site, velocidade, palavras-chave e conteúdos que respondem ao comprador."),
              ("i-trend","Ongoing de otimização","Ciclos mensais de ajustes, novos conteúdos e relatórios focados em geração de leads.")],
       how_eyebrow="Como funciona", how_h2="GEO e SEO trabalhando juntos",
       how_lead="O mesmo conteúdo que ranqueia no Google é o que as IAs usam para recomendar marcas. Por isso tratamos os dois como um só trabalho.",
       how=["Diagnóstico de visibilidade no Google e nas IAs generativas",
            "Mapa de perguntas e intenções de compra do seu público",
            "Otimização técnica do site e dados estruturados",
            "Produção e atualização de conteúdo orientado a autoridade",
            "Relatórios mensais de visibilidade, tráfego e leads"],
       connects=["fqd-studios","fqdtv","vendas"],
       faq=[("O que é GEO?","GEO, ou Generative Engine Optimization, é a otimização para que sua marca seja citada e recomendada em respostas de IAs generativas como ChatGPT, Gemini e Perplexity."),
            ("GEO substitui o SEO?","Não. Os dois se complementam: as IAs se apoiam em conteúdo bem estruturado e com autoridade, que é a base do SEO. Trabalhamos as duas frentes juntas."),
            ("Em quanto tempo vejo resultado?","SEO e GEO são trabalhos de médio prazo. A Naia mede a linha de base desde o início para que você acompanhe a evolução mês a mês.")]),
  dict(slug="fqdtv", unit="FQDTV", short="Mídia de nicho", icon="i-megaphone", color="blue", img="foto-abstrato-escuro.jpg",
       card="Mídias de penetração em públicos nichados. Sua marca falando com quem decide, no contexto certo.",
       tags=["Mídia segmentada", "Branded content", "Autoridade"],
       menu="Mídia para públicos de nicho",
       title="FQDTV: mídia de nicho para empresas",
       eyebrow="FQDTV · Mídia de nicho",
       h1_thin="Mídia de nicho", h1="para falar com quem decide.",
       lead="A FQDTV produz e distribui conteúdo para públicos segmentados. Sua marca chega com contexto e credibilidade a nichos que a mídia de massa não alcança.",
       pains_h2="Sua marca fala com o público certo?",
       pains=[("i-megaphone","Mídia de massa, público errado","Investimento em alcance amplo para vender a um grupo pequeno e específico de decisores."),
              ("i-globe","Marca desconhecida no setor","Concorrentes com menos entrega são lembrados primeiro porque aparecem mais."),
              ("i-message","Ciclo de venda longo","Sem autoridade prévia, cada reunião começa do zero e a confiança demora a ser construída.")],
       deliv_h2="Presença onde o seu nicho presta atenção",
       deliv=[("i-youtube","Programas e formatos","Entrevistas, séries e conteúdos editoriais pensados para cada segmento."),
              ("i-megaphone","Distribuição segmentada","Canais e comunidades que concentram o público que você precisa alcançar."),
              ("i-award","Branded content","Sua marca integrada ao conteúdo de forma relevante, não como interrupção."),
              ("i-chart","Mensuração","Alcance, engajamento e geração de oportunidades acompanhados por campanha.")],
       how_eyebrow="Para quem é", how_h2="Ideal para quem vende para poucos, mas grandes",
       how_lead="Mercados B2B, setores técnicos e nichos em que a decisão depende de confiança e reputação.",
       how=["Indústrias e distribuidores que precisam ser lembrados pelo comprador técnico",
            "Empresas entrando em um novo segmento ou região",
            "Marcas que querem posicionar seus executivos como referência",
            "Lançamentos de produtos para públicos específicos",
            "Eventos, feiras e ações que precisam de repercussão no setor"],
       connects=["fqd-studios","naia-geo-seo","vendas"],
       faq=[("O que é mídia de nicho?","É a comunicação direcionada a um público segmentado, com conteúdo e canais escolhidos para o contexto desse público, em vez de buscar alcance amplo."),
            ("A FQDTV produz o conteúdo?","Sim. Concebemos, produzimos e distribuímos. A programação diária da FQDTV é gravada no FQD Studios, o estúdio do grupo em São Paulo."),
            ("Como sei se a mídia gerou negócios?","Cada campanha tem indicadores de alcance e engajamento e, quando integrada ao comercial, de oportunidades geradas.")]),
  dict(slug="fqd-studios", unit="FQD Studios", short="Estúdio e conteúdo", icon="i-video", color="blue", img="foto-abstrato-capa.jpg",
       site="https://fqdstudios.com/",
       address=dict(street="Av. Queiroz Filho, 1700, Bloco D, Sala 802", district="Vila Hamburguesa", city="São Paulo", region="SP", zip="05319-000"),
       card="Estúdio em São Paulo e gravações externas para podcasts, lives, programas de bancada e conteúdo corporativo. Um estúdio, todos os formatos.",
       tags=["Podcast e videocast", "Lives no YouTube", "Conteúdo corporativo"],
       menu="Estúdio de gravação e gravações externas",
       title="Estúdio de podcast, lives e conteúdo corporativo em São Paulo",
       eyebrow="FQD Studios · Estúdio de gravação",
       h1_thin="Um estúdio.", h1="Todos os formatos.",
       lead="Cenário, transmissão e pós-produção sob o mesmo teto, ao lado do Parque Villa-Lobos, em São Paulo. Podcasts, lives, aulas, programas de bancada e conteúdo corporativo com captação em 4K e equipe técnica própria. Quando o conteúdo precisa acontecer fora, levamos a gravação até você.",
       pains_h2="O seu conteúdo está à altura da sua empresa?",
       pains=[("i-video","Conteúdo amador","Áudio ruim, imagem improvisada e uma percepção de marca abaixo do que a empresa entrega."),
              ("i-layers","Um fornecedor por etapa","Cenário, gravação, transmissão e edição com equipes diferentes, agendas desencontradas e meses entre a ideia e a publicação."),
              ("i-target","Vídeo sem objetivo","Conteúdo bonito, mas sem formato pensado para gerar autoridade e oportunidades.")],
       deliv_h2="Do set à entrega, sob o mesmo teto",
       deliv=[("i-message","Podcast e videocast","Áudio multipista e enquadramento planejado para os cortes das redes sociais."),
              ("i-youtube","Lives e transmissões","Transmissão direta para o YouTube com sinal estável, troca de câmeras, grafismos e transições ao vivo."),
              ("i-users","Bancada, aulas e corporativo","Programas de bancada para até 5 pessoas, conteúdo educacional, treinamentos, webinars e comunicação interna."),
              ("i-camera","Pós-produção e externas","Cortes, tratamento de áudio e cor no formato de cada plataforma, e equipe para gravações fora do estúdio.")],
       how_eyebrow="Como funciona", how_h2="Do briefing à entrega, sem trocar de fornecedor",
       how_lead="Você não precisa levar equipamento: câmeras, áudio, luz e operação estão incluídos. Recomendamos agendar com pelo menos 3 dias de antecedência.",
       how=["<b>Briefing:</b> formato, objetivo e identidade do projeto alinhados antes de gravar",
            "<b>Agendamento:</b> você escolhe o horário; cenário, luz e cores ficam prontos antes da sua chegada",
            "<b>Gravação:</b> câmeras PTZ, captação em 4K e corte ao vivo conduzidos pela equipe técnica do estúdio",
            "<b>Entrega:</b> conteúdo editado e cortado, no prazo combinado",
            "<b>Estrutura:</b> camarim, copa, ar-condicionado, estacionamento e segurança de prédio corporativo"],
       connects=["fqdtv","naia-geo-seo","vendas"],
       faq=[("Preciso levar algum equipamento?","Não. Câmeras, áudio, iluminação e operação estão incluídos."),
            ("Dá para fazer live no YouTube?","Sim. Transmitimos direto para o YouTube, com troca de câmeras, grafismos e transições ao vivo."),
            ("Onde fica o estúdio?","No Condomínio Villa Lobos Office Park, Av. Queiroz Filho, 1700, Bloco D, Sala 802, Vila Hamburguesa, São Paulo. Perto do Parque Villa-Lobos e da Marginal Pinheiros, a poucos minutos da estação Villa Lobos-Jaguaré da CPTM, com estacionamento no local."),
            ("Quanto custa?","Não trabalhamos com tabela fixa. Depois de uma conversa rápida sobre formato e objetivo, enviamos uma proposta sob medida.")]),
]
BY = {u["slug"]: u for u in UNITS}
OXYN = ["vendas", "pessoas", "inteligencia-artificial"]      # frentes dentro da Oxyn
EMPRESAS = ["naia-geo-seo", "fqdtv", "fqd-studios"]            # demais empresas do grupo
UNITS = [BY[s] for s in OXYN + EMPRESAS]
for u in UNITS:
    u["empresa"] = "Oxyn" if u["slug"] in OXYN else u["unit"]
# Logos oficiais das empresas do grupo (banner das paginas de solucao)
BY["naia-geo-seo"]["logo"] = "empresas/naia.svg"
BY["fqdtv"]["logo"] = "empresas/fqdtv.svg"
BY["fqd-studios"]["logo"] = "empresas/fqd-studios.svg"
# Site proprio de cada empresa (botao no banner, para o cliente saber mais)
BY["naia-geo-seo"].update(site="https://naia.today/", site_label="Site da Naia")
BY["fqdtv"].update(site="https://fqdtv.com.br/", site_label="Canal da FQDTV no YouTube")
BY["fqd-studios"].update(site_label="Site da FQD Studios")

# --------------------------------------------------------------------------
# Partes compartilhadas
# --------------------------------------------------------------------------
SPRITE = open(pathlib.Path(__file__).with_name("sprite.svg"), encoding="utf-8").read()
IMG = "/assets/img"
# Versao dos arquivos de estilo e script: muda a cada alteracao e obriga o navegador a baixar a versao nova
def _ver(rel):
    return hashlib.md5((OUT / rel).read_bytes()).hexdigest()[:10]
CSS_V, JS_V = _ver("assets/css/styles.css"), _ver("assets/js/main.js")

# Fundadores (Manual de Marca v1.0, slide "Fundadores"). Fotos: salvar em
# assets/img/fundadores/<slug>.jpg e preencher "foto".
LEADERS = [
  dict(nome="Caio Camarini", cargo="Co-CEO", foto="caio-camarini.jpg", bio="Executivo com mais de 20 anos em liderança comercial e desenvolvimento de negócios. Especialista em digitalização B2B e estratégias omnichannel, concluiu o programa de Negociação e Decisões Competitivas da Harvard Business School."),
  dict(nome="Erick Melo", cargo="Co-CEO", foto="erick-melo.jpg", bio="Empreendedor com mais de 20 anos em tecnologia e negócios. Fundou a Webjump, integra o Conselho do E-Commerce Brasil e concluiu o programa Managing Innovation da Harvard Business School."),
  dict(nome="Bruno Gurgel", cargo="CTO", foto="bruno-gurgel.jpg", bio="Empreendedor com mais de 20 anos em tecnologia, inovação e gestão, com passagens por R7, Whirlpool e Ambev."),
  dict(nome="Rodrigo Macena", cargo="COO", foto="rodrigo-macena.jpg", bio="Especialista em otimização de operações em grandes empresas, com passagem pela Porto Seguro e formação na Harvard Business School."),
  dict(nome="Beatriz Fonseca", cargo="CPO", foto="beatriz-fonseca.jpg", bio="Executiva com mais de 20 anos de experiência, 10 deles liderando equipes. Especialista em Pessoas e Cultura, pós-graduada em Psicologia Organizacional e formada no High Potential Leadership Program da Harvard Business School."),
  dict(nome="Vinicius Christe", cargo="CRO", foto="vinicius-christe.jpg", bio="Executivo com mais de 20 anos em planejamento e comercialização de mídia digital. Especialista em estratégia comercial, relacionamento com o mercado e novos formatos e veículos de mídia."),
]
# Clientes (logos em assets/img/clientes; exibidos em cinza, como pede o manual)
CLIENTS = [
  dict(nome="Expert Esquadrias", logo="expert-esquadrias.png", site="https://expertesquadrias.com.br/"),
  dict(nome="Harpix", logo="harpix.svg", site="https://harpix.com.br/"),
  dict(nome="Omni11", logo="omni11.png", site="https://omni11.com.br/"),
  dict(nome="FQD Studios", logo="fqd-studios-mono.svg", site="https://fqdstudios.com/"),
  dict(nome="Bersaglio Imóveis", logo="bersaglio-imoveis.png", site="https://www.bersaglioimoveis.com.br/"),
  dict(nome="Weinberg", logo="weinberg.png", site=""),
  dict(nome="Naia", logo="naia.svg", site="https://naia.today/"),
  dict(nome="iMasters", logo="imasters.png", site="https://imasters.com.br/"),
]
SECTORS = [("Indústria","i-factory"), ("Agro","i-wheat"), ("Farma","i-pill"), ("Varejo","i-store"),
           ("Educação","i-graduation"), ("Financeiro","i-bank"), ("Automotivo","i-car"), ("Aviação","i-plane")]

def head(title, desc, path, jsonld):
    url = SITE + path
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#141C22">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Oxyn Group">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{IMG}/logo-oxyn.png">
<link rel="icon" href="{IMG}/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{IMG}/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;600&family=Montserrat:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/styles.css?v={CSS_V}">
<script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=2)}
</script>
</head>
"""

CUR = ' aria-current="page"'

def nav(current=None):
    link = lambda u: f'            <a href="/solucoes/{u["slug"]}"{CUR if u["slug"]==current else ""}><b>{u["unit"]}</b><small>{u["menu"]}</small></a>'
    items = ('            <span class="nav__group">Oxyn</span>\n' + "\n".join(link(BY[s]) for s in OXYN) +
             '\n            <span class="nav__group">Empresas do grupo</span>\n' + "\n".join(link(BY[s]) for s in EMPRESAS))
    return f"""  <!-- NAV | logo 02 (fonte branca) sobre fundo escuro + dropdown de solucoes -->
  <nav class="nav" data-component="nav">
    <div class="container">
      <a href="/" class="brand" aria-label="Oxyn Group, página inicial">
        <img class="brand__logo" src="{IMG}/logo-oxyn-branco.png" alt="Oxyn Group" width="240" height="86">
      </a>
      <div class="nav__links" id="nav-links">
        <div class="nav__drop">
          <button type="button" aria-expanded="false">Soluções <svg class="icon icon--sm"><use href="#i-chevron-down"/></svg></button>
          <div class="nav__menu">
{items}
          </div>
        </div>
        <a href="/#metodo">Método</a>
        <a href="/#fundadores">Fundadores</a>
        <a href="/#contato" class="btn btn--ghost btn--sm">Fale com a Oxyn</a>
      </div>
      <button class="nav__toggle" aria-label="Abrir menu" aria-expanded="false" aria-controls="nav-links"><svg class="icon"><use href="#i-menu"/></svg></button>
    </div>
  </nav>
"""

def cta(thin, h2, lead):
    return f"""  <!-- CTA FINAL | foto escura + composicao assinatura entre fios finos | 1 botao ambar -->
  <section class="section section--overlay cta-final has-ring" id="contato" data-section="cta" style="--img:url('{IMG}/foto-abstrato-capa.jpg');--ring-o:.12;--ring-x:auto;--ring-y:-180px">
    <div class="container">
      <header class="section-head section-head--center signature" data-reveal>
        <h2 class="h2"><span class="thin">{thin}</span>{h2}</h2>
      </header>
      <p class="lead" style="text-align:center;margin:0 auto 32px" data-reveal>{lead}</p>
      <div class="btn-row" style="justify-content:center" data-reveal>
        <a href="{WA}" class="btn btn--amber btn--lg" target="_blank" rel="noopener">Agende um diagnóstico <span class="arrow">→</span></a>
        <a href="mailto:{EMAIL}" class="btn btn--ghost btn--lg">Enviar e-mail</a>
      </div>
      <div class="contact-line" data-reveal>
        <a href="{WA}" target="_blank" rel="noopener"><svg class="icon icon--sm"><use href="#i-phone"/></svg>{PHONE}</a>
        <a href="mailto:{EMAIL}"><svg class="icon icon--sm"><use href="#i-mail"/></svg>{EMAIL}</a>
      </div>
    </div>
  </section>
"""

def footer():
    sols = "".join(f'<li><a href="/solucoes/{u["slug"]}">{u["unit"]}</a></li>' for u in UNITS)
    return f"""  <!-- FOOTER -->
  <footer class="footer" data-component="footer">
    <div class="container">
      <div class="footer__grid">
        <div>
          <a href="/" class="brand"><img class="brand__logo" src="{IMG}/logo-oxyn-branco.png" alt="Oxyn Group" width="240" height="86" loading="lazy"></a>
          <p>Oxigenamos o crescimento B2B. Vendas, pessoas, IA, GEO, mídia e conteúdo para sua empresa vender mais.</p>
          <div class="socials">
            <a href="{LI}" aria-label="LinkedIn" target="_blank" rel="noopener"><svg class="icon icon--sm"><use href="#i-linkedin"/></svg></a>
            <a href="{IG}" aria-label="Instagram" target="_blank" rel="noopener"><svg class="icon icon--sm"><use href="#i-instagram"/></svg></a>
          </div>
        </div>
        <div><h4>Soluções</h4><ul>{sols}</ul></div>
        <div><h4>Oxyn Group</h4><ul>
          <li><a href="/#pilares">Pilares</a></li><li><a href="/#metodo">Método D.R.I.V.E.</a></li>
          <li><a href="/#fundadores">Fundadores</a></li><li><a href="/#contato">Contato</a></li></ul></div>
        <div><h4>Contato</h4><ul>
          <li><a href="{WA}" target="_blank" rel="noopener">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
      </div>
      <div class="footer__bottom"><span>© <span data-year>2026</span> Oxyn Serviços e Consultoria LTDA. Todos os direitos reservados.</span><a href="#">Política de Privacidade</a></div>
    </div>
  </footer>

  <a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Conversar no WhatsApp"><svg class="icon"><use href="#i-message"/></svg></a>

  <!-- COOKIE BANNER -->
  <div class="cookie" data-cookie>
    <span>Usamos cookies para melhorar sua experiência, analisar o uso do site e personalizar conteúdo.</span>
    <button class="btn" data-cookie-ok>Ok, entendi</button>
  </div>

<script src="/assets/js/main.js?v={JS_V}" defer></script>
</body>
</html>
"""

def body_open():
    return f'<body class="has-cookie">\n\n{SPRITE}\n'

def faq_block(items, title):
    html = "\n".join(f'        <details data-reveal><summary>{q}</summary><p>{a}</p></details>' for q,a in items)
    return f"""  <!-- FAQ -->
  <section class="section section--light" data-section="faq">
    <div class="container">
      <header class="section-head section-head--center" data-reveal>
        <p class="eyebrow">Perguntas frequentes</p>
        <h2 class="h2">{title}</h2>
      </header>
      <div class="faq">
{html}
      </div>
    </div>
  </section>

"""

def faq_ld(items):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}

ORG = {
  "@context": "https://schema.org", "@type": "Organization",
  "name": "Oxyn Group", "legalName": "Oxyn Serviços e Consultoria LTDA", "url": SITE,
  "logo": f"{SITE}{IMG}/logo-oxyn.png", "slogan": "Oxigenamos o crescimento B2B.",
  "email": EMAIL, "telephone": "+5511979706449", "sameAs": [IG, LI],
  "description": "Grupo de quatro empresas B2B focado em fazer clientes venderem mais: a Oxyn (consultoria comercial e terceirização de vendas, consultoria de RH e consultoria, treinamento e soluções de IA para toda a empresa), a Naia (GEO e SEO), a FQDTV (mídia de nicho) e a FQD Studios (estúdio de conteúdo).",
  "founder": [{"@type": "Person", "name": l["nome"], "jobTitle": l["cargo"]} for l in LEADERS],
  "subOrganization": [{"@type": "Organization", "name": "Oxyn", "url": SITE,
                       "department": [{"@type": "Organization", "name": BY[s]["unit"], "url": f'{SITE}/solucoes/{s}'} for s in OXYN]}]
                     + [{"@type": "Organization", "name": BY[s]["unit"], "url": f'{SITE}/solucoes/{s}'} for s in EMPRESAS],
}

def initials(n):
    p = n.split(); return (p[0][0] + p[-1][0]).upper()

# --------------------------------------------------------------------------
# HOME
# --------------------------------------------------------------------------
def home():
    service_cards = "\n".join(f"""        <a href="/solucoes/{u["slug"]}" class="card card--soft card--service" data-reveal>
          <svg class="icon icon--blue icon--lg"><use href="#{u["icon"]}"/></svg>
          <span class="card__unit">{u["empresa"]}</span>
          <h3 class="h3" style="margin-top:0">{u["short"]}</h3>
          <p>{u["card"]}</p>
          <div class="tags">{"".join(f'<span class="tag tag--blue">{t}</span>' for t in u["tags"])}</div>
          <span class="link-arrow">Conheça <span class="arrow">→</span></span>
        </a>""" for u in UNITS)
    tiles = "".join(f'<span class="sector"><svg class="icon"><use href="#{i}"/></svg><span>{n}</span></span>' for n,i in SECTORS)
    def client_tile(c):
        img = f'<img src="{IMG}/clientes/{c["logo"]}" alt="{c["nome"]}" loading="lazy">'
        if c["site"]:
            return f'<a class="logo-tile logo-tile--img" href="{c["site"]}" target="_blank" rel="noopener" title="{c["nome"]}">{img}</a>'
        return f'<span class="logo-tile logo-tile--img" title="{c["nome"]}">{img}</span>'
    client_tiles = "".join(client_tile(c) for c in CLIENTS)
    acionadas = {"pessoas":"Time e lideranças que sustentam", "inteligencia-artificial":"Consultoria, treinamento e soluções de IA",
                 "naia-geo-seo":"Visibilidade no Google e nas IAs", "fqdtv":"Reputação no seu nicho",
                 "fqd-studios":"Conteúdo que prova autoridade"}
    co = lambda s, nome: f'''<a class="sol__co" href="/solucoes/{s}"><b>{nome}</b><span>{acionadas[s]}</span></a>'''
    sol_frentes = "".join(co(s, BY[s]["short"].replace(" e RH","")) for s in ["pessoas","inteligencia-artificial"])
    sol_empresas = "".join(co(s, BY[s]["unit"]) for s in EMPRESAS)
    pillars = [("i-users","Conexões certas","Networking e know-how de fundadores com mais de 20 anos de vivência no setor B2B."),
               ("i-award","Experiência prática","Atuação real com indústrias, distribuidores e grandes contas, de agro a varejo."),
               ("i-layers","Sem modelo engessado","Abordagem consultiva e personalizada. O diagnóstico define a solução, não o contrário."),
               ("i-target","Metodologia própria","D.R.I.V.E., aplicada de ponta a ponta no processo comercial, com método e dados.")]
    pillar_cards = "\n".join(f"""        <article class="card card--soft card--feature" data-reveal>
          <div class="card__top"><span class="icon-badge"><svg class="icon"><use href="#{i}"/></svg></span><span class="num">{k+1}.</span></div>
          <h3 class="h4">{t}</h3>
          <p>{d}</p>
        </article>""" for k,(i,t,d) in enumerate(pillars))
    stats = [("80","%","das transações globais acontecem em ambiente B2B","Gartner"),
             ("32"," tri","é o tamanho estimado do mercado B2B em 2025","Coalition Technologies"),
             ("66","%","das empresas B2B estão revisando seus processos de vendas","The Sales Collective"),
             ("4"," em 10","líderes veem o conflito de canais como seu maior desafio","BCG")]
    stat_html = "\n".join(f"""          <div class="stat"><div class="stat__value" data-count="{v}" data-suffix="{suf}">{v}{suf}</div><div class="stat__label">{l}</div><div class="stat__source">Fonte: {src}</div></div>""" for v,suf,l,src in stats)
    drive = [("D","Descoberta","Quais empresas, perfis e decisores têm maior potencial de receita e fit operacional."),
             ("R","Ranqueamento","A energia do time concentrada nos leads com maior chance de conversão."),
             ("I","Investigação","Escuta estruturada das motivações, restrições e dependências do comprador."),
             ("V","Validação","O diagnóstico vira proposta clara, personalizada e financeiramente viável."),
             ("E","Execução","Acompanhamento até o fechamento, retroalimentando o sistema com dados.")]
    steps = "\n".join(f"""        <div class="step" data-reveal><span class="step__letter">{l}</span><h3 class="h5">{t}</h3><p>{d}</p></div>""" for l,t,d in drive)
    eco = [("i-search","Ser encontrado","naia-geo-seo","Naia coloca sua marca no Google e nas respostas das IAs."),
           ("i-megaphone","Ser lembrado","fqdtv","FQDTV e FQD Studios constroem autoridade no seu nicho."),
           ("i-trend","Converter","vendas","A Oxyn transforma oportunidades em contratos assinados."),
           ("i-users","Escalar","pessoas","As frentes Pessoas e IA da Oxyn dão estrutura, líderes e produtividade.")]
    eco_cards = "\n".join(f"""        <a href="/solucoes/{s}" class="card card--eco" data-reveal><svg class="icon icon--cyan"><use href="#{i}"/></svg><h3 class="h5">{t}</h3><p>{d}</p></a>""" for i,t,s,d in eco)
    leaders = "\n".join(f"""        <article class="founder" data-reveal>
          <div class="founder__photo{"" if l["foto"] else " founder__photo--vazia"}">{f'<img src="{IMG}/fundadores/{l["foto"]}" alt="{l["nome"]}, {l["cargo"]} da Oxyn Group" loading="lazy" width="600" height="800">' if l["foto"] else ""}</div>
          <div class="founder__body">
            <span class="founder__role">{l["cargo"]}</span>
            <h3 class="founder__name">{l["nome"]}</h3>
            <p>{l["bio"]}</p>
          </div>
        </article>""" for l in LEADERS)
    faq_home = [("O que é a Oxyn Group?","A Oxyn Group é um grupo de quatro empresas B2B que oxigena o crescimento de outras empresas: a Oxyn, com as frentes Vendas, Pessoas e IA; a Naia, de GEO e SEO; a FQDTV, de mídia de nicho; e a FQD Studios, de produção de conteúdo. Todas com o mesmo objetivo: fazer o cliente vender mais."),
                ("O que significa Business Converter™?","É a categoria que criamos para nos descrever. Não somos uma agência de representação nem uma consultoria que entrega um relatório e vai embora. Entramos na operação, estruturamos o que precisa ser estruturado e ficamos até o resultado aparecer."),
                ("Preciso contratar todas as frentes?","Não. Cada empresa do grupo pode ser contratada de forma independente. A vantagem de combinar frentes é ter um único parceiro cuidando da jornada inteira, da visibilidade ao fechamento."),
                ("Por onde começamos?","Pelo diagnóstico. Ele mostra se o gargalo está no processo, no time ou no mercado e define quais frentes fazem sentido para o seu momento.")]

    html = head("Oxyn Group | Oxigenamos o crescimento B2B",
                "Consultoria comercial B2B e terceirização de vendas, consultoria de RH, consultoria e soluções de IA, GEO e SEO, mídia de nicho e estúdio de conteúdo. Business Converter™: entramos na operação e ficamos até o resultado aparecer.",
                "/", [ORG, faq_ld(faq_home)])
    html += body_open()
    html += nav()
    html += f"""
  <!-- HERO | abstrato escuro (capa do manual) + anel em marca d'agua + grade de pontos -->
  <header class="hero has-ring" data-section="hero" style="--img:url('{IMG}/foto-abstrato-capa.jpg')">
    <div class="container">
      <span class="dotgrid" aria-hidden="true"></span>
      <div class="hero__content hero__content--home" data-reveal>
        <p class="sol__kicker">Oxyn Group · Business Converter™</p>
        <h1 class="sol__title"><small>Vendas que não</small><b>dependem</b><b>de sorte<span>.</span></b></h1>
        <p class="lead">Quando a venda trava, raramente é um problema só: a marca que ninguém encontra, o time sem método, o funil sem critério. Nós encontramos onde a sua venda trava e resolvemos de ponta a ponta, assumimos sua operação e destravamos os resultados. Vamos além da operação comercial: estruturamos o RH e formamos líderes, aplicamos inteligência artificial em toda a empresa, colocamos a sua marca no Google e nas respostas das IAs e produzimos mídia e conteúdo que constroem autoridade no seu setor.</p>
        <div class="btn-row">
          <a href="#contato" class="btn btn--primary btn--lg">Agende um diagnóstico <span class="arrow">→</span></a>
          <a href="#solucao" class="btn btn--ghost btn--lg">Veja como funciona</a>
        </div>
      </div>
      <div class="hero__pains" data-reveal>
        <span class="hero__pains-t">O que resolvemos</span>
        <div><em>01</em><b>Ninguém encontra a sua empresa</b><span>Nem no Google, nem nas respostas das IAs.</span></div>
        <div><em>02</em><b>A marca não tem autoridade</b><span>Desconhecida no setor e sem conteúdo que prove o que entrega.</span></div>
        <div><em>03</em><b>O time vende sem método</b><span>Sem processo, funil sem critério e resultado que oscila.</span></div>
        <div><em>04</em><b>As pessoas não sustentam</b><span>Contratação que não vinga e líderes sem preparo.</span></div>
        <div><em>05</em><b>A IA ainda não trabalha para você</b><span>Tarefas manuais em todas as áreas e cada um usando IA de um jeito.</span></div>
      </div>
    </div>
  </header>

  <!-- SETORES | trajetoria de cases: um icone por setor com o nome abaixo, direto no fundo -->
  <section class="section section--white section--tight" data-section="sectors" style="padding-block:48px">
    <p class="eyebrow" style="text-align:center;margin-bottom:24px">Trajetória de cases em oito setores</p>
    <div class="marquee">
      <div class="marquee__track" data-marquee>{tiles}</div>
    </div>
  </section>

  <!-- SOLUCAO COMPLETA | desenhado no Claude Design (A2): a Oxyn e a camada que diagnostica, aciona o grupo ou opera tudo -->
  <section class="sol" id="solucao" data-section="solution">
    <div class="sol__photo" aria-hidden="true"></div>
    <div class="container sol__top">
      <span class="dotgrid" aria-hidden="true"></span>
      <p class="sol__kicker" data-reveal>Como resolvemos</p>
      <h2 class="sol__title" data-reveal><small>A solução completa para</small><b>Incrementar</b><b>vendas<span>.</span></b></h2>
      <div class="sol__creds" data-reveal>
        <div class="sol__cred"><b>20+</b><span>anos de cada fundador <br>em vendas B2B</span></div>
        <div class="sol__cred"><b>4</b><span>empresas integradas <br>em um só grupo</span></div>
        <div class="sol__cred"><b>8</b><span>setores com cases, <br>de agro a aviação</span></div>
      </div>
    </div>
    <div class="container">
      <div class="sol__layer" data-reveal>
        <a class="sol__brand" href="/solucoes/vendas"><small>A camada que conecta tudo</small><b>OXYN</b></a>
        <div class="sol__step"><em>01</em><b>Diagnostica</b><span>Processo, time, carteira e mercado: mostra onde a venda trava.</span></div>
        <div class="sol__step"><em>02</em><b>Aciona o grupo</b><span>Reestrutura, treina e traz a empresa certa para cada gargalo.</span></div>
        <div class="sol__step"><em>03</em><b>Ou opera tudo</b><span>Assume a operação comercial como o time da sua empresa.</span></div>
      </div>
      <div class="sol__cos" data-reveal>
        <span class="sol__cos-label">O que a<br>Oxyn aciona</span>
        <div class="sol__group"><span class="sol__group-t">Frentes da Oxyn</span><div class="sol__group-items">{sol_frentes}</div></div>
        <div class="sol__group"><span class="sol__group-t">Empresas do grupo</span><div class="sol__group-items">{sol_empresas}</div></div>
      </div>
      <div class="sol__foot" data-reveal>
        <p>Estruturando, crescendo ou escalando: <strong>a Oxyn monta a combinação certa para o seu momento.</strong></p>
        <a href="#contato" class="btn btn--amber btn--lg">Agende um diagnóstico <span class="arrow">→</span></a>
      </div>
    </div>
  </section>

  <!-- PILARES | os quatro argumentos do manual -->
  <section class="section section--white has-ring" id="pilares" data-section="pillars" style="--ring-o:.08">
    <div class="container">
      <header class="section-head" data-reveal>
        <p class="eyebrow">Pilares</p>
        <h2 class="h2">O que sustenta cada entrega</h2>
      </header>
      <div class="grid grid--4">
{pillar_cards}
      </div>
    </div>
  </section>

  <!-- POSICIONAMENTO | composicao assinatura entre fios finos sobre foto escura -->
  <section class="section section--overlay photo-section" data-section="positioning" style="--img:url('{IMG}/foto-abstrato-escuro.jpg');--ov:.45">
    <div class="container">
      <div class="signature" data-reveal>
        <h2 class="display"><span class="thin">Somos</span>Business Converter™</h2>
        <p class="eyebrow" style="color:#fff">Não representamos marcas, nós vestimos a camisa.</p>
      </div>
      <p class="lead" style="text-align:center;margin:32px auto 0" data-reveal>Não somos uma agência de representação nem uma consultoria que entrega um relatório e vai embora. Entramos na operação, estruturamos o que precisa ser estruturado e ficamos até o resultado aparecer.</p>
    </div>
  </section>

  <!-- DADOS | Azul Oxyn solido, numeros em Barlow Light, fonte sempre visivel -->
  <section class="section section--white" data-section="stats" style="padding-block:64px 0">
    <div class="container">
      <p class="eyebrow" style="margin-bottom:16px">O poder do B2B</p>
      <div class="stats-band has-ring" data-reveal>
        <div class="stats">
{stat_html}
        </div>
      </div>
    </div>
  </section>

  <!-- SOLUCOES | as 4 empresas do grupo: Oxyn (3 frentes) + Naia, FQDTV, FQD Studios -->
  <section class="section section--white" id="solucoes" data-section="services">
    <div class="container">
      <header class="section-head section-head--center" data-reveal>
        <p class="eyebrow">Soluções</p>
        <h2 class="h2">Quatro empresas, a mesma lógica</h2>
        <p class="lead">A Oxyn, com as frentes Vendas, Pessoas e IA, mais Naia, FQDTV e FQD Studios. Contrate uma ou combine várias: todas trabalham pelo mesmo resultado, a sua receita.</p>
      </header>
      <div class="bento">
{service_cards}
      </div>
    </div>
  </section>

  <!-- ECOSSISTEMA | jornada de receita -->
  <section class="section section--navy" id="ecossistema" data-section="ecosystem">
    <div class="container">
      <header class="section-head section-head--center" data-reveal>
        <p class="eyebrow">Como atuamos</p>
        <h2 class="h2">Do primeiro contato ao contrato assinado</h2>
        <p class="lead small">Cada empresa e frente do grupo resolve uma etapa da jornada de receita. Juntas, encurtam o caminho entre ser descoberto e vender.</p>
      </header>
      <div class="grid grid--4 eco">
{eco_cards}
      </div>
    </div>
  </section>

  <!-- METODO D.R.I.V.E. -->
  <section class="section section--white has-ring" id="metodo" data-section="method" style="--ring-o:.08;--ring-y:-240px">
    <div class="container">
      <header class="section-head" data-reveal>
        <p class="eyebrow">Metodologia</p>
        <h2 class="h2">Nossa metodologia: D.R.I.V.E.</h2>
        <p class="lead">Inteligência, método e dados aplicados de ponta a ponta no processo comercial.</p>
      </header>
      <div class="steps">
{steps}
      </div>
      <div class="steps__result" data-reveal>
        <div><b>Resultado</b><p>Um processo comercial mensurável, com menos risco e mais conversão.</p></div>
        <a href="/solucoes/vendas" class="btn btn--ghost">Conheça a Oxyn Vendas <span class="arrow">→</span></a>
      </div>
    </div>
  </section>

  <!-- CLIENTES | mesmo layout da trajetoria; logos em cinza, como pede o manual -->
  <section class="section section--light section--tight" data-section="clients" style="padding-block:48px">
    <p class="eyebrow" style="text-align:center;margin-bottom:24px">Clientes</p>
    <div class="marquee">
      <div class="marquee__track" data-marquee>{client_tiles}</div>
    </div>
  </section>

  <!-- FUNDADORES | retratos dos fundadores (slide 10 da apresentacao Q4 2026) -->
  <section class="section founders" id="fundadores" data-section="leadership">
    <div class="container">
      <header class="founders__head" data-reveal>
        <div>
          <p class="sol__kicker">Fundadores</p>
          <h2 class="sol__title"><small>Quem respira B2B</small><b>há mais de 20 anos<span>.</span></b></h2>
        </div>
        <p class="lead">Liderança comercial, tecnologia, mídia e gestão de pessoas, com passagem por grandes empresas e formação na Harvard Business School. É essa experiência que aplicamos em cada cliente.</p>
      </header>
      <div class="founders__grid">
{leaders}
      </div>
    </div>
  </section>

"""
    html += faq_block(faq_home, "Antes de conversarmos")
    html += cta("Vamos além do óbvio", "Vamos conversar sobre a sua operação?", "Conte o seu desafio. Em uma conversa, mostramos onde a venda trava e quais frentes fazem sentido para o seu momento.")
    html += footer()
    return html

# --------------------------------------------------------------------------
# PAGINA DE SOLUCAO
# --------------------------------------------------------------------------
def unit_page(u):
    path = f'/solucoes/{u["slug"]}'
    service_ld = {"@context":"https://schema.org","@type":"Service","name":u["title"],"serviceType":u["short"],
                  "provider":{"@type":"Organization","name":"Oxyn Group","url":SITE},
                  "brand":{"@type":"Brand","name":u["unit"]},
                  "areaServed":"BR","description":u["lead"],"url":SITE+path}
    if u.get("site"):
        service_ld["sameAs"] = u["site"]
    if u.get("address"):
        a = u["address"]
        service_ld["location"] = {"@type":"Place","name":u["unit"],"address":{"@type":"PostalAddress","streetAddress":a["street"],
            "addressLocality":a["city"],"addressRegion":a["region"],"postalCode":a["zip"],"addressCountry":"BR"}}
    pains = "\n".join(f"""        <div class="pains__row" data-reveal><em>{k+1:02d}</em><div><b>{t}</b><span>{d}</span></div></div>""" for k,(i,t,d) in enumerate(u["pains"]))
    def deliv_cta(t):
        if not u.get("deliv_cta"):
            return ""
        return (f'''
          <a class="offer-cta" href="{wa_oferta(t)}" target="_blank" rel="noopener" data-oferta="{slugify(t)}">{u["deliv_cta"]} <span class="arrow">→</span></a>''')
    deliv = "\n".join(f"""        <article class="card card--soft card--feature{" card--offer" if u.get("deliv_cta") else ""}" data-reveal>
          <div class="card__top"><span class="icon-badge"><svg class="icon"><use href="#{i}"/></svg></span><span class="num">{k+1}.</span></div>
          <h3 class="h4">{t}</h3>
          <p>{d}</p>{deliv_cta(t)}
        </article>""" for k,(i,t,d) in enumerate(u["deliv"]))
    eb = u.get("deliv_eyebrow", "O que entregamos")   # vazio = sem rotulo acima do titulo
    deliv_eb = f'        <p class="eyebrow">{eb}</p>\n' if eb else ""
    checks = "\n".join(f"            <li>{c}</li>" for c in u["how"])
    conn = "\n".join(f"""        <a href="/solucoes/{o["slug"]}" class="card card--eco" data-reveal><svg class="icon icon--cyan"><use href="#{o["icon"]}"/></svg><span class="leader__role">{o["unit"]}</span><h3 class="h5">{o["short"]}</h3><p>{o["card"]}</p></a>"""
                     for o in (BY[s] for s in u["connects"]))
    tags = "".join(f'<span class="tag tag--dark">{t}</span>' for t in u["tags"])

    html = head(f'{u["title"]} | {u["unit"]}', u["lead"], path, [service_ld, faq_ld(u["faq"])])
    html += body_open()
    html += nav(u["slug"])
    html += f"""
  <!-- HERO interno | uma foto por pagina, sobreposicao escura -->
  <header class="hero hero--page has-ring" data-section="hero" style="--img:url('{IMG}/{u["img"]}')">
    <div class="container{" hero__split" if u.get("logo") else ""}">
      <div class="hero__content" data-reveal>
        <nav class="crumbs" aria-label="Trilha"><a href="/">Oxyn Group</a><span>/</span><a href="/#solucoes">Soluções</a><span>/</span><span>{u["unit"]}</span></nav>
        <p class="eyebrow">{u["eyebrow"]}</p>
        <h1 class="display"><span class="thin">{u["h1_thin"]}</span>{u["h1"]}</h1>
        <p class="lead">{u["lead"]}</p>
        <div class="tags">{tags}</div>
        <div class="btn-row">
          <a href="#contato" class="btn btn--primary">Vamos conversar <span class="arrow">→</span></a>
          <a href="#entregas" class="btn btn--ghost">O que entregamos</a>{f'''
          <a href="{u["site"]}" class="btn btn--ghost" target="_blank" rel="noopener">{u.get("site_label", "Site da " + u["unit"])} <svg class="icon icon--sm"><use href="#i-external"/></svg></a>''' if u.get("site") else ""}
        </div>
      </div>{f'''
      <div class="hero__logo" data-reveal><img src="{IMG}/{u["logo"]}" alt="Logo {u["unit"]}" width="360" height="240"></div>''' if u.get("logo") else ""}
    </div>
  </header>

  <!-- DESAFIO -->
  <section class="section pains" data-section="problem">
    <div class="container pains__wrap">
      <header class="pains__head" data-reveal>
        <p class="sol__kicker">O desafio</p>
        <h2 class="pains__title">{u["pains_h2"]}</h2>
        <p>Se a sua empresa se reconhece em algum destes pontos, a venda está deixando dinheiro na mesa.</p>
        <a href="#contato" class="link-arrow">Agende um diagnóstico <span class="arrow">→</span></a>
      </header>
      <div class="pains__list">
{pains}
      </div>
    </div>
  </section>

  <!-- ENTREGAS -->
  <section class="section section--white has-ring" id="entregas" data-section="deliverables" style="--ring-o:.08">
    <div class="container">
      <header class="section-head" data-reveal>
{deliv_eb}        <h2 class="h2">{u["deliv_h2"]}</h2>
      </header>
      <div class="grid grid--{len(u["deliv"])}">
{deliv}
      </div>
    </div>
  </section>

  <!-- COMO FUNCIONA -->
  <section class="section section--light" data-section="how">
    <div class="container split">
      <header class="section-head" data-reveal>
        <p class="eyebrow">{u["how_eyebrow"]}</p>
        <h2 class="h2">{u["how_h2"]}</h2>
        <p class="lead">{u["how_lead"]}</p>
        <div class="btn-row" style="margin-top:8px"><a href="#contato" class="btn btn--primary">Agende um diagnóstico <span class="arrow">→</span></a></div>
      </header>
      <ul class="checks card card--soft" data-reveal>
{checks}
      </ul>
    </div>
  </section>

  <!-- CONEXOES COM O GRUPO -->
  <section class="section section--navy" data-section="ecosystem">
    <div class="container">
      <header class="section-head section-head--center" data-reveal>
        <p class="eyebrow">Ecossistema Oxyn</p>
        <h2 class="h2">Potencialize com outras frentes do grupo</h2>
        <p class="lead small">Cada empresa e frente da Oxyn Group resolve uma etapa da jornada de receita. Combinadas, multiplicam o resultado.</p>
      </header>
      <div class="grid grid--3 eco">
{conn}
      </div>
    </div>
  </section>

"""
    html += faq_block(u["faq"], f'Dúvidas sobre {u["unit"]}')
    html += cta("Vamos além do óbvio", "Vamos conversar sobre a sua operação?", "Conte o seu desafio. Nosso time responde rápido e indica o melhor caminho para o seu momento.")
    html += footer()
    return html

# --------------------------------------------------------------------------
(OUT / "index.html").write_text(home(), encoding="utf-8")
(OUT / "solucoes").mkdir(exist_ok=True)
for u in UNITS:
    (OUT / "solucoes" / f'{u["slug"]}.html').write_text(unit_page(u), encoding="utf-8")

urls = ["/"] + [f'/solucoes/{u["slug"]}' for u in UNITS]
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}{p}</loc></url>\n" for p in urls) + "</urlset>\n", encoding="utf-8")
print("ok:", len(urls), "paginas")
