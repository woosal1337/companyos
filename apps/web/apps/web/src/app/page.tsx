import type { Metadata } from "next";
import { SiteNav } from "@/components/marketing/site-nav";
import { Hero } from "@/components/marketing/hero";
import { LogoCloud } from "@/components/marketing/logo-cloud";
import { DeepDive } from "@/components/marketing/deep-dive";
import { NowGrid } from "@/components/marketing/now-grid";
import { SceneStrip } from "@/components/marketing/scene-strip";
import { BoldBand } from "@/components/marketing/bold-band";
import { FinalCTA } from "@/components/marketing/final-cta";
import { SiteFooter } from "@/components/marketing/site-footer";

export const metadata: Metadata = {
  title: "CompanyOS · The coordination layer for your company",
  description:
    "Organizations, teams, projects, and Linear-style tasks in one system. Meetings with transcripts and AI summaries, notes, and a full activity log. Every AI feature runs on your own model key.",
  openGraph: {
    title: "CompanyOS · The coordination layer for your company",
    description:
      "Projects, meetings with AI summaries, notes, and an activity log in one system. Bring your own OpenAI or Anthropic key.",
    type: "website",
  },
};

export default function LandingPage() {
  return (
    <div className="flex min-h-dvh flex-col bg-canvas text-foreground">
      <SiteNav />
      <main className="flex-1">
        <Hero />
        <LogoCloud />
        <DeepDive />
        <NowGrid />
        <SceneStrip />
        <BoldBand />
        <FinalCTA />
      </main>
      <SiteFooter />
    </div>
  );
}
