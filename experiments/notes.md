## Size
3072 * float32 = 3072 * 4 bytes = 12k bytes total
384 bytes total = 3072/8 bytes = 3072 bits = 1 bit per point 

## PQ
### MSMARCO_500k 3072 dims
##### Uniform PQ
###### 64 bytes
PQ Sampling rate: Recall
- 0.3: Avg. recall@100 is 45.6908
- 0.5: Avg. recall@100 is 45.5364

###### 384 bytes
PQ Sampling rate: Recall
- 0.1: Avg. recall@100 is 86.2523
- 0.3: Avg. recall@100 is 86.2383


Summary of recall results:
Bytes,Recall
64,47.0814
96,60.3447
128,68.3855
160,73.4857
192,77.0812
224,79.5797
256,81.6388
288,82.9589
320,84.1393
352,85.202
384,86.2391

### Variable PQ
#### First 20 iters:

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
  --log_json log \
  > >(tee "${RUN_DIR}/stdout") \
  2> >(tee "${RUN_DIR}/stderr" >&2)

PQ_GREEDY_EVAL tag=init alloc=[8, 8, 8, 8, 8, 8, 8, 8] bytes=64 recall=47.616600

PQ_GREEDY_EVAL tag=it1_b0_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 8] bytes=72 recall=53.213200

PQ_GREEDY_EVAL tag=it1_b1_plus8 alloc=[8, 16, 8, 8, 8, 8, 8, 8] bytes=72 recall=52.304200

PQ_GREEDY_EVAL tag=it1_b2_plus8 alloc=[8, 8, 16, 8, 8, 8, 8, 8] bytes=72 recall=51.445700

PQ_GREEDY_EVAL tag=it1_b3_plus8 alloc=[8, 8, 8, 16, 8, 8, 8, 8] bytes=72 recall=50.632400

PQ_GREEDY_EVAL tag=it1_b4_plus8 alloc=[8, 8, 8, 8, 16, 8, 8, 8] bytes=72 recall=49.887700

PQ_GREEDY_EVAL tag=it1_b5_plus8 alloc=[8, 8, 8, 8, 8, 16, 8, 8] bytes=72 recall=49.810700

PQ_GREEDY_EVAL tag=it1_b6_plus8 alloc=[8, 8, 8, 8, 8, 8, 16, 8] bytes=72 recall=49.728900

PQ_GREEDY_EVAL tag=it1_b7_plus8 alloc=[8, 8, 8, 8, 8, 8, 8, 16] bytes=72 recall=49.730500

PQ_GREEDY_EVAL tag=it2_b0_plus8 alloc=[24, 8, 8, 8, 8, 8, 8, 8] bytes=80 recall=57.548100

PQ_GREEDY_EVAL tag=it2_b1_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 8] bytes=80 recall=57.430500

PQ_GREEDY_EVAL tag=it2_b2_plus8 alloc=[16, 8, 16, 8, 8, 8, 8, 8] bytes=80 recall=56.566300

PQ_GREEDY_EVAL tag=it2_b3_plus8 alloc=[16, 8, 8, 16, 8, 8, 8, 8] bytes=80 recall=56.073500

PQ_GREEDY_EVAL tag=it2_b4_plus8 alloc=[16, 8, 8, 8, 16, 8, 8, 8] bytes=80 recall=55.204700

PQ_GREEDY_EVAL tag=it2_b5_plus8 alloc=[16, 8, 8, 8, 8, 16, 8, 8] bytes=80 recall=55.099600

PQ_GREEDY_EVAL tag=it2_b6_plus8 alloc=[16, 8, 8, 8, 8, 8, 16, 8] bytes=80 recall=55.410900

PQ_GREEDY_EVAL tag=it2_b7_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 16] bytes=80 recall=55.262900

PQ_GREEDY_EVAL tag=it3_b0_plus8 alloc=[32, 8, 8, 8, 8, 8, 8, 8] bytes=88 recall=60.166800

PQ_GREEDY_EVAL tag=it3_b1_plus8 alloc=[24, 16, 8, 8, 8, 8, 8, 8] bytes=88 recall=61.157900

PQ_GREEDY_EVAL tag=it3_b2_plus8 alloc=[24, 8, 16, 8, 8, 8, 8, 8] bytes=88 recall=60.553700

PQ_GREEDY_EVAL tag=it3_b3_plus8 alloc=[24, 8, 8, 16, 8, 8, 8, 8] bytes=88 recall=59.940800

PQ_GREEDY_EVAL tag=it3_b4_plus8 alloc=[24, 8, 8, 8, 16, 8, 8, 8] bytes=88 recall=59.189000

PQ_GREEDY_EVAL tag=it3_b5_plus8 alloc=[24, 8, 8, 8, 8, 16, 8, 8] bytes=88 recall=59.015600

PQ_GREEDY_EVAL tag=it3_b6_plus8 alloc=[24, 8, 8, 8, 8, 8, 16, 8] bytes=88 recall=59.023100

PQ_GREEDY_EVAL tag=it3_b7_plus8 alloc=[24, 8, 8, 8, 8, 8, 8, 16] bytes=88 recall=59.075100

PQ_GREEDY_EVAL tag=it4_b0_plus8 alloc=[32, 16, 8, 8, 8, 8, 8, 8] bytes=96 recall=63.785000

PQ_GREEDY_EVAL tag=it4_b1_plus8 alloc=[24, 24, 8, 8, 8, 8, 8, 8] bytes=96 recall=63.649100

PQ_GREEDY_EVAL tag=it4_b2_plus8 alloc=[24, 16, 16, 8, 8, 8, 8, 8] bytes=96 recall=64.035000

PQ_GREEDY_EVAL tag=it4_b3_plus8 alloc=[24, 16, 8, 16, 8, 8, 8, 8] bytes=96 recall=63.282800

PQ_GREEDY_EVAL tag=it4_b4_plus8 alloc=[24, 16, 8, 8, 16, 8, 8, 8] bytes=96 recall=62.737200

PQ_GREEDY_EVAL tag=it4_b5_plus8 alloc=[24, 16, 8, 8, 8, 16, 8, 8] bytes=96 recall=62.646700

PQ_GREEDY_EVAL tag=it4_b6_plus8 alloc=[24, 16, 8, 8, 8, 8, 16, 8] bytes=96 recall=62.525200

PQ_GREEDY_EVAL tag=it4_b7_plus8 alloc=[24, 16, 8, 8, 8, 8, 8, 16] bytes=96 recall=62.668500

PQ_GREEDY_EVAL tag=it5_b0_plus8 alloc=[32, 16, 16, 8, 8, 8, 8, 8] bytes=104 recall=66.271300

PQ_GREEDY_EVAL tag=it5_b1_plus8 alloc=[24, 24, 16, 8, 8, 8, 8, 8] bytes=104 recall=66.252600

PQ_GREEDY_EVAL tag=it5_b2_plus8 alloc=[24, 16, 24, 8, 8, 8, 8, 8] bytes=104 recall=65.946300

PQ_GREEDY_EVAL tag=it5_b3_plus8 alloc=[24, 16, 16, 16, 8, 8, 8, 8] bytes=104 recall=65.965500

PQ_GREEDY_EVAL tag=it5_b4_plus8 alloc=[24, 16, 16, 8, 16, 8, 8, 8] bytes=104 recall=65.488700

PQ_GREEDY_EVAL tag=it5_b5_plus8 alloc=[24, 16, 16, 8, 8, 16, 8, 8] bytes=104 recall=65.313300

PQ_GREEDY_EVAL tag=it5_b6_plus8 alloc=[24, 16, 16, 8, 8, 8, 16, 8] bytes=104 recall=65.331200

PQ_GREEDY_EVAL tag=it5_b7_plus8 alloc=[24, 16, 16, 8, 8, 8, 8, 16] bytes=104 recall=65.264500

PQ_GREEDY_EVAL tag=it6_b0_plus8 alloc=[40, 16, 16, 8, 8, 8, 8, 8] bytes=112 recall=67.975100

PQ_GREEDY_EVAL tag=it6_b1_plus8 alloc=[32, 24, 16, 8, 8, 8, 8, 8] bytes=112 recall=68.457000

PQ_GREEDY_EVAL tag=it6_b2_plus8 alloc=[32, 16, 24, 8, 8, 8, 8, 8] bytes=112 recall=67.979700

PQ_GREEDY_EVAL tag=it6_b3_plus8 alloc=[32, 16, 16, 16, 8, 8, 8, 8] bytes=112 recall=68.072100

PQ_GREEDY_EVAL tag=it6_b4_plus8 alloc=[32, 16, 16, 8, 16, 8, 8, 8] bytes=112 recall=67.633500

PQ_GREEDY_EVAL tag=it6_b5_plus8 alloc=[32, 16, 16, 8, 8, 16, 8, 8] bytes=112 recall=67.627700

PQ_GREEDY_EVAL tag=it6_b6_plus8 alloc=[32, 16, 16, 8, 8, 8, 16, 8] bytes=112 recall=67.536100

PQ_GREEDY_EVAL tag=it6_b7_plus8 alloc=[32, 16, 16, 8, 8, 8, 8, 16] bytes=112 recall=67.614200

PQ_GREEDY_EVAL tag=it7_b0_plus8 alloc=[40, 24, 16, 8, 8, 8, 8, 8] bytes=120 recall=70.031700

PQ_GREEDY_EVAL tag=it7_b1_plus8 alloc=[32, 32, 16, 8, 8, 8, 8, 8] bytes=120 recall=69.959500

PQ_GREEDY_EVAL tag=it7_b2_plus8 alloc=[32, 24, 24, 8, 8, 8, 8, 8] bytes=120 recall=69.899300

PQ_GREEDY_EVAL tag=it7_b3_plus8 alloc=[32, 24, 16, 16, 8, 8, 8, 8] bytes=120 recall=70.078800

PQ_GREEDY_EVAL tag=it7_b4_plus8 alloc=[32, 24, 16, 8, 16, 8, 8, 8] bytes=120 recall=69.570100

PQ_GREEDY_EVAL tag=it7_b5_plus8 alloc=[32, 24, 16, 8, 8, 16, 8, 8] bytes=120 recall=69.631500

PQ_GREEDY_EVAL tag=it7_b6_plus8 alloc=[32, 24, 16, 8, 8, 8, 16, 8] bytes=120 recall=69.561300

PQ_GREEDY_EVAL tag=it7_b7_plus8 alloc=[32, 24, 16, 8, 8, 8, 8, 16] bytes=120 recall=69.597100

PQ_GREEDY_EVAL tag=it8_b0_plus8 alloc=[40, 24, 16, 16, 8, 8, 8, 8] bytes=128 recall=71.496000

PQ_GREEDY_EVAL tag=it8_b1_plus8 alloc=[32, 32, 16, 16, 8, 8, 8, 8] bytes=128 recall=71.474500

PQ_GREEDY_EVAL tag=it8_b2_plus8 alloc=[32, 24, 24, 16, 8, 8, 8, 8] bytes=128 recall=71.627100

PQ_GREEDY_EVAL tag=it8_b3_plus8 alloc=[32, 24, 16, 24, 8, 8, 8, 8] bytes=128 recall=71.251700

PQ_GREEDY_EVAL tag=it8_b4_plus8 alloc=[32, 24, 16, 16, 16, 8, 8, 8] bytes=128 recall=71.172300

PQ_GREEDY_EVAL tag=it8_b5_plus8 alloc=[32, 24, 16, 16, 8, 16, 8, 8] bytes=128 recall=71.207300

PQ_GREEDY_EVAL tag=it8_b6_plus8 alloc=[32, 24, 16, 16, 8, 8, 16, 8] bytes=128 recall=71.191300

PQ_GREEDY_EVAL tag=it8_b7_plus8 alloc=[32, 24, 16, 16, 8, 8, 8, 16] bytes=128 recall=71.217800

PQ_GREEDY_EVAL tag=it9_b0_plus8 alloc=[40, 24, 24, 16, 8, 8, 8, 8] bytes=136 recall=72.906600

PQ_GREEDY_EVAL tag=it9_b1_plus8 alloc=[32, 32, 24, 16, 8, 8, 8, 8] bytes=136 recall=72.847000

PQ_GREEDY_EVAL tag=it9_b2_plus8 alloc=[32, 24, 32, 16, 8, 8, 8, 8] bytes=136 recall=72.495000

PQ_GREEDY_EVAL tag=it9_b3_plus8 alloc=[32, 24, 24, 24, 8, 8, 8, 8] bytes=136 recall=72.574800

PQ_GREEDY_EVAL tag=it9_b4_plus8 alloc=[32, 24, 24, 16, 16, 8, 8, 8] bytes=136 recall=72.621100

PQ_GREEDY_EVAL tag=it9_b5_plus8 alloc=[32, 24, 24, 16, 8, 16, 8, 8] bytes=136 recall=72.521600

PQ_GREEDY_EVAL tag=it9_b6_plus8 alloc=[32, 24, 24, 16, 8, 8, 16, 8] bytes=136 recall=72.533100

PQ_GREEDY_EVAL tag=it9_b7_plus8 alloc=[32, 24, 24, 16, 8, 8, 8, 16] bytes=136 recall=72.600400

PQ_GREEDY_EVAL tag=it10_b0_plus8 alloc=[48, 24, 24, 16, 8, 8, 8, 8] bytes=144 recall=73.738300

PQ_GREEDY_EVAL tag=it10_b1_plus8 alloc=[40, 32, 24, 16, 8, 8, 8, 8] bytes=144 recall=74.208500

PQ_GREEDY_EVAL tag=it10_b2_plus8 alloc=[40, 24, 32, 16, 8, 8, 8, 8] bytes=144 recall=73.786000

