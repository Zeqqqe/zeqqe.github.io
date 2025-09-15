export async function onRequest({ request, next }) {
  const userAgent = request.headers.get("user-agent") || "";
  const url = new URL(request.url);

  // Check if it's a curl request and it's for the root path
  if (userAgent.includes("curl") && url.pathname === "/") {
    // Return the content of index.txt directly
    return new Response(`Welcome to ${url.hostname}, it seems you have used curl on this site, a very strange action to not return HTML.

[Your ASCII art and text content here]
`, {
      headers: { "Content-Type": "text/plain" },
    });
  }

  // If not a curl request, let the default static site handling take over
  return await next();
}
