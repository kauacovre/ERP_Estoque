Objetivo Final (atender os requisitos abaixo):

1 — Visão rápida (requisitos mínimos)
Funcionalidades essenciais:
Cadastro de produtos (SKU, nome, custo, preço)
Armazenagem por local/filial (warehouses / bins)
Saldo por produto x warehouse (quantity, reserved)
Movimentações imutáveis (entrada/saída/transferência/ajuste)
Reserva de estoque para pedidos
Inventário / contagens
Autenticação (JWT) e roles
Logs de auditoria

2 — Arquitetura sugerida
API: FastAPI (ou Django + DRF)
DB: PostgreSQL (transações e row locking)
ORM: SQLModel (ou SQLAlchemy) / ou Django ORM
Autenticação: JWT (fastapi-jwt-auth / simplejwt)
Frontend: React ou Vue (consome API)
Deploy: Docker + docker-compose; produção em DigitalOcean, Render ou Heroku-like + managed Postgres