PQ_GREEDY_EVAL tag=it10_b3_plus8 alloc=[40, 24, 24, 24, 8, 8, 8, 8] bytes=144 recall=73.872200

PQ_GREEDY_EVAL tag=it10_b4_plus8 alloc=[40, 24, 24, 16, 16, 8, 8, 8] bytes=144 recall=73.912300

PQ_GREEDY_EVAL tag=it10_b5_plus8 alloc=[40, 24, 24, 16, 8, 16, 8, 8] bytes=144 recall=73.873200

PQ_GREEDY_EVAL tag=it10_b6_plus8 alloc=[40, 24, 24, 16, 8, 8, 16, 8] bytes=144 recall=73.776400

PQ_GREEDY_EVAL tag=it10_b7_plus8 alloc=[40, 24, 24, 16, 8, 8, 8, 16] bytes=144 recall=73.820100

PQ_GREEDY_EVAL tag=it11_b0_plus8 alloc=[48, 32, 24, 16, 8, 8, 8, 8] bytes=152 recall=74.943100

PQ_GREEDY_EVAL tag=it11_b1_plus8 alloc=[40, 40, 24, 16, 8, 8, 8, 8] bytes=152 recall=75.060500

PQ_GREEDY_EVAL tag=it11_b2_plus8 alloc=[40, 32, 32, 16, 8, 8, 8, 8] bytes=152 recall=75.008700

PQ_GREEDY_EVAL tag=it11_b3_plus8 alloc=[40, 32, 24, 24, 8, 8, 8, 8] bytes=152 recall=75.097700

PQ_GREEDY_EVAL tag=it11_b4_plus8 alloc=[40, 32, 24, 16, 16, 8, 8, 8] bytes=152 recall=74.933700

PQ_GREEDY_EVAL tag=it11_b5_plus8 alloc=[40, 32, 24, 16, 8, 16, 8, 8] bytes=152 recall=75.001600

PQ_GREEDY_EVAL tag=it11_b6_plus8 alloc=[40, 32, 24, 16, 8, 8, 16, 8] bytes=152 recall=74.971200

PQ_GREEDY_EVAL tag=it11_b7_plus8 alloc=[40, 32, 24, 16, 8, 8, 8, 16] bytes=152 recall=74.999100

PQ_GREEDY_EVAL tag=it12_b0_plus8 alloc=[48, 32, 24, 24, 8, 8, 8, 8] bytes=160 recall=75.857000

PQ_GREEDY_EVAL tag=it12_b1_plus8 alloc=[40, 40, 24, 24, 8, 8, 8, 8] bytes=160 recall=75.959200

PQ_GREEDY_EVAL tag=it12_b2_plus8 alloc=[40, 32, 32, 24, 8, 8, 8, 8] bytes=160 recall=75.983400

PQ_GREEDY_EVAL tag=it12_b3_plus8 alloc=[40, 32, 24, 32, 8, 8, 8, 8] bytes=160 recall=75.702400

PQ_GREEDY_EVAL tag=it12_b4_plus8 alloc=[40, 32, 24, 24, 16, 8, 8, 8] bytes=160 recall=75.892300

PQ_GREEDY_EVAL tag=it12_b5_plus8 alloc=[40, 32, 24, 24, 8, 16, 8, 8] bytes=160 recall=75.947100

PQ_GREEDY_EVAL tag=it12_b6_plus8 alloc=[40, 32, 24, 24, 8, 8, 16, 8] bytes=160 recall=75.901000

PQ_GREEDY_EVAL tag=it12_b7_plus8 alloc=[40, 32, 24, 24, 8, 8, 8, 16] bytes=160 recall=75.908700

PQ_GREEDY_EVAL tag=it13_b0_plus8 alloc=[48, 32, 32, 24, 8, 8, 8, 8] bytes=168 recall=76.724100

PQ_GREEDY_EVAL tag=it13_b1_plus8 alloc=[40, 40, 32, 24, 8, 8, 8, 8] bytes=168 recall=76.685800

PQ_GREEDY_EVAL tag=it13_b2_plus8 alloc=[40, 32, 40, 24, 8, 8, 8, 8] bytes=168 recall=76.595600

PQ_GREEDY_EVAL tag=it13_b3_plus8 alloc=[40, 32, 32, 32, 8, 8, 8, 8] bytes=168 recall=76.537400

PQ_GREEDY_EVAL tag=it13_b4_plus8 alloc=[40, 32, 32, 24, 16, 8, 8, 8] bytes=168 recall=76.732700

PQ_GREEDY_EVAL tag=it13_b5_plus8 alloc=[40, 32, 32, 24, 8, 16, 8, 8] bytes=168 recall=76.726500

PQ_GREEDY_EVAL tag=it13_b6_plus8 alloc=[40, 32, 32, 24, 8, 8, 16, 8] bytes=168 recall=76.735500

PQ_GREEDY_EVAL tag=it13_b7_plus8 alloc=[40, 32, 32, 24, 8, 8, 8, 16] bytes=168 recall=76.820600

PQ_GREEDY_EVAL tag=it14_b0_plus8 alloc=[48, 32, 32, 24, 8, 8, 8, 16] bytes=176 recall=77.515500

PQ_GREEDY_EVAL tag=it14_b1_plus8 alloc=[40, 40, 32, 24, 8, 8, 8, 16] bytes=176 recall=77.537100

PQ_GREEDY_EVAL tag=it14_b2_plus8 alloc=[40, 32, 40, 24, 8, 8, 8, 16] bytes=176 recall=77.355900

PQ_GREEDY_EVAL tag=it14_b3_plus8 alloc=[40, 32, 32, 32, 8, 8, 8, 16] bytes=176 recall=77.347100

PQ_GREEDY_EVAL tag=it14_b4_plus8 alloc=[40, 32, 32, 24, 16, 8, 8, 16] bytes=176 recall=77.496100

PQ_GREEDY_EVAL tag=it14_b5_plus8 alloc=[40, 32, 32, 24, 8, 16, 8, 16] bytes=176 recall=77.568500

PQ_GREEDY_EVAL tag=it14_b6_plus8 alloc=[40, 32, 32, 24, 8, 8, 16, 16] bytes=176 recall=77.495000

PQ_GREEDY_EVAL tag=it14_b7_plus8 alloc=[40, 32, 32, 24, 8, 8, 8, 24] bytes=176 recall=77.252700

PQ_GREEDY_EVAL tag=it15_b0_plus8 alloc=[48, 32, 32, 24, 8, 16, 8, 16] bytes=184 recall=78.183500

PQ_GREEDY_EVAL tag=it15_b1_plus8 alloc=[40, 40, 32, 24, 8, 16, 8, 16] bytes=184 recall=78.210200

PQ_GREEDY_EVAL tag=it15_b2_plus8 alloc=[40, 32, 40, 24, 8, 16, 8, 16] bytes=184 recall=78.169500

PQ_GREEDY_EVAL tag=it15_b3_plus8 alloc=[40, 32, 32, 32, 8, 16, 8, 16] bytes=184 recall=78.072800

PQ_GREEDY_EVAL tag=it15_b4_plus8 alloc=[40, 32, 32, 24, 16, 16, 8, 16] bytes=184 recall=78.238700

PQ_GREEDY_EVAL tag=it15_b5_plus8 alloc=[40, 32, 32, 24, 8, 24, 8, 16] bytes=184 recall=78.017300

PQ_GREEDY_EVAL tag=it15_b6_plus8 alloc=[40, 32, 32, 24, 8, 16, 16, 16] bytes=184 recall=78.200300

PQ_GREEDY_EVAL tag=it15_b7_plus8 alloc=[40, 32, 32, 24, 8, 16, 8, 24] bytes=184 recall=78.057900

PQ_GREEDY_EVAL tag=it16_b0_plus8 alloc=[48, 32, 32, 24, 16, 16, 8, 16] bytes=192 recall=78.984200

PQ_GREEDY_EVAL tag=it16_b1_plus8 alloc=[40, 40, 32, 24, 16, 16, 8, 16] bytes=192 recall=79.010600

PQ_GREEDY_EVAL tag=it16_b2_plus8 alloc=[40, 32, 40, 24, 16, 16, 8, 16] bytes=192 recall=78.749400

PQ_GREEDY_EVAL tag=it16_b3_plus8 alloc=[40, 32, 32, 32, 16, 16, 8, 16] bytes=192 recall=78.900000

PQ_GREEDY_EVAL tag=it16_b4_plus8 alloc=[40, 32, 32, 24, 24, 16, 8, 16] bytes=192 recall=78.763500

PQ_GREEDY_EVAL tag=it16_b5_plus8 alloc=[40, 32, 32, 24, 16, 24, 8, 16] bytes=192 recall=78.820200

PQ_GREEDY_EVAL tag=it16_b6_plus8 alloc=[40, 32, 32, 24, 16, 16, 16, 16] bytes=192 recall=78.953400

PQ_GREEDY_EVAL tag=it16_b7_plus8 alloc=[40, 32, 32, 24, 16, 16, 8, 24] bytes=192 recall=78.779700

PQ_GREEDY_EVAL tag=it17_b0_plus8 alloc=[48, 40, 32, 24, 16, 16, 8, 16] bytes=200 recall=79.581200

PQ_GREEDY_EVAL tag=it17_b1_plus8 alloc=[40, 48, 32, 24, 16, 16, 8, 16] bytes=200 recall=79.530700

PQ_GREEDY_EVAL tag=it17_b2_plus8 alloc=[40, 40, 40, 24, 16, 16, 8, 16] bytes=200 recall=79.539500

PQ_GREEDY_EVAL tag=it17_b3_plus8 alloc=[40, 40, 32, 32, 16, 16, 8, 16] bytes=200 recall=79.483500

PQ_GREEDY_EVAL tag=it17_b4_plus8 alloc=[40, 40, 32, 24, 24, 16, 8, 16] bytes=200 recall=79.415200

PQ_GREEDY_EVAL tag=it17_b5_plus8 alloc=[40, 40, 32, 24, 16, 24, 8, 16] bytes=200 recall=79.377200

PQ_GREEDY_EVAL tag=it17_b6_plus8 alloc=[40, 40, 32, 24, 16, 16, 16, 16] bytes=200 recall=79.572100

PQ_GREEDY_EVAL tag=it17_b7_plus8 alloc=[40, 40, 32, 24, 16, 16, 8, 24] bytes=200 recall=79.431500

PQ_GREEDY_EVAL tag=it18_b0_plus8 alloc=[56, 40, 32, 24, 16, 16, 8, 16] bytes=208 recall=80.139100

PQ_GREEDY_EVAL tag=it18_b1_plus8 alloc=[48, 48, 32, 24, 16, 16, 8, 16] bytes=208 recall=80.176500

PQ_GREEDY_EVAL tag=it18_b2_plus8 alloc=[48, 40, 40, 24, 16, 16, 8, 16] bytes=208 recall=80.175100

PQ_GREEDY_EVAL tag=it18_b3_plus8 alloc=[48, 40, 32, 32, 16, 16, 8, 16] bytes=208 recall=80.096700

PQ_GREEDY_EVAL tag=it18_b4_plus8 alloc=[48, 40, 32, 24, 24, 16, 8, 16] bytes=208 recall=80.039700

PQ_GREEDY_EVAL tag=it18_b5_plus8 alloc=[48, 40, 32, 24, 16, 24, 8, 16] bytes=208 recall=80.073800

PQ_GREEDY_EVAL tag=it18_b6_plus8 alloc=[48, 40, 32, 24, 16, 16, 16, 16] bytes=208 recall=80.267300

PQ_GREEDY_EVAL tag=it18_b7_plus8 alloc=[48, 40, 32, 24, 16, 16, 8, 24] bytes=208 recall=80.042800

PQ_GREEDY_EVAL tag=it19_b0_plus8 alloc=[56, 40, 32, 24, 16, 16, 16, 16] bytes=216 recall=80.707300

PQ_GREEDY_EVAL tag=it19_b1_plus8 alloc=[48, 48, 32, 24, 16, 16, 16, 16] bytes=216 recall=80.807400

PQ_GREEDY_EVAL tag=it19_b2_plus8 alloc=[48, 40, 40, 24, 16, 16, 16, 16] bytes=216 recall=80.773200

PQ_GREEDY_EVAL tag=it19_b3_plus8 alloc=[48, 40, 32, 32, 16, 16, 16, 16] bytes=216 recall=80.778800

PQ_GREEDY_EVAL tag=it19_b4_plus8 alloc=[48, 40, 32, 24, 24, 16, 16, 16] bytes=216 recall=80.623900

PQ_GREEDY_EVAL tag=it19_b5_plus8 alloc=[48, 40, 32, 24, 16, 24, 16, 16] bytes=216 recall=80.702900

PQ_GREEDY_EVAL tag=it19_b6_plus8 alloc=[48, 40, 32, 24, 16, 16, 24, 16] bytes=216 recall=80.668900

PQ_GREEDY_EVAL tag=it19_b7_plus8 alloc=[48, 40, 32, 24, 16, 16, 16, 24] bytes=216 recall=80.641700

PQ_GREEDY_EVAL tag=it20_b0_plus8 alloc=[56, 48, 32, 24, 16, 16, 16, 16] bytes=224 recall=81.285000

PQ_GREEDY_EVAL tag=it20_b1_plus8 alloc=[48, 56, 32, 24, 16, 16, 16, 16] bytes=224 recall=81.192100

PQ_GREEDY_EVAL tag=it20_b2_plus8 alloc=[48, 48, 40, 24, 16, 16, 16, 16] bytes=224 recall=81.300600

PQ_GREEDY_EVAL tag=it20_b3_plus8 alloc=[48, 48, 32, 32, 16, 16, 16, 16] bytes=224 recall=81.254700

