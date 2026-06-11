
#!/usr/bin/env bash
set -euo pipefail
set -x

DATASET=scidocs
EMBEDDING_MODEL="openai_text_large_3"
BASE_FILE_NAME=base.bin
QUERY_FILE_NAME=query.bin
RUN_NAME=${RUN_NAME:-chunks_buckets_8_init_8_inc_8_max_384_sampl_01_bytes_384}

EMBEDDINGS_DIR=/home/jam1729/data/embeddings
DISKANN_DIR=/home/jam1729/DiskANN

BASE_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/${BASE_FILE_NAME}
QUERY_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/${QUERY_FILE_NAME}
GT_FILE=${EMBEDDINGS_DIR}/${DATASET}/${EMBEDDING_MODEL}/gt100.bin
RUN_DIR=/home/jam1729/runs/pq_search_runs/${DATASET}/${EMBEDDING_MODEL}/${RUN_NAME}_$(date +%Y%m%d_%H%M%S)

# TARGET_TOTAL_PQ_BYTES=384
# UNIF_PQ_BASE_PREFIX="${BASE_FILE%.bin}_unif"
# INFLATED_PQ_SUFFIX="_pq_compressed.bin_inflated.bin"
# UNIF_PQ_BASE_FILE="${UNIF_PQ_BASE_PREFIX}${INFLATED_PQ_SUFFIX}"
# UNIF_PQ_GT_FILE="${UNIF_PQ_BASE_PREFIX}_pq_compressed.bin_gt100"

# echo "Computing original ground truth..."
# ${DISKANN_DIR}/build/apps/utils/compute_groundtruth \
#     --data_type float \
#     --dist_fn l2 \
#     --base_file "$BASE_FILE" \
#     --query_file "$QUERY_FILE" \
#     --gt_file "$GT_FILE" \
#     --K 100

# echo "Generating PQ data..."
# ${DISKANN_DIR}/build/apps/utils/generate_pq \
#     float \
#     "$BASE_FILE" \
#     "$UNIF_PQ_BASE_PREFIX" \
#     "$TARGET_TOTAL_PQ_BYTES" \
#     0.1 0
 
# echo "Computing exact k-NN for PQ data..."
# ${DISKANN_DIR}/build/apps/utils/compute_groundtruth \
#     --data_type float \
#     --dist_fn l2 \
#     --base_file "$UNIF_PQ_BASE_FILE" \
#     --query_file "$QUERY_FILE" \
#     --gt_file "$UNIF_PQ_GT_FILE" \
#     --K 100
 
# echo "Calculating recall..."
# ${DISKANN_DIR}/build/apps/utils/calculate_recall \
#     "$GT_FILE" \
#     "$UNIF_PQ_GT_FILE" \
#     100

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
  --initial_chunks 8 \
  --increment 8 \
  --max_per_bucket 384 \
  --max_total_bytes 384 \
  --max_iters 50 \
  --log_json ${RUN_DIR}/log.json \
  > >(tee "${RUN_DIR}/stdout") \
  2> >(tee "${RUN_DIR}/stderr" >&2)