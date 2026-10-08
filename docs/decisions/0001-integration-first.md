# ADR 0001 — Plataforma integration-first

## Status

Aceita em 8 de outubro de 2026.

## Contexto

O planejamento inicial previa construir gradualmente um motor contábil próprio. A pesquisa de mercado mostrou que sistemas brasileiros consolidados já mantêm contabilidade, fiscal, folha, eSocial e obrigações por um custo diluído entre muitos clientes. Recriar esses motores atrasaria a abertura do escritório e aumentaria o risco regulatório.

## Decisão

O produto será a central operacional do escritório virtual. Ele organizará clientes, equipe, onboarding, solicitações, documentos, prazos, aprovações, atendimento, auditoria, IA e integrações.

Motores contratados continuarão responsáveis por cálculo e transmissão oficial. Bling e outros ERPs serão fontes operacionais dos clientes. Conectores serão implementados por interfaces versionadas, sem acoplar o domínio ao fornecedor.

## Consequências

- a `v0.1.0` não terá plano de contas, lançamentos ou períodos contábeis;
- a primeira integração-alvo será o Bling, mas a autorização OAuth não entra no primeiro incremento;
- nenhum token será armazenado até existir cofre de segredos e política de rotação;
- cadastro e onboarding tornam-se o primeiro fluxo vertical;
- a troca de fornecedor contábil não poderá exigir reescrita do portal.

