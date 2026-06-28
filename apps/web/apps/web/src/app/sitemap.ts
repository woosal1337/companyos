import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/seo";
import { POSTS } from "@/app/blog/_content/posts";

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();

  const staticEntries = ["/", "/about", "/contact", "/blog", "/changelog", "/privacy", "/terms"].map(
    (path) => ({
      url: `${SITE_URL}${path === "/" ? "" : path}`,
      lastModified: now,
    }),
  );

  const postEntries = POSTS.map((post) => ({
    url: `${SITE_URL}/blog/${post.slug}`,
    lastModified: new Date(`${post.date}T00:00:00Z`),
  }));

  return [...staticEntries, ...postEntries];
}
