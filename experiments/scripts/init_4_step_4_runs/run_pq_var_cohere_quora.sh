
#!/usr/bin/env bash
set -euo pipefail
set -x

DATASET=quora_500k
EMBEDDING_MODEL="cohere_v4"
BASE_FILE_NAME=base.bin
QUERY_FILE_NAME=query.bin
RUN_NAME=${RUN_NAME:-chunks_buckets_8_init_4_inc_4_max_192_sampl_01_bytes_192}

EMBEDDINGS_DIR=~/data/embeddings
DISKANN_DIR=~/DiskANN

BASE_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/${BASE_FILE_NAME}
QUERY_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/${QUERY_FILE_NAME}
GT_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/gt100.bin
RUN_DIR=~/runs/pq_search_runs/${DATASET}/${EMBEDDING_MODEL}/${RUN_NAME}_$(date +%Y%m%d_%H%M%S)

mkdir -p "${RUN_DIR}"
python $DISKANN_DIR/scripts/dev/greedy_pq_bucket_search.py \
  --base_file ${BASE_FILE} \
  --query_file ${QUERY_FILE} \
  --raw_gt_file ${GT_FILE} \
  --work_dir ${RUN_DIR} \
  --tools_dir ${DISKANN_DIR}/build/apps/utils \
  --k 100 \
  --sampling_rate 0.1 \
  --num_buckets 8 \
  --initial_chunks 4 \
  --increment 4 \
  --max_per_bucket 192 \
  --max_total_bytes 192 \
  --max_iters 50 \
  --log_json ${RUN_DIR}/log.json \
  > >(tee "${RUN_DIR}/stdout") \
  2> >(tee "${RUN_DIR}/stderr" >&2)