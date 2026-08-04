#!/usr/bin/env bash
# Runs the Matryoshka Block-OPQ pipeline comparison for Cohere v4 on dbpedia_entity_500k.

set -euo pipefail
set -x

DATASET=scidocs
EMBEDDING_MODEL="openai_text_large_3"
BASE_FILE_NAME=base.bin
QUERY_FILE_NAME=query.bin

EMBEDDINGS_DIR=/home/jam1729/data/embeddings
DISKANN_DIR=/home/jam1729/DiskANN

BASE_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/${BASE_FILE_NAME}
QUERY_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/${QUERY_FILE_NAME}
GT_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/gt100.bin

RUN_NAME="opq_comparison_$(date +%s)"
RUN_DIR="/home/jam1729/runs/opq_runs/${DATASET}/${EMBEDDING_MODEL}/${RUN_NAME}"
mkdir -p "${RUN_DIR}"

# Run the Python OPQ Orchestrator
${DISKANN_DIR}/.venv/bin/python3 ${DISKANN_DIR}/scripts/dev/run_opq_pipeline.py \
  --base_file "${BASE_FILE}" \
  --query_file "${QUERY_FILE}" \
  --raw_gt_file "${GT_FILE}" \
  --work_dir "${RUN_DIR}" \
  --tools_dir "${DISKANN_DIR}/build/apps/utils" \
  --k 100 \
  --sampling_rate 0.1 \
  --num_buckets 8 \
  --initial_chunks 8 \
  --increment 8 \
  --max_per_bucket 384 \
  --max_total_bytes 384 \
  --max_iters 50 \
  > >(tee "${RUN_DIR}/stdout.log") \
  2> >(tee "${RUN_DIR}/stderr.log" >&2)

echo "=================================================="
echo "Sweep finished. Output written to ${RUN_DIR}"
echo "Summary:"
cat "${RUN_DIR}/stdout.log" | grep -A 6 "OPQ EXPERIMENT SUMMARY" || true
echo "=================================================="
