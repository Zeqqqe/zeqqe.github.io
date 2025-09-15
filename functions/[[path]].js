export async function onRequest({ request, next }) {
  const userAgent = request.headers.get("user-agent") || "";
  const url = new URL(request.url);

  // Check if it's a curl request and it's for the root path
  if (userAgent.includes("curl") && url.pathname === "/") {
    // Return the content of index.txt directly
    return new Response("Welcome to www.zeqqe.dev, it seems you have use curl on this site, a very strange action to not return HTML.


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
I am a Linux live environment user, and I have accumulated over 13 Gigabytes of Linux lice ISOs.
"
`, {
      headers: { "Content-Type": "text/plain" },
    });
  }

  // If not a curl request, let the default static site handling take over
  return await next();
}
