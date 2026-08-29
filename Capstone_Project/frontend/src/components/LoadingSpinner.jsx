export default function LoadingSpinner({ label = "Loading..." }) {
  return (
    <div className="state-banner center">
      <div className="spinner" role="status" aria-label={label} />
      <p>{label}</p>
    </div>
  );
}
