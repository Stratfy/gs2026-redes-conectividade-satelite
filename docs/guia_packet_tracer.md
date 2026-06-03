# Guia passo a passo — Montagem no Cisco Packet Tracer

> Disciplina: **Network Architect Solutions** — Global Solution 2026 (Stratfy)
> Objetivo: montar o arquivo `.pkt` da rede da Escola Rural de Colniza-MT
> colando as configs deste repositório e validar (DHCP + ping entre redes).
> Tempo estimado: **10–15 minutos**.

Este projeto entrega **todas as configurações e tabelas prontas**. O binário
`.pkt` não é versionado; siga este guia para reproduzi-lo. Versão de referência:
**Cisco Packet Tracer 8.x**.

---

## 1. Arrastar os dispositivos para a área de trabalho

No canto inferior esquerdo do Packet Tracer:

1. **Network Devices > Routers** → arraste **1 Cisco 1941** (ISR4321 também
   serve; o enunciado pede 1941). Renomeie para `R-COLNIZA`.
2. **Network Devices > Switches** → arraste **2 Cisco 2960** (modelo `2960`).
   Renomeie para `SW-ACADEMICA` e `SW-ADMINISTRATIVA`.
3. **End Devices** → arraste pelo menos:
   - 2 **PC** para a rede Acadêmica (ex.: `PC-Sala1`, `PC-Lab1`);
   - 2 **PC** para a rede Administrativa (ex.: `PC-Coord`, `PC-Secret`).
4. (Opcional) Para representar a Internet via Starlink: arraste um **Router**
   genérico ou um dispositivo **Cloud/Modem** e nomeie `STARLINK`.

> Importante: o Cisco 1941 vem com 2 portas Gigabit *onboard* (G0/0, G0/1), que
> usamos para as duas LANs /26. Para a porta WAN do uplink Starlink
> (`GigabitEthernet0/0/0`), **desligue o router** (botão de power no equipamento),
> arraste o módulo **`HWIC-1GE-SFP`** para um slot livre, encaixe um transceiver
> de cobre **`GLC-T`** e ligue novamente. Alternativamente, para fins de validação
> apenas da LAN, basta deixar a WAN sem uso — o ping interno e o DHCP funcionam
> sem Internet.

---

## 2. Cabeamento

Use **Connections > Copper Straight-Through** (cabo reto) para todos os enlaces:

| De | Porta | Para | Porta |
|---|---|---|---|
| R-COLNIZA | GigabitEthernet0/0 | SW-ACADEMICA | FastEthernet0/24 |
| R-COLNIZA | GigabitEthernet0/1 | SW-ADMINISTRATIVA | FastEthernet0/24 |
| SW-ACADEMICA | FastEthernet0/1 | PC-Sala1 | FastEthernet0 |
| SW-ACADEMICA | FastEthernet0/2 | PC-Lab1 | FastEthernet0 |
| SW-ADMINISTRATIVA | FastEthernet0/1 | PC-Coord | FastEthernet0 |
| SW-ADMINISTRATIVA | FastEthernet0/2 | PC-Secret | FastEthernet0 |
| (opcional) R-COLNIZA | GigabitEthernet0/0/0 (módulo EHWIC-1GE) | STARLINK | porta LAN |

As luzes do link devem ficar **verdes** após alguns segundos.

---

## 3. Colar a configuração do roteador

1. Clique em **R-COLNIZA** → aba **CLI**.
2. Pressione **Enter** até aparecer `Router>`.
3. Cole o conteúdo de **`configs/router_1941.txt`**.
   - Dica: cole em blocos. Se uma linha de comentário (`!`) for recusada, ignore
     — o IOS aceita `!`, mas a ordem dos comandos é o que importa.
   - O comando `crypto key generate rsa` pode pedir confirmação de tamanho da
     chave; aceite (`1024`).
4. Confirme que terminou com `write memory` (ou rode `copy running-config
   startup-config`).

