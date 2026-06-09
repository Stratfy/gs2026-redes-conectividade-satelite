# Conectividade via Satélite para Escola em Região Remota — Colniza-MT

**Disciplina:** Network Architect Solutions
**Curso:** Engenharia de Software — FIAP — Turma **2ESPH**
**Evento:** Global Solution 2026 — *Economia Espacial*
**Grupo:** **Stratfy**
**Tema do grupo:** Sistema de Detecção de Incêndios Florestais (focos de calor por satélite + clima + desmatamento, Brasil 2025)

---

## Integrantes

| Nome | RM |
|---|---|
| Anthony Sforzin | RM562096 |
| Luigi Mendes Cabrini | RM563552 |
| Rogério Cruz Arroyo | RM563517 |
| Bruno Koeke | RM561309 |

---

## Resumo do projeto

Este entregável projeta a **rede de uma escola municipal rural em Colniza (MT)**,
o **município nº 1 do Brasil em focos de calor** segundo os dados reais do grupo
(42.141 focos na amostra, bioma Amazônia, risco de fogo ~0,815). A região está
no **arco do desmatamento**, é **isolada** (mais de 1.000 km de Cuiabá), de
**floresta densa** e **sem cobertura de celular/fibra** na zona rural.

A solução leva **Internet via satélite Starlink (órbita baixa, baixa latência)**
e a distribui internamente por uma rede **Cisco** bem projetada:

- **1x Roteador Cisco 1941** — gateway das LANs, **DHCP**, **NAT**, rota default
  para o uplink Starlink;
- **2x Switch Cisco 2960** — rede **Acadêmica** (salas + laboratório) e rede
  **Administrativa** (coordenação + administração);
- **Endereçamento `192.168.10.0/24` dividido em `/26`** (4 sub-redes de 62 hosts
  úteis; 2 ativas + 2 reservadas para expansão).

O projeto fecha o ciclo do tema do grupo: a economia espacial que **detecta** o
fogo (satélites INPE) passa também a **conectar** a comunidade (satélites
Starlink), habilitando **educação, telemedicina e alertas de incêndio** em tempo
real.

---

## Índice dos artefatos

| Artefato | Descrição |
|---|---|
| [`rede_escola_colniza.pkt`](rede_escola_colniza.pkt) | **Arquivo Cisco Packet Tracer** (50%): topologia lógica e física com Router 1941 + 2× Switch 2960 + hosts, DHCP, NAT e as duas sub-redes /26 configuradas |
| [`docs/documento_projeto.md`](docs/documento_projeto.md) | **Documento principal** (50%): região, problema de conectividade, Starlink (velocidade/custos/justificativa), solução, sub-redes e impacto social |
| [`docs/topologia.md`](docs/topologia.md) | Topologia física e lógica + diagrama **Mermaid** + lista de dispositivos e mapa de portas |
| [`docs/guia_packet_tracer.md`](docs/guia_packet_tracer.md) | Passo a passo para montar o `.pkt` e validar (DHCP + ping entre redes) |
| [`redes/tabela_subredes.md`](redes/tabela_subredes.md) | Projeto detalhado das **sub-redes /26** com verificação aritmética |
| [`redes/valida_subredes.py`](redes/valida_subredes.py) | Script Python (`ipaddress`) que **valida a aritmética** das /26 |
| [`configs/router_1941.txt`](configs/router_1941.txt) | Config IOS completa do **Cisco 1941** (interfaces, DHCP, NAT, rota) |
| [`configs/switch_2960_academica.txt`](configs/switch_2960_academica.txt) | Config do **Switch 2960** da rede Acadêmica (VLAN 10) |
| [`configs/switch_2960_administrativa.txt`](configs/switch_2960_administrativa.txt) | Config do **Switch 2960** da rede Administrativa (VLAN 20) |
| [`assets/prints/`](assets/prints/) | Local dos prints de cobertura Claro/TIM (ver `LEIAME.md`) |

> **Nota:** o arquivo **`rede_escola_colniza.pkt`** (Cisco Packet Tracer) está
> versionado neste repositório. As configurações (`configs/`), a tabela de
> sub-redes e o guia de montagem (`docs/guia_packet_tracer.md`) documentam e
> reproduzem o projeto. **Pendência:** inserir os 2 prints de cobertura
> (Claro/TIM) em `assets/prints/` e exportar o documento para PDF — ver
> `assets/prints/LEIAME.md`.

---

## Plano de endereçamento (resumo)

| Sub-rede | Rede | Máscara | Gateway | Faixa de hosts | Broadcast |
|---|---|---|---|---|---|
| **Acadêmica** | `192.168.10.0/26` | `255.255.255.192` | `192.168.10.1` | `.2`–`.62` | `192.168.10.63` |
| **Administrativa** | `192.168.10.64/26` | `255.255.255.192` | `192.168.10.65` | `.66`–`.126` | `192.168.10.127` |
| Reservada-1 | `192.168.10.128/26` | `255.255.255.192` | `192.168.10.129` | `.130`–`.190` | `192.168.10.191` |
| Reservada-2 | `192.168.10.192/26` | `255.255.255.192` | `192.168.10.193` | `.194`–`.254` | `192.168.10.255` |

---

## Como validar a aritmética das sub-redes

Requisito: **Python 3** (usa apenas a biblioteca padrão, módulo `ipaddress`).

```bash
python redes/valida_subredes.py
```

Saída obtida (exit code **0**):

```
PROJETO DE SUB-REDES /26 - Escola Rural de Colniza-MT
Bloco base ............ 192.168.10.0/24
Divisao em /26 ......... 4 sub-redes de 64 enderecos
Mascara /26 ........... 255.255.255.192 (esperada: 255.255.255.192)

TABELA VERIFICADA (calculada por ipaddress)
LAN1 - Rede Academica       192.168.10.0/26    gw 192.168.10.1   192.168.10.2-62    bcast .63   62 hosts
LAN2 - Rede Administrativa  192.168.10.64/26   gw 192.168.10.65  192.168.10.66-126  bcast .127  62 hosts
RESERVADA-1                 192.168.10.128/26  gw 192.168.10.129 192.168.10.130-190 bcast .191  62 hosts
RESERVADA-2                 192.168.10.192/26  gw 192.168.10.193 192.168.10.194-254 bcast .255  62 hosts

COERENCIA COM O DHCP DO ROUTER 1941
Pool ACADEMICA       rede=192.168.10.0/26   default-router=192.168.10.1   exclui .1-.2  -> 1o IP DHCP = 192.168.10.3
Pool ADMINISTRATIVA  rede=192.168.10.64/26  default-router=192.168.10.65  exclui .65-.66 -> 1o IP DHCP = 192.168.10.67

OK - todas as verificacoes aritmeticas das /26 passaram.
```

Isto comprova que **tabela de sub-redes**, **IPs das interfaces do router** e
**pools DHCP** (gateways, faixas e exclusões) estão **100% coerentes** entre si.
