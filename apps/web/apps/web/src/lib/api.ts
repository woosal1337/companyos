export class ApiError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

interface Envelope<T> {
  success: boolean;
  message: string;
  data: T;
}

interface RequestOptions {
  method?: "GET" | "POST" | "PATCH" | "PUT" | "DELETE";
  json?: unknown;
  signal?: AbortSignal;
}

let refreshInFlight: Promise<boolean> | null = null;

function refreshSession(): Promise<boolean> {
  if (!refreshInFlight) {
    refreshInFlight = fetch("/api/v1/auth/refresh", { method: "POST", credentials: "include" })
      .then((response) => response.ok)
      .catch(() => false)
      .finally(() => {
        refreshInFlight = null;
      });
  }
  return refreshInFlight;
}

function redirectToLogin(): void {
  if (typeof window === "undefined") return;
  if (!window.location.pathname.startsWith("/app")) return;
  window.location.assign(
    "/login?next=" + encodeURIComponent(window.location.pathname + window.location.search),
  );
}

async function request<T>(path: string, options: RequestOptions = {}, retried = false): Promise<T> {
  const { method = "GET", json, signal } = options;

  const response = await fetch(path, {
    method,
    credentials: "include",
    signal,
    headers: json !== undefined ? { "Content-Type": "application/json" } : undefined,
    body: json !== undefined ? JSON.stringify(json) : undefined,
  });

  if (response.status === 401 && typeof window !== "undefined") {
    const isAuthCall = path.includes("/auth/refresh") || path.includes("/auth/login");
    if (!retried && !isAuthCall && (await refreshSession())) {
      return request<T>(path, options, true);
    }
    if (!isAuthCall) redirectToLogin();
  }

  let envelope: Envelope<T> | undefined;
  try {
    envelope = (await response.json()) as Envelope<T>;
  } catch {
    envelope = undefined;
  }

  if (!response.ok || envelope === undefined || !envelope.success) {
    throw new ApiError(response.status, envelope?.message ?? `Request failed (${response.status})`);
  }

  return envelope.data;
}

export const api = {
  get: <T>(path: string, signal?: AbortSignal) => request<T>(path, { signal }),
  post: <T>(path: string, json?: unknown) => request<T>(path, { method: "POST", json }),
  put: <T>(path: string, json?: unknown) => request<T>(path, { method: "PUT", json }),
  patch: <T>(path: string, json?: unknown) => request<T>(path, { method: "PATCH", json }),
  delete: <T>(path: string, json?: unknown) => request<T>(path, { method: "DELETE", json }),
};

export function orgPath(orgId: string, suffix = ""): string {
  return `/api/v1/orgs/${orgId}${suffix}`;
}

export function errorMessage(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  if (error instanceof Error) return error.message;
  return "Something went wrong";
}
