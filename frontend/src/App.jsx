
import { useEffect, useState } from "react";
import {
  Leaf, MapPin, Search, RefreshCw, Plus,
  TrendingUp, ShoppingBasket
} from "lucide-react";

const API =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export default function App() {
  const [prices, setPrices] = useState([]);
  const [listings, setListings] = useState([]);
  const [markets, setMarkets] = useState([]);
  const [crop, setCrop] = useState("All crops");
  const [market, setMarket] = useState("All markets");
  const [search, setSearch] = useState("");
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [message, setMessage] = useState("");

  const [form, setForm] = useState({
    crop: "Potato",
    quantity_quintals: 5,
    location: "Jalpaiguri",
    quality: "Grade A",
    seller: "Demo Farmer",
  });

  async function loadData() {
    try {
      setError("");

      const [p, l, m] = await Promise.all([
        fetch(`${API}/api/crops`),
        fetch(`${API}/api/listings`),
        fetch(`${API}/api/markets`),
      ]);

      if (!p.ok || !l.ok || !m.ok) {
        throw new Error("Backend returned an error.");
      }

      const cropData = await p.json();
      const listingData = await l.json();

      setPrices(cropData.items);
      setListings(listingData.items);
      setMarkets(await m.json());
    } catch {
      setError(
        "Cannot connect to the backend. Start FastAPI on port 8000."
      );
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  const crops = [
    "All crops",
    ...new Set(prices.map((item) => item.crop)),
  ];

  const filtered = prices.filter((item) => {
    const matchesCrop =
      crop === "All crops" || item.crop === crop;
    const matchesMarket =
      market === "All markets" || item.market === market;
    const matchesSearch =
      `${item.crop} ${item.market}`
        .toLowerCase()
        .includes(search.toLowerCase());

    return matchesCrop && matchesMarket && matchesSearch;
  });

  async function addListing(event) {
    event.preventDefault();
    setMessage("");

    try {
      const response = await fetch(`${API}/api/listings`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...form,
          quantity_quintals: Number(form.quantity_quintals),
        }),
      });

      if (!response.ok) {
        throw new Error("Could not create crop lot.");
      }

      setMessage("Demo crop lot added successfully.");
      setShowForm(false);
      await loadData();
    } catch {
      setMessage("Unable to add the crop lot. Check the backend.");
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <Leaf size={27} />
          <div>
            <h2>Kisaan Setu</h2>
            <small>FARMER MARKET INTELLIGENCE</small>
          </div>
        </div>
        <span className="location">
          <MapPin size={16} /> West Bengal, India
        </span>
      </header>

      <main className="content">
        <div className="intro">
          <div>
            <p className="eyebrow">SIH26132 · MARKET LINKAGES</p>
            <h1>Good morning, Farmer</h1>
            <p>
              Compare crop prices and explore market opportunities.
            </p>
          </div>
          <button className="button" onClick={loadData}>
            <RefreshCw size={16} /> Refresh
          </button>
        </div>

        <div className="notice">
          Prototype: all displayed prices are synthetic examples,
          not live or verified mandi rates.
        </div>

        {error && <div className="message error">{error}</div>}
        {message && <div className="message">{message}</div>}

        <section className="stats">
          <article className="stat">
            <TrendingUp />
            <span>Price records</span>
            <strong>{prices.length}</strong>
          </article>
          <article className="stat">
            <Leaf />
            <span>Crops covered</span>
            <strong>{new Set(prices.map(p => p.crop)).size}</strong>
          </article>
          <article className="stat">
            <ShoppingBasket />
            <span>Available lots</span>
            <strong>{listings.length}</strong>
          </article>
        </section>

        <section className="panel">
          <div className="panel-heading">
            <div>
              <h2>Market price discovery</h2>
              <p>Compare sample prices by crop and market.</p>
            </div>
          </div>

          <div className="filters">
            <div className="search">
              <Search size={17} />
              <input
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Search crop or market"
              />
            </div>

            <select value={crop} onChange={e => setCrop(e.target.value)}>
              {crops.map(item => (
                <option key={item}>{item}</option>
              ))}
            </select>

            <select value={market} onChange={e => setMarket(e.target.value)}>
              <option>All markets</option>
              {markets.map(item => (
                <option key={item}>{item}</option>
              ))}
            </select>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Crop</th>
                  <th>Market</th>
                  <th>Sample price</th>
                  <th>Demand</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map(item => (
                  <tr key={item.id}>
                    <td>{item.crop}</td>
                    <td>{item.market}</td>
                    <td>₹{item.price.toLocaleString("en-IN")} / quintal</td>
                    <td>
                      <span className={`demand ${item.demand.toLowerCase()}`}>
                        {item.demand}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {!filtered.length && (
              <p className="empty">No matching prices found.</p>
            )}
          </div>
        </section>

        <section className="panel">
          <div className="panel-heading">
            <div>
              <h2>Available crop lots</h2>
              <p>Example lots listed by farmers and FPOs.</p>
            </div>
            <button
              className="button primary"
              onClick={() => setShowForm(!showForm)}
            >
              <Plus size={16} /> Add a lot
            </button>
          </div>

          {showForm && (
            <form className="form" onSubmit={addListing}>
              <label>
                Crop
                <select
                  value={form.crop}
                  onChange={e => setForm({...form, crop:e.target.value})}
                >
                  {["Potato", "Tomato", "Onion", "Cabbage",
                    "Brinjal", "Cauliflower"].map(item => (
                    <option key={item}>{item}</option>
                  ))}
                </select>
              </label>

              <label>
                Quantity (quintals)
                <input
                  type="number"
                  min="0.1"
                  step="0.1"
                  required
                  value={form.quantity_quintals}
                  onChange={e => setForm({
                    ...form,
                    quantity_quintals: e.target.value
                  })}
                />
              </label>

              <label>
                Location
                <input
                  required
                  value={form.location}
                  onChange={e => setForm({...form, location:e.target.value})}
                />
              </label>

              <label>
                Quality
                <select
                  value={form.quality}
                  onChange={e => setForm({...form, quality:e.target.value})}
                >
                  <option>Grade A</option>
                  <option>Grade B</option>
                  <option>Not graded</option>
                </select>
              </label>

              <label>
                Seller / FPO
                <input
                  required
                  value={form.seller}
                  onChange={e => setForm({...form, seller:e.target.value})}
                />
              </label>

              <button className="button primary" type="submit">
                Save demo lot
              </button>
            </form>
          )}

          <div className="lots">
            {listings.map(item => (
              <article className="lot" key={item.id}>
                <span className="lot-icon"><ShoppingBasket /></span>
                <h3>{item.crop}</h3>
                <p>{item.seller}</p>
                <p><MapPin size={14} /> {item.location}</p>
                <p>{item.quality}</p>
                <strong>{item.quantity_quintals} quintals</strong>
                <span className="available">Available · Demo</span>
              </article>
            ))}
            {!listings.length && <p className="empty">No crop lots yet.</p>}
          </div>
        </section>

        <footer>
          Kisaan Setu · SIH26132 prototype · Demo data only
        </footer>
      </main>
    </div>
  );
}
