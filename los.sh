set -u
mkdir -p /poolio/docker/mekotools-werkzeuge/wick
cat > /poolio/docker/mekotools-werkzeuge/wick/docker-compose.yml
cd /poolio/docker/mekotools-werkzeuge/wick
docker compose up -d 2>&1 | tail -6
sleep 12
echo "=== Zustand ==="
docker ps --filter name=mekotools-wick --format '{{.Names}} {{.Status}} {{.Image}}'
echo "=== im Netz erreichbar? ==="
docker exec mekotools-wick wget -qO- http://127.0.0.1/healthz 2>&1 | head -2
