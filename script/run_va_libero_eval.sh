#!/usr/bin/bash

set -x

# Start the server in the background
echo "Starting LingBot-VA server for Libero evaluation..."
save_root='visualization/libero_eval'
mkdir -p $save_root

python -m torch.distributed.run \
    --nproc_per_node 1 \
    --master_port 29061 \
    wan_va/wan_va_server.py \
    --config-name libero \
    --port 29056 \
    --save_root $save_root &
SERVER_PID=$!

# Wait for the server to be ready (you may need to adjust this sleep time)
echo "Waiting for server to initialize..."
sleep 60

# Start the client
echo "Starting Libero evaluation client..."
START=0
END=10

python evaluation/libero/client.py \
    --libero-benchmark libero_10 \
    --port 29056 \
    --test-num 50 \
    --task-range $START $END \
    --out-dir outputs/libero

# Kill the server after evaluation
kill $SERVER_PID
echo "Evaluation completed."
