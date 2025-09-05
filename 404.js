addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const response = await fetch(request)

  // Check if the response status is 404
  if (response.status === 404) {
    const custom404Page = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>404 - Not Found</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
            <style>
                body {
                    font-family: 'Inter', sans-serif;
                }
                .terminal-block {
                    font-family: 'JetBrains Mono', monospace;
                }
            </style>
        </head>
        <body class="bg-gray-900 text-gray-200 min-h-screen p-8">
            <main class="max-w-4xl mx-auto">
                <header class="mb-12">
                    <h1 class="text-4xl font-bold tracking-tight leading-none mb-4 text-emerald-300">zeqqe.dev</h1>
                </header>
                <section class="mb-10">
                    <h2 class="text-2xl font-bold mb-4">
                        <a href="/" class="text-emerald-400 underline">404 - NOT FOUND</a>
                    </h2>
                    <pre class="terminal-block whitespace-pre-wrap text-sm leading-relaxed bg-gray-800 border border-gray-700 p-4 rounded-lg shadow-lg">
> zeqqe.sh --find-page
    [INFO] Error: The requested resource could not be located.
    [INFO] Path not found.
                    </pre>
                </section>
                <section>
                    <h2 class="text-2xl font-bold mb-4">
                        <a href="/#contact" class="text-emerald-400 underline">RETURN</a>
                    </h2>
                    <div class="space-y-2">
                        <p>
                            <span class="text-emerald-400">EMAIL:</span> <a href="mailto:contact@zeqqe.dev" class="text-gray-200 underline">contact@zeqqe.dev</a>
                        </p>
                        <p>
                            <span class="text-emerald-400">HOMEPAGE:</span> <a href="/" class="text-gray-200 underline">zeqqe.dev</a>
                        </p>
                    </div>
                </section>
            </main>
        </body>
        </html>
    `;
    
    // Return the custom 404 page with a 404 status code
    return new Response(custom404Page, {
      status: 404,
      headers: { 'Content-Type': 'text/html' },
    });
  }

  // If the status is not 404, return the original response
  return response;
}
