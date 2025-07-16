echo "Running tests..."
docker-compose -f docker-compose-test.yaml up --build --abort-on-container-exit
echo "Cleaning up containers..."
docker-compose -f docker-compose-test.yaml down
