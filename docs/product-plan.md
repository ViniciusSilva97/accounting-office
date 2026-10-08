# Plano do produto — Central do Escritório Virtual

## Proposta

Uma plataforma própria para organizar toda a relação entre escritório, equipe, clientes e sistemas externos. O produto não substitui inicialmente Domínio, Questor, Fortes, SCI ou equivalentes; ele coordena o trabalho e cria uma experiência única para o cliente.

## Fronteiras

| Nossa plataforma | Sistemas externos |
| --- | --- |
| Onboarding, documentos e solicitações | Contabilidade oficial |
| Equipe, responsáveis e prazos | Apuração fiscal |
| Aprovações e comunicação | Folha e eSocial |
| Auditoria e indicadores | Obrigações acessórias |
| IA assistiva | Emissão fiscal e ERP |
| Integrações e sincronização | Transmissões governamentais |

## Roadmap

### v0.1.0 — Fundação operacional

- escritório e usuários;
- empresas clientes e atribuições;
- checklist automático de implantação;
- auditoria imutável;
- catálogo de conectores;
- painel web mínimo;
- Docker, testes e documentação.

### v0.2.0 — Portal e solicitações

- usuário do cliente;
- solicitações de admissão, férias, desligamento e documentos;
- comentários, anexos, aprovação e prazos;
- notificações;
- painel de pendências.

### v0.3.0 — Bling

- OAuth 2.0;
- sincronização incremental;
- webhooks idempotentes;
- clientes, notas, vendas, contas e documentos disponíveis na API;
- reconciliação e monitor de falhas.

### v0.4.0 — Sistema contábil

- conector do fornecedor escolhido;
- envio de dados operacionais;
- retorno de guias, relatórios e situação das rotinas;
- rastreabilidade entre origem e entrega.

### v0.5.0 — Inteligência operacional

- assistente supervisionado;
- identificação de documentos faltantes;
- explicação de relatórios;
- triagem de solicitações;
- métricas de produtividade e qualidade.

## Portões para produção

- MFA para equipe;
- HTTPS e gestão de segredos;
- backup e restauração testados;
- monitoramento e alertas;
- política LGPD e retenção;
- revisão de autorização por escritório e empresa;
- testes de integração em sandbox/homologação;
- contratos e escopo dos fornecedores validados.

