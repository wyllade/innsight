export default function Spinner({ text = "Loading..." }) {
  return (
    <div className="spinner">
      <div className="spin"></div>
      {text}
    </div>
  );
}
