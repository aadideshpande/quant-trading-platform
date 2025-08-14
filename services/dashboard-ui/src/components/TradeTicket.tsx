import React, { useMemo, useState } from 'react';

/**
 * TradeTicket (Bootstrap-friendly)
 * POST http://localhost:8000/order
 * Body: { symbol, side, quantity }
 */
export default function TradeTicket() {
  const BASE_URL = 'http://localhost:8000';

  const [symbol, setSymbol] = useState('');
  const [quantity, setQuantity] = useState<number | ''>('');
  const [side, setSide] = useState<'BUY' | 'SELL'>('BUY');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const isValid = useMemo(() => {
    const symOk = /^(?:[A-Za-z]{1,10}|[A-Za-z]{1,5}:[A-Za-z]{1,10})$/.test(symbol.trim());
    const qtyOk = typeof quantity === 'number' && Number.isFinite(quantity) && quantity > 0;
    return symOk && qtyOk;
  }, [symbol, quantity]);

  async function placeOrder(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setSuccess(null);

    try {
      const payload = {
        symbol: symbol.trim().toUpperCase(),
        side,
        quantity: Number(quantity),
      };

      const res = await fetch(`${BASE_URL}/order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP ${res.status}: ${text || res.statusText}`);
      }

      setSuccess(`Order placed successfully: ${side} ${quantity} ${symbol}`);
      // Optional: clear fields after success
      // setSymbol('');
      // setQuantity('');
    } catch (err: any) {
      setError(err?.message || 'Failed to place order');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="card mb-4">
      <div className="card-body">
        <h2 className="h4 mb-3">New Order</h2>
        <form onSubmit={placeOrder} className="row g-2 align-items-end">
          <div className="col-12 col-md-5">
            <label className="form-label mb-1">Symbol</label>
            <input
              className="form-control"
              placeholder="AAPL"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            />
          </div>

          <div className="col-6 col-md-3">
            <label className="form-label mb-1">Quantity</label>
            <input
              type="number"
              min={1}
              step={1}
              className="form-control"
              placeholder="100"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value === '' ? '' : Number(e.target.value))}
            />
          </div>

          <div className="col-6 col-md-2">
            <label className="form-label mb-1">Side</label>
            <select
              className="form-select"
              value={side}
              onChange={(e) => setSide(e.target.value as 'BUY' | 'SELL')}
            >
              <option value="BUY">BUY</option>
              <option value="SELL">SELL</option>
            </select>
          </div>

          <div className="col-12 col-md-2 d-grid">
            <button
              type="submit"
              disabled={!isValid || submitting}
              className="btn btn-primary"
            >
              {submitting ? 'Placing…' : `Place ${side} Order`}
            </button>
          </div>

          {!isValid && (
            <div className="col-12">
              <small className="text-warning">Enter a valid symbol and positive quantity.</small>
            </div>
          )}

          {error && (
            <div className="col-12">
              <small className="text-danger">{error}</small>
            </div>
          )}

          {success && (
            <div className="col-12">
              <small className="text-success">{success}</small>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
