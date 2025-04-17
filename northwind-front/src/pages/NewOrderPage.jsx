import { useEffect, useState } from 'react';
import {
  getAllCustomers,
  getAllCustomersDrive,
  getAllEmployees,
  getAllEmployeesDrive,
  getAllShippers,
  getAllShippersDrive,
  createOrder,
  createOrderDrive,
  createOrderDetails,
  createOrderDetailsDrive,
} from '../services/api';
import OrderItemRow from '../components/OrderItemRow';
import Loading from '../components/Loading';

export default function NewOrderPage() {
  const [useDrive, setUseDrive] = useState(false);
  const [loading, setLoading] = useState(true);
  const [customers, setCustomers] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [shippers, setShippers] = useState([]);

  const [order, setOrder] = useState({
    customerid: '',
    employeeid: '',
    orderdate: new Date().toISOString().substring(0, 10),
    requireddate: '',
    shippeddate: '',
    freight: 0,
    shipname: '',
    shipaddress: '',
    shipcity: '',
    shipregion: '',
    shippostalcode: '',
    shipcountry: '',
    shipperid: '',
  });

  const [items, setItems] = useState([]);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  // Carregar dados iniciais
  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const cust = await (useDrive ? getAllCustomersDrive() : getAllCustomers());
        const emp  = await (useDrive ? getAllEmployeesDrive() : getAllEmployees());
        const ship = await (useDrive ? getAllShippersDrive() : getAllShippers());
        setCustomers(cust.data);
        setEmployees(emp.data);
        setShippers(ship.data);
      } catch (err) {
        console.error(err);
        setErrorMsg('Falha ao carregar dados iniciais');
      } finally {
        setLoading(false);
      }
    })();
  }, [useDrive]);

  const handleItemChange = (idx, newItem) => {
    const clone = [...items];
    clone[idx] = newItem;
    setItems(clone);
  };

  const handleAddItem = () => {
    setItems([...items, { productid: '', unitprice: 1, quantity: 1, discount: 0 }]);
  };

  const handleRemoveItem = idx => {
    const clone = [...items];
    clone.splice(idx, 1);
    setItems(clone);
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');

    try {
      // 1) Cria o pedido
      const createOrderFn = useDrive ? createOrderDrive : createOrder;
      const res = await createOrderFn(order);

      // O backend devolve {product: orderid} ou similar.
      const newOrderId = res.data.product?.orderid || res.data.product || res.data.orderid;
      if (!newOrderId) throw new Error('ID do pedido não retornado pelo backend');

      // 2) Cria cada item (loop de detalhes)
      const createItemFn = useDrive ? createOrderDetailsDrive : createOrderDetails;
      await Promise.all(
        items.map(it =>
          createItemFn({
            ...it,
            orderid: newOrderId,
          }),
        ),
      );

      setSuccessMsg(`Pedido #${newOrderId} criado com sucesso!`);
      // resetar formulário
      setOrder(o => ({
        ...o,
        shipname: "Alfreds Futterkiste",
        shipaddress: "Obere Str. 57",
        shipcity: "Berlin",
        shipregion: "Lara",
        shippostalcode: "3508",
        shipcountry: "Germany",
        freight: 1.1
      }));
      setItems([]);
    } catch (err) {
    console.error(err);
    // tenta extrair exatamente o que o back mandou
    const msg =
      err.response?.data?.message ||
      err.response?.data?.error ||
      err.message ||
      'Erro desconhecido';
    setErrorMsg(msg);
  }
};

  if (loading) return <Loading />;

  return (
    <section className="order-page">
      <h2>Novo Pedido</h2>

      {/* seletor ORM / Drive */}
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
          Inseguro (Drive / SQL Injection)
        </label>
      </div>

      <form onSubmit={handleSubmit} className="order-form">
        <fieldset>
          <legend>Dados Gerais</legend>
          <label>
            Cliente:
            <select
              value={order.customerid}
              onChange={e => setOrder({ ...order, customerid: e.target.value })}
              required
            >
              <option value="" disabled>
                Selecione
              </option>
              {customers.map(c => (
                <option key={c.customerid} value={c.customerid}>
                  {c.companyname}
                </option>
              ))}
            </select>
          </label>

          <label>
            Vendedor:
            <select
              value={order.employeeid}
              onChange={e => setOrder({ ...order, employeeid: Number(e.target.value) })}
              required
            >
              <option value="" disabled>
                Selecione
              </option>
              {employees.map(e => (
                <option key={e.employeeid} value={e.employeeid}>
                  {e.firstname} {e.lastname}
                </option>
              ))}
            </select>
          </label>

          <label>
            Transportadora:
            <select
              value={order.shipperid}
              onChange={e => setOrder({ ...order, shipperid: Number(e.target.value) })}
            >
              <option value="">Sem transportadora</option>
              {shippers.map(s => (
                <option key={s.shipperid} value={s.shipperid}>
                  {s.companyname}
                </option>
              ))}
            </select>
          </label>

          <label>
            Data do Pedido:
            <input
              type="date"
              value={order.orderdate}
              onChange={e => setOrder({ ...order, orderdate: e.target.value })}
              required
            />
          </label>

          <label>
            Data Requerida:
            <input
              type="date"
              value={order.requireddate}
              onChange={e => setOrder({ ...order, requireddate: e.target.value })}
            />
          </label>

          <label>
            Data Envio:
            <input
              type="date"
              value={order.shippeddate}
              onChange={e => setOrder({ ...order, shippeddate: e.target.value })}
            />
          </label>
        </fieldset>

        <fieldset>
          <legend>Endereço de Entrega</legend>
          <label>
            Nome:
            <input
              type="text"
              value={order.shipname}
              onChange={e => setOrder({ ...order, shipname: e.target.value })}
              required
            />
          </label>
          <label>
            Endereço:
            <input
              type="text"
              value={order.shipaddress}
              onChange={e => setOrder({ ...order, shipaddress: e.target.value })}
              required
            />
          </label>
          <label>
            Cidade:
            <input
              type="text"
              value={order.shipcity}
              onChange={e => setOrder({ ...order, shipcity: e.target.value })}
            />
          </label>
          <label>
            Região:
            <input
              type="text"
              value={order.shipregion}
              onChange={e => setOrder({ ...order, shipregion: e.target.value })}
            />
          </label>
          <label>
            CEP:
            <input
              type="text"
              value={order.shippostalcode}
              onChange={e => setOrder({ ...order, shippostalcode: e.target.value })}
            />
          </label>
          <label>
            País:
            <input
              type="text"
              value={order.shipcountry}
              onChange={e => setOrder({ ...order, shipcountry: e.target.value })}
            />
          </label>
        </fieldset>

        <fieldset>
          <legend>Itens do Pedido</legend>
          <table className="items-table">
            <thead>
              <tr>
                <th>Produto</th>
                <th>Qtd.</th>
                <th>Desconto (%)</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {items.map((it, idx) => (
                <OrderItemRow
                  key={idx}
                  index={idx}
                  useDrive={useDrive}
                  item={it}
                  onChange={handleItemChange}
                  onRemove={handleRemoveItem}
                />
              ))}
            </tbody>
          </table>
        </fieldset>
        <button type="button" className="add-item-btn" onClick={handleAddItem}>
          Adicionar Item
        </button>

        <button type="submit" className="submit-btn">
          Salvar Pedido
        </button>
      </form>

      {successMsg && <p className="success">{successMsg}</p>}
      {errorMsg && <p className="error">{errorMsg}</p>}
    </section>
  );
}
