!#/bin/bash
# Step 1: Get the container ID

CONTAINER_ID=$(docker ps -q --filter "name=docker-postgres-1")


# Step 2: Check if the container ID was found
if [ -z "$CONTAINER_ID" ]; then
  echo "Container not found!"
  exit 1
fi

# Step 3: Extract the IP address
IP_ADDRESS=$(docker inspect $CONTAINER_ID | grep -i "ipaddress" | awk -F'"' '{print $4}')

# Step 4: Use the IP address in another command
echo "The container's IP address is: $IP_ADDRESS"
