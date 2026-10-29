"""Gera as paginas HTML do site Oxyn (home + 6 solucoes) a partir de dados.
Uso (na raiz do repo): python3 scripts/build.py
Edite os textos aqui e rode o script; ele sobrescreve index.html, solucoes/*.html e sitemap.xml.
"""
import json, sys, pathlib, hashlib, re

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
# O Oxyn Group sao 5 empresas: a Oxyn (frentes Vendas, Pessoas e SEO/GEO), Naia, FQDTV, FQD Studios e Prisma.
# Oxyn Vendas (antes "Comercial" no manual) e Oxyn Pessoas seguem o manual de marca;
# A antiga frente Oxyn IA virou a Prisma, empresa do grupo (logo do guia de marca da Prisma; pagina no visual Oxyn).
# --------------------------------------------------------------------------
UNITS = [
  dict(slug="vendas", seo_title="Consultoria de vendas B2B e terceirização comercial | Oxyn",
       seo_desc="Diagnóstico comercial, reestruturação do time, treinamento com a metodologia D.R.I.V.E., mentoria e operação de vendas terceirizada para empresas B2B.",
       unit="Oxyn Vendas", short="Vendas", icon="i-trend", color="blue", img="foto-leao.webp",
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
       connects=["prisma","pessoas","seo-geo"],
       faq=[("Qual a diferença entre reestruturar, treinar e operar?","Reestruturar é redesenhar o time: papéis, perfis, metas e rituais. Treinar é capacitar o time atual em método, prospecção e negociação. Operar é a Oxyn assumir a área comercial como o time da sua empresa."),
            ("Por que começar pelo diagnóstico?","Porque contratar mais vendedores raramente resolve. Na maioria dos casos, o problema está antes: no perfil de cliente mal definido ou em um funil sem critério de priorização. O diagnóstico mostra se o gargalo está no processo, no time ou no mercado."),
            ("A Oxyn representa a minha marca?","Não representamos marcas: vestimos a camisa. Quando faz sentido, assumimos a operação comercial com a sua marca, metas, rituais e indicadores compartilhados.")]),
  dict(slug="pessoas", seo_title="Consultoria de RH e formação de líderes | Oxyn Pessoas",
       seo_desc="Estruturamos o RH, formamos lideranças e atuamos como o RH da sua empresa. Cargos, carreiras, rituais de gestão e implantação em 90 dias.",
       unit="Oxyn Pessoas", short="Pessoas e RH", icon="i-users", color="blue", img="foto-broto.webp",
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
       connects=["vendas","prisma","fqd-studios"],
       faq=[("A consultoria de RH é só para a área comercial?","Não. Atendemos toda a estrutura da empresa: governança de RH, cargos e salários, lideranças e rituais de gestão. A experiência comercial do grupo ajuda especialmente em times de vendas."),
            ("O que é RH como serviço?","É quando a Oxyn atua como o RH da sua empresa, conduzindo rituais, clima e PDI, com uma transição planejada para um time interno quando fizer sentido."),
            ("Quanto tempo dura a implantação?","O ciclo padrão é de 90 dias: estruturar, implantar e sustentar. Ao final, a rotina está com a liderança e com o time de Pessoas da empresa.")]),
  dict(slug="prisma", seo_title="Consultoria de IA e tecnologia para empresas | Prisma",
       seo_desc="IA em escala com curadoria humana: consultoria em IA, treinamento e padronização do uso e soluções sob medida, com escopo fechado.",
       unit="Prisma", short="IA e tecnologia", icon="i-cpu", color="blue", img="foto-abstrato-escuro.webp",
       card="Consultoria de tecnologia que une IA em escala e curadoria humana: consultoria em IA, treinamento e padronização e soluções sob medida.",
       tags=["Consultoria em IA", "Treinamento e padronização", "Soluções sob medida"],
       menu="Consultoria, treinamento e soluções de IA",
       title="Prisma: consultoria de IA e tecnologia para empresas",
       eyebrow="Prisma · Make it simple",
       h1_thin="Solução,", h1="não horas.",
       lead="A Prisma é a consultoria de tecnologia do grupo. Une IA em escala com curadoria humana na arquitetura, no levantamento de necessidades e na qualidade da entrega. Em vendas, atendimento, marketing, financeiro, RH e operação: onde houver ganho.",
       pains_h2="A IA já chegou na sua empresa ou só no discurso?",
       pains=[("i-message","IA só no discurso","A empresa sabe que precisa, mas não sabe por onde começar nem como medir o retorno."),
              ("i-zap","Horas em tarefa repetitiva","Relatórios, atendimento, propostas e conferências manuais tomando o tempo de todas as áreas."),
              ("i-layers","Cada um usa de um jeito","Cada área testa uma ferramenta diferente, sem padrão, governança nem segurança de dados.")],
       deliv_h2="Três frentes, escopo limpo", deliv_cta="Quero conversar sobre isso",
       deliv=[("i-target","Consultoria em IA","Levantamento de necessidades com curadoria humana, mapa de oportunidades priorizado por retorno e plano de adoção por área. Três alternativas, uma recomendação."),
              ("i-users","Treinamento e padronização","Capacitação prática por área e padrões de uso: ferramentas aprovadas, prompts, fluxos de trabalho e regras de segurança de dados."),
              ("i-cpu","Soluções personalizadas com IA","Agentes, automações e sistemas sob medida, integrados às ferramentas que a empresa já usa. Arquitetura desenhada antes de qualquer linha de código.")],
       how_eyebrow="O modelo", how_h2="Uma ideia. Três caminhos.",
       how_lead="Como o prisma separa a luz em cores, recebemos uma ideia como foco e a desdobramos em alternativas. Você paga pela entrega, não por horas ou pessoas alocadas.",
       how=["<b>Descoberta:</b> extração de necessidades com curadoria humana, área por área",
            "<b>Arquitetura:</b> desenho da solução antes de qualquer linha de código, com três alternativas e uma recomendação",
            "<b>Entrega:</b> IA em escala na construção, revisão humana em cada decisão e escopo fechado",
            "<b>Adoção:</b> treinamento do time, padrões de uso e indicadores acompanhados depois da entrega"],
       connects=["vendas","pessoas","seo-geo"],
       faq=[("A Prisma atua só em vendas?","Não. Atuamos na empresa inteira: vendas, atendimento, marketing, financeiro, RH e operação. Onde houver tarefa repetitiva ou decisão que se beneficia de dados, a IA pode gerar ganho."),
            ("O que significa vender solução, não horas?","Você contrata uma entrega com escopo e prazo definidos, não um pacote de horas ou um time alocado. A IA acelera a construção e a curadoria humana garante a qualidade."),
            ("O que significa padronizar o uso de IA?","É definir quais ferramentas usar, para quê e com quais regras: políticas de uso, proteção de dados, prompts e fluxos de trabalho por área, para que todo o time use IA do mesmo jeito e com segurança."),
            ("Preciso ter uma equipe de tecnologia?","Não. Conduzimos levantamento, arquitetura, desenvolvimento e treinamento. Quando há integração com sistemas internos, trabalhamos junto com o seu time ou fornecedor de TI.")]),
  dict(slug="seo-geo", seo_title="SEO e GEO: sua marca no Google e nas IAs | Oxyn SEO/GEO",
       seo_desc="Implementação e ongoing de SEO e GEO para a sua marca aparecer no Google e ser recomendada pelo ChatGPT, Gemini e Perplexity, com resultado medido em vendas.",
       unit="Oxyn SEO/GEO", short="SEO e GEO", icon="i-search", color="blue", img="foto-abstrato-capa.webp",
       card="Implementação e ongoing de SEO e GEO: sua marca encontrada no Google e recomendada pelas IAs, com resultado medido em vendas e leads.",
       tags=["Implementação", "Ongoing", "Google e IAs"],
       menu="Implementação e ongoing de SEO e GEO",
       title="SEO e GEO para empresas",
       eyebrow="Oxyn SEO/GEO · Visibilidade orgânica",
       h1_thin="Quando seu cliente pergunta,", h1="a resposta é a sua marca.",
       lead="Antes de escolher um produto, um serviço ou uma empresa, o seu cliente pesquisa no Google e pergunta ao ChatGPT, ao Gemini e ao Perplexity. A Oxyn implementa e opera SEO e GEO para a sua marca aparecer nessas respostas e ser a recomendação, e acompanha o resultado até a venda, o contato ou o cadastro.",
       pains_h2="Quando seu cliente pergunta, quem aparece?",
       pains=[("i-message","Invisível nas IAs","Seu cliente pergunta a uma IA quem resolve o problema dele e a resposta cita os seus concorrentes."),
              ("i-trend","Tráfego que não vira resultado","O site recebe visitas, mas poucas viram venda, contato ou cadastro."),
              ("i-chart","Refém da mídia paga","O custo por lead sobe e a geração de demanda para no dia em que o investimento para."),
              ("i-globe","Ninguém sabe o que as IAs dizem","Descrições erradas, dados desatualizados e terceiros falando pela sua marca nas respostas.")],
       deliv_h2="Da implementação ao ongoing", deliv_cta="Quero conversar sobre isso",
       deliv=[("i-target","Diagnóstico e plano","Auditoria técnica, de conteúdo e de autoridade, linha de base no Google e nas IAs e um plano priorizado pelo que mais aproxima a venda."),
              ("i-layers","Fundação técnica","Arquitetura do site, indexação, velocidade, dados estruturados e uma descrição única da empresa, dos produtos e dos especialistas."),
              ("i-message","Conteúdo que responde ao seu cliente","Mapa das perguntas que o seu cliente faz em cada etapa da decisão e páginas que o Google ranqueia e as IAs usam como fonte."),
              ("i-award","Autoridade fora do site","Menções em veículos do seu mercado, porta-vozes, dados próprios e presença nos canais que as IAs consultam para recomendar marcas."),
              ("i-chart","Ongoing e monitoramento","Ciclos mensais de otimização, perguntas monitoradas nas principais IAs com a plataforma Naia e relatório ligado a vendas e leads."),
              ("i-users","Capacitação do seu time","Treinamento, playbook e padrões de conteúdo para os times de marketing, conteúdo e e-commerce. Os ativos, os dados e o conhecimento ficam com a sua empresa.")],
       how_eyebrow="Como funciona", how_h2="Implementação e ongoing, um só programa",
       how_lead="Primeiro entendemos e planejamos; depois executamos de forma contínua, com checkpoints que recalibram o plano. O objetivo não é mais tráfego: é mais venda.",
       how=["<b>Mês 1 · Implementação:</b> diagnóstico, linha de base no Google e nas IAs, mapa das perguntas do seu cliente e plano priorizado",
            "<b>Meses 2 e 3 · Fundação:</b> correções técnicas, dados estruturados, identidade da marca consistente e primeiros conteúdos-piloto",
            "<b>A partir do mês 4 · Ongoing:</b> ciclos mensais de conteúdo, autoridade e otimização, com novas perguntas monitoradas a cada trimestre",
            "<b>Todo mês:</b> relatório que conecta presença, tráfego e resultado: vendas, contatos e cadastros",
            "<b>A cada trimestre:</b> checkpoint executivo com o que funcionou, o que escalar e o roadmap recalibrado"],
       connects=["vendas","fqd-studios","naia-geo-seo"],
       faq=[("O que é GEO?","GEO, ou Generative Engine Optimization, é o trabalho para que a sua marca seja mencionada, citada como fonte e recomendada nas respostas de IAs como ChatGPT, Gemini, Perplexity e AI Overviews do Google."),
            ("GEO substitui o SEO?","Não. O SEO é a fundação: sem um site rastreável, bem estruturado e com autoridade, as IAs dificilmente usam a sua marca como fonte. O GEO amplia essa fundação para as respostas geradas por IA. Tratamos os dois como um só trabalho."),
            ("Qual a diferença entre a Oxyn SEO/GEO e a Naia?","A Naia é a plataforma do grupo que monitora a presença da sua marca nas IAs. A Oxyn SEO/GEO é o serviço: planeja, implementa e opera o trabalho, usando a Naia como painel de medição."),
            ("Por que a Oxyn mede até a venda?","Porque o nosso negócio é fazer empresas venderem mais. Visibilidade que não vira venda, contato ou cadastro não paga o investimento, por isso o relatório vai até o resultado do negócio."),
            ("Em quanto tempo vejo resultado?","As correções técnicas e os primeiros pilotos costumam mostrar sinais no primeiro trimestre. Autoridade e presença consistente nas IAs são construídas ao longo dos meses seguintes, e as metas são definidas depois da linha de base do primeiro mês.")]),
  dict(slug="naia-geo-seo", seo_title="Naia: monitoramento da sua marca nas IAs | GEO",
       seo_desc="A Naia mostra como ChatGPT, Gemini, Perplexity e AI Overviews falam da sua marca: menções, citações, concorrentes, fontes e evolução mês a mês.",
       unit="Naia", short="Plataforma de GEO", icon="i-search", color="blue", img="foto-abstrato-capa.webp",
       card="Plataforma de GEO que mostra como as IAs falam da sua marca: menções, citações, concorrentes e fontes, com série histórica.",
       tags=["Monitoramento multi-IA", "Concorrentes e fontes", "Série histórica"],
       menu="Plataforma de monitoramento da marca nas IAs",
       title="Naia: plataforma de monitoramento da marca nas IAs",
       eyebrow="Naia · Plataforma de GEO",
       h1_thin="Saiba o que as IAs", h1="dizem da sua marca.",
       lead="Seus clientes perguntam ao ChatGPT, ao Gemini e ao Perplexity antes de escolher uma marca. A Naia acompanha essas respostas de forma contínua e mostra onde a sua marca aparece, quem aparece no lugar dela e em quais fontes as IAs se apoiam.",
       pains_h2="Você sabe o que as IAs respondem sobre o seu mercado?",
       pains=[("i-message","Ninguém mede","A empresa não sabe se é citada, em quais perguntas, nem em qual posição da resposta."),
              ("i-globe","Concorrentes no seu lugar","Quando seu cliente pede uma indicação, a IA recomenda outra marca e você nem fica sabendo."),
              ("i-layers","Informação errada circulando","Descrições desatualizadas ou imprecisas sobre a empresa e os produtos, repetidas a cada nova resposta.")],
       deliv_h2="O que a Naia mostra",
       deliv=[("i-message","Presença nas respostas","Menções, citações da sua URL e posição da marca em ChatGPT, Gemini, Perplexity e AI Overviews."),
              ("i-target","Concorrentes e fontes","Quais marcas aparecem nas mesmas perguntas e em quais sites as IAs se apoiam para responder."),
              ("i-search","Precisão e alertas","Descrições erradas ou desatualizadas da sua marca identificadas para correção."),
              ("i-chart","Série histórica","Evolução por pergunta, por IA e por localidade, para medir o efeito de cada ação ao longo dos meses.")],
       how_eyebrow="Como funciona", how_h2="Do primeiro painel à evolução mensal",
       how_lead="A Naia é a camada de medição. A execução do trabalho de SEO e GEO fica com a Oxyn SEO/GEO, ou com o seu próprio time.",
       how=["<b>Configuração:</b> marca, concorrentes e as perguntas que o seu cliente faz às IAs",
            "<b>Linha de base:</b> primeira leitura de presença, citações e fontes em cada IA",
            "<b>Monitoramento contínuo:</b> coleta recorrente, com registro de IA, data e localidade",
            "<b>Painel e relatórios:</b> evolução mês a mês e comparação com os concorrentes",
            "<b>Escala:</b> novas perguntas e mercados adicionados sem trocar de plataforma"],
       connects=["seo-geo","fqd-studios","vendas"],
       faq=[("O que é GEO?","GEO, ou Generative Engine Optimization, é o trabalho para que a sua marca seja mencionada, citada como fonte e recomendada nas respostas de IAs generativas como ChatGPT, Gemini e Perplexity."),
            ("Qual a diferença entre a Naia e a Oxyn SEO/GEO?","A Naia é a plataforma que mede a presença da sua marca nas IAs. A Oxyn SEO/GEO é o serviço que planeja, implementa e opera o trabalho para melhorar essa presença, usando a Naia como painel."),
            ("Posso contratar só a plataforma?","Sim. A Naia pode ser usada pelo seu próprio time de marketing ou pela sua agência. Quando você quiser execução, a Oxyn SEO/GEO assume o trabalho."),
            ("Quais IAs a Naia acompanha?","As principais IAs generativas usadas pelos seus clientes, como ChatGPT, Gemini, Perplexity e as respostas com IA do Google.")]),
  dict(slug="fqdtv", seo_title="Mídia de nicho e branded content B2B | FQDTV",
       seo_desc="Programas, distribuição segmentada e branded content para a sua marca falar com quem decide a compra nos nichos que a mídia de massa não alcança.",
       unit="FQDTV", short="Mídia de nicho", icon="i-megaphone", color="blue", img="foto-abstrato-escuro.webp",
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
  dict(slug="fqd-studios", seo_title="Estúdio de podcast e vídeo em São Paulo | FQD Studios",
       seo_desc="Estúdio em São Paulo para podcast, videocast, lives, aulas e conteúdo corporativo, com captação em 4K, pós-produção e gravações externas.",
       unit="FQD Studios", short="Estúdio e conteúdo", icon="i-video", color="blue", img="foto-abstrato-capa.webp",
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
OXYN = ["vendas", "pessoas", "seo-geo"]                      # frentes dentro da Oxyn
EMPRESAS = ["naia-geo-seo", "fqdtv", "fqd-studios", "prisma"]  # demais empresas do grupo
UNITS = [BY[s] for s in OXYN + EMPRESAS]
for u in UNITS:
    u["empresa"] = "Oxyn" if u["slug"] in OXYN else u["unit"]
# Logos oficiais das empresas do grupo (banner das paginas de solucao)
BY["naia-geo-seo"]["logo"] = "empresas/naia.svg"
BY["fqdtv"]["logo"] = "empresas/fqdtv.svg"
BY["fqd-studios"]["logo"] = "empresas/fqd-studios.svg"
BY["prisma"]["logo"] = "empresas/prisma.svg"   # logo negativo extraido do guia de marca da Prisma
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
JS_V = _ver("assets/js/main.js")
def _min_css(t):
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = re.sub(r"\s+", " ", t)
    return re.sub(r"\s*([{};,>])\s*", r"\1", t).replace(";}", "}").strip()
CSS = _min_css((OUT / "assets/css/styles.css").read_text(encoding="utf-8"))

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
  dict(nome="Paula Torres", logo="paula-torres.svg", site="https://www.paulatorres.com.br/"),
]
SECTORS = [("Indústria","i-factory"), ("Agro","i-wheat"), ("Farma","i-pill"), ("Varejo","i-store"),
           ("Educação","i-graduation"), ("Financeiro","i-bank"), ("Automotivo","i-car"), ("Aviação","i-plane")]

def head(title, desc, path, jsonld, hero="foto-abstrato-capa.webp"):
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
<meta property="og:image" content="{SITE}{IMG}/og-oxyn.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{IMG}/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{IMG}/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{IMG}/{hero}" as="image" fetchpriority="high">
<style>{CSS}</style>
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
        <img class="brand__logo" src="{IMG}/logo-oxyn-branco.webp" alt="Oxyn Group" width="240" height="86">
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
  <section class="section section--overlay cta-final has-ring" id="contato" data-section="cta" style="--img:url('{IMG}/foto-abstrato-capa.webp');--ring-o:.12;--ring-x:auto;--ring-y:-180px">
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
    return f"""  </main>

  <!-- FOOTER -->
  <footer class="footer" data-component="footer">
    <div class="container">
      <div class="footer__grid">
        <div>
          <a href="/" class="brand"><img class="brand__logo" src="{IMG}/logo-oxyn-branco.webp" alt="Oxyn Group" width="240" height="86" loading="lazy"></a>
          <p>Oxigenamos o crescimento B2B. Vendas, pessoas, SEO e GEO, IA, mídia e conteúdo para sua empresa vender mais.</p>
          <div class="socials">
            <a href="{LI}" aria-label="LinkedIn" target="_blank" rel="noopener"><svg class="icon icon--sm"><use href="#i-linkedin"/></svg></a>
            <a href="{IG}" aria-label="Instagram" target="_blank" rel="noopener"><svg class="icon icon--sm"><use href="#i-instagram"/></svg></a>
          </div>
        </div>
        <div><p class="footer__t">Soluções</p><ul>{sols}</ul></div>
        <div><p class="footer__t">Oxyn Group</p><ul>
          <li><a href="/#pilares">Pilares</a></li><li><a href="/#metodo">Método D.R.I.V.E.</a></li>
          <li><a href="/#fundadores">Fundadores</a></li><li><a href="/#contato">Contato</a></li></ul></div>
        <div><p class="footer__t">Contato</p><ul>
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
  "description": "Grupo de cinco empresas B2B focado em fazer clientes venderem mais: a Oxyn (consultoria comercial e terceirização de vendas, consultoria de RH e SEO e GEO), a Naia (plataforma de GEO), a FQDTV (mídia de nicho), a FQD Studios (estúdio de conteúdo) e a Prisma (consultoria de IA e tecnologia).",
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
    acionadas = {"pessoas":"Time e lideranças que sustentam", "seo-geo":"Sua marca no Google e nas IAs",
                 "prisma":"IA e tecnologia com escopo fechado", "naia-geo-seo":"Presença da marca nas IAs, medida", "fqdtv":"Reputação no seu nicho",
                 "fqd-studios":"Conteúdo que prova autoridade"}
    co = lambda s, nome: f'''<a class="sol__co" href="/solucoes/{s}"><b>{nome}</b><span>{acionadas[s]}</span></a>'''
    sol_frentes = "".join(co(s, BY[s]["short"].replace(" e RH","")) for s in ["pessoas","seo-geo"])
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
    eco = [("i-search","Ser encontrado","seo-geo","Oxyn SEO/GEO e Naia colocam sua marca no Google e nas respostas das IAs."),
           ("i-megaphone","Ser lembrado","fqdtv","FQDTV e FQD Studios constroem autoridade no seu nicho."),
           ("i-trend","Converter","vendas","A Oxyn transforma oportunidades em contratos assinados."),
           ("i-users","Escalar","pessoas","Oxyn Pessoas e Prisma dão estrutura, líderes e produtividade com IA.")]
    eco_cards = "\n".join(f"""        <a href="/solucoes/{s}" class="card card--eco" data-reveal><svg class="icon icon--cyan"><use href="#{i}"/></svg><h3 class="h5">{t}</h3><p>{d}</p></a>""" for i,t,s,d in eco)
    leaders = "\n".join(f"""        <article class="founder" data-reveal>
          <div class="founder__photo{"" if l["foto"] else " founder__photo--vazia"}">{f'<img src="{IMG}/fundadores/{l["foto"]}" alt="{l["nome"]}, {l["cargo"]} da Oxyn Group" loading="lazy" width="600" height="800">' if l["foto"] else ""}</div>
          <div class="founder__body">
            <span class="founder__role">{l["cargo"]}</span>
            <h3 class="founder__name">{l["nome"]}</h3>
            <p>{l["bio"]}</p>
          </div>
        </article>""" for l in LEADERS)
    faq_home = [("O que é a Oxyn Group?","A Oxyn Group é um grupo de cinco empresas B2B que oxigena o crescimento de outras empresas: a Oxyn, com as frentes Vendas, Pessoas e SEO/GEO; a Naia, plataforma de GEO; a FQDTV, de mídia de nicho; a FQD Studios, de produção de conteúdo; e a Prisma, de IA e tecnologia. Todas com o mesmo objetivo: fazer o cliente vender mais."),
                ("O que significa Business Converter™?","É a categoria que criamos para nos descrever. Não somos uma agência de representação nem uma consultoria que entrega um relatório e vai embora. Entramos na operação, estruturamos o que precisa ser estruturado e ficamos até o resultado aparecer."),
                ("Preciso contratar todas as frentes?","Não. Cada empresa do grupo pode ser contratada de forma independente. A vantagem de combinar frentes é ter um único parceiro cuidando da jornada inteira, da visibilidade ao fechamento."),
                ("Por onde começamos?","Pelo diagnóstico. Ele mostra se o gargalo está no processo, no time ou no mercado e define quais frentes fazem sentido para o seu momento.")]

    html = head("Oxyn Group | Consultoria de vendas B2B e operação comercial",
                "Consultoria de vendas B2B, treinamento e operação comercial terceirizada, com RH, IA, GEO e SEO, mídia e conteúdo no mesmo grupo. Agende um diagnóstico.",
                "/", [ORG, faq_ld(faq_home)])
    html += body_open()
    html += nav()
    html += '  <main id="conteudo">'
    html += f"""
  <!-- HERO | abstrato escuro (capa do manual) + anel em marca d'agua + grade de pontos -->
  <header class="hero has-ring" data-section="hero" style="--img:url('{IMG}/foto-abstrato-capa.webp')">
    <div class="container">
      <span class="dotgrid" aria-hidden="true"></span>
      <div class="hero__content hero__content--home">
        <p class="sol__kicker">Oxyn Group · Business Converter™</p>
        <h1 class="sol__title"><small>Vendas que não</small><b>dependem</b><b>de sorte<span>.</span></b></h1>
        <p class="lead">Venda travada raramente tem uma causa só. A OXYN identifica a origem, assume a operação e conduz a virada por inteiro: comercial, liderança, inteligência artificial, presença digital e conteúdo, trabalhando pelo mesmo resultado.</p>
        <div class="btn-row">
          <a href="#contato" class="btn btn--primary btn--lg">Agende um diagnóstico <span class="arrow">→</span></a>
          <a href="#solucao" class="btn btn--ghost btn--lg">Veja como funciona</a>
        </div>
      </div>
      <div class="hero__pains">
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
        <div class="sol__cred"><b>5</b><span>empresas integradas <br>em um só grupo</span></div>
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
  <section class="section section--overlay photo-section" data-section="positioning" style="--img:url('{IMG}/foto-abstrato-escuro.webp');--ov:.45">
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

  <!-- SOLUCOES | as 5 empresas do grupo: Oxyn (3 frentes) na primeira linha + Naia, FQDTV, FQD Studios e Prisma na segunda -->
  <section class="section section--white" id="solucoes" data-section="services">
    <div class="container">
      <header class="section-head section-head--center" data-reveal>
        <p class="eyebrow">Soluções</p>
        <h2 class="h2">Cinco empresas, a mesma lógica</h2>
        <p class="lead">A Oxyn, com as frentes Vendas, Pessoas e SEO/GEO, mais Naia, FQDTV, FQD Studios e Prisma. Contrate uma ou combine várias: todas trabalham pelo mesmo resultado, a sua receita.</p>
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

    html = head(u["seo_title"], u["seo_desc"], path, [service_ld, faq_ld(u["faq"])], hero=u["img"])
    html += body_open()
    html += nav(u["slug"])
    html += '  <main id="conteudo">'
    html += f"""
  <!-- HERO interno | uma foto por pagina, sobreposicao escura -->
  <header class="hero hero--page has-ring" data-section="hero" style="--img:url('{IMG}/{u["img"]}')">
    <div class="container{" hero__split" if u.get("logo") else ""}">
      <div class="hero__content">
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
      <div class="hero__logo"><img src="{IMG}/{u["logo"]}" alt="Logo {u["unit"]}" width="360" height="240"></div>''' if u.get("logo") else ""}
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
      <div class="grid grid--{3 if len(u["deliv"]) == 6 else len(u["deliv"])}">
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

def not_found():
    """Pagina 404 (a Vercel serve o 404.html para qualquer endereco inexistente)."""
    html = head("Página não encontrada | Oxyn Group", "O endereço que você procurou não existe ou mudou de lugar.", "/404", [ORG])
    html = html.replace(f'<link rel="canonical" href="{SITE}/404">', '<meta name="robots" content="noindex">')
    links = "".join(f'<a href="/solucoes/{u["slug"]}">{u["unit"]}</a>' for u in UNITS)
    html += body_open() + nav() + '  <main id="conteudo">'
    html += f"""
  <header class="hero has-ring" data-section="hero" style="--img:url('{IMG}/foto-abstrato-capa.webp')">
    <div class="container">
      <div class="hero__content hero__content--home">
        <p class="sol__kicker">Erro 404</p>
        <h1 class="sol__title"><small>Esta página</small><b>não existe<span>.</span></b></h1>
        <p class="lead">O endereço pode ter mudado. Volte para o início ou vá direto para uma das nossas soluções.</p>
        <div class="btn-row"><a href="/" class="btn btn--primary btn--lg">Ir para o início <span class="arrow">→</span></a></div>
        <nav class="nf-links" aria-label="Soluções">{links}</nav>
      </div>
    </div>
  </header>
"""
    return html + footer()

(OUT / "404.html").write_text(not_found(), encoding="utf-8")

urls = ["/"] + [f'/solucoes/{u["slug"]}' for u in UNITS]
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}{p}</loc></url>\n" for p in urls) + "</urlset>\n", encoding="utf-8")
print("ok:", len(urls), "paginas")
