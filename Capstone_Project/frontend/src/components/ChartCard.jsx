import "./ChartCard.css";

/**
 * Renders a single backend-generated chart image. `chartKey` is the raw
 * key from the backend's charts map (e.g. "bar_chart") and is title-cased
 * for display; the backend is free to add/remove keys without any
 * frontend change, per the "don't hard-code chart filenames" requirement.
 */
export default function ChartCard({ chartKey, imageUrl, description }) {
  const title = chartKey
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <div className="chart-card glass-card">
      <h3 className="chart-card-title">{title}</h3>
      {description && <p className="chart-card-desc">{description}</p>}
      <div className="chart-card-image-wrap">
        <img src={imageUrl} alt={`${title} chart`} loading="lazy" />
      </div>
    </div>
  );
}
