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

  const handleFetch = () => {
    setLoading(true);
    setError('');
    setData([]);

    const fetchFn = useDrive
      ? getEmployeeRankingDrive(startDate, endDate)
      : getEmployeeRanking(startDate, endDate);

    fetchFn
      .then(res => {
        const payload = res.data;

        // Se o backend retornou { message: "..." } em 404 ou lógica customizada
        if (payload.message) {
          setError(payload.message);
          return;
        }

        // Se veio array vazio sem message
        if (Array.isArray(payload) && payload.length === 0) {
          setError('Nenhum funcionário encontrado para o intervalo de tempo fornecido.');
          return;
        }

        // Caso normal: lista de dados
        setData(payload);
      })
      .catch(err => {
        // Extrai a mensagem de erro enviada pelo backend, se existir
        const errMsg =
          err.response?.data?.error ||
          err.response?.data?.message ||
          err.message ||
          'Falha ao buscar ranking';
        setError(errMsg);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <section className="ranking-page">
      <h2>Ranking de Funcionários</h2>

      <div className="radio-group">
        <label>
          <input type="radio" checked={!useDrive} onChange={() => setUseDrive(false)} />
          Seguro&nbsp;(ORM)
        </label>
        <label>
          <input type="radio" checked={useDrive}  onChange={() => setUseDrive(true)}  />
          Inseguro&nbsp;(Drive)
        </label>
      </div>

      <div className="date-range">
        <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
        <span>até</span>
        <input type="date" value={endDate}   onChange={e => setEndDate(e.target.value)} />
        <button onClick={handleFetch}>Buscar</button>
      </div>

      {loading && <Loading text="Buscando…" />}
      {error   && <p className="error">{error}</p>}

      {(!loading && !error && data.length > 0) && (
        <div className="employee-ranking">
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
                  <td>{r.firstname} {r.lastname}</td>
                  <td>{r.soma_qtd_produtos}</td>
                  <td>{r.pedidos_qtd}</td>
                  <td>{Number(r.valor_total).toLocaleString('pt-BR', {
                        style:'currency', currency:'BRL'})}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}