import { NextResponse, type NextRequest } from "next/server";

function isAllowedNext(next: string | null | undefined): next is string {
  return Boolean(next) && (next!.startsWith("/app") || next!.startsWith("/authorize"));
}

export function middleware(request: NextRequest) {
  const host = (request.headers.get("host") ?? "").split(":")[0] ?? "";
  const { pathname } = request.nextUrl;

  if (host.startsWith("docs.")) {
    if (
      pathname.startsWith("/docs") ||
      pathname.startsWith("/_next") ||
      pathname.startsWith("/api") ||
      /\.[a-z0-9]+$/i.test(pathname)
    ) {
      return NextResponse.next();
    }
    const url = request.nextUrl.clone();
    url.pathname = pathname === "/" ? "/docs" : `/docs${pathname}`;
    return NextResponse.rewrite(url);
  }

  const appHost = process.env.APP_HOST;
  const docsHost = process.env.DOCS_HOST;
  if (appHost && docsHost && host === appHost && (pathname === "/docs" || pathname.startsWith("/docs/"))) {
    const url = request.nextUrl.clone();
    url.host = docsHost;
    url.pathname = pathname.replace(/^\/docs/, "") || "/";
    return NextResponse.redirect(url);
  }

  const hasSession = request.cookies.has("access_token");
  const isProtected = pathname.startsWith("/app") || pathname === "/authorize";

  if (isProtected && !hasSession) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("next", pathname + request.nextUrl.search);
    return NextResponse.redirect(loginUrl);
  }

  if ((pathname === "/login" || pathname === "/signup") && hasSession) {
    const next = request.nextUrl.searchParams.get("next");
    const target = isAllowedNext(next) ? next : "/app";
    return NextResponse.redirect(new URL(target, request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
