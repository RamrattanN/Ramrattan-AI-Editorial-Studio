import { useCallback, useEffect, useState } from "react";
import { type Author, api } from "./api.js";

export type AuthorState =
  | { status: "loading" }
  | { status: "signed_out" }
  | { status: "signed_in"; author: Author };

/**
 * Loads the authenticated Author from the server-side session. There is no
 * client-side fallback identity - if the session cookie is absent or
 * invalid, the Author is signed out, matching the "application state is
 * authoritative" requirement (Web Walking Skeleton 01, item 11).
 */
export function useAuthor() {
  const [state, setState] = useState<AuthorState>({ status: "loading" });

  const refresh = useCallback(async () => {
    try {
      const author = await api.me();
      setState({ status: "signed_in", author });
    } catch {
      setState({ status: "signed_out" });
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const signOut = useCallback(async () => {
    await api.logout();
    setState({ status: "signed_out" });
  }, []);

  return { state, refresh, signOut };
}
