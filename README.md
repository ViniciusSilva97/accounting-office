# Accounting Office

Fundação da central operacional do escritório contábil virtual.

## Entrega atual

A `v0.1.0` inicia o primeiro fluxo vertical:

1. autenticação da equipe;
2. cadastro de uma empresa cliente;
3. atribuição de responsável;
4. geração automática do checklist de implantação;
5. registro da ação na auditoria;
6. visualização em painel responsivo.

O catálogo de integrações já prevê Bling e sistemas contábeis brasileiros, mas não armazena credenciais nesta versão.

## Executar sem Docker

```bash
uv sync --dev
uv run python manage.py migrate
uv run python manage.py bootstrap_office \
  --legal-name "Escritório Exemplo Ltda" \
  --trade-name "Escritório Exemplo" \
  --tax-id "00.000.000/0001-00" \
  --office-email "contato@example.com" \
  --admin-email "admin@example.com" \
  --admin-name "Administrador"
uv run python manage.py runserver
```

O comando solicita a senha sem exibi-la no terminal. Para automação controlada, aceite-a pela variável `DJANGO_BOOTSTRAP_PASSWORD`.

## Executar com Docker

```bash
cp .env.example .env
docker compose up --build
```

## Qualidade

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest --cov=apps
uv run python manage.py check
```

## Segurança

Esta fundação usa dados fictícios. Ela ainda não está autorizada para dados reais. Consulte `docs/product-plan.md` para os portões de produção.

