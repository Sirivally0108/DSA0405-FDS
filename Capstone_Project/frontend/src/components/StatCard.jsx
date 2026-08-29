import "./StatCard.css";

/**
 * Small stat tile used across Analysis (rows, columns, missing values,
 * duplicates, outliers). The hexagon icon badge is the app's recurring
 * signature motif, echoed from the dashboard background art.
 */
export default function StatCard({ icon, label, value, tone = "leaf" }) {
  return (
    <div className={`stat-card stat-card-${tone}`}>
      <div className="hex-badge" aria-hidden="true">
        {icon}
      </div>
      <div className="stat-card-body">
        <span className="stat-card-value">{value}</span>
        <span className="stat-card-label">{label}</span>
      </div>
    </div>
  );
}