PQ_GREEDY_EVAL tag=it20_b4_plus8 alloc=[48, 48, 32, 24, 24, 16, 16, 16] bytes=224 recall=81.191300

PQ_GREEDY_EVAL tag=it20_b5_plus8 alloc=[48, 48, 32, 24, 16, 24, 16, 16] bytes=224 recall=81.221200

PQ_GREEDY_EVAL tag=it20_b6_plus8 alloc=[48, 48, 32, 24, 16, 16, 24, 16] bytes=224 recall=81.236500

PQ_GREEDY_EVAL tag=it20_b7_plus8 alloc=[48, 48, 32, 24, 16, 16, 16, 24] bytes=224 recall=81.140300

PQ_GREEDY_EVAL tag=init alloc=[48, 48, 40, 24, 16, 16, 16, 16] bytes=224 recall=81.246100

PQ_GREEDY_EVAL tag=it1_b0_plus8 alloc=[56, 48, 40, 24, 16, 16, 16, 16] bytes=232 recall=81.776100

PQ_GREEDY_EVAL tag=it1_b1_plus8 alloc=[48, 56, 40, 24, 16, 16, 16, 16] bytes=232 recall=81.666600

PQ_GREEDY_EVAL tag=it1_b2_plus8 alloc=[48, 48, 48, 24, 16, 16, 16, 16] bytes=232 recall=81.620500

PQ_GREEDY_EVAL tag=it1_b3_plus8 alloc=[48, 48, 40, 32, 16, 16, 16, 16] bytes=232 recall=81.704000

PQ_GREEDY_EVAL tag=it1_b4_plus8 alloc=[48, 48, 40, 24, 24, 16, 16, 16] bytes=232 recall=81.662500

PQ_GREEDY_EVAL tag=it1_b5_plus8 alloc=[48, 48, 40, 24, 16, 24, 16, 16] bytes=232 recall=81.657200

PQ_GREEDY_EVAL tag=it1_b6_plus8 alloc=[48, 48, 40, 24, 16, 16, 24, 16] bytes=232 recall=81.640300

PQ_GREEDY_EVAL tag=it1_b7_plus8 alloc=[48, 48, 40, 24, 16, 16, 16, 24] bytes=232 recall=81.685400

PQ_GREEDY_EVAL tag=it2_b0_plus8 alloc=[64, 48, 40, 24, 16, 16, 16, 16] bytes=240 recall=82.117800

PQ_GREEDY_EVAL tag=it2_b1_plus8 alloc=[56, 56, 40, 24, 16, 16, 16, 16] bytes=240 recall=82.139300

PQ_GREEDY_EVAL tag=it2_b2_plus8 alloc=[56, 48, 48, 24, 16, 16, 16, 16] bytes=240 recall=82.107400

PQ_GREEDY_EVAL tag=it2_b3_plus8 alloc=[56, 48, 40, 32, 16, 16, 16, 16] bytes=240 recall=82.235800

PQ_GREEDY_EVAL tag=it2_b4_plus8 alloc=[56, 48, 40, 24, 24, 16, 16, 16] bytes=240 recall=82.099300

PQ_GREEDY_EVAL tag=it2_b5_plus8 alloc=[56, 48, 40, 24, 16, 24, 16, 16] bytes=240 recall=82.159500

PQ_GREEDY_EVAL tag=it2_b6_plus8 alloc=[56, 48, 40, 24, 16, 16, 24, 16] bytes=240 recall=82.097700

PQ_GREEDY_EVAL tag=it2_b7_plus8 alloc=[56, 48, 40, 24, 16, 16, 16, 24] bytes=240 recall=82.162500

PQ_GREEDY_EVAL tag=it3_b0_plus8 alloc=[64, 48, 40, 32, 16, 16, 16, 16] bytes=248 recall=82.607600

PQ_GREEDY_EVAL tag=it3_b1_plus8 alloc=[56, 56, 40, 32, 16, 16, 16, 16] bytes=248 recall=82.559200

PQ_GREEDY_EVAL tag=it3_b2_plus8 alloc=[56, 48, 48, 32, 16, 16, 16, 16] bytes=248 recall=82.649900

PQ_GREEDY_EVAL tag=it3_b3_plus8 alloc=[56, 48, 40, 40, 16, 16, 16, 16] bytes=248 recall=82.520300

PQ_GREEDY_EVAL tag=it3_b4_plus8 alloc=[56, 48, 40, 32, 24, 16, 16, 16] bytes=248 recall=82.513800

PQ_GREEDY_EVAL tag=it3_b5_plus8 alloc=[56, 48, 40, 32, 16, 24, 16, 16] bytes=248 recall=82.569800

PQ_GREEDY_EVAL tag=it3_b6_plus8 alloc=[56, 48, 40, 32, 16, 16, 24, 16] bytes=248 recall=82.558000

PQ_GREEDY_EVAL tag=it3_b7_plus8 alloc=[56, 48, 40, 32, 16, 16, 16, 24] bytes=248 recall=82.555300

PQ_GREEDY_EVAL tag=it4_b0_plus8 alloc=[64, 48, 48, 32, 16, 16, 16, 16] bytes=256 recall=82.977200

PQ_GREEDY_EVAL tag=it4_b1_plus8 alloc=[56, 56, 48, 32, 16, 16, 16, 16] bytes=256 recall=82.904000

PQ_GREEDY_EVAL tag=it4_b2_plus8 alloc=[56, 48, 56, 32, 16, 16, 16, 16] bytes=256 recall=82.908000

PQ_GREEDY_EVAL tag=it4_b3_plus8 alloc=[56, 48, 48, 40, 16, 16, 16, 16] bytes=256 recall=82.908300

PQ_GREEDY_EVAL tag=it4_b4_plus8 alloc=[56, 48, 48, 32, 24, 16, 16, 16] bytes=256 recall=82.956200

PQ_GREEDY_EVAL tag=it4_b5_plus8 alloc=[56, 48, 48, 32, 16, 24, 16, 16] bytes=256 recall=82.974800

PQ_GREEDY_EVAL tag=it4_b6_plus8 alloc=[56, 48, 48, 32, 16, 16, 24, 16] bytes=256 recall=82.938300

PQ_GREEDY_EVAL tag=it4_b7_plus8 alloc=[56, 48, 48, 32, 16, 16, 16, 24] bytes=256 recall=82.910300

PQ_GREEDY_EVAL tag=it5_b0_plus8 alloc=[72, 48, 48, 32, 16, 16, 16, 16] bytes=264 recall=83.277400

PQ_GREEDY_EVAL tag=it5_b1_plus8 alloc=[64, 56, 48, 32, 16, 16, 16, 16] bytes=264 recall=83.323400

PQ_GREEDY_EVAL tag=it5_b2_plus8 alloc=[64, 48, 56, 32, 16, 16, 16, 16] bytes=264 recall=83.292700

PQ_GREEDY_EVAL tag=it5_b3_plus8 alloc=[64, 48, 48, 40, 16, 16, 16, 16] bytes=264 recall=83.308900

PQ_GREEDY_EVAL tag=it5_b4_plus8 alloc=[64, 48, 48, 32, 24, 16, 16, 16] bytes=264 recall=83.312900

PQ_GREEDY_EVAL tag=it5_b5_plus8 alloc=[64, 48, 48, 32, 16, 24, 16, 16] bytes=264 recall=83.404000

PQ_GREEDY_EVAL tag=it5_b6_plus8 alloc=[64, 48, 48, 32, 16, 16, 24, 16] bytes=264 recall=83.362200

PQ_GREEDY_EVAL tag=it5_b7_plus8 alloc=[64, 48, 48, 32, 16, 16, 16, 24] bytes=264 recall=83.323900

PQ_GREEDY_EVAL tag=it6_b0_plus8 alloc=[72, 48, 48, 32, 16, 24, 16, 16] bytes=272 recall=83.602600

PQ_GREEDY_EVAL tag=it6_b1_plus8 alloc=[64, 56, 48, 32, 16, 24, 16, 16] bytes=272 recall=83.634800

PQ_GREEDY_EVAL tag=it6_b2_plus8 alloc=[64, 48, 56, 32, 16, 24, 16, 16] bytes=272 recall=83.669800

PQ_GREEDY_EVAL tag=it6_b3_plus8 alloc=[64, 48, 48, 40, 16, 24, 16, 16] bytes=272 recall=83.653700

PQ_GREEDY_EVAL tag=it6_b4_plus8 alloc=[64, 48, 48, 32, 24, 24, 16, 16] bytes=272 recall=83.610900

PQ_GREEDY_EVAL tag=it6_b5_plus8 alloc=[64, 48, 48, 32, 16, 32, 16, 16] bytes=272 recall=83.625600

PQ_GREEDY_EVAL tag=it6_b6_plus8 alloc=[64, 48, 48, 32, 16, 24, 24, 16] bytes=272 recall=83.640100

PQ_GREEDY_EVAL tag=it6_b7_plus8 alloc=[64, 48, 48, 32, 16, 24, 16, 24] bytes=272 recall=83.679900

PQ_GREEDY_EVAL tag=it7_b0_plus8 alloc=[72, 48, 48, 32, 16, 24, 16, 24] bytes=280 recall=83.964600

PQ_GREEDY_EVAL tag=it7_b1_plus8 alloc=[64, 56, 48, 32, 16, 24, 16, 24] bytes=280 recall=83.989800

PQ_GREEDY_EVAL tag=it7_b2_plus8 alloc=[64, 48, 56, 32, 16, 24, 16, 24] bytes=280 recall=83.949900

PQ_GREEDY_EVAL tag=it7_b3_plus8 alloc=[64, 48, 48, 40, 16, 24, 16, 24] bytes=280 recall=83.933200

PQ_GREEDY_EVAL tag=it7_b4_plus8 alloc=[64, 48, 48, 32, 24, 24, 16, 24] bytes=280 recall=84.015200

PQ_GREEDY_EVAL tag=it7_b5_plus8 alloc=[64, 48, 48, 32, 16, 32, 16, 24] bytes=280 recall=83.870900

PQ_GREEDY_EVAL tag=it7_b6_plus8 alloc=[64, 48, 48, 32, 16, 24, 24, 24] bytes=280 recall=83.963200

PQ_GREEDY_EVAL tag=it7_b7_plus8 alloc=[64, 48, 48, 32, 16, 24, 16, 32] bytes=280 recall=83.879800

PQ_GREEDY_EVAL tag=it8_b0_plus8 alloc=[72, 48, 48, 32, 24, 24, 16, 24] bytes=288 recall=84.238400

PQ_GREEDY_EVAL tag=it8_b1_plus8 alloc=[64, 56, 48, 32, 24, 24, 16, 24] bytes=288 recall=84.363500

PQ_GREEDY_EVAL tag=it8_b2_plus8 alloc=[64, 48, 56, 32, 24, 24, 16, 24] bytes=288 recall=84.295100

PQ_GREEDY_EVAL tag=it8_b3_plus8 alloc=[64, 48, 48, 40, 24, 24, 16, 24] bytes=288 recall=84.312800

PQ_GREEDY_EVAL tag=it8_b4_plus8 alloc=[64, 48, 48, 32, 32, 24, 16, 24] bytes=288 recall=84.247600

PQ_GREEDY_EVAL tag=it8_b5_plus8 alloc=[64, 48, 48, 32, 24, 32, 16, 24] bytes=288 recall=84.225800

PQ_GREEDY_EVAL tag=it8_b6_plus8 alloc=[64, 48, 48, 32, 24, 24, 24, 24] bytes=288 recall=84.235100

PQ_GREEDY_EVAL tag=it8_b7_plus8 alloc=[64, 48, 48, 32, 24, 24, 16, 32] bytes=288 recall=84.212900

PQ_GREEDY_EVAL tag=it9_b0_plus8 alloc=[72, 56, 48, 32, 24, 24, 16, 24] bytes=296 recall=84.588400

PQ_GREEDY_EVAL tag=it9_b1_plus8 alloc=[64, 64, 48, 32, 24, 24, 16, 24] bytes=296 recall=84.647400

PQ_GREEDY_EVAL tag=it9_b2_plus8 alloc=[64, 56, 56, 32, 24, 24, 16, 24] bytes=296 recall=84.589300

PQ_GREEDY_EVAL tag=it9_b3_plus8 alloc=[64, 56, 48, 40, 24, 24, 16, 24] bytes=296 recall=84.630700

PQ_GREEDY_EVAL tag=it9_b4_plus8 alloc=[64, 56, 48, 32, 32, 24, 16, 24] bytes=296 recall=84.520800

PQ_GREEDY_EVAL tag=it9_b5_plus8 alloc=[64, 56, 48, 32, 24, 32, 16, 24] bytes=296 recall=84.548600

PQ_GREEDY_EVAL tag=it9_b6_plus8 alloc=[64, 56, 48, 32, 24, 24, 24, 24] bytes=296 recall=84.524800

PQ_GREEDY_EVAL tag=it9_b7_plus8 alloc=[64, 56, 48, 32, 24, 24, 16, 32] bytes=296 recall=84.529100

PQ_GREEDY_EVAL tag=it10_b0_plus8 alloc=[72, 64, 48, 32, 24, 24, 16, 24] bytes=304 recall=84.926800

PQ_GREEDY_EVAL tag=it10_b1_plus8 alloc=[64, 72, 48, 32, 24, 24, 16, 24] bytes=304 recall=84.804900

PQ_GREEDY_EVAL tag=it10_b2_plus8 alloc=[64, 64, 56, 32, 24, 24, 16, 24] bytes=304 recall=84.884200

PQ_GREEDY_EVAL tag=it10_b3_plus8 alloc=[64, 64, 48, 40, 24, 24, 16, 24] bytes=304 recall=84.914900

PQ_GREEDY_EVAL tag=it10_b4_plus8 alloc=[64, 64, 48, 32, 32, 24, 16, 24] bytes=304 recall=84.875600

