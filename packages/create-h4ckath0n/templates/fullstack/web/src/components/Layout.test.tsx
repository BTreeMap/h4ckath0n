import { render, screen, fireEvent } from "@testing-library/react";
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
  it("defaults to system preference and applies dark from system settings", () => {
    mockMatchMedia(true);
    renderLayout();

    expect(localStorage.getItem("theme-preference")).toBe("system");
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
    expect(screen.getByRole("button", { name: "Theme: system" })).toBeInTheDocument();
  });

  it("cycles through system, light, and dark preferences", () => {
    mockMatchMedia(false);
    renderLayout();

    const button = screen.getByRole("button", { name: "Theme: system" });
    fireEvent.click(button);
    expect(localStorage.getItem("theme-preference")).toBe("light");
    expect(document.documentElement.getAttribute("data-theme")).toBe("light");

    fireEvent.click(button);
    expect(localStorage.getItem("theme-preference")).toBe("dark");
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");

    fireEvent.click(button);
    expect(localStorage.getItem("theme-preference")).toBe("system");
    expect(document.documentElement.getAttribute("data-theme")).toBe("light");
  });
});
