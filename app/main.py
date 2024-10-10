import socket

def handle_request(request):
    # Split request lines
    request_lines = request.splitlines()
    
    # The first line is the request line (method, path, version)
    request_line = request_lines[0]
    print(f"Request Line: {request_line}")  # For debugging
    
    # Split the request line into parts
    method, path, _ = request_line.split()

    # Determine response based on path
    if path == "/":
        return b"HTTP/1.1 200 OK\r\n\r\n"
    else:
        return b"HTTP/1.1 404 Not Found\r\n\r\n"

def main():
    print("Starting server...")
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 4221))
    server_socket.listen(1)
    print("Server is listening on port 4221...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        
        # Receive the request (you can set a buffer size, here it's 1024 bytes)
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Request received:\n{request}")
        
        # Handle the request and get the response
        response = handle_request(request)
        
        # Send the response
        client_socket.sendall(response)
        client_socket.close()

if __name__ == "__main__":
    main()
