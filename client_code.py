import socket

valid_queries = {
    "Q1": "What is the average moisture inside my kitchen fridge in the past three hours?",
    "Q2": "What is the average water consumption per cycle in my smart dishwasher?",
    "Q3": "Which device consumed more electricity among my three IoT devices?"
}

def start_client():
    host = input("Enter the server IP address: ")
    port = int(input("Enter the port number of the server: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print("Connected to the server.")

            while True:
                print("\nAvailable queries:")
                for key, query in valid_queries.items():
                    print(f"{key}: {query}")

                query = input("\nEnter your query (Q1, Q2, Q3) or type 'exit' to quit: ")
                if query.lower() == "exit":
                    print("Closing connection to the server.")
                    break

                if query not in valid_queries:
                    print("Invalid query. Please try again.")
                    continue

                # Send the query to the server
                s.sendall(query.encode())

                # Receive the server's response
                response = s.recv(1024).decode()
                print(f"Server response: {response}")

        except Exception as e:
            print(f"Failed to connect or communicate with the server: {e}")

if __name__ == '__main__':
    start_client()