PQ_GREEDY_EVAL tag=it10_b5_plus8 alloc=[64, 64, 48, 32, 24, 32, 16, 24] bytes=304 recall=84.874600

PQ_GREEDY_EVAL tag=it10_b6_plus8 alloc=[64, 64, 48, 32, 24, 24, 24, 24] bytes=304 recall=84.942100

PQ_GREEDY_EVAL tag=it10_b7_plus8 alloc=[64, 64, 48, 32, 24, 24, 16, 32] bytes=304 recall=84.854200

PQ_GREEDY_EVAL tag=it11_b0_plus8 alloc=[72, 64, 48, 32, 24, 24, 24, 24] bytes=312 recall=85.174900

PQ_GREEDY_EVAL tag=it11_b1_plus8 alloc=[64, 72, 48, 32, 24, 24, 24, 24] bytes=312 recall=85.085000

PQ_GREEDY_EVAL tag=it11_b2_plus8 alloc=[64, 64, 56, 32, 24, 24, 24, 24] bytes=312 recall=85.153300

PQ_GREEDY_EVAL tag=it11_b3_plus8 alloc=[64, 64, 48, 40, 24, 24, 24, 24] bytes=312 recall=85.186100

PQ_GREEDY_EVAL tag=it11_b4_plus8 alloc=[64, 64, 48, 32, 32, 24, 24, 24] bytes=312 recall=85.136500

PQ_GREEDY_EVAL tag=it11_b5_plus8 alloc=[64, 64, 48, 32, 24, 32, 24, 24] bytes=312 recall=85.150000

PQ_GREEDY_EVAL tag=it11_b6_plus8 alloc=[64, 64, 48, 32, 24, 24, 32, 24] bytes=312 recall=85.139700

PQ_GREEDY_EVAL tag=it11_b7_plus8 alloc=[64, 64, 48, 32, 24, 24, 24, 32] bytes=312 recall=85.093700

PQ_GREEDY_EVAL tag=it12_b0_plus8 alloc=[72, 64, 48, 40, 24, 24, 24, 24] bytes=320 recall=85.473900

PQ_GREEDY_EVAL tag=it12_b1_plus8 alloc=[64, 72, 48, 40, 24, 24, 24, 24] bytes=320 recall=85.405000

PQ_GREEDY_EVAL tag=it12_b2_plus8 alloc=[64, 64, 56, 40, 24, 24, 24, 24] bytes=320 recall=85.459000

PQ_GREEDY_EVAL tag=it12_b3_plus8 alloc=[64, 64, 48, 48, 24, 24, 24, 24] bytes=320 recall=85.401900

PQ_GREEDY_EVAL tag=it12_b4_plus8 alloc=[64, 64, 48, 40, 32, 24, 24, 24] bytes=320 recall=85.385400

PQ_GREEDY_EVAL tag=it12_b5_plus8 alloc=[64, 64, 48, 40, 24, 32, 24, 24] bytes=320 recall=85.378700

PQ_GREEDY_EVAL tag=it12_b6_plus8 alloc=[64, 64, 48, 40, 24, 24, 32, 24] bytes=320 recall=85.416000

PQ_GREEDY_EVAL tag=it12_b7_plus8 alloc=[64, 64, 48, 40, 24, 24, 24, 32] bytes=320 recall=85.376800

PQ_GREEDY_EVAL tag=it13_b0_plus8 alloc=[80, 64, 48, 40, 24, 24, 24, 24] bytes=328 recall=85.689800

PQ_GREEDY_EVAL tag=it13_b1_plus8 alloc=[72, 72, 48, 40, 24, 24, 24, 24] bytes=328 recall=85.668100

PQ_GREEDY_EVAL tag=it13_b2_plus8 alloc=[72, 64, 56, 40, 24, 24, 24, 24] bytes=328 recall=85.714500

PQ_GREEDY_EVAL tag=it13_b3_plus8 alloc=[72, 64, 48, 48, 24, 24, 24, 24] bytes=328 recall=85.719300

PQ_GREEDY_EVAL tag=it13_b4_plus8 alloc=[72, 64, 48, 40, 32, 24, 24, 24] bytes=328 recall=85.635500

PQ_GREEDY_EVAL tag=it13_b5_plus8 alloc=[72, 64, 48, 40, 24, 32, 24, 24] bytes=328 recall=85.687500

PQ_GREEDY_EVAL tag=it13_b6_plus8 alloc=[72, 64, 48, 40, 24, 24, 32, 24] bytes=328 recall=85.715300

PQ_GREEDY_EVAL tag=it13_b7_plus8 alloc=[72, 64, 48, 40, 24, 24, 24, 32] bytes=328 recall=85.672900

PQ_GREEDY_EVAL tag=it14_b0_plus8 alloc=[80, 64, 48, 48, 24, 24, 24, 24] bytes=336 recall=85.898600

PQ_GREEDY_EVAL tag=it14_b1_plus8 alloc=[72, 72, 48, 48, 24, 24, 24, 24] bytes=336 recall=85.876600

PQ_GREEDY_EVAL tag=it14_b2_plus8 alloc=[72, 64, 56, 48, 24, 24, 24, 24] bytes=336 recall=85.971900

PQ_GREEDY_EVAL tag=it14_b3_plus8 alloc=[72, 64, 48, 56, 24, 24, 24, 24] bytes=336 recall=85.908900

PQ_GREEDY_EVAL tag=it14_b4_plus8 alloc=[72, 64, 48, 48, 32, 24, 24, 24] bytes=336 recall=85.900700

PQ_GREEDY_EVAL tag=it14_b5_plus8 alloc=[72, 64, 48, 48, 24, 32, 24, 24] bytes=336 recall=85.908600

PQ_GREEDY_EVAL tag=it14_b6_plus8 alloc=[72, 64, 48, 48, 24, 24, 32, 24] bytes=336 recall=85.880200

PQ_GREEDY_EVAL tag=it14_b7_plus8 alloc=[72, 64, 48, 48, 24, 24, 24, 32] bytes=336 recall=85.940700

PQ_GREEDY_EVAL tag=it15_b0_plus8 alloc=[80, 64, 56, 48, 24, 24, 24, 24] bytes=344 recall=86.184400

PQ_GREEDY_EVAL tag=it15_b1_plus8 alloc=[72, 72, 56, 48, 24, 24, 24, 24] bytes=344 recall=86.131700

PQ_GREEDY_EVAL tag=it15_b2_plus8 alloc=[72, 64, 64, 48, 24, 24, 24, 24] bytes=344 recall=86.190800

PQ_GREEDY_EVAL tag=it15_b3_plus8 alloc=[72, 64, 56, 56, 24, 24, 24, 24] bytes=344 recall=86.175200

PQ_GREEDY_EVAL tag=it15_b4_plus8 alloc=[72, 64, 56, 48, 32, 24, 24, 24] bytes=344 recall=86.166000

PQ_GREEDY_EVAL tag=it15_b5_plus8 alloc=[72, 64, 56, 48, 24, 32, 24, 24] bytes=344 recall=86.170500

PQ_GREEDY_EVAL tag=it15_b6_plus8 alloc=[72, 64, 56, 48, 24, 24, 32, 24] bytes=344 recall=86.169600

PQ_GREEDY_EVAL tag=it15_b7_plus8 alloc=[72, 64, 56, 48, 24, 24, 24, 32] bytes=344 recall=86.155400

PQ_GREEDY_EVAL tag=it16_b0_plus8 alloc=[80, 64, 64, 48, 24, 24, 24, 24] bytes=352 recall=86.369300

PQ_GREEDY_EVAL tag=it16_b1_plus8 alloc=[72, 72, 64, 48, 24, 24, 24, 24] bytes=352 recall=86.406400

PQ_GREEDY_EVAL tag=it16_b2_plus8 alloc=[72, 64, 72, 48, 24, 24, 24, 24] bytes=352 recall=86.388100

PQ_GREEDY_EVAL tag=it16_b3_plus8 alloc=[72, 64, 64, 56, 24, 24, 24, 24] bytes=352 recall=86.450300

PQ_GREEDY_EVAL tag=it16_b4_plus8 alloc=[72, 64, 64, 48, 32, 24, 24, 24] bytes=352 recall=86.392800

PQ_GREEDY_EVAL tag=it16_b5_plus8 alloc=[72, 64, 64, 48, 24, 32, 24, 24] bytes=352 recall=86.379900

PQ_GREEDY_EVAL tag=it16_b6_plus8 alloc=[72, 64, 64, 48, 24, 24, 32, 24] bytes=352 recall=86.405000

PQ_GREEDY_EVAL tag=it16_b7_plus8 alloc=[72, 64, 64, 48, 24, 24, 24, 32] bytes=352 recall=86.434000

PQ_GREEDY_EVAL tag=it17_b0_plus8 alloc=[80, 64, 64, 56, 24, 24, 24, 24] bytes=360 recall=86.650300

PQ_GREEDY_EVAL tag=it17_b1_plus8 alloc=[72, 72, 64, 56, 24, 24, 24, 24] bytes=360 recall=86.606300

PQ_GREEDY_EVAL tag=it17_b2_plus8 alloc=[72, 64, 72, 56, 24, 24, 24, 24] bytes=360 recall=86.569500

PQ_GREEDY_EVAL tag=it17_b3_plus8 alloc=[72, 64, 64, 64, 24, 24, 24, 24] bytes=360 recall=86.564600

PQ_GREEDY_EVAL tag=it17_b4_plus8 alloc=[72, 64, 64, 56, 32, 24, 24, 24] bytes=360 recall=86.625800

PQ_GREEDY_EVAL tag=it17_b5_plus8 alloc=[72, 64, 64, 56, 24, 32, 24, 24] bytes=360 recall=86.593000

PQ_GREEDY_EVAL tag=it17_b6_plus8 alloc=[72, 64, 64, 56, 24, 24, 32, 24] bytes=360 recall=86.544800

PQ_GREEDY_EVAL tag=it17_b7_plus8 alloc=[72, 64, 64, 56, 24, 24, 24, 32] bytes=360 recall=86.621100

PQ_GREEDY_EVAL tag=it18_b0_plus8 alloc=[88, 64, 64, 56, 24, 24, 24, 24] bytes=368 recall=86.823400

PQ_GREEDY_EVAL tag=it18_b1_plus8 alloc=[80, 72, 64, 56, 24, 24, 24, 24] bytes=368 recall=86.865900

PQ_GREEDY_EVAL tag=it18_b2_plus8 alloc=[80, 64, 72, 56, 24, 24, 24, 24] bytes=368 recall=86.772300

PQ_GREEDY_EVAL tag=it18_b3_plus8 alloc=[80, 64, 64, 64, 24, 24, 24, 24] bytes=368 recall=86.833200

PQ_GREEDY_EVAL tag=it18_b4_plus8 alloc=[80, 64, 64, 56, 32, 24, 24, 24] bytes=368 recall=86.797400

PQ_GREEDY_EVAL tag=it18_b5_plus8 alloc=[80, 64, 64, 56, 24, 32, 24, 24] bytes=368 recall=86.836200

PQ_GREEDY_EVAL tag=it18_b6_plus8 alloc=[80, 64, 64, 56, 24, 24, 32, 24] bytes=368 recall=86.815500

PQ_GREEDY_EVAL tag=it18_b7_plus8 alloc=[80, 64, 64, 56, 24, 24, 24, 32] bytes=368 recall=86.822900

PQ_GREEDY_EVAL tag=it19_b0_plus8 alloc=[88, 72, 64, 56, 24, 24, 24, 24] bytes=376 recall=87.080100

PQ_GREEDY_EVAL tag=it19_b1_plus8 alloc=[80, 80, 64, 56, 24, 24, 24, 24] bytes=376 recall=87.068300

PQ_GREEDY_EVAL tag=it19_b2_plus8 alloc=[80, 72, 72, 56, 24, 24, 24, 24] bytes=376 recall=87.002300

PQ_GREEDY_EVAL tag=it19_b3_plus8 alloc=[80, 72, 64, 64, 24, 24, 24, 24] bytes=376 recall=87.046400

PQ_GREEDY_EVAL tag=it19_b4_plus8 alloc=[80, 72, 64, 56, 32, 24, 24, 24] bytes=376 recall=87.013800

PQ_GREEDY_EVAL tag=it19_b5_plus8 alloc=[80, 72, 64, 56, 24, 32, 24, 24] bytes=376 recall=87.011000

PQ_GREEDY_EVAL tag=it19_b6_plus8 alloc=[80, 72, 64, 56, 24, 24, 32, 24] bytes=376 recall=87.039800

PQ_GREEDY_EVAL tag=it19_b7_plus8 alloc=[80, 72, 64, 56, 24, 24, 24, 32] bytes=376 recall=87.046700

PQ_GREEDY_EVAL tag=it20_b0_plus8 alloc=[96, 72, 64, 56, 24, 24, 24, 24] bytes=384 recall=87.231900

PQ_GREEDY_EVAL tag=it20_b1_plus8 alloc=[88, 80, 64, 56, 24, 24, 24, 24] bytes=384 recall=87.267600

PQ_GREEDY_EVAL tag=it20_b2_plus8 alloc=[88, 72, 72, 56, 24, 24, 24, 24] bytes=384 recall=87.223400

PQ_GREEDY_EVAL tag=it20_b3_plus8 alloc=[88, 72, 64, 64, 24, 24, 24, 24] bytes=384 recall=87.240100

PQ_GREEDY_EVAL tag=it20_b4_plus8 alloc=[88, 72, 64, 56, 32, 24, 24, 24] bytes=384 recall=87.209000

PQ_GREEDY_EVAL tag=it20_b5_plus8 alloc=[88, 72, 64, 56, 24, 32, 24, 24] bytes=384 recall=87.262900

