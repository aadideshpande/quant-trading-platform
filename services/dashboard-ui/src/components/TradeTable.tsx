import React from 'react';

interface Trade {
  id: number;
  symbol: string;
  quantity: number;
  side: string;
  timestamp: string;
}

interface Props {
  data: Trade[];
}

const TradeTable: React.FC<Props> = ({ data }) => (
  <table className="table table-hover">
    <thead>
      <tr>
        <th>ID</th>
        <th>Symbol</th>
        <th>Quantity</th>
        <th>Side</th>
        <th>Timestamp</th>
      </tr>
    </thead>
    <tbody>
      {data.map((t, idx) => (
        <tr key={idx}>
          <td>{t.id}</td>
          <td>{t.symbol}</td>
          <td>{t.quantity}</td>
          <td>{t.side}</td>
          <td>{new Date(t.timestamp).toLocaleString()}</td>
        </tr>
      ))}
    </tbody>
  </table>
);

export default TradeTable;
