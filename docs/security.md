# Segurança e dados reais

## Estado atual

Esta versão é uma fundação de desenvolvimento. Use somente dados fictícios.

## Controles já presentes

- usuário personalizado e hash Argon2;
- escopo obrigatório por escritório para usuários regulares;
- autorização por empresa;
- UUID nas URLs;
- proteção CSRF e sessões Django;
- auditoria das ações centrais;
- configuração de produção exige banco e segredo explícitos;
- cookies seguros, redirecionamento HTTPS e HSTS em produção;
- nenhum token de integração armazenado.

## Portões obrigatórios antes de dados reais

1. autenticação multifator;
2. cofre de segredos e rotação de credenciais;
3. backup criptografado e restauração testada;
4. observabilidade e alertas;
5. política LGPD, retenção e resposta a incidentes;
6. análise de ameaças e teste de isolamento;
7. homologação dos conectores;
8. contrato de tratamento de dados com fornecedores;
9. infraestrutura de produção revisada;
10. teste de recuperação e continuidade operacional.

## Integrações

Credenciais OAuth, certificados e tokens não poderão ser gravados em `non_secret_settings`. O campo aceita somente identificadores e preferências sem segredo. A implementação de cada conector deverá usar um armazenamento próprio protegido e registrar somente metadados na auditoria.

