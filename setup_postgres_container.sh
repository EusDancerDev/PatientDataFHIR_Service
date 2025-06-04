#! /usr/bin/env zsh

# Stop and remove existing container if it exists
docker stop km0-postgres || true
docker rm km0-postgres || true

# Run new PostgreSQL container
# Network binding explanation:
# -p 5432:5432 means:
#   - Left side (host): Binds to all interfaces (0.0.0.0) on port 5432
#   - Right side (container): Maps to container's internal port 5432
# This allows connections from:
#   - Local machine via localhost:5432
#   - Docker containers via host.docker.internal:5432
#   - Other machines on the network via <your-ip>:5432
# Note: Using 127.0.0.1:5432:5432 would limit connections to only localhost
docker run --name km0-postgres \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=admin \
  --restart unless-stopped \
  -d postgres:16.6

# Wait for PostgreSQL to start up
echo "Waiting for PostgreSQL to start..."
sleep 5

# Create KM0 database if it doesn't exist
docker exec -i km0-postgres psql -U postgres -c "CREATE DATABASE \"KM0\";" || true

echo "PostgreSQL container is ready!"
echo "To restore data, run:"
echo "cat km0_backup.sql | docker exec -i km0-postgres psql -U postgres -d KM0" 