CREATE TABLE stock_tickers (
  ticker TEXT PRIMARY KEY,
  name TEXT,
  industry TEXT
);

CREATE TABLE stock_prices (
  time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  ticker TEXT,
  open NUMERIC,
  high NUMERIC,
  low NUMERIC,
  close NUMERIC,
  close_adj NUMERIC,
  volume NUMERIC,
  FOREIGN KEY (ticker) REFERENCES stock_tickers (ticker)
);

SELECT create_hypertable('stock_prices', 'time');

create index on stock_prices (ticker, time desc);