Valide no router:
```
show ip interface brief
```
Esperado: `GigabitEthernet0/0` = `192.168.10.1` (up/up) e
`GigabitEthernet0/1` = `192.168.10.65` (up/up).

```
show ip dhcp pool
```
Esperado: pools `ACADEMICA` e `ADMINISTRATIVA` listados.

---

## 4. Colar a configuração dos switches

1. Clique em **SW-ACADEMICA** → **CLI** → cole
   **`configs/switch_2960_academica.txt`**.
2. Clique em **SW-ADMINISTRATIVA** → **CLI** → cole
   **`configs/switch_2960_administrativa.txt`**.

Valide em cada switch:
```
show vlan brief
```
Esperado: VLAN `10 ACADEMICA` (ou `20 ADMINISTRATIVA`) com as portas de acesso.

---

## 5. Configurar os PCs para DHCP

Para **cada PC**:

1. Clique no PC → aba **Desktop** → **IP Configuration**.
2. Marque **DHCP**.
3. Aguarde a mensagem **"DHCP request successful"**.

Resultado esperado (coerente com `redes/tabela_subredes.md`):

| PC | Rede | IP esperado (faixa) | Gateway | Máscara |
|---|---|---|---|---|
| PC-Sala1, PC-Lab1 | Acadêmica | `192.168.10.3`–`192.168.10.62` | `192.168.10.1` | `255.255.255.192` |
| PC-Coord, PC-Secret | Administrativa | `192.168.10.67`–`192.168.10.126` | `192.168.10.65` | `255.255.255.192` |

> Os endereços `.1`/`.2`/`.62` (acadêmica) e `.65`/`.66`/`.126` (administrativa)
> **não** são entregues (estão em `ip dhcp excluded-address`), por isso o
> primeiro IP cai em `.3` e `.67`. O `.62` e o `.126` são os IPs de gerência dos
> switches — excluídos para evitar conflito.

No router, confira as concessões:
```
show ip dhcp binding
```

---

## 6. Testes de validação (o que demonstrar na avaliação)

### 6.1 Ping dentro da mesma rede
No **PC-Sala1** → Desktop → **Command Prompt**:
```
ping 192.168.10.4      (IP do PC-Lab1)
```
Esperado: **respostas (Reply)**, 0% de perda.

### 6.2 Ping entre as duas redes (roteamento pelo 1941)
No **PC-Sala1** (Acadêmica) faça ping em um PC da Administrativa:
```
ping 192.168.10.67     (IP do PC-Coord)
```
Esperado: **respostas (Reply)** — prova que o Cisco 1941 roteia entre as /26.
(O primeiro pacote pode dar timeout por causa do ARP; do 2º em diante responde.)

### 6.3 Ping no gateway
```
ping 192.168.10.1      (gateway da rede Acadêmica)
ping 192.168.10.65     (gateway da rede Administrativa)
```
Esperado: respostas dos dois gateways.

### 6.4 (Opcional) Saída para a Internet via Starlink
Se o `STARLINK` foi montado e tem rota/serviço de Internet, um `ping 8.8.8.8`
deve sair pelo NAT do 1941. Para a avaliação da LAN, os testes 6.1–6.3 já
demonstram o funcionamento completo de sub-redes + DHCP + roteamento.

---

## 7. Checklist final

- [ ] R-COLNIZA com G0/0 `.1` e G0/1 `.65` up/up.
- [ ] Dois switches com VLAN 10 e VLAN 20 e port-security.
- [ ] PCs recebendo IP por DHCP nas faixas corretas (`.3+` e `.67+`).
- [ ] Ping OK dentro da mesma rede.
- [ ] Ping OK **entre** as duas redes (roteamento).
- [ ] `show ip dhcp binding` mostra as concessões.
- [ ] Salvar o arquivo como `escola_colniza.pkt`.

Pronto: a rede da Escola Rural de Colniza-MT está montada e validada,
coerente com a tabela de sub-redes e o script `redes/valida_subredes.py`.
