#!/usr/bin/env bash
set -euo pipefail

DATASET=scidocs
EMBEDDING_MODEL="cohere_v4"
BASE_FILE_NAME=base.bin
QUERY_FILE_NAME=query.bin

EMBEDDINGS_DIR=~/data/embeddings
DISKANN_DIR=~/DiskANN

BASE_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/${BASE_FILE_NAME}
QUERY_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/${QUERY_FILE_NAME}
GT_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/gt100.bin

# Array of byte values from the table
BYTE_VALUES=(32 48 64 80 96 112 128 144 160 176 192)

# Create output directory for this sweep
SWEEP_DIR="~/runs/pq_sweep_$(date +%s)/unif"
mkdir -p "$SWEEP_DIR"

echo "Starting PQ sweep in $SWEEP_DIR"
echo "=================================================="

for TARGET_TOTAL_PQ_BYTES in "${BYTE_VALUES[@]}"; do
    echo ""
    echo "Running with TARGET_TOTAL_PQ_BYTES=$TARGET_TOTAL_PQ_BYTES"
    echo "=================================================="
    
    # Create unique output prefix for this byte value
    RUN_SUFFIX="_bytes_${TARGET_TOTAL_PQ_BYTES}"
    UNIF_PQ_BASE_PREFIX="${BASE_FILE%.bin}_unif${RUN_SUFFIX}"
    INFLATED_PQ_SUFFIX="_pq_compressed.bin_inflated.bin"
    UNIF_PQ_BASE_FILE="${UNIF_PQ_BASE_PREFIX}${INFLATED_PQ_SUFFIX}"
    UNIF_PQ_GT_FILE="${UNIF_PQ_BASE_PREFIX}_pq_compressed.bin_gt100"
    
    # Create run-specific directory
    RUN_DIR="${SWEEP_DIR}/bytes_${TARGET_TOTAL_PQ_BYTES}"
    mkdir -p "$RUN_DIR"
    
    echo "Output prefix: $UNIF_PQ_BASE_PREFIX"
    echo "Run directory: $RUN_DIR"
    
    # Generating PQ data
    echo "Generating PQ data..."
    ${DISKANN_DIR}/build/apps/utils/generate_pq \
        float \
        "$BASE_FILE" \
        "$UNIF_PQ_BASE_PREFIX" \
        "$TARGET_TOTAL_PQ_BYTES" \
        0.1 0 | tee "$RUN_DIR/generate_pq.log"
    
    # Computing exact k-NN for PQ data
    echo "Computing exact k-NN for PQ data..."
    ${DISKANN_DIR}/build/apps/utils/compute_groundtruth \
        --data_type float \
        --dist_fn l2 \
        --base_file "$UNIF_PQ_BASE_FILE" \
        --query_file "$QUERY_FILE" \
        --gt_file "$UNIF_PQ_GT_FILE" \
        --K 100 | tee "$RUN_DIR/compute_groundtruth.log"
    
    # Calculating recall
    echo "Calculating recall..."
    RECALL_OUTPUT=$(${DISKANN_DIR}/build/apps/utils/calculate_recall \
        "$GT_FILE" \
        "$UNIF_PQ_GT_FILE" \
        100 | tee "$RUN_DIR/calculate_recall.log")
    
    echo "Bytes=$TARGET_TOTAL_PQ_BYTES - $RECALL_OUTPUT"
    
done

echo ""
echo "=================================================="
echo "PQ sweep completed!"
echo "Results directory: $SWEEP_DIR"
echo "=================================================="

# Summary of results
echo ""
echo "Summary of recall results:"
echo "Bytes,Recall"
for TARGET_TOTAL_PQ_BYTES in "${BYTE_VALUES[@]}"; do
    RUN_DIR="${SWEEP_DIR}/bytes_${TARGET_TOTAL_PQ_BYTES}"
    if [ -f "$RUN_DIR/calculate_recall.log" ]; then
        RECALL=$(tail -1 "$RUN_DIR/calculate_recall.log" | grep -oP '\d+\.\d+' || echo "N/A")
        echo "$TARGET_TOTAL_PQ_BYTES,$RECALL"
    fi
done