PQ_GREEDY_EVAL tag=it20_b6_plus8 alloc=[88, 72, 64, 56, 24, 24, 32, 24] bytes=384 recall=87.244800

PQ_GREEDY_EVAL tag=it20_b7_plus8 alloc=[88, 72, 64, 56, 24, 24, 24, 32] bytes=384 recall=87.255900


### MSMARCO Cohere
##### Uniform PQ
==================================================
PQ sweep completed!
Results directory: /tmp/pq_sweep_1777931889
==================================================

Summary of recall results:
Bytes,Recall
64,55.2628
96,64.3423
128,69.6057
160,73.0056
192,76.0669
224,78.5006
256,80.9112
288,82.6294
320,84.4576
352,85.7685
384,87.6948

#### Variable PQ
PQ_GREEDY_EVAL tag=init alloc=[8, 8, 8, 8, 8, 8, 8, 8] bytes=64 recall=55.446400

PQ_GREEDY_EVAL tag=it1_b0_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 8] bytes=72 recall=58.355200

PQ_GREEDY_EVAL tag=it1_b1_plus8 alloc=[8, 16, 8, 8, 8, 8, 8, 8] bytes=72 recall=58.299300

PQ_GREEDY_EVAL tag=it1_b2_plus8 alloc=[8, 8, 16, 8, 8, 8, 8, 8] bytes=72 recall=58.061500

PQ_GREEDY_EVAL tag=it1_b3_plus8 alloc=[8, 8, 8, 16, 8, 8, 8, 8] bytes=72 recall=57.948600

PQ_GREEDY_EVAL tag=it1_b4_plus8 alloc=[8, 8, 8, 8, 16, 8, 8, 8] bytes=72 recall=57.915600

PQ_GREEDY_EVAL tag=it1_b5_plus8 alloc=[8, 8, 8, 8, 8, 16, 8, 8] bytes=72 recall=57.411300

PQ_GREEDY_EVAL tag=it1_b6_plus8 alloc=[8, 8, 8, 8, 8, 8, 16, 8] bytes=72 recall=57.461300

PQ_GREEDY_EVAL tag=it1_b7_plus8 alloc=[8, 8, 8, 8, 8, 8, 8, 16] bytes=72 recall=57.233100

PQ_GREEDY_EVAL tag=it2_b0_plus8 alloc=[24, 8, 8, 8, 8, 8, 8, 8] bytes=80 recall=60.069900

PQ_GREEDY_EVAL tag=it2_b1_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 8] bytes=80 recall=60.755700

PQ_GREEDY_EVAL tag=it2_b2_plus8 alloc=[16, 8, 16, 8, 8, 8, 8, 8] bytes=80 recall=60.599400

PQ_GREEDY_EVAL tag=it2_b3_plus8 alloc=[16, 8, 8, 16, 8, 8, 8, 8] bytes=80 recall=60.403600

PQ_GREEDY_EVAL tag=it2_b4_plus8 alloc=[16, 8, 8, 8, 16, 8, 8, 8] bytes=80 recall=60.533700

PQ_GREEDY_EVAL tag=it2_b5_plus8 alloc=[16, 8, 8, 8, 8, 16, 8, 8] bytes=80 recall=60.086000

PQ_GREEDY_EVAL tag=it2_b6_plus8 alloc=[16, 8, 8, 8, 8, 8, 16, 8] bytes=80 recall=60.046000

PQ_GREEDY_EVAL tag=it2_b7_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 16] bytes=80 recall=59.945300

PQ_GREEDY_EVAL tag=it3_b0_plus8 alloc=[24, 16, 8, 8, 8, 8, 8, 8] bytes=88 recall=62.460600

PQ_GREEDY_EVAL tag=it3_b1_plus8 alloc=[16, 24, 8, 8, 8, 8, 8, 8] bytes=88 recall=62.190800

PQ_GREEDY_EVAL tag=it3_b2_plus8 alloc=[16, 16, 16, 8, 8, 8, 8, 8] bytes=88 recall=62.818800

PQ_GREEDY_EVAL tag=it3_b3_plus8 alloc=[16, 16, 8, 16, 8, 8, 8, 8] bytes=88 recall=62.716900

PQ_GREEDY_EVAL tag=it3_b4_plus8 alloc=[16, 16, 8, 8, 16, 8, 8, 8] bytes=88 recall=62.756700

PQ_GREEDY_EVAL tag=it3_b5_plus8 alloc=[16, 16, 8, 8, 8, 16, 8, 8] bytes=88 recall=62.311700

PQ_GREEDY_EVAL tag=it3_b6_plus8 alloc=[16, 16, 8, 8, 8, 8, 16, 8] bytes=88 recall=62.195400

PQ_GREEDY_EVAL tag=it3_b7_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 16] bytes=88 recall=62.223800

PQ_GREEDY_EVAL tag=it4_b0_plus8 alloc=[24, 16, 16, 8, 8, 8, 8, 8] bytes=96 recall=64.417600

PQ_GREEDY_EVAL tag=it4_b1_plus8 alloc=[16, 24, 16, 8, 8, 8, 8, 8] bytes=96 recall=64.244400

PQ_GREEDY_EVAL tag=it4_b2_plus8 alloc=[16, 16, 24, 8, 8, 8, 8, 8] bytes=96 recall=64.338700

PQ_GREEDY_EVAL tag=it4_b3_plus8 alloc=[16, 16, 16, 16, 8, 8, 8, 8] bytes=96 recall=64.555300

PQ_GREEDY_EVAL tag=it4_b4_plus8 alloc=[16, 16, 16, 8, 16, 8, 8, 8] bytes=96 recall=64.666600

PQ_GREEDY_EVAL tag=it4_b5_plus8 alloc=[16, 16, 16, 8, 8, 16, 8, 8] bytes=96 recall=64.342100

PQ_GREEDY_EVAL tag=it4_b6_plus8 alloc=[16, 16, 16, 8, 8, 8, 16, 8] bytes=96 recall=64.252000

PQ_GREEDY_EVAL tag=it4_b7_plus8 alloc=[16, 16, 16, 8, 8, 8, 8, 16] bytes=96 recall=64.144700

PQ_GREEDY_EVAL tag=it5_b0_plus8 alloc=[24, 16, 16, 8, 16, 8, 8, 8] bytes=104 recall=66.082700

PQ_GREEDY_EVAL tag=it5_b1_plus8 alloc=[16, 24, 16, 8, 16, 8, 8, 8] bytes=104 recall=66.065500

PQ_GREEDY_EVAL tag=it5_b2_plus8 alloc=[16, 16, 24, 8, 16, 8, 8, 8] bytes=104 recall=65.919600

PQ_GREEDY_EVAL tag=it5_b3_plus8 alloc=[16, 16, 16, 16, 16, 8, 8, 8] bytes=104 recall=66.328200

PQ_GREEDY_EVAL tag=it5_b4_plus8 alloc=[16, 16, 16, 8, 24, 8, 8, 8] bytes=104 recall=65.892800

PQ_GREEDY_EVAL tag=it5_b5_plus8 alloc=[16, 16, 16, 8, 16, 16, 8, 8] bytes=104 recall=66.036000

PQ_GREEDY_EVAL tag=it5_b6_plus8 alloc=[16, 16, 16, 8, 16, 8, 16, 8] bytes=104 recall=65.843800

PQ_GREEDY_EVAL tag=it5_b7_plus8 alloc=[16, 16, 16, 8, 16, 8, 8, 16] bytes=104 recall=65.935400

PQ_GREEDY_EVAL tag=it6_b0_plus8 alloc=[24, 16, 16, 16, 16, 8, 8, 8] bytes=112 recall=67.523800

PQ_GREEDY_EVAL tag=it6_b1_plus8 alloc=[16, 24, 16, 16, 16, 8, 8, 8] bytes=112 recall=67.559900

PQ_GREEDY_EVAL tag=it6_b2_plus8 alloc=[16, 16, 24, 16, 16, 8, 8, 8] bytes=112 recall=67.517200

PQ_GREEDY_EVAL tag=it6_b3_plus8 alloc=[16, 16, 16, 24, 16, 8, 8, 8] bytes=112 recall=67.376100

PQ_GREEDY_EVAL tag=it6_b4_plus8 alloc=[16, 16, 16, 16, 24, 8, 8, 8] bytes=112 recall=67.358500

PQ_GREEDY_EVAL tag=it6_b5_plus8 alloc=[16, 16, 16, 16, 16, 16, 8, 8] bytes=112 recall=67.482500

PQ_GREEDY_EVAL tag=it6_b6_plus8 alloc=[16, 16, 16, 16, 16, 8, 16, 8] bytes=112 recall=67.437800

PQ_GREEDY_EVAL tag=it6_b7_plus8 alloc=[16, 16, 16, 16, 16, 8, 8, 16] bytes=112 recall=67.515000

PQ_GREEDY_EVAL tag=it7_b0_plus8 alloc=[24, 24, 16, 16, 16, 8, 8, 8] bytes=120 recall=68.804600

PQ_GREEDY_EVAL tag=it7_b1_plus8 alloc=[16, 32, 16, 16, 16, 8, 8, 8] bytes=120 recall=68.547100

PQ_GREEDY_EVAL tag=it7_b2_plus8 alloc=[16, 24, 24, 16, 16, 8, 8, 8] bytes=120 recall=68.773900

PQ_GREEDY_EVAL tag=it7_b3_plus8 alloc=[16, 24, 16, 24, 16, 8, 8, 8] bytes=120 recall=68.509900

PQ_GREEDY_EVAL tag=it7_b4_plus8 alloc=[16, 24, 16, 16, 24, 8, 8, 8] bytes=120 recall=68.598600

PQ_GREEDY_EVAL tag=it7_b5_plus8 alloc=[16, 24, 16, 16, 16, 16, 8, 8] bytes=120 recall=68.757900

PQ_GREEDY_EVAL tag=it7_b6_plus8 alloc=[16, 24, 16, 16, 16, 8, 16, 8] bytes=120 recall=68.515900

PQ_GREEDY_EVAL tag=it7_b7_plus8 alloc=[16, 24, 16, 16, 16, 8, 8, 16] bytes=120 recall=68.599300

PQ_GREEDY_EVAL tag=it8_b0_plus8 alloc=[32, 24, 16, 16, 16, 8, 8, 8] bytes=128 recall=69.794100

PQ_GREEDY_EVAL tag=it8_b1_plus8 alloc=[24, 32, 16, 16, 16, 8, 8, 8] bytes=128 recall=69.737100

PQ_GREEDY_EVAL tag=it8_b2_plus8 alloc=[24, 24, 24, 16, 16, 8, 8, 8] bytes=128 recall=69.823400

PQ_GREEDY_EVAL tag=it8_b3_plus8 alloc=[24, 24, 16, 24, 16, 8, 8, 8] bytes=128 recall=69.810200

PQ_GREEDY_EVAL tag=it8_b4_plus8 alloc=[24, 24, 16, 16, 24, 8, 8, 8] bytes=128 recall=69.807200

PQ_GREEDY_EVAL tag=it8_b5_plus8 alloc=[24, 24, 16, 16, 16, 16, 8, 8] bytes=128 recall=70.009600

PQ_GREEDY_EVAL tag=it8_b6_plus8 alloc=[24, 24, 16, 16, 16, 8, 16, 8] bytes=128 recall=69.715000

PQ_GREEDY_EVAL tag=it8_b7_plus8 alloc=[24, 24, 16, 16, 16, 8, 8, 16] bytes=128 recall=69.827400

PQ_GREEDY_EVAL tag=it9_b0_plus8 alloc=[32, 24, 16, 16, 16, 16, 8, 8] bytes=136 recall=70.775800

PQ_GREEDY_EVAL tag=it9_b1_plus8 alloc=[24, 32, 16, 16, 16, 16, 8, 8] bytes=136 recall=70.746300

PQ_GREEDY_EVAL tag=it9_b2_plus8 alloc=[24, 24, 24, 16, 16, 16, 8, 8] bytes=136 recall=70.913800

PQ_GREEDY_EVAL tag=it9_b3_plus8 alloc=[24, 24, 16, 24, 16, 16, 8, 8] bytes=136 recall=70.766600

PQ_GREEDY_EVAL tag=it9_b4_plus8 alloc=[24, 24, 16, 16, 24, 16, 8, 8] bytes=136 recall=70.820100

PQ_GREEDY_EVAL tag=it9_b5_plus8 alloc=[24, 24, 16, 16, 16, 24, 8, 8] bytes=136 recall=70.687000

PQ_GREEDY_EVAL tag=it9_b6_plus8 alloc=[24, 24, 16, 16, 16, 16, 16, 8] bytes=136 recall=70.799300

PQ_GREEDY_EVAL tag=it9_b7_plus8 alloc=[24, 24, 16, 16, 16, 16, 8, 16] bytes=136 recall=70.830400

PQ_GREEDY_EVAL tag=it10_b0_plus8 alloc=[32, 24, 24, 16, 16, 16, 8, 8] bytes=144 recall=71.784500

PQ_GREEDY_EVAL tag=it10_b1_plus8 alloc=[24, 32, 24, 16, 16, 16, 8, 8] bytes=144 recall=71.831400

PQ_GREEDY_EVAL tag=it10_b2_plus8 alloc=[24, 24, 32, 16, 16, 16, 8, 8] bytes=144 recall=71.858000

PQ_GREEDY_EVAL tag=it10_b3_plus8 alloc=[24, 24, 24, 24, 16, 16, 8, 8] bytes=144 recall=71.832700

PQ_GREEDY_EVAL tag=it10_b4_plus8 alloc=[24, 24, 24, 16, 24, 16, 8, 8] bytes=144 recall=71.794000

