# Conectividade via Satélite para Escola em Região Remota
## Escola Municipal Rural de Colniza-MT

> **Disciplina:** Network Architect Solutions
> **Curso:** Engenharia de Software — FIAP — Turma 2ESPH
> **Evento:** Global Solution 2026 — Economia Espacial
> **Tema do grupo (Stratfy):** Sistema de Detecção de Incêndios Florestais
> (focos de calor por satélite + clima + desmatamento no Brasil, 2025)

---

## 1. Integrantes do grupo Stratfy

| Nome | RM |
|---|---|
| Anthony Sforzin | RM562096 |
| Luigi Mendes Cabrini | RM563552 |
| Rogério Cruz Arroyo | RM563517 |
| Bruno Koeke | RM561309 |

---

## 2. Conexão com o tema do grupo

O grupo Stratfy desenvolve um **Sistema de Detecção de Incêndios Florestais**
que cruza focos de calor de satélite (INPE/BDQueimadas), clima (INMET) e
desmatamento (PRODES). A análise dos dados reais de 2025 (3.466.399 focos)
mostra que **a fronteira do fogo está exatamente onde a infraestrutura de
telecomunicações é mais precária**: o arco do desmatamento e a região MATOPIBA.

Esta entrega de **Network Architect Solutions** resolve a outra ponta do
problema: **de nada adianta detectar o fogo por satélite se a comunidade local
não tem conectividade** para receber o alerta, acionar a brigada e proteger
alunos e moradores. Levar Internet de qualidade a uma escola rural no epicentro
das queimadas é, portanto, parte integrante da solução do grupo.

---

## 3. Região escolhida: Colniza (MT)

### 3.1 Por que Colniza?

**Colniza** é um município do extremo noroeste de **Mato Grosso**, na divisa com
**Amazonas** e **Rondônia**, dentro do bioma **Amazônia** e do **arco do
desmatamento**. A escolha é **diretamente sustentada pelos dados reais do
projeto**:

> Na amostra agregada do grupo (`build/dados-preparados/focos_municipios_agg.csv`),
> **Colniza-MT é o município nº 1 do Brasil em focos de calor**, com
> **42.141 focos** na amostra, bioma **Amazônia**, **risco de fogo médio ≈ 0,815**
> (muito alto), centroide em **lat −9,16 / lon −60,21**.

| Indicador (dados do projeto) | Colniza-MT |
|---|---|
| Posição no ranking de focos (amostra) | **1º lugar do Brasil** |
| Focos de calor (amostra) | 42.141 |
| Bioma predominante | Amazônia |
| Risco de fogo médio | ~0,815 (alto) |
| Coordenadas (centroide) | −9,16 ; −60,21 |

> Município alternativo coerente: **Apuí-AM** (5º lugar, 27.220 focos, também na
> Amazônia). Optamos por **Colniza** por ser o nº 1 absoluto e por ilustrar de
> forma extrema o cenário de "muito fogo, pouca infraestrutura".

### 3.2 Caracterização: relevo, vegetação, distância e infraestrutura

- **Distância e isolamento:** Colniza fica a **mais de 1.000 km de Cuiabá**
  (capital), com acesso por estradas de terra (não pavimentadas em boa parte),
  intransitáveis em vários trechos durante a estação chuvosa. É um dos
  municípios mais **isolados** de Mato Grosso.
- **Relevo e vegetação:** terreno de **floresta amazônica densa**, com vales,
  rios e cobertura vegetal alta. Essa densidade de copas **bloqueia o sinal**
  de rádio/celular e dificulta lançar fibra óptica por longas distâncias.
- **Baixa infraestrutura:** cobertura de telefonia móvel **escassa e
  concentrada na sede**; a zona rural — onde ficam muitas escolas e
  comunidades — é praticamente **sombra de sinal**. Energia elétrica
  **instável**, com quedas frequentes (daí o uso de **no-break/UPS** no
  projeto). Não há backbone de fibra chegando às escolas rurais.
- **Pressão de queimadas:** por estar no arco do desmatamento, a região
  concentra **focos intensos na estação seca (ago–out/2025)**, ameaçando
  diretamente a comunidade escolar.

