import { useState } from 'react';
import { getEmployeeRanking, getEmployeeRankingDrive } from '../services/api';
import Loading from '../components/Loading';

export default function EmployeeRankingPage() {
  const [useDrive, setUseDrive] = useState(false);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFetch = async () => {
    try {
      setLoading(true);
      setError('');
      const res = useDrive
        ? await getEmployeeRankingDrive(startDate, endDate)
        : await getEmployeeRanking(startDate, endDate);
      setData(res.data);
    } catch (err) {
      console.error(err);
      setError('Falha ao buscar ranking');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="ranking-page">
      <h2>Ranking de Funcionários</h2>
      <div className="backend-toggle">
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

      <div className="date-range">
        <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
        <span>até</span>
        <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} />
        <button onClick={handleFetch}>Buscar</button>
      </div>

      {loading && <Loading text="Buscando..." />}
      {error && <p className="error">{error}</p>}
      {!!data.length && (
        <table className="ranking-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Funcionário</th>
              <th>Qtd. Produtos</th>
              <th>Qtd. Pedidos</th>
              <th>Valor Total</th>
            </tr>
          </thead>
          <tbody>
            {data.map(r => (
              <tr key={r.position}>
                <td>{r.position}</td>
                <td>
                  {r.firstname} {r.lastname}
                </td>
                <td>{r.soma_qtd_produtos}</td>
                <td>{r.pedidos_qtd}</td>
                <td>{r.valor_total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}