PQ_GREEDY_EVAL tag=it10_b5_plus8 alloc=[24, 24, 24, 16, 16, 24, 8, 8] bytes=144 recall=71.685000

PQ_GREEDY_EVAL tag=it10_b6_plus8 alloc=[24, 24, 24, 16, 16, 16, 16, 8] bytes=144 recall=71.833500

PQ_GREEDY_EVAL tag=it10_b7_plus8 alloc=[24, 24, 24, 16, 16, 16, 8, 16] bytes=144 recall=71.781800

PQ_GREEDY_EVAL tag=it11_b0_plus8 alloc=[32, 24, 32, 16, 16, 16, 8, 8] bytes=152 recall=72.615800

PQ_GREEDY_EVAL tag=it11_b1_plus8 alloc=[24, 32, 32, 16, 16, 16, 8, 8] bytes=152 recall=72.613200

PQ_GREEDY_EVAL tag=it11_b2_plus8 alloc=[24, 24, 40, 16, 16, 16, 8, 8] bytes=152 recall=72.350100

PQ_GREEDY_EVAL tag=it11_b3_plus8 alloc=[24, 24, 32, 24, 16, 16, 8, 8] bytes=152 recall=72.640100

PQ_GREEDY_EVAL tag=it11_b4_plus8 alloc=[24, 24, 32, 16, 24, 16, 8, 8] bytes=152 recall=72.622900

PQ_GREEDY_EVAL tag=it11_b5_plus8 alloc=[24, 24, 32, 16, 16, 24, 8, 8] bytes=152 recall=72.494600

PQ_GREEDY_EVAL tag=it11_b6_plus8 alloc=[24, 24, 32, 16, 16, 16, 16, 8] bytes=152 recall=72.574100

PQ_GREEDY_EVAL tag=it11_b7_plus8 alloc=[24, 24, 32, 16, 16, 16, 8, 16] bytes=152 recall=72.647100

PQ_GREEDY_EVAL tag=it12_b0_plus8 alloc=[32, 24, 32, 16, 16, 16, 8, 16] bytes=160 recall=73.465800

PQ_GREEDY_EVAL tag=it12_b1_plus8 alloc=[24, 32, 32, 16, 16, 16, 8, 16] bytes=160 recall=73.478200

PQ_GREEDY_EVAL tag=it12_b2_plus8 alloc=[24, 24, 40, 16, 16, 16, 8, 16] bytes=160 recall=73.167300

PQ_GREEDY_EVAL tag=it12_b3_plus8 alloc=[24, 24, 32, 24, 16, 16, 8, 16] bytes=160 recall=73.484100

PQ_GREEDY_EVAL tag=it12_b4_plus8 alloc=[24, 24, 32, 16, 24, 16, 8, 16] bytes=160 recall=73.512600

PQ_GREEDY_EVAL tag=it12_b5_plus8 alloc=[24, 24, 32, 16, 16, 24, 8, 16] bytes=160 recall=73.325500

PQ_GREEDY_EVAL tag=it12_b6_plus8 alloc=[24, 24, 32, 16, 16, 16, 16, 16] bytes=160 recall=73.458500

PQ_GREEDY_EVAL tag=it12_b7_plus8 alloc=[24, 24, 32, 16, 16, 16, 8, 24] bytes=160 recall=73.196800

PQ_GREEDY_EVAL tag=it13_b0_plus8 alloc=[32, 24, 32, 16, 24, 16, 8, 16] bytes=168 recall=74.340500

PQ_GREEDY_EVAL tag=it13_b1_plus8 alloc=[24, 32, 32, 16, 24, 16, 8, 16] bytes=168 recall=74.274400

PQ_GREEDY_EVAL tag=it13_b2_plus8 alloc=[24, 24, 40, 16, 24, 16, 8, 16] bytes=168 recall=74.044400

PQ_GREEDY_EVAL tag=it13_b3_plus8 alloc=[24, 24, 32, 24, 24, 16, 8, 16] bytes=168 recall=74.258600

PQ_GREEDY_EVAL tag=it13_b4_plus8 alloc=[24, 24, 32, 16, 32, 16, 8, 16] bytes=168 recall=74.144600

PQ_GREEDY_EVAL tag=it13_b5_plus8 alloc=[24, 24, 32, 16, 24, 24, 8, 16] bytes=168 recall=74.129100

PQ_GREEDY_EVAL tag=it13_b6_plus8 alloc=[24, 24, 32, 16, 24, 16, 16, 16] bytes=168 recall=74.220500

PQ_GREEDY_EVAL tag=it13_b7_plus8 alloc=[24, 24, 32, 16, 24, 16, 8, 24] bytes=168 recall=74.059900

PQ_GREEDY_EVAL tag=it14_b0_plus8 alloc=[40, 24, 32, 16, 24, 16, 8, 16] bytes=176 recall=74.961200

PQ_GREEDY_EVAL tag=it14_b1_plus8 alloc=[32, 32, 32, 16, 24, 16, 8, 16] bytes=176 recall=75.158000

PQ_GREEDY_EVAL tag=it14_b2_plus8 alloc=[32, 24, 40, 16, 24, 16, 8, 16] bytes=176 recall=74.906300

PQ_GREEDY_EVAL tag=it14_b3_plus8 alloc=[32, 24, 32, 24, 24, 16, 8, 16] bytes=176 recall=75.188100

PQ_GREEDY_EVAL tag=it14_b4_plus8 alloc=[32, 24, 32, 16, 32, 16, 8, 16] bytes=176 recall=75.085100

PQ_GREEDY_EVAL tag=it14_b5_plus8 alloc=[32, 24, 32, 16, 24, 24, 8, 16] bytes=176 recall=74.985400

PQ_GREEDY_EVAL tag=it14_b6_plus8 alloc=[32, 24, 32, 16, 24, 16, 16, 16] bytes=176 recall=75.060000

PQ_GREEDY_EVAL tag=it14_b7_plus8 alloc=[32, 24, 32, 16, 24, 16, 8, 24] bytes=176 recall=74.843800

PQ_GREEDY_EVAL tag=it15_b0_plus8 alloc=[40, 24, 32, 24, 24, 16, 8, 16] bytes=184 recall=75.735500

PQ_GREEDY_EVAL tag=it15_b1_plus8 alloc=[32, 32, 32, 24, 24, 16, 8, 16] bytes=184 recall=75.893300

PQ_GREEDY_EVAL tag=it15_b2_plus8 alloc=[32, 24, 40, 24, 24, 16, 8, 16] bytes=184 recall=75.683100

PQ_GREEDY_EVAL tag=it15_b3_plus8 alloc=[32, 24, 32, 32, 24, 16, 8, 16] bytes=184 recall=75.764000

PQ_GREEDY_EVAL tag=it15_b4_plus8 alloc=[32, 24, 32, 24, 32, 16, 8, 16] bytes=184 recall=75.866000

PQ_GREEDY_EVAL tag=it15_b5_plus8 alloc=[32, 24, 32, 24, 24, 24, 8, 16] bytes=184 recall=75.728800

PQ_GREEDY_EVAL tag=it15_b6_plus8 alloc=[32, 24, 32, 24, 24, 16, 16, 16] bytes=184 recall=75.747300

PQ_GREEDY_EVAL tag=it15_b7_plus8 alloc=[32, 24, 32, 24, 24, 16, 8, 24] bytes=184 recall=75.639400

PQ_GREEDY_EVAL tag=it16_b0_plus8 alloc=[40, 32, 32, 24, 24, 16, 8, 16] bytes=192 recall=76.580100

PQ_GREEDY_EVAL tag=it16_b1_plus8 alloc=[32, 40, 32, 24, 24, 16, 8, 16] bytes=192 recall=76.395700

PQ_GREEDY_EVAL tag=it16_b2_plus8 alloc=[32, 32, 40, 24, 24, 16, 8, 16] bytes=192 recall=76.382400

PQ_GREEDY_EVAL tag=it16_b3_plus8 alloc=[32, 32, 32, 32, 24, 16, 8, 16] bytes=192 recall=76.564800

PQ_GREEDY_EVAL tag=it16_b4_plus8 alloc=[32, 32, 32, 24, 32, 16, 8, 16] bytes=192 recall=76.516600

PQ_GREEDY_EVAL tag=it16_b5_plus8 alloc=[32, 32, 32, 24, 24, 24, 8, 16] bytes=192 recall=76.562300

PQ_GREEDY_EVAL tag=it16_b6_plus8 alloc=[32, 32, 32, 24, 24, 16, 16, 16] bytes=192 recall=76.538100

PQ_GREEDY_EVAL tag=it16_b7_plus8 alloc=[32, 32, 32, 24, 24, 16, 8, 24] bytes=192 recall=76.400400

PQ_GREEDY_EVAL tag=it17_b0_plus8 alloc=[48, 32, 32, 24, 24, 16, 8, 16] bytes=200 recall=77.076400

PQ_GREEDY_EVAL tag=it17_b1_plus8 alloc=[40, 40, 32, 24, 24, 16, 8, 16] bytes=200 recall=77.123800

PQ_GREEDY_EVAL tag=it17_b2_plus8 alloc=[40, 32, 40, 24, 24, 16, 8, 16] bytes=200 recall=77.167600

PQ_GREEDY_EVAL tag=it17_b3_plus8 alloc=[40, 32, 32, 32, 24, 16, 8, 16] bytes=200 recall=77.186100

PQ_GREEDY_EVAL tag=it17_b4_plus8 alloc=[40, 32, 32, 24, 32, 16, 8, 16] bytes=200 recall=77.253700

PQ_GREEDY_EVAL tag=it17_b5_plus8 alloc=[40, 32, 32, 24, 24, 24, 8, 16] bytes=200 recall=77.140100

PQ_GREEDY_EVAL tag=it17_b6_plus8 alloc=[40, 32, 32, 24, 24, 16, 16, 16] bytes=200 recall=77.288300

PQ_GREEDY_EVAL tag=it17_b7_plus8 alloc=[40, 32, 32, 24, 24, 16, 8, 24] bytes=200 recall=77.046100

PQ_GREEDY_EVAL tag=it18_b0_plus8 alloc=[48, 32, 32, 24, 24, 16, 16, 16] bytes=208 recall=77.729900

PQ_GREEDY_EVAL tag=it18_b1_plus8 alloc=[40, 40, 32, 24, 24, 16, 16, 16] bytes=208 recall=77.788300

PQ_GREEDY_EVAL tag=it18_b2_plus8 alloc=[40, 32, 40, 24, 24, 16, 16, 16] bytes=208 recall=77.771600

PQ_GREEDY_EVAL tag=it18_b3_plus8 alloc=[40, 32, 32, 32, 24, 16, 16, 16] bytes=208 recall=77.827800

PQ_GREEDY_EVAL tag=it18_b4_plus8 alloc=[40, 32, 32, 24, 32, 16, 16, 16] bytes=208 recall=77.887800

PQ_GREEDY_EVAL tag=it18_b5_plus8 alloc=[40, 32, 32, 24, 24, 24, 16, 16] bytes=208 recall=77.796400

PQ_GREEDY_EVAL tag=it18_b6_plus8 alloc=[40, 32, 32, 24, 24, 16, 24, 16] bytes=208 recall=77.826400

PQ_GREEDY_EVAL tag=it18_b7_plus8 alloc=[40, 32, 32, 24, 24, 16, 16, 24] bytes=208 recall=77.708600

PQ_GREEDY_EVAL tag=it19_b0_plus8 alloc=[48, 32, 32, 24, 32, 16, 16, 16] bytes=216 recall=78.347400

PQ_GREEDY_EVAL tag=it19_b1_plus8 alloc=[40, 40, 32, 24, 32, 16, 16, 16] bytes=216 recall=78.384100

PQ_GREEDY_EVAL tag=it19_b2_plus8 alloc=[40, 32, 40, 24, 32, 16, 16, 16] bytes=216 recall=78.413500

PQ_GREEDY_EVAL tag=it19_b3_plus8 alloc=[40, 32, 32, 32, 32, 16, 16, 16] bytes=216 recall=78.493800

PQ_GREEDY_EVAL tag=it19_b4_plus8 alloc=[40, 32, 32, 24, 40, 16, 16, 16] bytes=216 recall=78.391000

PQ_GREEDY_EVAL tag=it19_b5_plus8 alloc=[40, 32, 32, 24, 32, 24, 16, 16] bytes=216 recall=78.484700

PQ_GREEDY_EVAL tag=it19_b6_plus8 alloc=[40, 32, 32, 24, 32, 16, 24, 16] bytes=216 recall=78.468800

PQ_GREEDY_EVAL tag=it19_b7_plus8 alloc=[40, 32, 32, 24, 32, 16, 16, 24] bytes=216 recall=78.426900

PQ_GREEDY_EVAL tag=it20_b0_plus8 alloc=[48, 32, 32, 32, 32, 16, 16, 16] bytes=224 recall=78.944800

PQ_GREEDY_EVAL tag=it20_b1_plus8 alloc=[40, 40, 32, 32, 32, 16, 16, 16] bytes=224 recall=79.048700

PQ_GREEDY_EVAL tag=it20_b2_plus8 alloc=[40, 32, 40, 32, 32, 16, 16, 16] bytes=224 recall=79.029400

PQ_GREEDY_EVAL tag=it20_b3_plus8 alloc=[40, 32, 32, 40, 32, 16, 16, 16] bytes=224 recall=78.931200

PQ_GREEDY_EVAL tag=it20_b4_plus8 alloc=[40, 32, 32, 32, 40, 16, 16, 16] bytes=224 recall=78.960900

PQ_GREEDY_EVAL tag=it20_b5_plus8 alloc=[40, 32, 32, 32, 32, 24, 16, 16] bytes=224 recall=79.126100

