import { Navigate, Route, Routes } from "react-router-dom";
import { AuthCallback } from "./pages/AuthCallback.js";
import { Home } from "./pages/Home.js";
import { Project } from "./pages/Project.js";
import { SignIn } from "./pages/SignIn.js";
import { useAuthor } from "./useAuthor.js";

export default function App() {
  const { state, refresh, signOut } = useAuthor();

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Ramrattan AI Editorial Studio</h1>
        {state.status === "signed_in" && (
          <div>
            <span className="status-line" style={{ marginRight: "0.75rem" }}>
              {state.author.email}
            </span>
            <button className="button-secondary" onClick={() => void signOut()}>
              Sign out
            </button>
          </div>
        )}
      </header>

      <main className="app-main">
        {state.status === "loading" ? (
          <p className="status-line">Loading…</p>
        ) : (
          <Routes>
            <Route
              path="/auth/callback"
              element={<AuthCallback onSignedIn={refresh} />}
            />
            {state.status === "signed_out" ? (
              <>
                <Route path="/sign-in" element={<SignIn />} />
                <Route path="*" element={<Navigate to="/sign-in" replace />} />
              </>
            ) : (
              <>
                <Route path="/" element={<Home />} />
                <Route path="/projects/:id" element={<Project />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </>
            )}
          </Routes>
        )}
      </main>
    </div>
  );
}
