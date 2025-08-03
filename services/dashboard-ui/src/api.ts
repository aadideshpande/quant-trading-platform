import axios from 'axios';

const ORDER_SERVICE = 'http://localhost:8000';
const PORTFOLIO_SERVICE = 'http://localhost:8002';

export const fetchTrades = () =>
  axios.get(`${ORDER_SERVICE}/trades`).then(res => res.data);

export const fetchPortfolio = () =>
  axios.get(`${PORTFOLIO_SERVICE}/portfolio`).then(res => res.data);
