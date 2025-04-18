import { useState } from 'react';
import {
  getOrderById,
  getOrderByIdDrive,
  getOrderDetails,
  getOrderDetailsDrive,
} from '../services/api';
import Loading from '../components/Loading';

export default function OrderReportPage() {
  const [useDrive, setUseDrive] = useState(false);
  const [orderId, setOrderId] = useState('');
  const [orderData, setOrderData] = useState(null);
  const [details, setDetails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleSearch = async () => {
    if (!orderId) return;

    setLoading(true);
    setErrorMsg('');
    setOrderData(null);
    setDetails([]);

    try {
      const getOrderFn = useDrive ? getOrderByIdDrive : getOrderById;
      const getDetailsFn = useDrive ? getOrderDetailsDrive : getOrderDetails;

      const [orderRes, detailsRes] = await Promise.all([
        getOrderFn(orderId),
        getDetailsFn(orderId),
      ]);

      setOrderData(orderRes.data);
      setDetails(detailsRes.data);
    } catch (err) {
      console.error(err);
      const msg =
        err.response?.data?.message ||
        err.response?.data?.error ||
        err.message ||
        'Erro ao buscar pedido';
      setErrorMsg(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="order-report-page">
      <h2>Relatório de Pedido</h2>

      <div className="radio-group">
        <label>
          <input
            type="radio"
            name="backend"
            checked={!useDrive}
            onChange={() => setUseDrive(false)}
          />
          Seguro (ORM)
        </label>
        <label>
          <input
            type="radio"
            name="backend"
            checked={useDrive}
            onChange={() => setUseDrive(true)}
          />
          Inseguro (Drive)
        </label>
      </div>

      <div className="search-area">
        <input
          type="number"
          value={orderId}
          placeholder="ID do Pedido"
          onChange={e => setOrderId(e.target.value)}
        />
        <button onClick={handleSearch}>Buscar</button>
      </div>

      {loading && <Loading text="Buscando dados do pedido…" />}
      {errorMsg && <p className="error">{errorMsg}</p>}

      {!loading && orderData && (
        <div className="report-results">
          <h3>Dados do Pedido</h3>
          <ul>
            <li><strong>ID:</strong> {orderData.orderid}</li>
            <li><strong>Data:</strong> {orderData.orderdate}</li>
            <li><strong>Cliente:</strong> {orderData.companyname}</li>
            <li><strong>Vendedor:</strong> {orderData.firstname} {orderData.lastname}</li>
          </ul>

          <h3>Itens do Pedido</h3>
          <table className="order-items-table">
            <thead>
              <tr>
                <th>Nome do produto</th>
                <th>Preço Unitário</th>
                <th>Quantidade</th>
                <th>Subtotal</th>
              </tr>
            </thead>
            <tbody>
              {details.map((item, idx) => {
                console.log(item)
                const subtotal =
                  item.unitprice * item.quantity;
                return (
                  <tr key={idx}>
                    <td>{item.productname}</td>
                    <td>R$ {item.unitprice}</td>
                    <td>{item.quantity}</td>
                    <td>R$ {subtotal}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
