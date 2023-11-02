# Web Proxy Server

This project involves the development of a simple web proxy server that focuses on caching and handling HTTP GET requests. The proxy server acts as an intermediary between web clients (e.g., web browsers) and web servers, improving performance by caching web pages.

## Features

- **Accepts HTTP Requests**: The proxy server accepts incoming HTTP requests from web clients like web browsers.

- **Caching**: It checks if the requested web page is available in the local cache. If found, it serves the page from the cache. Otherwise, it fetches the object from the origin server on behalf of the client.

- **Local Cache**: The proxy creates a local copy of the object to serve future requests. The local file structure mimics the URL directory structure.

- **Error Handling**: For requests other than GET, the proxy responds with "400 Bad Request." Similarly, if the origin server responds with a status other than "200 OK," the proxy returns a "400 Bad Request" response to the client.

- **Non-Persistent HTTP**: The proxy server supports non-persistent HTTP (HTTP 1.0). It closes the TCP connection after serving an HTTP request and includes the "Connection: close" header in the response.

- **Support for Text and Binary Files**: The proxy handles both text (e.g., HTML files) and binary (e.g., images, PDF) files.

## Running the Proxy Server

1. Start the proxy server program.
2. Configure your web browser to use the proxy server. You can usually set this in your browser's settings, specifying the proxy's IP address and port number.

Alternatively, you can directly provide the proxy's IP address and port number in your browser's address bar.

## Assumptions

- The proxy assumes it will receive well-formatted GET requests. Other types of requests result in a "400 Bad Request" response.

- The proxy cache always contains the latest version of the object, and objects are never updated at the origin server.

- All requests are for a single object on the internet, so the proxy does not handle complex web pages with embedded objects.

- Web clients and the web proxy run on the same machine.

Feel free to explore and use this web proxy server for your needs. It provides a basic caching mechanism to improve web page retrieval performance.
