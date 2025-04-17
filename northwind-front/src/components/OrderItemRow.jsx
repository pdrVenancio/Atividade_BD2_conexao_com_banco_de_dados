// src/components/OrderItemRow.jsx

import { useEffect, useState } from 'react';
import { getAllProducts, getAllProductsDrive } from '../services/api';

export default function OrderItemRow({
  index,
  useDrive,
  item,
  onChange,
  onRemove,
}) {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = useDrive ? getAllProductsDrive : getAllProducts;
    fetchProducts().then(res => setProducts(res.data));
  }, [useDrive]);

  return (
    <tr>
      <td>
        <select
          value={item.productid}
          onChange={e =>
            onChange(index, {
              ...item,
              productid: Number(e.target.value),
            })
          }
          required
        >
          <option value="" disabled>
            Selecione o produto
          </option>
          {products.map(p => (
            <option key={p.productid} value={p.productid}>
              {p.productname}
            </option>
          ))}
        </select>
      </td>

      <td>
        <input
          type="text"
          value={item.quantity}
          placeholder="Qtd."
          onChange={e =>
            onChange(index, { ...item, quantity: e.target.value })
          }
          required
        />
      </td>

      <td>
        <input
          type="text"
          value={item.discount}
          placeholder="Ex: 0.1"
          onChange={e =>
            onChange(index, { ...item, discount: e.target.value })
          }
        />
      </td>

      <td>
        <button type="button" onClick={() => onRemove(index)}>
          Remover
        </button>
      </td>
    </tr>
  );
}
