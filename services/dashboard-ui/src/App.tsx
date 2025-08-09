import React, { useEffect, useState } from 'react';
import { fetchPortfolio, fetchTrades } from './api';
import PortfolioTable from './components/PortfolioTable';
import TradeTable from './components/TradeTable';

function App() {
  const [portfolio, setPortfolio] = useState([]);
  const [total, setTotal] = useState(0);
  const [trades, setTrades] = useState([]);

  const loadData = async () => {
    try {
      const portfolioData = await fetchPortfolio();
      setPortfolio(portfolioData.portfolio);
      setTotal(portfolioData.total_value);

      const tradesData = await fetchTrades();
      setTrades(tradesData);
    } catch (err) {
      console.error('Error loading data', err);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000); // auto-refresh every 5 sec
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container mt-4">
      <h1 className="mb-4">📊 Real-Time Portfolio Dashboard</h1>
      <h3>Total Value: ${total.toFixed(2)}</h3>
      <hr />
      <h4>Holdings</h4>
      <PortfolioTable data={portfolio} />
      <h4 className="mt-4">Recent Trades</h4>
      <TradeTable data={trades.slice(0, 10)} />
    </div>
  );
}

export default App;
