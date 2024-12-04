import socket
import threading
from database_utils import query_database

def handle_client(conn, addr):
    print(f"Connected by {addr}")

    try:
        while True:
            # Receive data from the client
            data = conn.recv(1024).decode()
            if not data:
                break

            print(f"Received query: {data}")

            # Process the query
            if data == "Q1":
                response = f"Average moisture (RH%): {query_database('Q1')}"
            elif data == "Q2":
                response = f"Average water consumption (gallons): {query_database('Q2')}"
            elif data == "Q3":
                response = f"Device with highest electricity consumption: {query_database('Q3')}"
            else:
                response = "Invalid query. Please use Q1, Q2, or Q3."

            # Send the response back to the client
            conn.sendall(response.encode())

    except Exception as e:
        print(f"Error while communicating with {addr}: {e}")

    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

def start_server():
    host = input("Enter the server IP address ('0.0.0.0' for all IPv4 addresses): ")
    port = int(input("Enter the port number of the server: "))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server is listening on port {port}...")

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

    except Exception as e:
        print(f"Server error: {e}")

    finally:
        server_socket.close()
        print("Server stopped.")

if __name__ == '__main__':
    start_server()