import { createContext, useContext, useState, useCallback } from "react";

const ToastContext = createContext(null);

export function ToastProvider({ children }) {
  const [msg, setMsg] = useState("");
  const [visible, setVisible] = useState(false);
  let timer = null;

  const show = useCallback((message, duration = 3000) => {
    setMsg(message);
    setVisible(true);
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => setVisible(false), duration);
  }, []);

  return (
    <ToastContext.Provider value={show}>
      {children}
      <div className={`toast ${visible ? "show" : ""}`}>{msg}</div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within ToastProvider");
  return ctx;
}
