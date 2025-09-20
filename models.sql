CREATE TABLE items (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  sku TEXT UNIQUE,
  quantity INTEGER DEFAULT 0,
  reorder_level INTEGER DEFAULT 10,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE inventory_movements (
  id SERIAL PRIMARY KEY,
  item_id INTEGER REFERENCES items(id),
  change INTEGER,
  note TEXT,
  created_at TIMESTAMP DEFAULT now()
);
