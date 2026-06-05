# ADR 004 — Repositório de conhecimento como página separada

**Data:** 2026-06-05
**Status:** Aceito
**Sprint:** 3

## Contexto

A Sprint 3 adiciona conteúdo doutrinário denso: inventário de autores,
brocardos latinos, direito comparado glocal (global + local, Robertson, 1990s).
Havia duas opções de alocação: seção expansível dentro da página do Grafo
ou página separada no menu do Streamlit.

## Decisão

Página separada `5_📚_Repositório.py`.

Razões:
1. O repositório é um produto editorial autônomo — não é acessório do grafo
2. Usuários diferentes têm jornadas diferentes: o dev júnior vai direto ao grafo;
   o advogado doutrinador vai ao repositório
3. Scroll infinito como espaço editorial (Sprint 4) exige página própria
4. Separação permite evolução independente das duas páginas

## Alternativas consideradas

- Seção expansível no grafo — descartado: sobrecarrega a página principal
- Modal/overlay — descartado: limitação técnica do Streamlit

## Consequências

- Menu lateral do Streamlit fica com 5 páginas (adequado para MVP)
- Repositório evolui para atlas editorial nas Sprints 4–6
- Grafo mantém foco na visualização interativa
