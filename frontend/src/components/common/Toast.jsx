import { useState, useCallback, useRef } from "react";
import { ToastContext } from "./toastContext";

export function ToastProvider({ children }) {
  const [msg, setMsg] = useState("");
  const [visible, setVisible] = useState(false);
  const timerRef = useRef(null);

  const show = useCallback((message, duration = 3000) => {
    setMsg(message);
    setVisible(true);
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => setVisible(false), duration);
  }, []);

  return (
    <ToastContext.Provider value={show}>
      {children}
      <div className={`toast ${visible ? "show" : ""}`}>{msg}</div>
    </ToastContext.Provider>
  );
}
