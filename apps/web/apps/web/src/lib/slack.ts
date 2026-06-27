export function buildSlackMessage(
  meetingTitle: string,
  actionItems: string[],
  shareUrl: string | null
): string {
  const lines = [`*${meetingTitle}* — meeting summary`];
  if (actionItems.length > 0) {
    lines.push("", "*Action items*");
    for (const item of actionItems.slice(0, 8)) {
      lines.push(`• ${item}`);
    }
  }
  if (shareUrl) {
    lines.push("", `Ask the AI about this meeting: ${shareUrl}`);
  }
  return lines.join("\n");
}
