Objetivo final (atender os requisitos abaixo):

1 — Visão geral / requisitos mínimos
Funcionalidades essenciais de um ERP de estoque:
Cadastro de produtos (SKU, nome, descrição, unidade, custo, preço)
Armazenagem por locais/filiais (warehouses / bins)
Controle de movimentações (entrada, saída, transferência)
Lote / validade (opcional)
Fornecedores e compras
Pedidos de venda (reservar estoque)
Inventário / contagem cíclica
Relatórios (saldo atual, movimentações, histórico por período)
Segurança: autenticação (JWT), autorização (roles), audit log (quem fez o quê)
API REST (ou GraphQL) consumida por web ou mobile

2 — Tech stack sugerido (prático)
Backend: Node.js + Express
DB primária: MongoDB (bom para iterações rápidas; transações possíveis com replica set)
Autenticação: JWT + refresh tokens
Frontend: React (ou Vue) — padrão SPA; Tailwind para UI rápida
Dev/infra: Docker, GitHub Actions (CI), MongoDB Atlas (prod), Nginx como reverse proxy
Deploy inicial: VPS/Hostinger ou serviço gerenciado (Render, Vercel para front, Heroku-like para backend)
Observabilidade: logs (winston), métricas básicas, backups de DB

3 — Modelo de dados (entidades principais)
(Resumo; campos importantes)
Produto
sku (string, único)
name (string)
description (string)
unit (string) — ex: unidade, kg, caixa
cost (number)
price (number)
trackLots (bool)
createdAt, updatedAt
Warehouse (local)
name
address
code
createdAt
Stock (saldo por produto x warehouse)
productId
warehouseId
quantity (number)
reserved (number) — para pedidos não entregues
lastUpdated
StockMovement (registro imutável)
productId
warehouseId
type (IN, OUT, TRANSFER, ADJUSTMENT, RESERVE, RELEASE)
quantity (number)
relatedDocument (pedidoId, notaFiscal, compraId)
userId
reason
createdAt
Supplier
name, contact, leadTime, etc.
Order (venda)
items: [{productId, qty, unitPrice}]
status: CREATED / RESERVED / SHIPPED / CANCELLED
warehouseId
createdBy
User
name, email, passwordHash, role (admin, manager, clerk)
Audit Log (alternativa: usar StockMovement + logs)
action, collection, documentId, userId, before, after, timestamp

4 — Endpoints essenciais (REST)
Usuário autenticado com JWT.
Products
GET /api/products
POST /api/products
GET /api/products/:id
PUT /api/products/:id
DELETE /api/products/:id
Warehouses
GET /api/warehouses
POST /api/warehouses
Stock / Movements
GET /api/stock?productId=&warehouseId= — retorna saldo
POST /api/stock/move — cria StockMovement e atualiza saldo (atomically)
POST /api/stock/transfer — transfer between warehouses (two movements in a tx)
GET /api/stock/movements?productId=&dateFrom=&dateTo=
Orders
POST /api/orders — cria pedido e reserva estoque
POST /api/orders/:id/ship — consome estoque
POST /api/orders/:id/cancel — libera reservas
Reports
GET /api/reports/stock-valuation
GET /api/reports/movements
Auth
POST /api/auth/login
POST /api/auth/refresh
GET /api/auth/me
