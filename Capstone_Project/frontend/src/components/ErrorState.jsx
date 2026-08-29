/**
 * Shared error / empty state block. Used for "no dataset selected",
 * backend failures, and "no charts available" — every page must show
 * this instead of a blank screen when something isn't ready.
 */
export default function ErrorState({ title, message, action }) {
  return (
    <div className="state-banner error glass-card">
      <h3>{title}</h3>
      {message && <p>{message}</p>}
      {action}
    </div>
  );
}
