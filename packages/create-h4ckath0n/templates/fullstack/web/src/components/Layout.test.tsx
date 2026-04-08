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
      expect(
        screen.getAllByRole("button", { name: "Theme: system (dark)" })[0],
      ).toBeInTheDocument();
    });
  });

  it("toggle from system exits system and flips effective theme", async () => {
    mockMatchMedia(true);
    renderLayout();

    const button = screen.getAllByRole("button", { name: "Theme: system (dark)" })[0]!;
    fireEvent.click(button);

    await waitFor(() => {
      expect(localStorage.getItem("theme-preference")).toBe("light");
      expect(document.documentElement.getAttribute("data-theme")).toBe("light");
      expect(
        screen.getAllByRole("button", { name: "Theme: light" })[0],
      ).toBeInTheDocument();
    });
  });

  it("toggle switches only between explicit light and dark", async () => {
    mockMatchMedia(false);
    localStorage.setItem("theme-preference", "light");
    renderLayout();

    const button = screen.getAllByRole("button", { name: "Theme: light" })[0]!;

    fireEvent.click(button);
    await waitFor(() => {
      expect(localStorage.getItem("theme-preference")).toBe("dark");
      expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
      expect(
        screen.getAllByRole("button", { name: "Theme: dark" })[0],
      ).toBeInTheDocument();
    });

    fireEvent.click(button);
    await waitFor(() => {
      expect(localStorage.getItem("theme-preference")).toBe("light");
      expect(document.documentElement.getAttribute("data-theme")).toBe("light");
      expect(
        screen.queryByRole("button", { name: /Theme: system/ }),
      ).not.toBeInTheDocument();
    });
  });
});
