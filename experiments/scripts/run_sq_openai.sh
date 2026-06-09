#!/usr/bin/env bash
set -euo pipefail
set -x

DATASET=scifact
EMBEDDING_MODEL="openai_text_large_3"
BASE_FILE_NAME=base.bin
QUERY_FILE_NAME=query.bin
RUN_NAME=${RUN_NAME:-sq_buckets_8_init_8_inc_8_max_384_sampl_01_bytes_384_stride}
ALLOCATION_STRATEGY=${ALLOCATION_STRATEGY:-stride}

EMBEDDINGS_DIR=/home/jam1729/data/embeddings
DISKANN_DIR=/home/jam1729/DiskANN

BASE_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/${BASE_FILE_NAME}
QUERY_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/${QUERY_FILE_NAME}
GT_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/gt100.bin
RUN_DIR=/home/jam1729/runs/sq_search_runs/${DATASET}/${EMBEDDING_MODEL}/${RUN_NAME}_$(date +%Y%m%d_%H%M%S)

mkdir -p "${RUN_DIR}"
"${DISKANN_DIR}/.venv/bin/python3" $DISKANN_DIR/scripts/dev/greedy_sq_bucket_search.py \
  --base_file ${BASE_FILE} \
  --query_file ${QUERY_FILE} \
  --raw_gt_file ${GT_FILE} \
  --work_dir ${RUN_DIR} \
  --tools_dir ${DISKANN_DIR}/build/apps/utils \
  --k 100 \
  --sampling_rate 0.1 \
  --num_buckets 8 \
  --initial_chunks 8 \
  --increment 8 \
  --max_per_bucket 384 \
  --max_total_bytes 384 \
  --max_iters 50 \
  --seed 42 \
  --allocation_strategy "$ALLOCATION_STRATEGY" \
  --log_json ${RUN_DIR}/log.json \
  > >(tee "${RUN_DIR}/stdout") \
  2> >(tee "${RUN_DIR}/stderr" >&2)
