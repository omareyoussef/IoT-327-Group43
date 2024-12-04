# IoT End-to-End System - CECS 327 - Group43

## Overview
This project implements an IoT system that integrates sensor data, a MongoDB database, and a client-server architecture. It supports three specific queries related to IoT devices and processes results in PST and imperial units.

## Features
- **Q1**: Average moisture inside the fridge in the past three hours.
- **Q2**: Average water consumption per dishwasher cycle.
- **Q3**: Device with the highest electricity consumption.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/omareyoussef/IoT-327-Group43.git
   cd IoT-End-To-End-System
   ```

2. Install dependencies:
	```bash
	pip install pymongo certifi
	```

3. Configure MongoDB with your Atlas credentials and populate the database with IoT data.

4. Start the TCP server:
	```bash
	python server_code.py
	```

5. Start the TCP client:
	```bash
	python client_code.py
	```

## After Running the Server and Client

1. On the client, you’ll see a list of available queries:

- Q1: Average fridge moisture.
- Q2: Average dishwasher water consumption.
- Q3: Device with highest electricity consumption.

2. Enter one of the queries (e.g., Q1) to send it to the server.

3. The server will process the query, interact with the database, and return the result to the client.

4. The result will be displayed on the client screen.