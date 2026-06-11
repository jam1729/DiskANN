#!/usr/bin/env bash
set -euo pipefail

DATASET=quora_500k
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

ALLOCATION_STRATEGY=${ALLOCATION_STRATEGY:-stride}

# Create output directory for this sweep
SWEEP_DIR="~/runs/sq_sweep_$(date +%s)/unif"
mkdir -p "$SWEEP_DIR"

echo "Starting SQ sweep in $SWEEP_DIR"
echo "=================================================="

for TARGET_TOTAL_SQ_BYTES in "${BYTE_VALUES[@]}"; do
    echo ""
    echo "Running with TARGET_TOTAL_SQ_BYTES=$TARGET_TOTAL_SQ_BYTES"
    echo "=================================================="
    
    # Create unique output prefix for this byte value
    RUN_SUFFIX="_bytes_${TARGET_TOTAL_SQ_BYTES}"
    UNIF_SQ_BASE_PREFIX="${BASE_FILE%.bin}_unif_sq${RUN_SUFFIX}"
    INFLATED_SQ_SUFFIX="_sq_compressed.bin_inflated.bin"
    UNIF_SQ_BASE_FILE="${UNIF_SQ_BASE_PREFIX}${INFLATED_SQ_SUFFIX}"
    UNIF_SQ_GT_FILE="${UNIF_SQ_BASE_PREFIX}_sq_compressed.bin_gt100"
    
    # Create run-specific directory
    RUN_DIR="${SWEEP_DIR}/bytes_${TARGET_TOTAL_SQ_BYTES}"
    mkdir -p "$RUN_DIR"
    
    echo "Output prefix: $UNIF_SQ_BASE_PREFIX"
    echo "Run directory: $RUN_DIR"
    
    # Generate SQ calibration file
    echo "Generating SQ uniform-like calibration..."
    "${DISKANN_DIR}/.venv/bin/python3" "${DISKANN_DIR}/experiments/generate_sq_uniform_calibration.py" \
        --base_file "$BASE_FILE" \
        --output_cal_file "$RUN_DIR/sq_calibration.bin" \
        --target_bytes "$TARGET_TOTAL_SQ_BYTES" \
        --sampling_rate 0.1 \
        --seed 42 \
        --allocation_strategy "$ALLOCATION_STRATEGY" | tee "$RUN_DIR/generate_calibration.log"
        
    # Generating SQ data
    echo "Generating SQ data..."
    "${DISKANN_DIR}/build/apps/utils/generate_sq_variable" \
        "$BASE_FILE" \
        "${UNIF_SQ_BASE_PREFIX}_sq_compressed.bin" \
        "$RUN_DIR/sq_calibration.bin" | tee "$RUN_DIR/generate_sq.log"
        
    # Reconstructing float32 data
    echo "Reconstructing float32 data from SQ..."
    "${DISKANN_DIR}/build/apps/utils/int8_to_float_scale_variable" \
        "${UNIF_SQ_BASE_PREFIX}_sq_compressed.bin" \
        "$UNIF_SQ_BASE_FILE" \
        "$RUN_DIR/sq_calibration.bin" | tee "$RUN_DIR/int8_to_float.log"
    
    # Computing exact k-NN for SQ data
    echo "Computing exact k-NN for SQ data..."
    "${DISKANN_DIR}/build/apps/utils/compute_groundtruth" \
        --data_type float \
        --dist_fn l2 \
        --base_file "$UNIF_SQ_BASE_FILE" \
        --query_file "$QUERY_FILE" \
        --gt_file "$UNIF_SQ_GT_FILE" \
        --K 100 | tee "$RUN_DIR/compute_groundtruth.log"
    
    # Calculating recall
    echo "Calculating recall..."
    RECALL_OUTPUT=$("${DISKANN_DIR}/build/apps/utils/calculate_recall" \
        "$GT_FILE" \
        "$UNIF_SQ_GT_FILE" \
        100 | tee "$RUN_DIR/calculate_recall.log")
    
    echo "Bytes=$TARGET_TOTAL_SQ_BYTES - $RECALL_OUTPUT"
    
    # Clean up huge temporary files (each base inflated file is 3.1 GB!)
    echo "Cleaning up large intermediate files..."
    rm -f "$UNIF_SQ_BASE_FILE" "$UNIF_SQ_GT_FILE" "${UNIF_SQ_BASE_PREFIX}_sq_compressed.bin"
    
done

echo ""
echo "=================================================="
echo "SQ sweep completed!"
echo "Results directory: $SWEEP_DIR"
echo "=================================================="

# Summary of results
echo ""
echo "Summary of SQ recall results:"
echo "Bytes,Recall"
for TARGET_TOTAL_SQ_BYTES in "${BYTE_VALUES[@]}"; do
    RUN_DIR="${SWEEP_DIR}/bytes_${TARGET_TOTAL_SQ_BYTES}"
    if [ -f "$RUN_DIR/calculate_recall.log" ]; then
        RECALL=$(tail -1 "$RUN_DIR/calculate_recall.log" | grep -oP '\d+\.\d+' || echo "N/A")
        echo "$TARGET_TOTAL_SQ_BYTES,$RECALL"
    fi
done
