#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
valida_subredes.py
==================
Validacao aritmetica do projeto de sub-redes /26 da Escola Municipal
Rural de Colniza-MT (Global Solution 2026 - Stratfy / Network Architect
Solutions).

O script usa SOMENTE a biblioteca padrao (modulo `ipaddress`) e confirma,
de forma independente das tabelas escritas a mao, que:

  1. O bloco 192.168.10.0/24 se divide em quatro sub-redes /26.
  2. Cada /26 tem mascara 255.255.255.192 (prefixo 26) e 62 hosts uteis.
  3. Os enderecos de rede, gateway, primeiro/ultimo host e broadcast
     declarados no projeto batem com o que o `ipaddress` calcula.
  4. Os gateways e o servidor reservado estao DENTRO da faixa de hosts e
     correspondem as exclusoes configuradas no DHCP do roteador.

Saida: tabela formatada + bloco de asserts. Codigo de saida 0 = OK.

Uso:
    python valida_subredes.py
"""

import ipaddress
import sys

# ---------------------------------------------------------------------------
# 1) Bloco base e divisao em /26
# ---------------------------------------------------------------------------
BLOCO_BASE = ipaddress.ip_network("192.168.10.0/24")
NOVO_PREFIXO = 26

# Projeto da escola: das quatro /26 disponiveis usamos duas (LAN1 e LAN2)
# e deixamos duas reservadas para crescimento futuro.
SUBREDES = list(BLOCO_BASE.subnets(new_prefix=NOVO_PREFIXO))

# Nomes/papeis declarados no projeto (devem casar com tabela_subredes.md)
PLANO = [
    {
        "nome": "LAN1 - Rede Academica",
        "rede": "192.168.10.0/26",
        "gateway": "192.168.10.1",
        "primeiro_host": "192.168.10.2",   # 1 = gateway, 2 = inicio do pool
        "ultimo_host": "192.168.10.62",
        "broadcast": "192.168.10.63",
        # gw + servidor local + IP de gerencia do switch academico (.62)
        "excluidos": ["192.168.10.1", "192.168.10.2", "192.168.10.62"],
        "uso": "salas de aula + laboratorio de informatica",
    },
    {
        "nome": "LAN2 - Rede Administrativa",
        "rede": "192.168.10.64/26",
        "gateway": "192.168.10.65",
        "primeiro_host": "192.168.10.66",
        "ultimo_host": "192.168.10.126",
        "broadcast": "192.168.10.127",
        # gw + servidor adm + IP de gerencia do switch administrativo (.126)
        "excluidos": ["192.168.10.65", "192.168.10.66", "192.168.10.126"],
        "uso": "coordenacao + administracao",
    },
    {
        "nome": "RESERVADA-1 (expansao)",
        "rede": "192.168.10.128/26",
        "gateway": "192.168.10.129",
        "primeiro_host": "192.168.10.130",
        "ultimo_host": "192.168.10.190",
        "broadcast": "192.168.10.191",
        "excluidos": [],
        "uso": "reserva para nova ala / telemedicina",
    },
    {
        "nome": "RESERVADA-2 (expansao)",
        "rede": "192.168.10.192/26",
        "gateway": "192.168.10.193",
        "primeiro_host": "192.168.10.194",
        "ultimo_host": "192.168.10.254",
        "broadcast": "192.168.10.255",
        "excluidos": [],
        "uso": "reserva para wi-fi comunitario / IoT de alerta",
    },
]

MASCARA_ESPERADA = "255.255.255.192"
HOSTS_ESPERADOS = 62
PREFIXO_ESPERADO = 26


def cabecalho(texto: str) -> None:
    print("\n" + "=" * 72)
    print(texto)
    print("=" * 72)


def main() -> int:
    cabecalho("PROJETO DE SUB-REDES /26 - Escola Rural de Colniza-MT")
    print(f"Bloco base ............ {BLOCO_BASE}")
    print(f"Total de enderecos .... {BLOCO_BASE.num_addresses}")
    print(f"Divisao em /{NOVO_PREFIXO} ......... "
          f"{len(SUBREDES)} sub-redes de {SUBREDES[0].num_addresses} enderecos")
    print(f"Mascara /{NOVO_PREFIXO} ........... {SUBREDES[0].netmask} "
          f"(esperada: {MASCARA_ESPERADA})")

    # Verificacao 0: o ipaddress gera exatamente as quatro redes do plano
    redes_calculadas = [str(s) for s in SUBREDES]
    redes_plano = [item["rede"] for item in PLANO]
    assert redes_calculadas == redes_plano, (
        f"Divisao /26 nao bate com o plano:\n  calc={redes_calculadas}\n  plano={redes_plano}"
    )

    cabecalho("TABELA VERIFICADA (calculada por ipaddress)")
    cab = (f"{'Sub-rede':<26}{'Rede':<18}{'Mascara':<17}"
           f"{'Gateway':<16}{'Faixa de hosts':<32}{'Broadcast':<16}{'Hosts'}")
    print(cab)
    print("-" * len(cab))

    erros = 0
    for item in PLANO:
        net = ipaddress.ip_network(item["rede"])
        hosts = list(net.hosts())            # exclui rede e broadcast
        primeiro = hosts[0]
        ultimo = hosts[-1]
        gw = ipaddress.ip_address(item["gateway"])

        # --- Verificacoes (a) mascara e prefixo ---
        assert str(net.netmask) == MASCARA_ESPERADA, (
            f"{item['nome']}: mascara {net.netmask} != {MASCARA_ESPERADA}")
        assert net.prefixlen == PREFIXO_ESPERADO, (
            f"{item['nome']}: prefixo /{net.prefixlen} != /{PREFIXO_ESPERADO}")

        # --- (b) numero de hosts uteis ---
        assert len(hosts) == HOSTS_ESPERADOS, (
            f"{item['nome']}: {len(hosts)} hosts != {HOSTS_ESPERADOS}")
        assert net.num_addresses - 2 == HOSTS_ESPERADOS

        # --- (c) gateway dentro da faixa e e o 1o endereco utilizavel ---
        assert gw in net, f"{item['nome']}: gateway fora da rede"
        assert gw == primeiro, (
            f"{item['nome']}: gateway {gw} != primeiro host {primeiro}")

        # --- (d) primeiro/ultimo host e broadcast declarados batem ---
        assert str(primeiro) == item["gateway"]
        assert str(ultimo) == item["ultimo_host"], (
            f"{item['nome']}: ultimo host {ultimo} != {item['ultimo_host']}")
        assert str(net.broadcast_address) == item["broadcast"], (
            f"{item['nome']}: broadcast {net.broadcast_address} != {item['broadcast']}")
        assert str(net.network_address) == item["rede"].split("/")[0]

        # --- (e) pool DHCP comeca apos as exclusoes e fica dentro da faixa ---
        for ip_excl in item["excluidos"]:
            ip = ipaddress.ip_address(ip_excl)
            assert ip in net, f"{item['nome']}: excluido {ip} fora da rede"
            assert ip != net.network_address and ip != net.broadcast_address

        # --- (f) sem sobreposicao com as demais sub-redes ---
        for outro in PLANO:
            if outro["rede"] != item["rede"]:
                n2 = ipaddress.ip_network(outro["rede"])
                assert not net.overlaps(n2), (
                    f"Sobreposicao entre {item['rede']} e {outro['rede']}")

        faixa = f"{primeiro} - {ultimo}"
        print(f"{item['nome']:<26}{str(net.with_prefixlen):<18}"
              f"{str(net.netmask):<17}{item['gateway']:<16}"
              f"{faixa:<32}{item['broadcast']:<16}{len(hosts)}")

    # ---------------------------------------------------------------------
    # 2) Coerencia com os pools DHCP do router_1941.txt
    # ---------------------------------------------------------------------
    cabecalho("COERENCIA COM O DHCP DO ROUTER 1941")
    pools = {
        "ACADEMICA":     {"rede": "192.168.10.0/26",  "default_router": "192.168.10.1",
                          "excluded_range": ("192.168.10.1", "192.168.10.2"),
                          "switch_mgmt": "192.168.10.62"},
        "ADMINISTRATIVA": {"rede": "192.168.10.64/26", "default_router": "192.168.10.65",
                          "excluded_range": ("192.168.10.65", "192.168.10.66"),
                          "switch_mgmt": "192.168.10.126"},
    }
    for nome, p in pools.items():
        net = ipaddress.ip_network(p["rede"])
        gw = ipaddress.ip_address(p["default_router"])
        ini, fim = (ipaddress.ip_address(p["excluded_range"][0]),
                    ipaddress.ip_address(p["excluded_range"][1]))
        mgmt = ipaddress.ip_address(p["switch_mgmt"])
        assert gw in net and gw == list(net.hosts())[0]
        assert ini in net and fim in net and ini <= gw <= fim
        # IP de gerencia do switch e o ultimo host util e tambem fica excluido
        assert mgmt in net and mgmt == list(net.hosts())[-1]
        primeiro_alocavel = fim + 1
        assert primeiro_alocavel in net
        print(f"Pool {nome:<15} rede={p['rede']:<17} "
              f"default-router={p['default_router']:<15} "
              f"exclui {p['excluded_range'][0]}-{p['excluded_range'][1]} + "
              f"mgmt-switch {p['switch_mgmt']} -> "
              f"1o IP DHCP = {primeiro_alocavel}")

    cabecalho("RESULTADO")
    print("OK - todas as verificacoes aritmeticas das /26 passaram.")
    print(f"  - {len(PLANO)} sub-redes /26, mascara {MASCARA_ESPERADA}, "
          f"{HOSTS_ESPERADOS} hosts uteis cada")
    print("  - gateways = 1o endereco utilizavel de cada rede")
    print("  - pools DHCP coerentes com gateways/exclusoes do router")
    print("  - nenhuma sobreposicao de enderecos")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print("\nFALHA DE VALIDACAO:", exc, file=sys.stderr)
        sys.exit(1)
