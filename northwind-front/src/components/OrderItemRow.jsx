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
    (async () => {
      const res = useDrive ? await getAllProductsDrive() : await getAllProducts();
      setProducts(res.data);
    })();
  }, [useDrive]);

  return (
    <tr>
      <td>
        <select
          value={item.productid || ''}
          onChange={e => onChange(index, { ...item, productid: Number(e.target.value) })}
          required
        >
          <option value="" disabled>
            Produto
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
          type="number"
          min="1"
          value={item.quantity || ''}
          onChange={e => onChange(index, { ...item, quantity: Number(e.target.value) })}
          required
        />
      </td>
      <td>
        <input
          type="number"
          step="0.01"
          min="0"
          max="1"
          value={item.discount || 0}
          onChange={e => onChange(index, { ...item, discount: Number(e.target.value) })}
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
