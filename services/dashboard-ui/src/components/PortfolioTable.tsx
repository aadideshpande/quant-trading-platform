import React from 'react';

interface Holding {
  symbol: string;
  quantity: number;
  price: number;
  value: number;
}

interface Props {
  data: Holding[];
}

const PortfolioTable: React.FC<Props> = ({ data }) => (
  <table className="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Symbol</th>
        <th>Quantity</th>
        <th>Price</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      {data.map((item, idx) => (
        <tr key={idx}>
          <td>{item.symbol}</td>
          <td>{item.quantity}</td>
          <td>${item.price.toFixed(2)}</td>
          <td>${item.value.toFixed(2)}</td>
        </tr>
      ))}
    </tbody>
  </table>
);

export default PortfolioTable;
