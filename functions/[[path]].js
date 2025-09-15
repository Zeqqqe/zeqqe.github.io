export async function onRequest({ request, next }) {
  const userAgent = request.headers.get("user-agent");

  if (userAgent && userAgent.includes("curl")) {
    const url = new URL(request.url);
    if (url.pathname === "/") {
      return new Response(null, {
        status: 302,
        headers: { Location: "/index.txt" },
      });
    }
  }

  // If the User-Agent is not 'curl' or the path is not the root,
  // continue to the next middleware or serve the static file.
  return await next();
}
