import { Routes, Route, NavLink } from 'react-router-dom';
import NewOrderPage from './pages/NewOrderPage';
import EmployeeRankingPage from './pages/EmployeeRankingPage';
import './App.css';
import OrdersReportPage from './pages/OrdersReportPage';

export default function App() {
  return (
    <div className="app-container">
      <nav className="navbar">
        <h1>Northwind • Sistema de Pedidos</h1>
        <div className="links">
          <NavLink to="/" end>
            Novo Pedido
          </NavLink>
          <NavLink to="/ranking">Ranking Funcionários</NavLink>
          <NavLink to="/order">Listar Pedidos</NavLink>
        </div>
      </nav>
      <main className="main">
        <Routes>
          <Route path="/" element={<NewOrderPage />} />
          <Route path="/ranking" element={<EmployeeRankingPage />} />
          <Route path="/order" element={<OrdersReportPage />} />
        </Routes>
      </main>
    </div>
  );
}
