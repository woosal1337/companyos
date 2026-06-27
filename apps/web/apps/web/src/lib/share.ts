export function shareMeetingPath(token: string): string {
  return `/share/meetings/${token}`;
}

export function shareMeetingUrl(origin: string, token: string): string {
  return `${origin.replace(/\/$/, "")}${shareMeetingPath(token)}`;
}

export function shareApiPath(token: string, suffix = ""): string {
  return `/api/v1/share/meetings/${token}${suffix}`;
}