PQ_GREEDY_EVAL tag=it20_b6_plus8 alloc=[40, 32, 32, 32, 32, 16, 24, 16] bytes=224 recall=78.961200

PQ_GREEDY_EVAL tag=it20_b7_plus8 alloc=[40, 32, 32, 32, 32, 16, 16, 24] bytes=224 recall=79.010300

PQ_GREEDY_EVAL tag=it21_b0_plus8 alloc=[48, 32, 32, 32, 32, 24, 16, 16] bytes=232 recall=79.487500

PQ_GREEDY_EVAL tag=it21_b1_plus8 alloc=[40, 40, 32, 32, 32, 24, 16, 16] bytes=232 recall=79.570200

PQ_GREEDY_EVAL tag=it21_b2_plus8 alloc=[40, 32, 40, 32, 32, 24, 16, 16] bytes=232 recall=79.548000

PQ_GREEDY_EVAL tag=it21_b3_plus8 alloc=[40, 32, 32, 40, 32, 24, 16, 16] bytes=232 recall=79.492600

PQ_GREEDY_EVAL tag=it21_b4_plus8 alloc=[40, 32, 32, 32, 40, 24, 16, 16] bytes=232 recall=79.614900

PQ_GREEDY_EVAL tag=it21_b5_plus8 alloc=[40, 32, 32, 32, 32, 32, 16, 16] bytes=232 recall=79.626500

PQ_GREEDY_EVAL tag=it21_b6_plus8 alloc=[40, 32, 32, 32, 32, 24, 24, 16] bytes=232 recall=79.590000

PQ_GREEDY_EVAL tag=it21_b7_plus8 alloc=[40, 32, 32, 32, 32, 24, 16, 24] bytes=232 recall=79.640000

PQ_GREEDY_EVAL tag=it22_b0_plus8 alloc=[48, 32, 32, 32, 32, 24, 16, 24] bytes=240 recall=79.946800

PQ_GREEDY_EVAL tag=it22_b1_plus8 alloc=[40, 40, 32, 32, 32, 24, 16, 24] bytes=240 recall=80.116000

PQ_GREEDY_EVAL tag=it22_b2_plus8 alloc=[40, 32, 40, 32, 32, 24, 16, 24] bytes=240 recall=80.126800

PQ_GREEDY_EVAL tag=it22_b3_plus8 alloc=[40, 32, 32, 40, 32, 24, 16, 24] bytes=240 recall=80.049400

PQ_GREEDY_EVAL tag=it22_b4_plus8 alloc=[40, 32, 32, 32, 40, 24, 16, 24] bytes=240 recall=80.028500

PQ_GREEDY_EVAL tag=it22_b5_plus8 alloc=[40, 32, 32, 32, 32, 32, 16, 24] bytes=240 recall=80.085200

PQ_GREEDY_EVAL tag=it22_b6_plus8 alloc=[40, 32, 32, 32, 32, 24, 24, 24] bytes=240 recall=80.060000

PQ_GREEDY_EVAL tag=it22_b7_plus8 alloc=[40, 32, 32, 32, 32, 24, 16, 32] bytes=240 recall=79.981400

PQ_GREEDY_EVAL tag=it23_b0_plus8 alloc=[48, 32, 40, 32, 32, 24, 16, 24] bytes=248 recall=80.521100

PQ_GREEDY_EVAL tag=it23_b1_plus8 alloc=[40, 40, 40, 32, 32, 24, 16, 24] bytes=248 recall=80.648100

PQ_GREEDY_EVAL tag=it23_b2_plus8 alloc=[40, 32, 48, 32, 32, 24, 16, 24] bytes=248 recall=80.484700

PQ_GREEDY_EVAL tag=it23_b3_plus8 alloc=[40, 32, 40, 40, 32, 24, 16, 24] bytes=248 recall=80.529400

PQ_GREEDY_EVAL tag=it23_b4_plus8 alloc=[40, 32, 40, 32, 40, 24, 16, 24] bytes=248 recall=80.631500

PQ_GREEDY_EVAL tag=it23_b5_plus8 alloc=[40, 32, 40, 32, 32, 32, 16, 24] bytes=248 recall=80.663600

PQ_GREEDY_EVAL tag=it23_b6_plus8 alloc=[40, 32, 40, 32, 32, 24, 24, 24] bytes=248 recall=80.621900

PQ_GREEDY_EVAL tag=it23_b7_plus8 alloc=[40, 32, 40, 32, 32, 24, 16, 32] bytes=248 recall=80.543300

PQ_GREEDY_EVAL tag=it24_b0_plus8 alloc=[48, 32, 40, 32, 32, 32, 16, 24] bytes=256 recall=81.058900

PQ_GREEDY_EVAL tag=it24_b1_plus8 alloc=[40, 40, 40, 32, 32, 32, 16, 24] bytes=256 recall=81.154700

PQ_GREEDY_EVAL tag=it24_b2_plus8 alloc=[40, 32, 48, 32, 32, 32, 16, 24] bytes=256 recall=81.056600

PQ_GREEDY_EVAL tag=it24_b3_plus8 alloc=[40, 32, 40, 40, 32, 32, 16, 24] bytes=256 recall=81.068300

PQ_GREEDY_EVAL tag=it24_b4_plus8 alloc=[40, 32, 40, 32, 40, 32, 16, 24] bytes=256 recall=81.133500

PQ_GREEDY_EVAL tag=it24_b5_plus8 alloc=[40, 32, 40, 32, 32, 40, 16, 24] bytes=256 recall=81.017200

PQ_GREEDY_EVAL tag=it24_b6_plus8 alloc=[40, 32, 40, 32, 32, 32, 24, 24] bytes=256 recall=81.137200

PQ_GREEDY_EVAL tag=it24_b7_plus8 alloc=[40, 32, 40, 32, 32, 32, 16, 32] bytes=256 recall=81.082800

PQ_GREEDY_EVAL tag=it25_b0_plus8 alloc=[48, 40, 40, 32, 32, 32, 16, 24] bytes=264 recall=81.587800

PQ_GREEDY_EVAL tag=it25_b1_plus8 alloc=[40, 48, 40, 32, 32, 32, 16, 24] bytes=264 recall=81.625400

PQ_GREEDY_EVAL tag=it25_b2_plus8 alloc=[40, 40, 48, 32, 32, 32, 16, 24] bytes=264 recall=81.594000

PQ_GREEDY_EVAL tag=it25_b3_plus8 alloc=[40, 40, 40, 40, 32, 32, 16, 24] bytes=264 recall=81.624100

PQ_GREEDY_EVAL tag=it25_b4_plus8 alloc=[40, 40, 40, 32, 40, 32, 16, 24] bytes=264 recall=81.611700

PQ_GREEDY_EVAL tag=it25_b5_plus8 alloc=[40, 40, 40, 32, 32, 40, 16, 24] bytes=264 recall=81.577400

PQ_GREEDY_EVAL tag=it25_b6_plus8 alloc=[40, 40, 40, 32, 32, 32, 24, 24] bytes=264 recall=81.680500

PQ_GREEDY_EVAL tag=it25_b7_plus8 alloc=[40, 40, 40, 32, 32, 32, 16, 32] bytes=264 recall=81.615000

PQ_GREEDY_EVAL tag=it26_b0_plus8 alloc=[48, 40, 40, 32, 32, 32, 24, 24] bytes=272 recall=82.131200

PQ_GREEDY_EVAL tag=it26_b1_plus8 alloc=[40, 48, 40, 32, 32, 32, 24, 24] bytes=272 recall=82.107000

PQ_GREEDY_EVAL tag=it26_b2_plus8 alloc=[40, 40, 48, 32, 32, 32, 24, 24] bytes=272 recall=82.116500

PQ_GREEDY_EVAL tag=it26_b3_plus8 alloc=[40, 40, 40, 40, 32, 32, 24, 24] bytes=272 recall=82.111300

PQ_GREEDY_EVAL tag=it26_b4_plus8 alloc=[40, 40, 40, 32, 40, 32, 24, 24] bytes=272 recall=82.139400

PQ_GREEDY_EVAL tag=it26_b5_plus8 alloc=[40, 40, 40, 32, 32, 40, 24, 24] bytes=272 recall=82.066000

PQ_GREEDY_EVAL tag=it26_b6_plus8 alloc=[40, 40, 40, 32, 32, 32, 32, 24] bytes=272 recall=82.067000

PQ_GREEDY_EVAL tag=it26_b7_plus8 alloc=[40, 40, 40, 32, 32, 32, 24, 32] bytes=272 recall=82.099600

PQ_GREEDY_EVAL tag=it27_b0_plus8 alloc=[48, 40, 40, 32, 40, 32, 24, 24] bytes=280 recall=82.606300

PQ_GREEDY_EVAL tag=it27_b1_plus8 alloc=[40, 48, 40, 32, 40, 32, 24, 24] bytes=280 recall=82.588800

PQ_GREEDY_EVAL tag=it27_b2_plus8 alloc=[40, 40, 48, 32, 40, 32, 24, 24] bytes=280 recall=82.652300

PQ_GREEDY_EVAL tag=it27_b3_plus8 alloc=[40, 40, 40, 40, 40, 32, 24, 24] bytes=280 recall=82.645800

PQ_GREEDY_EVAL tag=it27_b4_plus8 alloc=[40, 40, 40, 32, 48, 32, 24, 24] bytes=280 recall=82.520900

PQ_GREEDY_EVAL tag=it27_b5_plus8 alloc=[40, 40, 40, 32, 40, 40, 24, 24] bytes=280 recall=82.570900

PQ_GREEDY_EVAL tag=it27_b6_plus8 alloc=[40, 40, 40, 32, 40, 32, 32, 24] bytes=280 recall=82.618600

PQ_GREEDY_EVAL tag=it27_b7_plus8 alloc=[40, 40, 40, 32, 40, 32, 24, 32] bytes=280 recall=82.593400

PQ_GREEDY_EVAL tag=it28_b0_plus8 alloc=[48, 40, 48, 32, 40, 32, 24, 24] bytes=288 recall=83.089100

PQ_GREEDY_EVAL tag=it28_b1_plus8 alloc=[40, 48, 48, 32, 40, 32, 24, 24] bytes=288 recall=83.048300

PQ_GREEDY_EVAL tag=it28_b2_plus8 alloc=[40, 40, 56, 32, 40, 32, 24, 24] bytes=288 recall=82.865500

PQ_GREEDY_EVAL tag=it28_b3_plus8 alloc=[40, 40, 48, 40, 40, 32, 24, 24] bytes=288 recall=83.068500

PQ_GREEDY_EVAL tag=it28_b4_plus8 alloc=[40, 40, 48, 32, 48, 32, 24, 24] bytes=288 recall=83.004700

PQ_GREEDY_EVAL tag=it28_b5_plus8 alloc=[40, 40, 48, 32, 40, 40, 24, 24] bytes=288 recall=82.974500

PQ_GREEDY_EVAL tag=it28_b6_plus8 alloc=[40, 40, 48, 32, 40, 32, 32, 24] bytes=288 recall=83.050900

PQ_GREEDY_EVAL tag=it28_b7_plus8 alloc=[40, 40, 48, 32, 40, 32, 24, 32] bytes=288 recall=83.015600

PQ_GREEDY_EVAL tag=it29_b0_plus8 alloc=[56, 40, 48, 32, 40, 32, 24, 24] bytes=296 recall=83.307700

PQ_GREEDY_EVAL tag=it29_b1_plus8 alloc=[48, 48, 48, 32, 40, 32, 24, 24] bytes=296 recall=83.482800

PQ_GREEDY_EVAL tag=it29_b2_plus8 alloc=[48, 40, 56, 32, 40, 32, 24, 24] bytes=296 recall=83.281700

PQ_GREEDY_EVAL tag=it29_b3_plus8 alloc=[48, 40, 48, 40, 40, 32, 24, 24] bytes=296 recall=83.515900

PQ_GREEDY_EVAL tag=it29_b4_plus8 alloc=[48, 40, 48, 32, 48, 32, 24, 24] bytes=296 recall=83.503000

PQ_GREEDY_EVAL tag=it29_b5_plus8 alloc=[48, 40, 48, 32, 40, 40, 24, 24] bytes=296 recall=83.433800

PQ_GREEDY_EVAL tag=it29_b6_plus8 alloc=[48, 40, 48, 32, 40, 32, 32, 24] bytes=296 recall=83.473100

PQ_GREEDY_EVAL tag=it29_b7_plus8 alloc=[48, 40, 48, 32, 40, 32, 24, 32] bytes=296 recall=83.491400

PQ_GREEDY_EVAL tag=it30_b0_plus8 alloc=[56, 40, 48, 40, 40, 32, 24, 24] bytes=304 recall=83.762800

PQ_GREEDY_EVAL tag=it30_b1_plus8 alloc=[48, 48, 48, 40, 40, 32, 24, 24] bytes=304 recall=83.983000

PQ_GREEDY_EVAL tag=it30_b2_plus8 alloc=[48, 40, 56, 40, 40, 32, 24, 24] bytes=304 recall=83.829100

PQ_GREEDY_EVAL tag=it30_b3_plus8 alloc=[48, 40, 48, 48, 40, 32, 24, 24] bytes=304 recall=83.976400

PQ_GREEDY_EVAL tag=it30_b4_plus8 alloc=[48, 40, 48, 40, 48, 32, 24, 24] bytes=304 recall=83.916300

PQ_GREEDY_EVAL tag=it30_b5_plus8 alloc=[48, 40, 48, 40, 40, 40, 24, 24] bytes=304 recall=83.884700

PQ_GREEDY_EVAL tag=it30_b6_plus8 alloc=[48, 40, 48, 40, 40, 32, 32, 24] bytes=304 recall=84.002000

