# Projeto de Sub-redes /26 — Escola Municipal Rural de Colniza-MT

> Disciplina: **Network Architect Solutions** — Global Solution 2026 (Stratfy)
> Bloco base escolhido: **`192.168.10.0/24`** dividido em sub-redes **`/26`**.

## 1. Por que /26?

A escola tem duas redes lógicas que **devem ficar isoladas** uma da outra
(segurança e organização do tráfego):

| Rede | Quem usa | Estimativa de hosts |
|---|---|---|
| **Acadêmica** | salas de aula, laboratório de informática (notebooks/tablets dos alunos, projetor IP) | ~30–40 dispositivos |
| **Administrativa** | coordenação, secretaria, diretoria, impressora de rede | ~10–20 dispositivos |

Uma máscara **/26** entrega **64 endereços por sub-rede (62 hosts úteis)**, folga
confortável para o crescimento de cada rede sem desperdiçar o bloco. Dividir o
`/24` em `/26` gera **4 sub-redes**: usamos **2** agora (Acadêmica e
Administrativa) e deixamos **2 reservadas** para expansão futura (ex.: ponto de
telemedicina e Wi-Fi comunitário/IoT de alerta de incêndio).

## 2. Verificação aritmética da /26

```
/26  ->  prefixo com 26 bits de rede e 6 bits de host
Bits de host = 32 - 26 = 6
Endereços por sub-rede = 2^6 = 64
Hosts úteis = 64 - 2 (rede + broadcast) = 62
Máscara = 11111111.11111111.11111111.11000000 = 255.255.255.192
Salto de rede (4o octeto) = 256 - 192 = 64  -> redes em .0, .64, .128, .192
```

Total: `4 sub-redes x 64 = 256 = /24`. Confere com o bloco base.

## 3. Tabela de sub-redes (4 x /26)

| # | Sub-rede / papel | Endereço de rede | Máscara | Gateway (1º IP) | Faixa de hosts utilizáveis | Broadcast | Hosts úteis |
|---|---|---|---|---|---|---|---|
| 1 | **Acadêmica** (salas + laboratório) | `192.168.10.0/26` | `255.255.255.192` | `192.168.10.1` | `192.168.10.2` – `192.168.10.62` | `192.168.10.63` | 62 |
| 2 | **Administrativa** (coord. + admin.) | `192.168.10.64/26` | `255.255.255.192` | `192.168.10.65` | `192.168.10.66` – `192.168.10.126` | `192.168.10.127` | 62 |
| 3 | Reservada-1 (telemedicina) | `192.168.10.128/26` | `255.255.255.192` | `192.168.10.129` | `192.168.10.130` – `192.168.10.190` | `192.168.10.191` | 62 |
| 4 | Reservada-2 (Wi-Fi comunitário / IoT) | `192.168.10.192/26` | `255.255.255.192` | `192.168.10.193` | `192.168.10.194` – `192.168.10.254` | `192.168.10.255` | 62 |

> As linhas 3 e 4 ficam **provisionadas no plano de endereçamento**, mas **não**
> são configuradas no roteador agora (sem interface/pool), para manter a config
> enxuta. Estão prontas para ativação quando a infraestrutura crescer.

## 4. Endereços reservados (não entram no DHCP)

Em cada rede ativa reservamos os dois primeiros endereços úteis **e o último**
(usado pela gerência do switch):

| Sub-rede | `.1`/`.65` (gateway) | `.2`/`.66` (servidor local) | `.62`/`.126` (gerência do switch) | 1º IP entregue por DHCP |
|---|---|---|---|---|
| Acadêmica `192.168.10.0/26` | `192.168.10.1` (G0/0 do router) | `192.168.10.2` (servidor/NAS de conteúdo offline) | `192.168.10.62` (SVI VLAN 10 do SW-ACADEMICA) | `192.168.10.3` |
| Administrativa `192.168.10.64/26` | `192.168.10.65` (G0/1 do router) | `192.168.10.66` (servidor/impressora administrativa) | `192.168.10.126` (SVI VLAN 20 do SW-ADMINISTRATIVA) | `192.168.10.67` |

Todos esses endereços são declarados como `ip dhcp excluded-address` no Cisco
1941 (ver `configs/router_1941.txt`) — **coerência total** entre tabela,
interfaces, IPs de gerência dos switches e pools DHCP. Assim o DHCP nunca
entrega um IP já em uso por gateway, servidor ou switch.

## 5. Endereçamento do enlace de saída (Starlink)

O Cisco 1941 possui apenas duas interfaces Gigabit *onboard* (**G0/0** e **G0/1**),
ambas dedicadas às LANs /26 (Acadêmica e Administrativa), exatamente como exige o
enunciado. Para o uplink de Internet, o roteador é equipado com um **módulo EHWIC
Gigabit (`HWIC-1GE-SFP`)** no slot 0, que fornece a interface **`GigabitEthernet0/0/0`**
usada como **porta WAN**. O modem/roteador Starlink atua como gateway de Internet
em uma **rede de trânsito separada** (fora do bloco /24 da LAN), fazendo NAT/CGNAT
para a operadora:

| Enlace | Rede | Lado escola (1941 — G0/0/0, módulo EHWIC) | Lado Starlink |
|---|---|---|---|
| Trânsito WAN | `192.168.100.0/30` (fora do bloco /24 da LAN) | `192.168.100.2` | `192.168.100.1` (gateway Starlink, NAT/CGNAT para a Internet) |

> Na montagem do Packet Tracer, adicione ao 1941 um módulo Gigabit
> (`HWIC-1GE-SFP` + transceiver de cobre `GLC-T`) para habilitar a interface
> `G0/0/0`. O passo a passo está em `docs/guia_packet_tracer.md`; a topologia
> física completa em `docs/topologia.md`.

## 6. Conferência automatizada

A aritmética desta tabela é **validada por script** (`redes/valida_subredes.py`,
módulo `ipaddress` da biblioteca padrão). Saída resumida:

```
LAN1 - Rede Academica       192.168.10.0/26    255.255.255.192  gw 192.168.10.1   192.168.10.2-62    bcast .63   62 hosts
LAN2 - Rede Administrativa  192.168.10.64/26   255.255.255.192  gw 192.168.10.65  192.168.10.66-126  bcast .127  62 hosts
RESERVADA-1                 192.168.10.128/26  255.255.255.192  gw 192.168.10.129 192.168.10.130-190 bcast .191  62 hosts
RESERVADA-2                 192.168.10.192/26  255.255.255.192  gw 192.168.10.193 192.168.10.194-254 bcast .255  62 hosts
OK - todas as verificacoes aritmeticas das /26 passaram.
```
