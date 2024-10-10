import socket
import threading
import os

# Define a function to handle each client connection
def handle_client(client_socket):
    try:
        # Receive the request from the client
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request:\n{request}")

        # Parse the request line and headers
        headers = request.split("\r\n")
        request_line = headers[0]
        method, path, _ = request_line.split()
        headers_dict = {}
        
        # Parse headers into a dictionary
        for header in headers[1:]:
            if ": " in header:
                key, value = header.split(": ", 1)
                headers_dict[key] = value

        # Example of reading the body for POST requests
        if method == "POST":
            content_length = int(headers_dict.get('Content-Length', 0))
            body = client_socket.recv(content_length).decode('utf-8')
            print(f"Request body: {body}")

        # Handle GET requests and respond with a file
        if method == "GET":
            if path == "/":
                path = "/index.html"  # Serve an index.html page by default

            # Check if the requested file exists
            file_path = "." + path
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    body = f.read()
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    "Content-Type: text/html\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )
                client_socket.sendall(response.encode('utf-8') + body)
            else:
                # File not found response
                response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Length: 13\r\n"
                    "Content-Type: text/plain\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "404 Not Found"
                )
                client_socket.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()


def main():
    # Set up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 4221))
    server_socket.listen(5)
    print("Server listening on port 4221...")

    # Accept connections concurrently using threads
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")
            # Handle each connection in a new thread
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
