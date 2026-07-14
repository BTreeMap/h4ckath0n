import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeEach, vi } from "vitest";
import { MemoryRouter, Route, Routes } from "react-router";
import { Layout } from "./Layout";

vi.mock("../auth", () => ({
  useAuth: () => ({
    isAuthenticated: false,
    logout: vi.fn(),
  }),
}));

function mockMatchMedia(matches: boolean) {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation(() => ({
      matches,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      addListener: vi.fn(),
      removeListener: vi.fn(),
    })),
  });
}

function renderLayout() {
  return render(
    <MemoryRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<div>home</div>} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

function getThemeButtons(name: string) {
  return screen.getAllByRole("button", { name });
}

beforeEach(() => {
  localStorage.clear();
  document.documentElement.removeAttribute("data-theme");
});

describe("Layout theme preference", () => {
  it("defaults to system preference and applies dark from system settings", async () => {
    mockMatchMedia(true);
    renderLayout();

    await waitFor(() => {
      expect(localStorage.getItem("theme-preference")).toBe("system");
      expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
      expect(getThemeButtons("Theme: system (dark)")).toHaveLength(2);
    });
  });

  it("toggle from system exits system and flips effective theme", async () => {
    mockMatchMedia(true);
    renderLayout();

    const button = getThemeButtons("Theme: system (dark)")[0]!;
    fireEvent.click(button);

    await waitFor(() => {
      expect(localStorage.getItem("theme-preference")).toBe("light");
      expect(document.documentElement.getAttribute("data-theme")).toBe("light");
      expect(getThemeButtons("Theme: light")).toHaveLength(2);
    });
  });

  it("toggle switches only between explicit light and dark", async () => {
    mockMatchMedia(false);
    localStorage.setItem("theme-preference", "light");
    renderLayout();

    const button = getThemeButtons("Theme: light")[0]!;

    fireEvent.click(button);
    await waitFor(() => {
      expect(localStorage.getItem("theme-preference")).toBe("dark");
      expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
      expect(getThemeButtons("Theme: dark")).toHaveLength(2);
    });

    fireEvent.click(button);
    await waitFor(() => {
      expect(localStorage.getItem("theme-preference")).toBe("light");
      expect(document.documentElement.getAttribute("data-theme")).toBe("light");
      expect(screen.queryAllByRole("button", { name: /Theme: system/ })).toHaveLength(0);
    });
  });

  it("labels the mobile menu control and exposes its state", async () => {
    mockMatchMedia(false);
    renderLayout();

    const menuButton = screen.getByRole("button", { name: "Open menu" });
    expect(menuButton).toHaveAttribute("aria-expanded", "false");
    expect(menuButton).toHaveAttribute("aria-controls", "mobile-navigation");

    fireEvent.click(menuButton);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Close menu" })).toHaveAttribute(
        "aria-expanded",
        "true",
      );
      expect(screen.getByRole("region", { name: "Mobile navigation" })).toBeInTheDocument();
    });
  });
});