Esse conjunto — **isolamento + floresta densa + infraestrutura terrestre
inviável + alto risco de incêndio** — torna a **conectividade via satélite** a
única solução técnica e economicamente realista.

---

## 4. Problema de conectividade (cobertura das operadoras)

A conectividade terrestre (celular/fibra) é inviável na zona rural de Colniza.
Para **comprovar visualmente**, este documento se apoia nos **mapas oficiais de
cobertura** das operadoras.

### 4.1 Onde capturar os prints (instruções)

> **Espaço reservado para o print da cobertura Claro/TIM.** Capture e salve em
> `assets/prints/` com os nomes indicados, e insira a imagem abaixo de cada item.

1. **Mapa de cobertura da Claro**
   - Acesse o mapa oficial de cobertura da Claro (site da Claro → "Mapa de
     cobertura" / "Cobertura da rede").
   - Busque por **"Colniza, MT"**.
   - Aproxime o mapa na **zona rural** do município (fora da sede).
   - Capture a tela mostrando a **ausência/escassez de 4G/5G** na área rural.
   - Salve como **`assets/prints/cobertura_claro_colniza.png`**.

   > 🖼️ **[INSERIR PRINT AQUI]** — salve o arquivo em `assets/prints/cobertura_claro_colniza.png`
   > e descomente a linha abaixo:
   > <!-- ![Cobertura Claro em Colniza-MT](../assets/prints/cobertura_claro_colniza.png) -->

   *Figura 1 — Cobertura Claro na região de Colniza-MT (print a inserir pelo grupo).*

2. **Mapa de cobertura da TIM**
   - Acesse o mapa oficial de cobertura da TIM (site da TIM → "Cobertura").
   - Busque por **"Colniza, MT"** e aproxime na zona rural.
   - Capture a tela evidenciando a **falta de sinal** fora da sede.
   - Salve como **`assets/prints/cobertura_tim_colniza.png`**.

   > 🖼️ **[INSERIR PRINT AQUI]** — salve o arquivo em `assets/prints/cobertura_tim_colniza.png`
   > e descomente a linha abaixo:
   > <!-- ![Cobertura TIM em Colniza-MT](../assets/prints/cobertura_tim_colniza.png) -->

   *Figura 2 — Cobertura TIM na região de Colniza-MT (print a inserir pelo grupo).*

> **Observação esperada nos mapas:** cobertura móvel (3G/4G) **concentrada na
> sede urbana** e **inexistente ou intermitente** nas comunidades rurais e na
> localização da escola. Não há oferta de banda larga fixa por fibra. Isso
> justifica tecnicamente a opção por satélite.

---

## 5. Empresa de satélite escolhida: Starlink

Escolhemos a **Starlink (SpaceX)**, serviço de Internet via **constelação de
satélites em órbita baixa (LEO)**. É a opção recomendada por unir **baixa
latência** (graças à órbita baixa), **alta velocidade** e **disponibilidade
real em todo o território brasileiro**, inclusive na Amazônia — onde já é usada
por escolas, postos de saúde e operações de fiscalização ambiental.

### 5.1 Por que Starlink (e não satélite geoestacionário tradicional)?

| Critério | Starlink (LEO) | Satélite geoestacionário (GEO) clássico |
|---|---|---|
| Latência | **Baixa (~25–60 ms)** | Alta (600+ ms) — ruim para videochamada |
| Velocidade típica | **50–250 Mbps** download | 10–40 Mbps |
| Instalação | **Autoinstalável**, kit único | Requer técnico, antena grande |
| Disponibilidade em Colniza | **Sim** (cobre todo o Brasil) | Sim, mas com latência alta |
| Adequação a aulas online / telemedicina | **Alta** | Limitada pela latência |

A latência baixa é decisiva para **videoaulas, telemedicina e
videoconferência** — exatamente os usos sociais que justificam o projeto.

### 5.2 Velocidade, disponibilidade e custos (estimativa de projeto)

> Valores de referência para o plano residencial/fixo no Brasil. Os valores
> exatos devem ser confirmados no site oficial da Starlink no momento da
> contratação; aqui usamos faixas representativas para o dimensionamento.

| Item | Estimativa de referência |
|---|---|
| **Velocidade de download** | ~50 a 250 Mbps (típico 100 Mbps) |
| **Velocidade de upload** | ~10 a 25 Mbps |
| **Latência** | ~25 a 60 ms |
| **Disponibilidade na região** | **Sim** — cobertura ativa em todo o Brasil, incluindo a Amazônia/Colniza |
| **Custo do equipamento (kit/antena)** | **~R$ 1.500 a R$ 2.500** (kit padrão: antena + roteador Wi-Fi + cabos), pagamento único |
| **Custo de instalação** | **Autoinstalação (R$ 0 de mão de obra)** — basta fixar a antena com visada do céu e ligar; mão de obra local opcional |
| **Mensalidade (plano residencial fixo)** | **~R$ 200 a R$ 350 / mês** |

> **Observação:** a Starlink frequentemente roda **promoções no valor do kit** e
> oferece **planos específicos** (residencial, móvel, prioritário). Para uma
> escola pública, vale avaliar **convênios/editais** (governo de MT, MEC,
> programas de inclusão digital) que podem **subsidiar o equipamento e a
> mensalidade**.

### 5.3 Justificativa da escolha

Para Colniza, Starlink é a melhor relação **custo × benefício × viabilidade**:

1. **Cobre a área** onde Claro/TIM não chegam (item 4) — disponibilidade
   imediata, sem depender de obra de fibra.
2. **Latência baixa** habilita os usos sociais de maior valor (telemedicina,
   videoaula, alertas em tempo real).
3. **Instalação simples e rápida**, adequada à falta de técnicos especializados
   na região.
4. **Custo previsível** (kit único + mensalidade fixa), compatível com
   orçamento de programas públicos de inclusão digital.

---

## 6. Explicação da solução

A solução leva a Internet da Starlink **para dentro da escola** e a distribui de
forma **organizada e segura** por uma rede local bem projetada:

1. A **antena Starlink** (no telhado, com visada do céu) recebe o sinal dos
   satélites LEO e o entrega ao **modem/roteador Starlink** dentro da escola.
2. O modem Starlink se conecta à **porta WAN do roteador Cisco 1941**, que é o
   **cérebro da rede interna**. O 1941:
   - é o **gateway** das duas redes locais;
   - faz **NAT/PAT** (todas as estações saem para a Internet por um único IP);
   - fornece **DHCP** (entrega IP automático aos computadores);
   - tem **rota default** apontando para o gateway Starlink.
3. O 1941 conecta-se a **dois switches Cisco 2960**, um para cada rede:
   - **Switch Acadêmico** → salas de aula + laboratório de informática;
   - **Switch Administrativo** → coordenação, secretaria e diretoria.
4. Os **PCs e notebooks** ligam-se aos switches e recebem IP automaticamente.

A rede é **segmentada em duas sub-redes /26 isoladas** (VLAN 10 e VLAN 20). Isso
traz **organização, segurança e controle**: o tráfego administrativo (dados de
alunos, documentos) fica separado do tráfego do laboratório, e o roteamento
entre elas passa pelo 1941, onde se pode aplicar políticas de acesso.

> Detalhes técnicos completos: topologia em `docs/topologia.md`, tabela de
> endereçamento em `redes/tabela_subredes.md`, configurações em `configs/` e o
> passo a passo de montagem em `docs/guia_packet_tracer.md`.

---

## 7. Projeto de sub-redes (resumo)

Bloco **`192.168.10.0/24`** dividido em **`/26`** (4 sub-redes de 64 endereços,
**62 hosts úteis** cada, máscara **`255.255.255.192`**):

| Sub-rede / papel | Rede | Gateway | Faixa de hosts | Broadcast |
|---|---|---|---|---|
| **Acadêmica** (salas + laboratório) | `192.168.10.0/26` | `192.168.10.1` | `.2` – `.62` | `192.168.10.63` |
| **Administrativa** (coord. + admin.) | `192.168.10.64/26` | `192.168.10.65` | `.66` – `.126` | `192.168.10.127` |
| Reservada-1 (telemedicina) | `192.168.10.128/26` | `192.168.10.129` | `.130` – `.190` | `192.168.10.191` |
| Reservada-2 (Wi-Fi comunitário / IoT) | `192.168.10.192/26` | `192.168.10.193` | `.194` – `.254` | `192.168.10.255` |

### 7.1 Verificação aritmética da /26

```
/26 -> 32 - 26 = 6 bits de host -> 2^6 = 64 endereços por sub-rede
Hosts úteis = 64 - 2 = 62
Máscara = 255.255.255.192   (salto de rede = 256 - 192 = 64)
Redes em .0, .64, .128, .192  ->  4 x 64 = 256 = /24  (confere)
```

> Esta aritmética é **validada automaticamente** pelo script
> `redes/valida_subredes.py` (módulo `ipaddress`), que confirma máscara, número
> de hosts, gateways, faixas, broadcast e a coerência com os pools DHCP do
> roteador. Saída do teste registrada no `README.md`.

---

## 8. Impacto social da conectividade

Conectar a Escola Rural de Colniza transforma a comunidade em várias frentes —
e fecha o ciclo do **Sistema de Detecção de Incêndios** do grupo:

### 8.1 Educação
- **Acesso a conteúdo digital e plataformas de ensino** (vídeos, ENEM, cursos
  online) antes inacessíveis na zona rural.
- **Videoaulas e reforço a distância**, reduzindo o isolamento pedagógico de
  professores e alunos.
- **Inclusão digital** de crianças e jovens que hoje não têm contato com a
  Internet, ampliando oportunidades de futuro.

### 8.2 Telemedicina
- A escola vira **ponto de telessaúde** da comunidade: **teleconsultas** com
  médicos de centros urbanos, **encaminhamento de exames** e **orientação em
  emergências**, sem a viagem de mais de 1.000 km até a capital.
- Em uma região onde o posto de saúde é distante, a **latência baixa da
  Starlink** viabiliza atendimento por vídeo em tempo real.

### 8.3 Alertas de incêndio (integração com o projeto do grupo)
- Com Internet, a escola e a comunidade **recebem em tempo real os alertas de
  focos de calor** gerados pelo Sistema de Detecção do grupo Stratfy
  (dados INPE/INMET/PRODES).
- Permite **acionar brigadas e a Defesa Civil**, **evacuar com antecedência** e
  **proteger alunos** durante a estação seca (ago–out), quando os focos
  explodem na região.
- A escola pode hospedar **sensores IoT** (a sub-rede reservada-2 já está
  provisionada) que enviam leituras ambientais para o sistema central via
  Starlink, ampliando a malha de detecção.

> **Síntese:** a mesma economia espacial que **detecta** o fogo do céu (satélites
> do INPE) agora também **conecta** a comunidade do solo (satélites Starlink),
> fechando o ciclo entre **detectar, alertar e proteger** — exatamente a
> proposta do grupo Stratfy na Global Solution 2026.

---

## 9. Índice de artefatos do repositório

| Arquivo | Conteúdo |
|---|---|
| `README.md` | Apresentação do grupo, resumo e índice |
| `docs/documento_projeto.md` | **Este documento** (principal) |
| `docs/topologia.md` | Topologia física/lógica + diagrama Mermaid |
| `docs/guia_packet_tracer.md` | Passo a passo de montagem e validação no Packet Tracer |
| `redes/tabela_subredes.md` | Projeto detalhado das sub-redes /26 |
| `redes/valida_subredes.py` | Script de validação aritmética (módulo `ipaddress`) |
| `configs/router_1941.txt` | Configuração IOS completa do Cisco 1941 (DHCP + NAT) |
| `configs/switch_2960_academica.txt` | Configuração do switch da rede Acadêmica |
| `configs/switch_2960_administrativa.txt` | Configuração do switch da rede Administrativa |
| `assets/prints/` | Local para os prints de cobertura Claro/TIM |
