import { Outlet, Link } from "react-router";
import { useAuth } from "../auth";
import { Sun, Moon, Shield, LogOut, LayoutDashboard, Settings, Radio } from "lucide-react";
import { useState, useEffect } from "react";

const THEME_STORAGE_KEY = "theme-preference";
const THEME_ORDER = ["system", "light", "dark"] as const;
type ThemePreference = (typeof THEME_ORDER)[number];

function getThemePreference(): ThemePreference {
  const stored = localStorage.getItem(THEME_STORAGE_KEY);
  return THEME_ORDER.includes(stored as ThemePreference)
    ? (stored as ThemePreference)
    : "system";
}

function getEffectiveTheme(theme: ThemePreference): "light" | "dark" {
  return theme === "system"
    ? (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light")
    : theme;
}

export function Layout() {
  const { isAuthenticated, logout } = useAuth();
  const [theme, setTheme] = useState<ThemePreference>(() =>
    typeof window === "undefined" ? "system" : getThemePreference()
  );
  const [effectiveTheme, setEffectiveTheme] = useState<"light" | "dark">(() =>
    typeof window === "undefined" ? "light" : getEffectiveTheme(getThemePreference())
  );

  useEffect(() => {
    const applyTheme = (nextTheme: ThemePreference) => {
      const nextEffectiveTheme = getEffectiveTheme(nextTheme);
      document.documentElement.setAttribute("data-theme", nextEffectiveTheme);
      setEffectiveTheme(nextEffectiveTheme);
    };

    localStorage.setItem(THEME_STORAGE_KEY, theme);
    applyTheme(theme);

    if (theme !== "system") return;

    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = () => applyTheme("system");

    mediaQuery.addEventListener?.("change", onChange);
    mediaQuery.addListener?.(onChange);
    return () => {
      mediaQuery.removeEventListener?.("change", onChange);
      mediaQuery.removeListener?.(onChange);
    };
  }, [theme]);

  return (
    <div className="min-h-screen bg-surface">
      <nav className="border-b border-border bg-surface/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center gap-2 font-bold text-lg text-text">
              <Shield className="w-5 h-5 text-primary" />
              <span>{"{{PROJECT_NAME}}"}</span>
            </Link>

            <div className="flex items-center gap-3">
              <button
                onClick={() => {
                  const current = THEME_ORDER.indexOf(theme);
                  setTheme(THEME_ORDER[(current + 1) % THEME_ORDER.length]!);
                }}
                className="p-2 rounded-xl hover:bg-surface-alt transition-colors"
                aria-label={`Theme: ${theme}`}
              >
                {effectiveTheme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              </button>

              {isAuthenticated ? (
                <>
                  <Link
                    to="/dashboard"
                    className="flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-xl hover:bg-surface-alt transition-colors"
                    data-testid="nav-dashboard"
                  >
                    <LayoutDashboard className="w-4 h-4" />
                    Dashboard
                  </Link>
                  <Link
                    to="/settings"
                    className="flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-xl hover:bg-surface-alt transition-colors"
                    data-testid="nav-settings"
                  >
                    <Settings className="w-4 h-4" />
                    Settings
                  </Link>
                  <Link
                    to="/demo/realtime"
                    className="flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-xl hover:bg-surface-alt transition-colors"
                    data-testid="nav-realtime"
                  >
                    <Radio className="w-4 h-4" />
                    Realtime
                  </Link>
                  <button
                    onClick={() => void logout()}
                    className="flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-xl hover:bg-surface-alt transition-colors text-danger"
                    data-testid="nav-logout"
                  >
                    <LogOut className="w-4 h-4" />
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="px-3 py-1.5 text-sm rounded-xl hover:bg-surface-alt transition-colors"
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="px-4 py-1.5 text-sm bg-primary text-white rounded-xl hover:bg-primary-hover transition-colors"
                  >
                    Register
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  );
}
