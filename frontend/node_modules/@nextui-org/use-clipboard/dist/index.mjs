// src/index.ts
import { useState } from "react";
function useClipboard({ timeout = 2e3 } = {}) {
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const [copyTimeout, setCopyTimeout] = useState(null);
  const onClearTimeout = () => {
    if (copyTimeout) {
      clearTimeout(copyTimeout);
    }
  };
  const handleCopyResult = (value) => {
    onClearTimeout();
    setCopyTimeout(setTimeout(() => setCopied(false), timeout));
    setCopied(value);
  };
  const copy = (valueToCopy) => {
    if ("clipboard" in navigator) {
      navigator.clipboard.writeText(valueToCopy).then(() => handleCopyResult(true)).catch((err) => setError(err));
    } else {
      setError(new Error("useClipboard: navigator.clipboard is not supported"));
    }
  };
  const reset = () => {
    setCopied(false);
    setError(null);
    onClearTimeout();
  };
  return { copy, reset, error, copied };
}
export {
  useClipboard
};
