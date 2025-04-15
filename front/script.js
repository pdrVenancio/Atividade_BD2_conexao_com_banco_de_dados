document.addEventListener('DOMContentLoaded', () => {
    // Elementos UI
    const ui = {
        addProductBtn: document.getElementById('addProductBtn'),
        productsContainer: document.getElementById('productsContainer'),
        orderForm: document.getElementById('orderForm'),
        resultContainers: {
            insert: document.getElementById('orderInsertResult'),
            order: document.getElementById('orderResult'),
            ranking: document.getElementById('rankingResult')
        }
    };

    // Clonar template de produto
    ui.addProductBtn.addEventListener('click', () => {
        const template = document.querySelector('.product-grid');
        const clone = template.cloneNode(true);
        clone.querySelectorAll('input').forEach(input => input.value = '');
        ui.productsContainer.appendChild(clone);
    });

    // Controllers
    const orderController = {
        getData: () => ({
            customer: document.getElementById('customerName').value.trim(),
            employee: document.getElementById('employeeName').value.trim(),
            order_date: document.getElementById('orderDate').value || new Date().toISOString().split('T')[0],
            products: Array.from(document.querySelectorAll('.product-grid'))
                .map(product => ({
                    product_name: product.querySelector('.productName').value.trim(),
                    quantity: product.querySelector('.productQty').value,
                    unit_price: product.querySelector('.productPrice').value
                }))
                .filter(p => p.product_name)
        }),

        submit: async (mode) => {
            const data = orderController.getData();
            
            if (!data.customer || !data.employee || !data.products.length) {
                alert('Preencha cliente, vendedor e pelo menos 1 produto!');
                return;
            }

            try {
                const res = await fetch('/api/orders', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({...data, safe: mode === 'safe'})
                });
                ui.resultContainers.insert.textContent = JSON.stringify(await res.json(), null, 2);
            } catch (error) {
                ui.resultContainers.insert.textContent = 'Erro ao enviar pedido';
            }
        }
    };

    // Handlers
    const handlers = {
        getOrder: async () => {
            const orderId = document.getElementById('orderIdInput').value;
            if (!orderId) return alert('Informe o ID do pedido');
            
            try {
                const res = await fetch(`/api/order/${orderId}`);
                const data = await res.json();
                ui.resultContainers.order.textContent = handlers.formatOrder(data);
            } catch {
                ui.resultContainers.order.textContent = 'Erro ao buscar pedido';
            }
        },

        getRanking: async () => {
            const start = document.getElementById('startDate').value;
            const end = document.getElementById('endDate').value;
            if (!start || !end) return alert('Selecione o período');
            
            try {
                const res = await fetch(`/api/employee-ranking?start_date=${start}&end_date=${end}`);
                const data = await res.json();
                ui.resultContainers.ranking.textContent = handlers.formatRanking(data.ranking || []);
            } catch {
                ui.resultContainers.ranking.textContent = 'Erro ao gerar ranking';
            }
        },

        formatOrder: (data) => {
            if (data.error) return data.error;
            const details = data.order_details || [];
            return `
Pedido #${data.order_id || 'N/A'}
Data: ${data.order_date || '---'}
Cliente: ${data.customer_name || '---'}
Vendedor: ${data.employee_name || '---'}
Itens:
${details.map(d => `• ${d.product_name} - ${d.quantity}x $${d.unit_price || 0}`).join('\n')}
Total: $${details.reduce((t, d) => t + (d.quantity * (d.unit_price || 0)), 0)}`;
        },

        formatRanking: (ranking) => {
            if (!ranking.length) return 'Sem resultados';
            return ranking.map((e, i) => 
                `${i+1}º ${e.firstname} ${e.lastname}
Pedidos: ${e.soma_qtd || 0}
Valor: $${e.valor_total || 0}`
            ).join('\n\n');
        }
    };

    // Eventos
    document.getElementById('submitOrderUnsafe').addEventListener('click', () => orderController.submit('unsafe'));
    document.getElementById('submitOrderSafe').addEventListener('click', () => orderController.submit('safe'));
    document.getElementById('getOrderBtn').addEventListener('click', handlers.getOrder);
    document.getElementById('getRankingBtn').addEventListener('click', handlers.getRanking);
});