# Estado atual para continuidade

**Data:** 8 de outubro de 2026  
**Versão:** `0.1.0-dev`

## Decisão central

O projeto é a central operacional do escritório contábil virtual. Não devemos construir agora motores de contabilidade, folha ou fiscal. Esses processos serão executados por sistemas brasileiros especializados e integrados à nossa plataforma.

## Implementado

- Django 5.2, PostgreSQL, Docker e `uv`;
- escritório e usuário personalizado;
- papéis `ADMIN`, `ACCOUNTANT`, `ANALYST` e `VIEWER`;
- cliente PF/PJ e escopo serviços/comércio/misto;
- atribuição de acesso por cliente;
- serviço transacional de cadastro;
- seis tarefas automáticas de onboarding;
- conclusão de tarefas e ativação automática;
- auditoria imutável na camada de aplicação;
- catálogo de conectores sem armazenamento de segredo;
- login, painel, cadastro e detalhe do cliente;
- comando `bootstrap_office`;
- testes, lint, formatação e verificação de migrações.

## Próximo incremento recomendado

Criar o módulo de solicitações do cliente, começando por quatro tipos: documento, admissão, férias e desligamento. Cada solicitação deverá ter estado, prazo, responsável, comentários, anexos e auditoria. O usuário externo do cliente entrará somente após o fluxo interno estar testado.

## Não fazer ainda

- OAuth real do Bling;
- transmissão ao eSocial;
- cálculos de folha ou impostos;
- lançamentos contábeis;
- IA com dados reais;
- armazenamento de certificados ou tokens no banco comum.

