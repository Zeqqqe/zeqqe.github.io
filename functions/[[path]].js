export async function onRequest({ request, next }) {
  const userAgent = request.headers.get("user-agent") || "";
  const url = new URL(request.url);

  if (userAgent.includes("curl") && url.pathname === "/") {
    const textContent = `Welcome to www.zeqqe.dev, it seems you have use curl on this site, a very strange action to not return HTML.


                                 #
####  ##   ## #  ## #  ##     ## #  ##  #   #
   # #  # #  ## #  ## #  #   #  ## #  # #   #
  #  #### #   # #   # ####   #   # ####  # #
 #   #    #   # #   # #      #   # #     # #
#    #  # #  ## #  ## #  #   #  ## #  #   #
####  ##   ## #  ## #  ##  #  ## #  ##    #
              #     #
              #     #



LINKS:
GitHub — https://github.com/Zeqqqe
Discord — @zeqqqe
Email — contact@zeqqe.dev 

—————————————————————————

INFO:
I am a Linux live environment user, and I have accumulated over 13 Gigabytes of Linux lice ISOs.`;

    return new Response(textContent, {
      headers: {
        "Content-Type": "text/plain",
      },
    });
  } else if (url.pathname === "/") {
    // Get the original response from Cloudflare Pages (your index.html)
    const response = await next();
    const originalBody = await response.text();

    // Create a new response with the body from the original response
    return new Response(originalBody, {
      headers: {
        "Content-Type": "text/html",
      },
    });
  }

  // For all other paths, let Cloudflare Pages handle them normally
  return next();
}
