import { useEffect, useRef, useState } from "react";

// Debounces a value. For object/array values we compare by JSON to avoid
// the timer constantly resetting because of new reference identities.
export function useDebounce(value, delay = 300) {
  const [debounced, setDebounced] = useState(value);
  const lastSerialized = useRef(JSON.stringify(value));

  useEffect(() => {
    const serialized = JSON.stringify(value);
    if (serialized === lastSerialized.current) {
      return; // no semantic change
    }
    const t = setTimeout(() => {
      lastSerialized.current = serialized;
      setDebounced(value);
    }, delay);
    return () => clearTimeout(t);
  }, [value, delay]);

  return debounced;
}
