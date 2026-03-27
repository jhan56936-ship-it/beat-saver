import http.server
import ssl

# Simple HTTPS server using cert.pem and key.pem in the current directory
server_address = ('0.0.0.0', 8443)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Create SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# Wrap the server socket
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Serving HTTPS on {server_address[0]} port {server_address[1]} (https://localhost:8443/) ...")
httpd.serve_forever()
