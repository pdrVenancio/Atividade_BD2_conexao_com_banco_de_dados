import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
});

// Clientes
export const getAllCustomers = () => api.get('/orm-customers-get-all');
export const getAllCustomersDrive = () => api.get('/drive-customers-get-all');

// Funcionários
export const getAllEmployees = () => api.get('/orm-employee-get-all');
export const getAllEmployeesDrive = () => api.get('/drive-employee-get-all');

// Produtos
export const getAllProducts = () => api.get('/orm-product-get-all');
export const getAllProductsDrive = () => api.get('/drive-product-get-all');

// Shippers
export const getAllShippers = () => api.get('/orm-shipp-get-all');
export const getAllShippersDrive = () => api.get('/drive-shipp-get-all');

// Pedidos (Orders)
export const createOrder = payload => api.post('/orm-orders/insert', payload);
export const createOrderDrive = payload => api.post('/drive-orders/insert', payload);
export const getOrderById = id => api.get(`/orm-orders-get/${id}`);
export const getOrderByIdDrive = id => api.get(`/drive-orders-get/${id}`);

// Detalhes do Pedido (OrderDetails)
export const createOrderDetails = payload => api.post('/orm-order_details/insert', payload);
export const createOrderDetailsDrive = payload => api.post('/drive-order_details/insert', payload);
export const getOrderDetails = id => api.get(`/orm-orders_details/${id}`);
export const getOrderDetailsDrive = id => api.get(`/drive-orders_details/${id}`);

// Relatório de ranking
export const getEmployeeRanking = (startDate, endDate) =>
  api.get('/orm-employee-ranking', { params: { start_date: startDate, end_date: endDate } });
export const getEmployeeRankingDrive = (startDate, endDate) =>
  api.get('/drive-employee-ranking', { params: { start_date: startDate, end_date: endDate } });

export default api;