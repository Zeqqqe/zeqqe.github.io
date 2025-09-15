export async function onRequest({ request }) {
  const userAgent = request.headers.get("user-agent") || "";
  const url = new URL(request.url);

  // Check if the user-agent is 'curl' and the path is the root
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

    // Return the text content directly
    return new Response(textContent, {
      headers: {
        "Content-Type": "text/plain",
      },
    });
  }

  // Otherwise, let the normal static site serving handle the request
  return new Response(null, { status: 404 });
}