PQ_GREEDY_EVAL tag=it30_b7_plus8 alloc=[48, 40, 48, 40, 40, 32, 24, 32] bytes=304 recall=83.994100

PQ_GREEDY_EVAL tag=it31_b0_plus8 alloc=[56, 40, 48, 40, 40, 32, 32, 24] bytes=312 recall=84.236100

PQ_GREEDY_EVAL tag=it31_b1_plus8 alloc=[48, 48, 48, 40, 40, 32, 32, 24] bytes=312 recall=84.449300

PQ_GREEDY_EVAL tag=it31_b2_plus8 alloc=[48, 40, 56, 40, 40, 32, 32, 24] bytes=312 recall=84.178100

PQ_GREEDY_EVAL tag=it31_b3_plus8 alloc=[48, 40, 48, 48, 40, 32, 32, 24] bytes=312 recall=84.372800

PQ_GREEDY_EVAL tag=it31_b4_plus8 alloc=[48, 40, 48, 40, 48, 32, 32, 24] bytes=312 recall=84.402600

PQ_GREEDY_EVAL tag=it31_b5_plus8 alloc=[48, 40, 48, 40, 40, 40, 32, 24] bytes=312 recall=84.345300

PQ_GREEDY_EVAL tag=it31_b6_plus8 alloc=[48, 40, 48, 40, 40, 32, 40, 24] bytes=312 recall=84.349100

PQ_GREEDY_EVAL tag=it31_b7_plus8 alloc=[48, 40, 48, 40, 40, 32, 32, 32] bytes=312 recall=84.437500

PQ_GREEDY_EVAL tag=it32_b0_plus8 alloc=[56, 48, 48, 40, 40, 32, 32, 24] bytes=320 recall=84.757900

PQ_GREEDY_EVAL tag=it32_b1_plus8 alloc=[48, 56, 48, 40, 40, 32, 32, 24] bytes=320 recall=84.672300

PQ_GREEDY_EVAL tag=it32_b2_plus8 alloc=[48, 48, 56, 40, 40, 32, 32, 24] bytes=320 recall=84.691000

PQ_GREEDY_EVAL tag=it32_b3_plus8 alloc=[48, 48, 48, 48, 40, 32, 32, 24] bytes=320 recall=84.830700

PQ_GREEDY_EVAL tag=it32_b4_plus8 alloc=[48, 48, 48, 40, 48, 32, 32, 24] bytes=320 recall=84.875500

PQ_GREEDY_EVAL tag=it32_b5_plus8 alloc=[48, 48, 48, 40, 40, 40, 32, 24] bytes=320 recall=84.799900

PQ_GREEDY_EVAL tag=it32_b6_plus8 alloc=[48, 48, 48, 40, 40, 32, 40, 24] bytes=320 recall=84.769300

PQ_GREEDY_EVAL tag=it32_b7_plus8 alloc=[48, 48, 48, 40, 40, 32, 32, 32] bytes=320 recall=84.928400

PQ_GREEDY_EVAL tag=it33_b0_plus8 alloc=[56, 48, 48, 40, 40, 32, 32, 32] bytes=328 recall=85.152400

PQ_GREEDY_EVAL tag=it33_b1_plus8 alloc=[48, 56, 48, 40, 40, 32, 32, 32] bytes=328 recall=85.162600

PQ_GREEDY_EVAL tag=it33_b2_plus8 alloc=[48, 48, 56, 40, 40, 32, 32, 32] bytes=328 recall=85.079100

PQ_GREEDY_EVAL tag=it33_b3_plus8 alloc=[48, 48, 48, 48, 40, 32, 32, 32] bytes=328 recall=85.238100

PQ_GREEDY_EVAL tag=it33_b4_plus8 alloc=[48, 48, 48, 40, 48, 32, 32, 32] bytes=328 recall=85.261900

PQ_GREEDY_EVAL tag=it33_b5_plus8 alloc=[48, 48, 48, 40, 40, 40, 32, 32] bytes=328 recall=85.255200

PQ_GREEDY_EVAL tag=it33_b6_plus8 alloc=[48, 48, 48, 40, 40, 32, 40, 32] bytes=328 recall=85.259900

PQ_GREEDY_EVAL tag=it33_b7_plus8 alloc=[48, 48, 48, 40, 40, 32, 32, 40] bytes=328 recall=85.232800

PQ_GREEDY_EVAL tag=it34_b0_plus8 alloc=[56, 48, 48, 40, 48, 32, 32, 32] bytes=336 recall=85.618600

PQ_GREEDY_EVAL tag=it34_b1_plus8 alloc=[48, 56, 48, 40, 48, 32, 32, 32] bytes=336 recall=85.485000

PQ_GREEDY_EVAL tag=it34_b2_plus8 alloc=[48, 48, 56, 40, 48, 32, 32, 32] bytes=336 recall=85.508300

PQ_GREEDY_EVAL tag=it34_b3_plus8 alloc=[48, 48, 48, 48, 48, 32, 32, 32] bytes=336 recall=85.672300

PQ_GREEDY_EVAL tag=it34_b4_plus8 alloc=[48, 48, 48, 40, 56, 32, 32, 32] bytes=336 recall=85.536400

PQ_GREEDY_EVAL tag=it34_b5_plus8 alloc=[48, 48, 48, 40, 48, 40, 32, 32] bytes=336 recall=85.648400

PQ_GREEDY_EVAL tag=it34_b6_plus8 alloc=[48, 48, 48, 40, 48, 32, 40, 32] bytes=336 recall=85.604600

PQ_GREEDY_EVAL tag=it34_b7_plus8 alloc=[48, 48, 48, 40, 48, 32, 32, 40] bytes=336 recall=85.587700

PQ_GREEDY_EVAL tag=it35_b0_plus8 alloc=[56, 48, 48, 48, 48, 32, 32, 32] bytes=344 recall=85.925400

PQ_GREEDY_EVAL tag=it35_b1_plus8 alloc=[48, 56, 48, 48, 48, 32, 32, 32] bytes=344 recall=85.907900

PQ_GREEDY_EVAL tag=it35_b2_plus8 alloc=[48, 48, 56, 48, 48, 32, 32, 32] bytes=344 recall=85.939700

PQ_GREEDY_EVAL tag=it35_b3_plus8 alloc=[48, 48, 48, 56, 48, 32, 32, 32] bytes=344 recall=85.864800

PQ_GREEDY_EVAL tag=it35_b4_plus8 alloc=[48, 48, 48, 48, 56, 32, 32, 32] bytes=344 recall=85.932500

PQ_GREEDY_EVAL tag=it35_b5_plus8 alloc=[48, 48, 48, 48, 48, 40, 32, 32] bytes=344 recall=86.010300

PQ_GREEDY_EVAL tag=it35_b6_plus8 alloc=[48, 48, 48, 48, 48, 32, 40, 32] bytes=344 recall=85.974800

PQ_GREEDY_EVAL tag=it35_b7_plus8 alloc=[48, 48, 48, 48, 48, 32, 32, 40] bytes=344 recall=86.021800

PQ_GREEDY_EVAL tag=it36_b0_plus8 alloc=[56, 48, 48, 48, 48, 32, 32, 40] bytes=352 recall=86.346300

PQ_GREEDY_EVAL tag=it36_b1_plus8 alloc=[48, 56, 48, 48, 48, 32, 32, 40] bytes=352 recall=86.281200

PQ_GREEDY_EVAL tag=it36_b2_plus8 alloc=[48, 48, 56, 48, 48, 32, 32, 40] bytes=352 recall=86.212200

PQ_GREEDY_EVAL tag=it36_b3_plus8 alloc=[48, 48, 48, 56, 48, 32, 32, 40] bytes=352 recall=86.236500

PQ_GREEDY_EVAL tag=it36_b4_plus8 alloc=[48, 48, 48, 48, 56, 32, 32, 40] bytes=352 recall=86.296100

PQ_GREEDY_EVAL tag=it36_b5_plus8 alloc=[48, 48, 48, 48, 48, 40, 32, 40] bytes=352 recall=86.384200

PQ_GREEDY_EVAL tag=it36_b6_plus8 alloc=[48, 48, 48, 48, 48, 32, 40, 40] bytes=352 recall=86.340700

PQ_GREEDY_EVAL tag=it36_b7_plus8 alloc=[48, 48, 48, 48, 48, 32, 32, 48] bytes=352 recall=86.275200

PQ_GREEDY_EVAL tag=it37_b0_plus8 alloc=[56, 48, 48, 48, 48, 40, 32, 40] bytes=360 recall=86.676500

PQ_GREEDY_EVAL tag=it37_b1_plus8 alloc=[48, 56, 48, 48, 48, 40, 32, 40] bytes=360 recall=86.639800

PQ_GREEDY_EVAL tag=it37_b2_plus8 alloc=[48, 48, 56, 48, 48, 40, 32, 40] bytes=360 recall=86.703400

PQ_GREEDY_EVAL tag=it37_b3_plus8 alloc=[48, 48, 48, 56, 48, 40, 32, 40] bytes=360 recall=86.640000

PQ_GREEDY_EVAL tag=it37_b4_plus8 alloc=[48, 48, 48, 48, 56, 40, 32, 40] bytes=360 recall=86.633200

PQ_GREEDY_EVAL tag=it37_b5_plus8 alloc=[48, 48, 48, 48, 48, 48, 32, 40] bytes=360 recall=86.713200

PQ_GREEDY_EVAL tag=it37_b6_plus8 alloc=[48, 48, 48, 48, 48, 40, 40, 40] bytes=360 recall=86.735500

PQ_GREEDY_EVAL tag=it37_b7_plus8 alloc=[48, 48, 48, 48, 48, 40, 32, 48] bytes=360 recall=86.686100

PQ_GREEDY_EVAL tag=it38_b0_plus8 alloc=[56, 48, 48, 48, 48, 40, 40, 40] bytes=368 recall=87.025800

PQ_GREEDY_EVAL tag=it38_b1_plus8 alloc=[48, 56, 48, 48, 48, 40, 40, 40] bytes=368 recall=87.034100

PQ_GREEDY_EVAL tag=it38_b2_plus8 alloc=[48, 48, 56, 48, 48, 40, 40, 40] bytes=368 recall=87.031900

PQ_GREEDY_EVAL tag=it38_b3_plus8 alloc=[48, 48, 48, 56, 48, 40, 40, 40] bytes=368 recall=86.999300

PQ_GREEDY_EVAL tag=it38_b4_plus8 alloc=[48, 48, 48, 48, 56, 40, 40, 40] bytes=368 recall=86.978500

PQ_GREEDY_EVAL tag=it38_b5_plus8 alloc=[48, 48, 48, 48, 48, 48, 40, 40] bytes=368 recall=87.070900

PQ_GREEDY_EVAL tag=it38_b6_plus8 alloc=[48, 48, 48, 48, 48, 40, 48, 40] bytes=368 recall=87.090000

PQ_GREEDY_EVAL tag=it38_b7_plus8 alloc=[48, 48, 48, 48, 48, 40, 40, 48] bytes=368 recall=86.995800

PQ_GREEDY_EVAL tag=it39_b0_plus8 alloc=[56, 48, 48, 48, 48, 40, 48, 40] bytes=376 recall=87.326200

PQ_GREEDY_EVAL tag=it39_b1_plus8 alloc=[48, 56, 48, 48, 48, 40, 48, 40] bytes=376 recall=87.339300

PQ_GREEDY_EVAL tag=it39_b2_plus8 alloc=[48, 48, 56, 48, 48, 40, 48, 40] bytes=376 recall=87.274200

PQ_GREEDY_EVAL tag=it39_b3_plus8 alloc=[48, 48, 48, 56, 48, 40, 48, 40] bytes=376 recall=87.267800

PQ_GREEDY_EVAL tag=it39_b4_plus8 alloc=[48, 48, 48, 48, 56, 40, 48, 40] bytes=376 recall=87.301300

PQ_GREEDY_EVAL tag=it39_b5_plus8 alloc=[48, 48, 48, 48, 48, 48, 48, 40] bytes=376 recall=87.347100

PQ_GREEDY_EVAL tag=it39_b6_plus8 alloc=[48, 48, 48, 48, 48, 40, 56, 40] bytes=376 recall=87.249900

PQ_GREEDY_EVAL tag=it39_b7_plus8 alloc=[48, 48, 48, 48, 48, 40, 48, 48] bytes=376 recall=87.339300

PQ_GREEDY_EVAL tag=it40_b0_plus8 alloc=[56, 48, 48, 48, 48, 48, 48, 40] bytes=384 recall=87.689300

PQ_GREEDY_EVAL tag=it40_b1_plus8 alloc=[48, 56, 48, 48, 48, 48, 48, 40] bytes=384 recall=87.661500

PQ_GREEDY_EVAL tag=it40_b2_plus8 alloc=[48, 48, 56, 48, 48, 48, 48, 40] bytes=384 recall=87.594100

PQ_GREEDY_EVAL tag=it40_b3_plus8 alloc=[48, 48, 48, 56, 48, 48, 48, 40] bytes=384 recall=87.587800

PQ_GREEDY_EVAL tag=it40_b4_plus8 alloc=[48, 48, 48, 48, 56, 48, 48, 40] bytes=384 recall=87.644300

PQ_GREEDY_EVAL tag=it40_b5_plus8 alloc=[48, 48, 48, 48, 48, 56, 48, 40] bytes=384 recall=87.540800

PQ_GREEDY_EVAL tag=it40_b6_plus8 alloc=[48, 48, 48, 48, 48, 48, 56, 40] bytes=384 recall=87.566900

PQ_GREEDY_EVAL tag=it40_b7_plus8 alloc=[48, 48, 48, 48, 48, 48, 48, 48] bytes=384 recall=87.680700