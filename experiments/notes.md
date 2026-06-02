## Size

3072 * float32 = 3072 * 4 bytes = 12k bytes total

384 bytes total = 3072/8 bytes = 3072 bits = 1 bit per point

## Commands dump
```
rclone sync ./embeddings jamji1729-gmail-gdrive: --drive-root-folder-id 123thqFh7P5ZzVh-0zM4cjJJQ60Og4V1d -P --dry-run
```

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

  
  
### MS Marco - text-embedding-3-large
#### Uniform PQ
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

  

#### Variable PQ

##### First 20 iters:
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

  
##### Next 20 iters, started as a separate run from where it was left
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

#### Uniform PQ

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


### DBPedia OpenAI-text-large-3

#### Uniform PQ
PQ sweep completed! Results directory: /tmp/pq_sweep_1778870055
Summary of recall results:
Bytes,Recall
64,38.2475
96,54.12
128,63.8625
160,69.695
192,73.9175
224,76.6725
256,78.9625
288,80.1775
320,81.6125
352,82.935
384,83.7425
#### Variable PQ
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

--max_per_bucket 192 \

--max_total_bytes 384 \

--max_iters 50 \

--log_json ${RUN_DIR}/log.json \

> >(tee "${RUN_DIR}/stdout") \

2> >(tee "${RUN_DIR}/stderr" >&2)



PQ_GREEDY_EVAL tag=init alloc=[8, 8, 8, 8, 8, 8, 8, 8] bytes=64 recall=38.307500

PQ_GREEDY_EVAL tag=it1_b0_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 8] bytes=72 recall=45.290000

PQ_GREEDY_EVAL tag=it1_b1_plus8 alloc=[8, 16, 8, 8, 8, 8, 8, 8] bytes=72 recall=43.545000

PQ_GREEDY_EVAL tag=it1_b2_plus8 alloc=[8, 8, 16, 8, 8, 8, 8, 8] bytes=72 recall=42.362500

PQ_GREEDY_EVAL tag=it1_b3_plus8 alloc=[8, 8, 8, 16, 8, 8, 8, 8] bytes=72 recall=41.882500

PQ_GREEDY_EVAL tag=it1_b4_plus8 alloc=[8, 8, 8, 8, 16, 8, 8, 8] bytes=72 recall=40.480000

PQ_GREEDY_EVAL tag=it1_b5_plus8 alloc=[8, 8, 8, 8, 8, 16, 8, 8] bytes=72 recall=40.812500

PQ_GREEDY_EVAL tag=it1_b6_plus8 alloc=[8, 8, 8, 8, 8, 8, 16, 8] bytes=72 recall=41.160000

PQ_GREEDY_EVAL tag=it1_b7_plus8 alloc=[8, 8, 8, 8, 8, 8, 8, 16] bytes=72 recall=40.895000

PQ_GREEDY_EVAL tag=it2_b0_plus8 alloc=[24, 8, 8, 8, 8, 8, 8, 8] bytes=80 recall=49.702500

PQ_GREEDY_EVAL tag=it2_b1_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 8] bytes=80 recall=50.372500

PQ_GREEDY_EVAL tag=it2_b2_plus8 alloc=[16, 8, 16, 8, 8, 8, 8, 8] bytes=80 recall=49.387500

PQ_GREEDY_EVAL tag=it2_b3_plus8 alloc=[16, 8, 8, 16, 8, 8, 8, 8] bytes=80 recall=48.840000

PQ_GREEDY_EVAL tag=it2_b4_plus8 alloc=[16, 8, 8, 8, 16, 8, 8, 8] bytes=80 recall=47.387500

PQ_GREEDY_EVAL tag=it2_b5_plus8 alloc=[16, 8, 8, 8, 8, 16, 8, 8] bytes=80 recall=47.435000

PQ_GREEDY_EVAL tag=it2_b6_plus8 alloc=[16, 8, 8, 8, 8, 8, 16, 8] bytes=80 recall=47.987500

PQ_GREEDY_EVAL tag=it2_b7_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 16] bytes=80 recall=47.622500

PQ_GREEDY_EVAL tag=it3_b0_plus8 alloc=[24, 16, 8, 8, 8, 8, 8, 8] bytes=88 recall=54.367500

PQ_GREEDY_EVAL tag=it3_b1_plus8 alloc=[16, 24, 8, 8, 8, 8, 8, 8] bytes=88 recall=53.562500

PQ_GREEDY_EVAL tag=it3_b2_plus8 alloc=[16, 16, 16, 8, 8, 8, 8, 8] bytes=88 recall=54.472500

PQ_GREEDY_EVAL tag=it3_b3_plus8 alloc=[16, 16, 8, 16, 8, 8, 8, 8] bytes=88 recall=53.465000

PQ_GREEDY_EVAL tag=it3_b4_plus8 alloc=[16, 16, 8, 8, 16, 8, 8, 8] bytes=88 recall=52.220000

PQ_GREEDY_EVAL tag=it3_b5_plus8 alloc=[16, 16, 8, 8, 8, 16, 8, 8] bytes=88 recall=52.392500

PQ_GREEDY_EVAL tag=it3_b6_plus8 alloc=[16, 16, 8, 8, 8, 8, 16, 8] bytes=88 recall=52.057500

PQ_GREEDY_EVAL tag=it3_b7_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 16] bytes=88 recall=52.425000

PQ_GREEDY_EVAL tag=it4_b0_plus8 alloc=[24, 16, 16, 8, 8, 8, 8, 8] bytes=96 recall=58.497500

PQ_GREEDY_EVAL tag=it4_b1_plus8 alloc=[16, 24, 16, 8, 8, 8, 8, 8] bytes=96 recall=57.095000

PQ_GREEDY_EVAL tag=it4_b2_plus8 alloc=[16, 16, 24, 8, 8, 8, 8, 8] bytes=96 recall=56.687500

PQ_GREEDY_EVAL tag=it4_b3_plus8 alloc=[16, 16, 16, 16, 8, 8, 8, 8] bytes=96 recall=57.277500

PQ_GREEDY_EVAL tag=it4_b4_plus8 alloc=[16, 16, 16, 8, 16, 8, 8, 8] bytes=96 recall=56.110000

PQ_GREEDY_EVAL tag=it4_b5_plus8 alloc=[16, 16, 16, 8, 8, 16, 8, 8] bytes=96 recall=56.052500

PQ_GREEDY_EVAL tag=it4_b6_plus8 alloc=[16, 16, 16, 8, 8, 8, 16, 8] bytes=96 recall=56.520000

PQ_GREEDY_EVAL tag=it4_b7_plus8 alloc=[16, 16, 16, 8, 8, 8, 8, 16] bytes=96 recall=56.307500

PQ_GREEDY_EVAL tag=it5_b0_plus8 alloc=[32, 16, 16, 8, 8, 8, 8, 8] bytes=104 recall=60.882500

PQ_GREEDY_EVAL tag=it5_b1_plus8 alloc=[24, 24, 16, 8, 8, 8, 8, 8] bytes=104 recall=60.762500

PQ_GREEDY_EVAL tag=it5_b2_plus8 alloc=[24, 16, 24, 8, 8, 8, 8, 8] bytes=104 recall=60.185000

PQ_GREEDY_EVAL tag=it5_b3_plus8 alloc=[24, 16, 16, 16, 8, 8, 8, 8] bytes=104 recall=60.515000

PQ_GREEDY_EVAL tag=it5_b4_plus8 alloc=[24, 16, 16, 8, 16, 8, 8, 8] bytes=104 recall=59.762500

PQ_GREEDY_EVAL tag=it5_b5_plus8 alloc=[24, 16, 16, 8, 8, 16, 8, 8] bytes=104 recall=59.790000

PQ_GREEDY_EVAL tag=it5_b6_plus8 alloc=[24, 16, 16, 8, 8, 8, 16, 8] bytes=104 recall=59.737500

PQ_GREEDY_EVAL tag=it5_b7_plus8 alloc=[24, 16, 16, 8, 8, 8, 8, 16] bytes=104 recall=59.745000

PQ_GREEDY_EVAL tag=it6_b0_plus8 alloc=[40, 16, 16, 8, 8, 8, 8, 8] bytes=112 recall=62.555000

PQ_GREEDY_EVAL tag=it6_b1_plus8 alloc=[32, 24, 16, 8, 8, 8, 8, 8] bytes=112 recall=63.007500

PQ_GREEDY_EVAL tag=it6_b2_plus8 alloc=[32, 16, 24, 8, 8, 8, 8, 8] bytes=112 recall=63.070000

PQ_GREEDY_EVAL tag=it6_b3_plus8 alloc=[32, 16, 16, 16, 8, 8, 8, 8] bytes=112 recall=63.180000

PQ_GREEDY_EVAL tag=it6_b4_plus8 alloc=[32, 16, 16, 8, 16, 8, 8, 8] bytes=112 recall=62.237500

PQ_GREEDY_EVAL tag=it6_b5_plus8 alloc=[32, 16, 16, 8, 8, 16, 8, 8] bytes=112 recall=62.170000

PQ_GREEDY_EVAL tag=it6_b6_plus8 alloc=[32, 16, 16, 8, 8, 8, 16, 8] bytes=112 recall=62.127500

PQ_GREEDY_EVAL tag=it6_b7_plus8 alloc=[32, 16, 16, 8, 8, 8, 8, 16] bytes=112 recall=62.132500

PQ_GREEDY_EVAL tag=it7_b0_plus8 alloc=[40, 16, 16, 16, 8, 8, 8, 8] bytes=120 recall=64.717500

PQ_GREEDY_EVAL tag=it7_b1_plus8 alloc=[32, 24, 16, 16, 8, 8, 8, 8] bytes=120 recall=65.652500

PQ_GREEDY_EVAL tag=it7_b2_plus8 alloc=[32, 16, 24, 16, 8, 8, 8, 8] bytes=120 recall=64.852500

PQ_GREEDY_EVAL tag=it7_b3_plus8 alloc=[32, 16, 16, 24, 8, 8, 8, 8] bytes=120 recall=64.567500

PQ_GREEDY_EVAL tag=it7_b4_plus8 alloc=[32, 16, 16, 16, 16, 8, 8, 8] bytes=120 recall=64.357500

PQ_GREEDY_EVAL tag=it7_b5_plus8 alloc=[32, 16, 16, 16, 8, 16, 8, 8] bytes=120 recall=64.542500

PQ_GREEDY_EVAL tag=it7_b6_plus8 alloc=[32, 16, 16, 16, 8, 8, 16, 8] bytes=120 recall=64.270000

PQ_GREEDY_EVAL tag=it7_b7_plus8 alloc=[32, 16, 16, 16, 8, 8, 8, 16] bytes=120 recall=64.600000

PQ_GREEDY_EVAL tag=it8_b0_plus8 alloc=[40, 24, 16, 16, 8, 8, 8, 8] bytes=128 recall=66.630000

PQ_GREEDY_EVAL tag=it8_b1_plus8 alloc=[32, 32, 16, 16, 8, 8, 8, 8] bytes=128 recall=66.640000

PQ_GREEDY_EVAL tag=it8_b2_plus8 alloc=[32, 24, 24, 16, 8, 8, 8, 8] bytes=128 recall=67.050000

PQ_GREEDY_EVAL tag=it8_b3_plus8 alloc=[32, 24, 16, 24, 8, 8, 8, 8] bytes=128 recall=66.590000

PQ_GREEDY_EVAL tag=it8_b4_plus8 alloc=[32, 24, 16, 16, 16, 8, 8, 8] bytes=128 recall=66.997500

PQ_GREEDY_EVAL tag=it8_b5_plus8 alloc=[32, 24, 16, 16, 8, 16, 8, 8] bytes=128 recall=66.827500

PQ_GREEDY_EVAL tag=it8_b6_plus8 alloc=[32, 24, 16, 16, 8, 8, 16, 8] bytes=128 recall=66.572500

PQ_GREEDY_EVAL tag=it8_b7_plus8 alloc=[32, 24, 16, 16, 8, 8, 8, 16] bytes=128 recall=66.687500

PQ_GREEDY_EVAL tag=it9_b0_plus8 alloc=[40, 24, 24, 16, 8, 8, 8, 8] bytes=136 recall=68.417500

PQ_GREEDY_EVAL tag=it9_b1_plus8 alloc=[32, 32, 24, 16, 8, 8, 8, 8] bytes=136 recall=67.957500

PQ_GREEDY_EVAL tag=it9_b2_plus8 alloc=[32, 24, 32, 16, 8, 8, 8, 8] bytes=136 recall=68.282500

PQ_GREEDY_EVAL tag=it9_b3_plus8 alloc=[32, 24, 24, 24, 8, 8, 8, 8] bytes=136 recall=68.510000

PQ_GREEDY_EVAL tag=it9_b4_plus8 alloc=[32, 24, 24, 16, 16, 8, 8, 8] bytes=136 recall=68.555000

PQ_GREEDY_EVAL tag=it9_b5_plus8 alloc=[32, 24, 24, 16, 8, 16, 8, 8] bytes=136 recall=68.267500

PQ_GREEDY_EVAL tag=it9_b6_plus8 alloc=[32, 24, 24, 16, 8, 8, 16, 8] bytes=136 recall=68.497500

PQ_GREEDY_EVAL tag=it9_b7_plus8 alloc=[32, 24, 24, 16, 8, 8, 8, 16] bytes=136 recall=68.250000

PQ_GREEDY_EVAL tag=it10_b0_plus8 alloc=[40, 24, 24, 16, 16, 8, 8, 8] bytes=144 recall=69.832500

PQ_GREEDY_EVAL tag=it10_b1_plus8 alloc=[32, 32, 24, 16, 16, 8, 8, 8] bytes=144 recall=69.600000

PQ_GREEDY_EVAL tag=it10_b2_plus8 alloc=[32, 24, 32, 16, 16, 8, 8, 8] bytes=144 recall=69.472500

PQ_GREEDY_EVAL tag=it10_b3_plus8 alloc=[32, 24, 24, 24, 16, 8, 8, 8] bytes=144 recall=69.635000

PQ_GREEDY_EVAL tag=it10_b4_plus8 alloc=[32, 24, 24, 16, 24, 8, 8, 8] bytes=144 recall=69.270000

PQ_GREEDY_EVAL tag=it10_b5_plus8 alloc=[32, 24, 24, 16, 16, 16, 8, 8] bytes=144 recall=69.567500

PQ_GREEDY_EVAL tag=it10_b6_plus8 alloc=[32, 24, 24, 16, 16, 8, 16, 8] bytes=144 recall=69.545000

PQ_GREEDY_EVAL tag=it10_b7_plus8 alloc=[32, 24, 24, 16, 16, 8, 8, 16] bytes=144 recall=69.615000

PQ_GREEDY_EVAL tag=it11_b0_plus8 alloc=[48, 24, 24, 16, 16, 8, 8, 8] bytes=152 recall=70.957500

PQ_GREEDY_EVAL tag=it11_b1_plus8 alloc=[40, 32, 24, 16, 16, 8, 8, 8] bytes=152 recall=71.127500

PQ_GREEDY_EVAL tag=it11_b2_plus8 alloc=[40, 24, 32, 16, 16, 8, 8, 8] bytes=152 recall=70.955000

PQ_GREEDY_EVAL tag=it11_b3_plus8 alloc=[40, 24, 24, 24, 16, 8, 8, 8] bytes=152 recall=70.670000

PQ_GREEDY_EVAL tag=it11_b4_plus8 alloc=[40, 24, 24, 16, 24, 8, 8, 8] bytes=152 recall=70.205000

PQ_GREEDY_EVAL tag=it11_b5_plus8 alloc=[40, 24, 24, 16, 16, 16, 8, 8] bytes=152 recall=70.642500

PQ_GREEDY_EVAL tag=it11_b6_plus8 alloc=[40, 24, 24, 16, 16, 8, 16, 8] bytes=152 recall=70.702500

PQ_GREEDY_EVAL tag=it11_b7_plus8 alloc=[40, 24, 24, 16, 16, 8, 8, 16] bytes=152 recall=70.385000

PQ_GREEDY_EVAL tag=it12_b0_plus8 alloc=[48, 32, 24, 16, 16, 8, 8, 8] bytes=160 recall=72.010000

PQ_GREEDY_EVAL tag=it12_b1_plus8 alloc=[40, 40, 24, 16, 16, 8, 8, 8] bytes=160 recall=71.852500

PQ_GREEDY_EVAL tag=it12_b2_plus8 alloc=[40, 32, 32, 16, 16, 8, 8, 8] bytes=160 recall=72.357500

PQ_GREEDY_EVAL tag=it12_b3_plus8 alloc=[40, 32, 24, 24, 16, 8, 8, 8] bytes=160 recall=71.990000

PQ_GREEDY_EVAL tag=it12_b4_plus8 alloc=[40, 32, 24, 16, 24, 8, 8, 8] bytes=160 recall=71.712500

PQ_GREEDY_EVAL tag=it12_b5_plus8 alloc=[40, 32, 24, 16, 16, 16, 8, 8] bytes=160 recall=72.397500

PQ_GREEDY_EVAL tag=it12_b6_plus8 alloc=[40, 32, 24, 16, 16, 8, 16, 8] bytes=160 recall=72.247500

PQ_GREEDY_EVAL tag=it12_b7_plus8 alloc=[40, 32, 24, 16, 16, 8, 8, 16] bytes=160 recall=72.090000

PQ_GREEDY_EVAL tag=it13_b0_plus8 alloc=[48, 32, 24, 16, 16, 16, 8, 8] bytes=168 recall=73.187500

PQ_GREEDY_EVAL tag=it13_b1_plus8 alloc=[40, 40, 24, 16, 16, 16, 8, 8] bytes=168 recall=73.090000

PQ_GREEDY_EVAL tag=it13_b2_plus8 alloc=[40, 32, 32, 16, 16, 16, 8, 8] bytes=168 recall=73.090000

PQ_GREEDY_EVAL tag=it13_b3_plus8 alloc=[40, 32, 24, 24, 16, 16, 8, 8] bytes=168 recall=73.025000

PQ_GREEDY_EVAL tag=it13_b4_plus8 alloc=[40, 32, 24, 16, 24, 16, 8, 8] bytes=168 recall=72.465000

PQ_GREEDY_EVAL tag=it13_b5_plus8 alloc=[40, 32, 24, 16, 16, 24, 8, 8] bytes=168 recall=72.860000

PQ_GREEDY_EVAL tag=it13_b6_plus8 alloc=[40, 32, 24, 16, 16, 16, 16, 8] bytes=168 recall=73.217500

PQ_GREEDY_EVAL tag=it13_b7_plus8 alloc=[40, 32, 24, 16, 16, 16, 8, 16] bytes=168 recall=73.047500

PQ_GREEDY_EVAL tag=it14_b0_plus8 alloc=[48, 32, 24, 16, 16, 16, 16, 8] bytes=176 recall=74.227500

PQ_GREEDY_EVAL tag=it14_b1_plus8 alloc=[40, 40, 24, 16, 16, 16, 16, 8] bytes=176 recall=73.657500

PQ_GREEDY_EVAL tag=it14_b2_plus8 alloc=[40, 32, 32, 16, 16, 16, 16, 8] bytes=176 recall=73.952500

PQ_GREEDY_EVAL tag=it14_b3_plus8 alloc=[40, 32, 24, 24, 16, 16, 16, 8] bytes=176 recall=73.752500

PQ_GREEDY_EVAL tag=it14_b4_plus8 alloc=[40, 32, 24, 16, 24, 16, 16, 8] bytes=176 recall=73.582500

PQ_GREEDY_EVAL tag=it14_b5_plus8 alloc=[40, 32, 24, 16, 16, 24, 16, 8] bytes=176 recall=73.550000

PQ_GREEDY_EVAL tag=it14_b6_plus8 alloc=[40, 32, 24, 16, 16, 16, 24, 8] bytes=176 recall=73.572500

PQ_GREEDY_EVAL tag=it14_b7_plus8 alloc=[40, 32, 24, 16, 16, 16, 16, 16] bytes=176 recall=74.145000

PQ_GREEDY_EVAL tag=it15_b0_plus8 alloc=[56, 32, 24, 16, 16, 16, 16, 8] bytes=184 recall=74.850000

PQ_GREEDY_EVAL tag=it15_b1_plus8 alloc=[48, 40, 24, 16, 16, 16, 16, 8] bytes=184 recall=74.832500

PQ_GREEDY_EVAL tag=it15_b2_plus8 alloc=[48, 32, 32, 16, 16, 16, 16, 8] bytes=184 recall=74.885000

PQ_GREEDY_EVAL tag=it15_b3_plus8 alloc=[48, 32, 24, 24, 16, 16, 16, 8] bytes=184 recall=74.770000

PQ_GREEDY_EVAL tag=it15_b4_plus8 alloc=[48, 32, 24, 16, 24, 16, 16, 8] bytes=184 recall=74.482500

PQ_GREEDY_EVAL tag=it15_b5_plus8 alloc=[48, 32, 24, 16, 16, 24, 16, 8] bytes=184 recall=74.537500

PQ_GREEDY_EVAL tag=it15_b6_plus8 alloc=[48, 32, 24, 16, 16, 16, 24, 8] bytes=184 recall=74.585000

PQ_GREEDY_EVAL tag=it15_b7_plus8 alloc=[48, 32, 24, 16, 16, 16, 16, 16] bytes=184 recall=74.930000

PQ_GREEDY_EVAL tag=it16_b0_plus8 alloc=[56, 32, 24, 16, 16, 16, 16, 16] bytes=192 recall=75.625000

PQ_GREEDY_EVAL tag=it16_b1_plus8 alloc=[48, 40, 24, 16, 16, 16, 16, 16] bytes=192 recall=75.632500

PQ_GREEDY_EVAL tag=it16_b2_plus8 alloc=[48, 32, 32, 16, 16, 16, 16, 16] bytes=192 recall=75.860000

PQ_GREEDY_EVAL tag=it16_b3_plus8 alloc=[48, 32, 24, 24, 16, 16, 16, 16] bytes=192 recall=75.702500

PQ_GREEDY_EVAL tag=it16_b4_plus8 alloc=[48, 32, 24, 16, 24, 16, 16, 16] bytes=192 recall=75.675000

PQ_GREEDY_EVAL tag=it16_b5_plus8 alloc=[48, 32, 24, 16, 16, 24, 16, 16] bytes=192 recall=75.572500

PQ_GREEDY_EVAL tag=it16_b6_plus8 alloc=[48, 32, 24, 16, 16, 16, 24, 16] bytes=192 recall=75.330000

PQ_GREEDY_EVAL tag=it16_b7_plus8 alloc=[48, 32, 24, 16, 16, 16, 16, 24] bytes=192 recall=75.587500

PQ_GREEDY_EVAL tag=it17_b0_plus8 alloc=[56, 32, 32, 16, 16, 16, 16, 16] bytes=200 recall=76.490000

PQ_GREEDY_EVAL tag=it17_b1_plus8 alloc=[48, 40, 32, 16, 16, 16, 16, 16] bytes=200 recall=76.397500

PQ_GREEDY_EVAL tag=it17_b2_plus8 alloc=[48, 32, 40, 16, 16, 16, 16, 16] bytes=200 recall=76.475000

PQ_GREEDY_EVAL tag=it17_b3_plus8 alloc=[48, 32, 32, 24, 16, 16, 16, 16] bytes=200 recall=76.407500

PQ_GREEDY_EVAL tag=it17_b4_plus8 alloc=[48, 32, 32, 16, 24, 16, 16, 16] bytes=200 recall=76.190000

PQ_GREEDY_EVAL tag=it17_b5_plus8 alloc=[48, 32, 32, 16, 16, 24, 16, 16] bytes=200 recall=76.435000

PQ_GREEDY_EVAL tag=it17_b6_plus8 alloc=[48, 32, 32, 16, 16, 16, 24, 16] bytes=200 recall=76.160000

PQ_GREEDY_EVAL tag=it17_b7_plus8 alloc=[48, 32, 32, 16, 16, 16, 16, 24] bytes=200 recall=76.365000

PQ_GREEDY_EVAL tag=it18_b0_plus8 alloc=[64, 32, 32, 16, 16, 16, 16, 16] bytes=208 recall=76.810000

PQ_GREEDY_EVAL tag=it18_b1_plus8 alloc=[56, 40, 32, 16, 16, 16, 16, 16] bytes=208 recall=77.205000

PQ_GREEDY_EVAL tag=it18_b2_plus8 alloc=[56, 32, 40, 16, 16, 16, 16, 16] bytes=208 recall=77.162500

PQ_GREEDY_EVAL tag=it18_b3_plus8 alloc=[56, 32, 32, 24, 16, 16, 16, 16] bytes=208 recall=77.310000

PQ_GREEDY_EVAL tag=it18_b4_plus8 alloc=[56, 32, 32, 16, 24, 16, 16, 16] bytes=208 recall=77.010000

PQ_GREEDY_EVAL tag=it18_b5_plus8 alloc=[56, 32, 32, 16, 16, 24, 16, 16] bytes=208 recall=77.015000

PQ_GREEDY_EVAL tag=it18_b6_plus8 alloc=[56, 32, 32, 16, 16, 16, 24, 16] bytes=208 recall=76.830000

PQ_GREEDY_EVAL tag=it18_b7_plus8 alloc=[56, 32, 32, 16, 16, 16, 16, 24] bytes=208 recall=76.887500

PQ_GREEDY_EVAL tag=it19_b0_plus8 alloc=[64, 32, 32, 24, 16, 16, 16, 16] bytes=216 recall=77.580000

PQ_GREEDY_EVAL tag=it19_b1_plus8 alloc=[56, 40, 32, 24, 16, 16, 16, 16] bytes=216 recall=77.787500

PQ_GREEDY_EVAL tag=it19_b2_plus8 alloc=[56, 32, 40, 24, 16, 16, 16, 16] bytes=216 recall=77.862500

PQ_GREEDY_EVAL tag=it19_b3_plus8 alloc=[56, 32, 32, 32, 16, 16, 16, 16] bytes=216 recall=77.630000

PQ_GREEDY_EVAL tag=it19_b4_plus8 alloc=[56, 32, 32, 24, 24, 16, 16, 16] bytes=216 recall=77.830000

PQ_GREEDY_EVAL tag=it19_b5_plus8 alloc=[56, 32, 32, 24, 16, 24, 16, 16] bytes=216 recall=77.525000

PQ_GREEDY_EVAL tag=it19_b6_plus8 alloc=[56, 32, 32, 24, 16, 16, 24, 16] bytes=216 recall=77.545000

PQ_GREEDY_EVAL tag=it19_b7_plus8 alloc=[56, 32, 32, 24, 16, 16, 16, 24] bytes=216 recall=77.580000

PQ_GREEDY_EVAL tag=it20_b0_plus8 alloc=[64, 32, 40, 24, 16, 16, 16, 16] bytes=224 recall=78.237500

PQ_GREEDY_EVAL tag=it20_b1_plus8 alloc=[56, 40, 40, 24, 16, 16, 16, 16] bytes=224 recall=78.525000

PQ_GREEDY_EVAL tag=it20_b2_plus8 alloc=[56, 32, 48, 24, 16, 16, 16, 16] bytes=224 recall=78.122500

PQ_GREEDY_EVAL tag=it20_b3_plus8 alloc=[56, 32, 40, 32, 16, 16, 16, 16] bytes=224 recall=78.192500

PQ_GREEDY_EVAL tag=it20_b4_plus8 alloc=[56, 32, 40, 24, 24, 16, 16, 16] bytes=224 recall=78.357500

PQ_GREEDY_EVAL tag=it20_b5_plus8 alloc=[56, 32, 40, 24, 16, 24, 16, 16] bytes=224 recall=78.132500

PQ_GREEDY_EVAL tag=it20_b6_plus8 alloc=[56, 32, 40, 24, 16, 16, 24, 16] bytes=224 recall=78.145000

PQ_GREEDY_EVAL tag=it20_b7_plus8 alloc=[56, 32, 40, 24, 16, 16, 16, 24] bytes=224 recall=77.920000

PQ_GREEDY_EVAL tag=it21_b0_plus8 alloc=[64, 40, 40, 24, 16, 16, 16, 16] bytes=232 recall=79.112500

PQ_GREEDY_EVAL tag=it21_b1_plus8 alloc=[56, 48, 40, 24, 16, 16, 16, 16] bytes=232 recall=79.200000

PQ_GREEDY_EVAL tag=it21_b2_plus8 alloc=[56, 40, 48, 24, 16, 16, 16, 16] bytes=232 recall=78.742500

PQ_GREEDY_EVAL tag=it21_b3_plus8 alloc=[56, 40, 40, 32, 16, 16, 16, 16] bytes=232 recall=78.997500

PQ_GREEDY_EVAL tag=it21_b4_plus8 alloc=[56, 40, 40, 24, 24, 16, 16, 16] bytes=232 recall=78.795000

PQ_GREEDY_EVAL tag=it21_b5_plus8 alloc=[56, 40, 40, 24, 16, 24, 16, 16] bytes=232 recall=78.730000

PQ_GREEDY_EVAL tag=it21_b6_plus8 alloc=[56, 40, 40, 24, 16, 16, 24, 16] bytes=232 recall=79.177500

PQ_GREEDY_EVAL tag=it21_b7_plus8 alloc=[56, 40, 40, 24, 16, 16, 16, 24] bytes=232 recall=78.870000

PQ_GREEDY_EVAL tag=it22_b0_plus8 alloc=[64, 48, 40, 24, 16, 16, 16, 16] bytes=240 recall=79.700000

PQ_GREEDY_EVAL tag=it22_b1_plus8 alloc=[56, 56, 40, 24, 16, 16, 16, 16] bytes=240 recall=79.527500

PQ_GREEDY_EVAL tag=it22_b2_plus8 alloc=[56, 48, 48, 24, 16, 16, 16, 16] bytes=240 recall=79.667500

PQ_GREEDY_EVAL tag=it22_b3_plus8 alloc=[56, 48, 40, 32, 16, 16, 16, 16] bytes=240 recall=79.422500

PQ_GREEDY_EVAL tag=it22_b4_plus8 alloc=[56, 48, 40, 24, 24, 16, 16, 16] bytes=240 recall=79.262500

PQ_GREEDY_EVAL tag=it22_b5_plus8 alloc=[56, 48, 40, 24, 16, 24, 16, 16] bytes=240 recall=79.482500

PQ_GREEDY_EVAL tag=it22_b6_plus8 alloc=[56, 48, 40, 24, 16, 16, 24, 16] bytes=240 recall=79.440000

PQ_GREEDY_EVAL tag=it22_b7_plus8 alloc=[56, 48, 40, 24, 16, 16, 16, 24] bytes=240 recall=79.267500

PQ_GREEDY_EVAL tag=it23_b0_plus8 alloc=[72, 48, 40, 24, 16, 16, 16, 16] bytes=248 recall=79.725000

PQ_GREEDY_EVAL tag=it23_b1_plus8 alloc=[64, 56, 40, 24, 16, 16, 16, 16] bytes=248 recall=79.867500

PQ_GREEDY_EVAL tag=it23_b2_plus8 alloc=[64, 48, 48, 24, 16, 16, 16, 16] bytes=248 recall=79.857500

PQ_GREEDY_EVAL tag=it23_b3_plus8 alloc=[64, 48, 40, 32, 16, 16, 16, 16] bytes=248 recall=79.990000

PQ_GREEDY_EVAL tag=it23_b4_plus8 alloc=[64, 48, 40, 24, 24, 16, 16, 16] bytes=248 recall=79.742500

PQ_GREEDY_EVAL tag=it23_b5_plus8 alloc=[64, 48, 40, 24, 16, 24, 16, 16] bytes=248 recall=79.810000

PQ_GREEDY_EVAL tag=it23_b6_plus8 alloc=[64, 48, 40, 24, 16, 16, 24, 16] bytes=248 recall=79.522500

PQ_GREEDY_EVAL tag=it23_b7_plus8 alloc=[64, 48, 40, 24, 16, 16, 16, 24] bytes=248 recall=79.825000

PQ_GREEDY_EVAL tag=it24_b0_plus8 alloc=[72, 48, 40, 32, 16, 16, 16, 16] bytes=256 recall=80.322500

PQ_GREEDY_EVAL tag=it24_b1_plus8 alloc=[64, 56, 40, 32, 16, 16, 16, 16] bytes=256 recall=80.355000

PQ_GREEDY_EVAL tag=it24_b2_plus8 alloc=[64, 48, 48, 32, 16, 16, 16, 16] bytes=256 recall=80.582500

PQ_GREEDY_EVAL tag=it24_b3_plus8 alloc=[64, 48, 40, 40, 16, 16, 16, 16] bytes=256 recall=80.217500

PQ_GREEDY_EVAL tag=it24_b4_plus8 alloc=[64, 48, 40, 32, 24, 16, 16, 16] bytes=256 recall=80.082500

PQ_GREEDY_EVAL tag=it24_b5_plus8 alloc=[64, 48, 40, 32, 16, 24, 16, 16] bytes=256 recall=80.275000

PQ_GREEDY_EVAL tag=it24_b6_plus8 alloc=[64, 48, 40, 32, 16, 16, 24, 16] bytes=256 recall=80.460000

PQ_GREEDY_EVAL tag=it24_b7_plus8 alloc=[64, 48, 40, 32, 16, 16, 16, 24] bytes=256 recall=80.272500

PQ_GREEDY_EVAL tag=it25_b0_plus8 alloc=[72, 48, 48, 32, 16, 16, 16, 16] bytes=264 recall=80.967500

PQ_GREEDY_EVAL tag=it25_b1_plus8 alloc=[64, 56, 48, 32, 16, 16, 16, 16] bytes=264 recall=80.685000

PQ_GREEDY_EVAL tag=it25_b2_plus8 alloc=[64, 48, 56, 32, 16, 16, 16, 16] bytes=264 recall=80.745000

PQ_GREEDY_EVAL tag=it25_b3_plus8 alloc=[64, 48, 48, 40, 16, 16, 16, 16] bytes=264 recall=80.760000

PQ_GREEDY_EVAL tag=it25_b4_plus8 alloc=[64, 48, 48, 32, 24, 16, 16, 16] bytes=264 recall=80.682500

PQ_GREEDY_EVAL tag=it25_b5_plus8 alloc=[64, 48, 48, 32, 16, 24, 16, 16] bytes=264 recall=80.760000

PQ_GREEDY_EVAL tag=it25_b6_plus8 alloc=[64, 48, 48, 32, 16, 16, 24, 16] bytes=264 recall=81.005000

PQ_GREEDY_EVAL tag=it25_b7_plus8 alloc=[64, 48, 48, 32, 16, 16, 16, 24] bytes=264 recall=80.890000

PQ_GREEDY_EVAL tag=it26_b0_plus8 alloc=[72, 48, 48, 32, 16, 16, 24, 16] bytes=272 recall=81.085000

PQ_GREEDY_EVAL tag=it26_b1_plus8 alloc=[64, 56, 48, 32, 16, 16, 24, 16] bytes=272 recall=81.245000

PQ_GREEDY_EVAL tag=it26_b2_plus8 alloc=[64, 48, 56, 32, 16, 16, 24, 16] bytes=272 recall=81.225000

PQ_GREEDY_EVAL tag=it26_b3_plus8 alloc=[64, 48, 48, 40, 16, 16, 24, 16] bytes=272 recall=80.945000

PQ_GREEDY_EVAL tag=it26_b4_plus8 alloc=[64, 48, 48, 32, 24, 16, 24, 16] bytes=272 recall=81.130000

PQ_GREEDY_EVAL tag=it26_b5_plus8 alloc=[64, 48, 48, 32, 16, 24, 24, 16] bytes=272 recall=81.225000

PQ_GREEDY_EVAL tag=it26_b6_plus8 alloc=[64, 48, 48, 32, 16, 16, 32, 16] bytes=272 recall=81.230000

PQ_GREEDY_EVAL tag=it26_b7_plus8 alloc=[64, 48, 48, 32, 16, 16, 24, 24] bytes=272 recall=81.275000

PQ_GREEDY_EVAL tag=it27_b0_plus8 alloc=[72, 48, 48, 32, 16, 16, 24, 24] bytes=280 recall=81.525000

PQ_GREEDY_EVAL tag=it27_b1_plus8 alloc=[64, 56, 48, 32, 16, 16, 24, 24] bytes=280 recall=81.590000

PQ_GREEDY_EVAL tag=it27_b2_plus8 alloc=[64, 48, 56, 32, 16, 16, 24, 24] bytes=280 recall=81.360000

PQ_GREEDY_EVAL tag=it27_b3_plus8 alloc=[64, 48, 48, 40, 16, 16, 24, 24] bytes=280 recall=81.365000

PQ_GREEDY_EVAL tag=it27_b4_plus8 alloc=[64, 48, 48, 32, 24, 16, 24, 24] bytes=280 recall=81.585000

PQ_GREEDY_EVAL tag=it27_b5_plus8 alloc=[64, 48, 48, 32, 16, 24, 24, 24] bytes=280 recall=81.532500

PQ_GREEDY_EVAL tag=it27_b6_plus8 alloc=[64, 48, 48, 32, 16, 16, 32, 24] bytes=280 recall=81.365000

PQ_GREEDY_EVAL tag=it27_b7_plus8 alloc=[64, 48, 48, 32, 16, 16, 24, 32] bytes=280 recall=81.545000

PQ_GREEDY_EVAL tag=it28_b0_plus8 alloc=[72, 56, 48, 32, 16, 16, 24, 24] bytes=288 recall=82.080000

PQ_GREEDY_EVAL tag=it28_b1_plus8 alloc=[64, 64, 48, 32, 16, 16, 24, 24] bytes=288 recall=81.790000

PQ_GREEDY_EVAL tag=it28_b2_plus8 alloc=[64, 56, 56, 32, 16, 16, 24, 24] bytes=288 recall=81.885000

PQ_GREEDY_EVAL tag=it28_b3_plus8 alloc=[64, 56, 48, 40, 16, 16, 24, 24] bytes=288 recall=81.950000

PQ_GREEDY_EVAL tag=it28_b4_plus8 alloc=[64, 56, 48, 32, 24, 16, 24, 24] bytes=288 recall=81.777500

PQ_GREEDY_EVAL tag=it28_b5_plus8 alloc=[64, 56, 48, 32, 16, 24, 24, 24] bytes=288 recall=81.895000

PQ_GREEDY_EVAL tag=it28_b6_plus8 alloc=[64, 56, 48, 32, 16, 16, 32, 24] bytes=288 recall=81.820000

PQ_GREEDY_EVAL tag=it28_b7_plus8 alloc=[64, 56, 48, 32, 16, 16, 24, 32] bytes=288 recall=81.882500

PQ_GREEDY_EVAL tag=it29_b0_plus8 alloc=[80, 56, 48, 32, 16, 16, 24, 24] bytes=296 recall=82.067500

PQ_GREEDY_EVAL tag=it29_b1_plus8 alloc=[72, 64, 48, 32, 16, 16, 24, 24] bytes=296 recall=82.097500

PQ_GREEDY_EVAL tag=it29_b2_plus8 alloc=[72, 56, 56, 32, 16, 16, 24, 24] bytes=296 recall=82.145000

PQ_GREEDY_EVAL tag=it29_b3_plus8 alloc=[72, 56, 48, 40, 16, 16, 24, 24] bytes=296 recall=82.175000

PQ_GREEDY_EVAL tag=it29_b4_plus8 alloc=[72, 56, 48, 32, 24, 16, 24, 24] bytes=296 recall=82.270000

PQ_GREEDY_EVAL tag=it29_b5_plus8 alloc=[72, 56, 48, 32, 16, 24, 24, 24] bytes=296 recall=82.285000

PQ_GREEDY_EVAL tag=it29_b6_plus8 alloc=[72, 56, 48, 32, 16, 16, 32, 24] bytes=296 recall=82.335000

PQ_GREEDY_EVAL tag=it29_b7_plus8 alloc=[72, 56, 48, 32, 16, 16, 24, 32] bytes=296 recall=82.297500

PQ_GREEDY_EVAL tag=it30_b0_plus8 alloc=[80, 56, 48, 32, 16, 16, 32, 24] bytes=304 recall=82.377500

PQ_GREEDY_EVAL tag=it30_b1_plus8 alloc=[72, 64, 48, 32, 16, 16, 32, 24] bytes=304 recall=82.832500

PQ_GREEDY_EVAL tag=it30_b2_plus8 alloc=[72, 56, 56, 32, 16, 16, 32, 24] bytes=304 recall=82.527500

PQ_GREEDY_EVAL tag=it30_b3_plus8 alloc=[72, 56, 48, 40, 16, 16, 32, 24] bytes=304 recall=82.512500

PQ_GREEDY_EVAL tag=it30_b4_plus8 alloc=[72, 56, 48, 32, 24, 16, 32, 24] bytes=304 recall=82.612500

PQ_GREEDY_EVAL tag=it30_b5_plus8 alloc=[72, 56, 48, 32, 16, 24, 32, 24] bytes=304 recall=82.875000

PQ_GREEDY_EVAL tag=it30_b6_plus8 alloc=[72, 56, 48, 32, 16, 16, 40, 24] bytes=304 recall=82.652500

PQ_GREEDY_EVAL tag=it30_b7_plus8 alloc=[72, 56, 48, 32, 16, 16, 32, 32] bytes=304 recall=82.275000

PQ_GREEDY_EVAL tag=it31_b0_plus8 alloc=[80, 56, 48, 32, 16, 24, 32, 24] bytes=312 recall=83.087500

PQ_GREEDY_EVAL tag=it31_b1_plus8 alloc=[72, 64, 48, 32, 16, 24, 32, 24] bytes=312 recall=82.895000

PQ_GREEDY_EVAL tag=it31_b2_plus8 alloc=[72, 56, 56, 32, 16, 24, 32, 24] bytes=312 recall=82.772500

PQ_GREEDY_EVAL tag=it31_b3_plus8 alloc=[72, 56, 48, 40, 16, 24, 32, 24] bytes=312 recall=82.772500

PQ_GREEDY_EVAL tag=it31_b4_plus8 alloc=[72, 56, 48, 32, 24, 24, 32, 24] bytes=312 recall=82.855000

PQ_GREEDY_EVAL tag=it31_b5_plus8 alloc=[72, 56, 48, 32, 16, 32, 32, 24] bytes=312 recall=82.567500

PQ_GREEDY_EVAL tag=it31_b6_plus8 alloc=[72, 56, 48, 32, 16, 24, 40, 24] bytes=312 recall=82.545000

PQ_GREEDY_EVAL tag=it31_b7_plus8 alloc=[72, 56, 48, 32, 16, 24, 32, 32] bytes=312 recall=82.822500

PQ_GREEDY_EVAL tag=it32_b0_plus8 alloc=[88, 56, 48, 32, 16, 24, 32, 24] bytes=320 recall=83.135000

PQ_GREEDY_EVAL tag=it32_b1_plus8 alloc=[80, 64, 48, 32, 16, 24, 32, 24] bytes=320 recall=83.210000

PQ_GREEDY_EVAL tag=it32_b2_plus8 alloc=[80, 56, 56, 32, 16, 24, 32, 24] bytes=320 recall=83.017500

PQ_GREEDY_EVAL tag=it32_b3_plus8 alloc=[80, 56, 48, 40, 16, 24, 32, 24] bytes=320 recall=83.275000

PQ_GREEDY_EVAL tag=it32_b4_plus8 alloc=[80, 56, 48, 32, 24, 24, 32, 24] bytes=320 recall=83.040000

PQ_GREEDY_EVAL tag=it32_b5_plus8 alloc=[80, 56, 48, 32, 16, 32, 32, 24] bytes=320 recall=83.095000

PQ_GREEDY_EVAL tag=it32_b6_plus8 alloc=[80, 56, 48, 32, 16, 24, 40, 24] bytes=320 recall=83.150000

PQ_GREEDY_EVAL tag=it32_b7_plus8 alloc=[80, 56, 48, 32, 16, 24, 32, 32] bytes=320 recall=83.117500

PQ_GREEDY_EVAL tag=it33_b0_plus8 alloc=[88, 56, 48, 40, 16, 24, 32, 24] bytes=328 recall=83.667500

PQ_GREEDY_EVAL tag=it33_b1_plus8 alloc=[80, 64, 48, 40, 16, 24, 32, 24] bytes=328 recall=83.470000

PQ_GREEDY_EVAL tag=it33_b2_plus8 alloc=[80, 56, 56, 40, 16, 24, 32, 24] bytes=328 recall=83.507500

PQ_GREEDY_EVAL tag=it33_b3_plus8 alloc=[80, 56, 48, 48, 16, 24, 32, 24] bytes=328 recall=83.615000

PQ_GREEDY_EVAL tag=it33_b4_plus8 alloc=[80, 56, 48, 40, 24, 24, 32, 24] bytes=328 recall=83.430000

PQ_GREEDY_EVAL tag=it33_b5_plus8 alloc=[80, 56, 48, 40, 16, 32, 32, 24] bytes=328 recall=83.452500

PQ_GREEDY_EVAL tag=it33_b6_plus8 alloc=[80, 56, 48, 40, 16, 24, 40, 24] bytes=328 recall=83.295000

PQ_GREEDY_EVAL tag=it33_b7_plus8 alloc=[80, 56, 48, 40, 16, 24, 32, 32] bytes=328 recall=83.535000

PQ_GREEDY_EVAL tag=it34_b0_plus8 alloc=[96, 56, 48, 40, 16, 24, 32, 24] bytes=336 recall=83.620000

PQ_GREEDY_EVAL tag=it34_b1_plus8 alloc=[88, 64, 48, 40, 16, 24, 32, 24] bytes=336 recall=83.665000

PQ_GREEDY_EVAL tag=it34_b2_plus8 alloc=[88, 56, 56, 40, 16, 24, 32, 24] bytes=336 recall=83.720000

PQ_GREEDY_EVAL tag=it34_b3_plus8 alloc=[88, 56, 48, 48, 16, 24, 32, 24] bytes=336 recall=83.535000

PQ_GREEDY_EVAL tag=it34_b4_plus8 alloc=[88, 56, 48, 40, 24, 24, 32, 24] bytes=336 recall=83.812500

PQ_GREEDY_EVAL tag=it34_b5_plus8 alloc=[88, 56, 48, 40, 16, 32, 32, 24] bytes=336 recall=83.510000

PQ_GREEDY_EVAL tag=it34_b6_plus8 alloc=[88, 56, 48, 40, 16, 24, 40, 24] bytes=336 recall=83.812500

PQ_GREEDY_EVAL tag=it34_b7_plus8 alloc=[88, 56, 48, 40, 16, 24, 32, 32] bytes=336 recall=83.647500

PQ_GREEDY_EVAL tag=it35_b0_plus8 alloc=[96, 56, 48, 40, 16, 24, 40, 24] bytes=344 recall=83.857500

PQ_GREEDY_EVAL tag=it35_b1_plus8 alloc=[88, 64, 48, 40, 16, 24, 40, 24] bytes=344 recall=84.007500

PQ_GREEDY_EVAL tag=it35_b2_plus8 alloc=[88, 56, 56, 40, 16, 24, 40, 24] bytes=344 recall=83.772500

PQ_GREEDY_EVAL tag=it35_b3_plus8 alloc=[88, 56, 48, 48, 16, 24, 40, 24] bytes=344 recall=83.850000

PQ_GREEDY_EVAL tag=it35_b4_plus8 alloc=[88, 56, 48, 40, 24, 24, 40, 24] bytes=344 recall=83.910000

PQ_GREEDY_EVAL tag=it35_b5_plus8 alloc=[88, 56, 48, 40, 16, 32, 40, 24] bytes=344 recall=83.735000

PQ_GREEDY_EVAL tag=it35_b6_plus8 alloc=[88, 56, 48, 40, 16, 24, 48, 24] bytes=344 recall=83.772500

PQ_GREEDY_EVAL tag=it35_b7_plus8 alloc=[88, 56, 48, 40, 16, 24, 40, 32] bytes=344 recall=83.957500

PQ_GREEDY_EVAL tag=it36_b0_plus8 alloc=[96, 64, 48, 40, 16, 24, 40, 24] bytes=352 recall=84.030000

PQ_GREEDY_EVAL tag=it36_b1_plus8 alloc=[88, 72, 48, 40, 16, 24, 40, 24] bytes=352 recall=84.127500

PQ_GREEDY_EVAL tag=it36_b2_plus8 alloc=[88, 64, 56, 40, 16, 24, 40, 24] bytes=352 recall=84.202500

PQ_GREEDY_EVAL tag=it36_b3_plus8 alloc=[88, 64, 48, 48, 16, 24, 40, 24] bytes=352 recall=84.340000

PQ_GREEDY_EVAL tag=it36_b4_plus8 alloc=[88, 64, 48, 40, 24, 24, 40, 24] bytes=352 recall=84.320000

PQ_GREEDY_EVAL tag=it36_b5_plus8 alloc=[88, 64, 48, 40, 16, 32, 40, 24] bytes=352 recall=84.155000

PQ_GREEDY_EVAL tag=it36_b6_plus8 alloc=[88, 64, 48, 40, 16, 24, 48, 24] bytes=352 recall=84.102500

PQ_GREEDY_EVAL tag=it36_b7_plus8 alloc=[88, 64, 48, 40, 16, 24, 40, 32] bytes=352 recall=84.047500

PQ_GREEDY_EVAL tag=it37_b0_plus8 alloc=[96, 64, 48, 48, 16, 24, 40, 24] bytes=360 recall=84.490000

PQ_GREEDY_EVAL tag=it37_b1_plus8 alloc=[88, 72, 48, 48, 16, 24, 40, 24] bytes=360 recall=84.415000

PQ_GREEDY_EVAL tag=it37_b2_plus8 alloc=[88, 64, 56, 48, 16, 24, 40, 24] bytes=360 recall=84.562500

PQ_GREEDY_EVAL tag=it37_b3_plus8 alloc=[88, 64, 48, 56, 16, 24, 40, 24] bytes=360 recall=84.445000

PQ_GREEDY_EVAL tag=it37_b4_plus8 alloc=[88, 64, 48, 48, 24, 24, 40, 24] bytes=360 recall=84.455000

PQ_GREEDY_EVAL tag=it37_b5_plus8 alloc=[88, 64, 48, 48, 16, 32, 40, 24] bytes=360 recall=84.415000

PQ_GREEDY_EVAL tag=it37_b6_plus8 alloc=[88, 64, 48, 48, 16, 24, 48, 24] bytes=360 recall=84.067500

PQ_GREEDY_EVAL tag=it37_b7_plus8 alloc=[88, 64, 48, 48, 16, 24, 40, 32] bytes=360 recall=84.337500

PQ_GREEDY_EVAL tag=it38_b0_plus8 alloc=[96, 64, 56, 48, 16, 24, 40, 24] bytes=368 recall=84.687500

PQ_GREEDY_EVAL tag=it38_b1_plus8 alloc=[88, 72, 56, 48, 16, 24, 40, 24] bytes=368 recall=84.847500

PQ_GREEDY_EVAL tag=it38_b2_plus8 alloc=[88, 64, 64, 48, 16, 24, 40, 24] bytes=368 recall=84.762500

PQ_GREEDY_EVAL tag=it38_b3_plus8 alloc=[88, 64, 56, 56, 16, 24, 40, 24] bytes=368 recall=84.812500

PQ_GREEDY_EVAL tag=it38_b4_plus8 alloc=[88, 64, 56, 48, 24, 24, 40, 24] bytes=368 recall=84.697500

PQ_GREEDY_EVAL tag=it38_b5_plus8 alloc=[88, 64, 56, 48, 16, 32, 40, 24] bytes=368 recall=84.422500

PQ_GREEDY_EVAL tag=it38_b6_plus8 alloc=[88, 64, 56, 48, 16, 24, 48, 24] bytes=368 recall=84.657500

PQ_GREEDY_EVAL tag=it38_b7_plus8 alloc=[88, 64, 56, 48, 16, 24, 40, 32] bytes=368 recall=84.642500

PQ_GREEDY_EVAL tag=it39_b0_plus8 alloc=[96, 72, 56, 48, 16, 24, 40, 24] bytes=376 recall=85.027500

PQ_GREEDY_EVAL tag=it39_b1_plus8 alloc=[88, 80, 56, 48, 16, 24, 40, 24] bytes=376 recall=84.885000

PQ_GREEDY_EVAL tag=it39_b2_plus8 alloc=[88, 72, 64, 48, 16, 24, 40, 24] bytes=376 recall=84.907500

PQ_GREEDY_EVAL tag=it39_b3_plus8 alloc=[88, 72, 56, 56, 16, 24, 40, 24] bytes=376 recall=85.095000

PQ_GREEDY_EVAL tag=it39_b4_plus8 alloc=[88, 72, 56, 48, 24, 24, 40, 24] bytes=376 recall=84.932500

PQ_GREEDY_EVAL tag=it39_b5_plus8 alloc=[88, 72, 56, 48, 16, 32, 40, 24] bytes=376 recall=84.917500

PQ_GREEDY_EVAL tag=it39_b6_plus8 alloc=[88, 72, 56, 48, 16, 24, 48, 24] bytes=376 recall=85.062500

PQ_GREEDY_EVAL tag=it39_b7_plus8 alloc=[88, 72, 56, 48, 16, 24, 40, 32] bytes=376 recall=85.032500

PQ_GREEDY_EVAL tag=it40_b0_plus8 alloc=[96, 72, 56, 56, 16, 24, 40, 24] bytes=384 recall=85.185000

PQ_GREEDY_EVAL tag=it40_b1_plus8 alloc=[88, 80, 56, 56, 16, 24, 40, 24] bytes=384 recall=85.267500

PQ_GREEDY_EVAL tag=it40_b2_plus8 alloc=[88, 72, 64, 56, 16, 24, 40, 24] bytes=384 recall=85.295000

PQ_GREEDY_EVAL tag=it40_b3_plus8 alloc=[88, 72, 56, 64, 16, 24, 40, 24] bytes=384 recall=85.182500

PQ_GREEDY_EVAL tag=it40_b4_plus8 alloc=[88, 72, 56, 56, 24, 24, 40, 24] bytes=384 recall=85.245000

PQ_GREEDY_EVAL tag=it40_b5_plus8 alloc=[88, 72, 56, 56, 16, 32, 40, 24] bytes=384 recall=85.172500

PQ_GREEDY_EVAL tag=it40_b6_plus8 alloc=[88, 72, 56, 56, 16, 24, 48, 24] bytes=384 recall=85.230000

PQ_GREEDY_EVAL tag=it40_b7_plus8 alloc=[88, 72, 56, 56, 16, 24, 40, 32] bytes=384 recall=85.112500

### DBPedia Cohere v4
#### Variable PQ

PQ_GREEDY_EVAL tag=init alloc=[8, 8, 8, 8, 8, 8, 8, 8] bytes=64 recall=49.190000

PQ_GREEDY_EVAL tag=it1_b0_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 8] bytes=72 recall=52.835000

PQ_GREEDY_EVAL tag=it1_b1_plus8 alloc=[8, 16, 8, 8, 8, 8, 8, 8] bytes=72 recall=52.050000

PQ_GREEDY_EVAL tag=it1_b2_plus8 alloc=[8, 8, 16, 8, 8, 8, 8, 8] bytes=72 recall=52.082500

PQ_GREEDY_EVAL tag=it1_b3_plus8 alloc=[8, 8, 8, 16, 8, 8, 8, 8] bytes=72 recall=51.930000

PQ_GREEDY_EVAL tag=it1_b4_plus8 alloc=[8, 8, 8, 8, 16, 8, 8, 8] bytes=72 recall=52.570000

PQ_GREEDY_EVAL tag=it1_b5_plus8 alloc=[8, 8, 8, 8, 8, 16, 8, 8] bytes=72 recall=51.780000

PQ_GREEDY_EVAL tag=it1_b6_plus8 alloc=[8, 8, 8, 8, 8, 8, 16, 8] bytes=72 recall=51.527500

PQ_GREEDY_EVAL tag=it1_b7_plus8 alloc=[8, 8, 8, 8, 8, 8, 8, 16] bytes=72 recall=51.345000

PQ_GREEDY_EVAL tag=it2_b0_plus8 alloc=[24, 8, 8, 8, 8, 8, 8, 8] bytes=80 recall=54.670000

PQ_GREEDY_EVAL tag=it2_b1_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 8] bytes=80 recall=55.167500

PQ_GREEDY_EVAL tag=it2_b2_plus8 alloc=[16, 8, 16, 8, 8, 8, 8, 8] bytes=80 recall=55.917500

PQ_GREEDY_EVAL tag=it2_b3_plus8 alloc=[16, 8, 8, 16, 8, 8, 8, 8] bytes=80 recall=55.357500

PQ_GREEDY_EVAL tag=it2_b4_plus8 alloc=[16, 8, 8, 8, 16, 8, 8, 8] bytes=80 recall=55.152500

PQ_GREEDY_EVAL tag=it2_b5_plus8 alloc=[16, 8, 8, 8, 8, 16, 8, 8] bytes=80 recall=54.667500

PQ_GREEDY_EVAL tag=it2_b6_plus8 alloc=[16, 8, 8, 8, 8, 8, 16, 8] bytes=80 recall=54.555000

PQ_GREEDY_EVAL tag=it2_b7_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 16] bytes=80 recall=54.702500

PQ_GREEDY_EVAL tag=it3_b0_plus8 alloc=[24, 8, 16, 8, 8, 8, 8, 8] bytes=88 recall=57.130000

PQ_GREEDY_EVAL tag=it3_b1_plus8 alloc=[16, 16, 16, 8, 8, 8, 8, 8] bytes=88 recall=57.997500

PQ_GREEDY_EVAL tag=it3_b2_plus8 alloc=[16, 8, 24, 8, 8, 8, 8, 8] bytes=88 recall=57.457500

PQ_GREEDY_EVAL tag=it3_b3_plus8 alloc=[16, 8, 16, 16, 8, 8, 8, 8] bytes=88 recall=57.910000

PQ_GREEDY_EVAL tag=it3_b4_plus8 alloc=[16, 8, 16, 8, 16, 8, 8, 8] bytes=88 recall=57.777500

PQ_GREEDY_EVAL tag=it3_b5_plus8 alloc=[16, 8, 16, 8, 8, 16, 8, 8] bytes=88 recall=57.327500

PQ_GREEDY_EVAL tag=it3_b6_plus8 alloc=[16, 8, 16, 8, 8, 8, 16, 8] bytes=88 recall=57.082500

PQ_GREEDY_EVAL tag=it3_b7_plus8 alloc=[16, 8, 16, 8, 8, 8, 8, 16] bytes=88 recall=57.512500

PQ_GREEDY_EVAL tag=it4_b0_plus8 alloc=[24, 16, 16, 8, 8, 8, 8, 8] bytes=96 recall=59.630000

PQ_GREEDY_EVAL tag=it4_b1_plus8 alloc=[16, 24, 16, 8, 8, 8, 8, 8] bytes=96 recall=59.337500

PQ_GREEDY_EVAL tag=it4_b2_plus8 alloc=[16, 16, 24, 8, 8, 8, 8, 8] bytes=96 recall=59.540000

PQ_GREEDY_EVAL tag=it4_b3_plus8 alloc=[16, 16, 16, 16, 8, 8, 8, 8] bytes=96 recall=60.262500

PQ_GREEDY_EVAL tag=it4_b4_plus8 alloc=[16, 16, 16, 8, 16, 8, 8, 8] bytes=96 recall=60.420000

PQ_GREEDY_EVAL tag=it4_b5_plus8 alloc=[16, 16, 16, 8, 8, 16, 8, 8] bytes=96 recall=59.732500

PQ_GREEDY_EVAL tag=it4_b6_plus8 alloc=[16, 16, 16, 8, 8, 8, 16, 8] bytes=96 recall=59.777500

PQ_GREEDY_EVAL tag=it4_b7_plus8 alloc=[16, 16, 16, 8, 8, 8, 8, 16] bytes=96 recall=59.547500

PQ_GREEDY_EVAL tag=it5_b0_plus8 alloc=[24, 16, 16, 8, 16, 8, 8, 8] bytes=104 recall=61.325000

PQ_GREEDY_EVAL tag=it5_b1_plus8 alloc=[16, 24, 16, 8, 16, 8, 8, 8] bytes=104 recall=61.582500

PQ_GREEDY_EVAL tag=it5_b2_plus8 alloc=[16, 16, 24, 8, 16, 8, 8, 8] bytes=104 recall=61.282500

PQ_GREEDY_EVAL tag=it5_b3_plus8 alloc=[16, 16, 16, 16, 16, 8, 8, 8] bytes=104 recall=62.115000

PQ_GREEDY_EVAL tag=it5_b4_plus8 alloc=[16, 16, 16, 8, 24, 8, 8, 8] bytes=104 recall=61.282500

PQ_GREEDY_EVAL tag=it5_b5_plus8 alloc=[16, 16, 16, 8, 16, 16, 8, 8] bytes=104 recall=61.620000

PQ_GREEDY_EVAL tag=it5_b6_plus8 alloc=[16, 16, 16, 8, 16, 8, 16, 8] bytes=104 recall=61.587500

PQ_GREEDY_EVAL tag=it5_b7_plus8 alloc=[16, 16, 16, 8, 16, 8, 8, 16] bytes=104 recall=61.575000

PQ_GREEDY_EVAL tag=it6_b0_plus8 alloc=[24, 16, 16, 16, 16, 8, 8, 8] bytes=112 recall=63.185000

PQ_GREEDY_EVAL tag=it6_b1_plus8 alloc=[16, 24, 16, 16, 16, 8, 8, 8] bytes=112 recall=63.270000

PQ_GREEDY_EVAL tag=it6_b2_plus8 alloc=[16, 16, 24, 16, 16, 8, 8, 8] bytes=112 recall=63.355000

PQ_GREEDY_EVAL tag=it6_b3_plus8 alloc=[16, 16, 16, 24, 16, 8, 8, 8] bytes=112 recall=63.247500

PQ_GREEDY_EVAL tag=it6_b4_plus8 alloc=[16, 16, 16, 16, 24, 8, 8, 8] bytes=112 recall=63.162500

PQ_GREEDY_EVAL tag=it6_b5_plus8 alloc=[16, 16, 16, 16, 16, 16, 8, 8] bytes=112 recall=63.202500

PQ_GREEDY_EVAL tag=it6_b6_plus8 alloc=[16, 16, 16, 16, 16, 8, 16, 8] bytes=112 recall=63.285000

PQ_GREEDY_EVAL tag=it6_b7_plus8 alloc=[16, 16, 16, 16, 16, 8, 8, 16] bytes=112 recall=63.220000

PQ_GREEDY_EVAL tag=it7_b0_plus8 alloc=[24, 16, 24, 16, 16, 8, 8, 8] bytes=120 recall=64.567500

PQ_GREEDY_EVAL tag=it7_b1_plus8 alloc=[16, 24, 24, 16, 16, 8, 8, 8] bytes=120 recall=64.527500

PQ_GREEDY_EVAL tag=it7_b2_plus8 alloc=[16, 16, 32, 16, 16, 8, 8, 8] bytes=120 recall=64.170000

PQ_GREEDY_EVAL tag=it7_b3_plus8 alloc=[16, 16, 24, 24, 16, 8, 8, 8] bytes=120 recall=64.507500

PQ_GREEDY_EVAL tag=it7_b4_plus8 alloc=[16, 16, 24, 16, 24, 8, 8, 8] bytes=120 recall=64.372500

PQ_GREEDY_EVAL tag=it7_b5_plus8 alloc=[16, 16, 24, 16, 16, 16, 8, 8] bytes=120 recall=65.010000

PQ_GREEDY_EVAL tag=it7_b6_plus8 alloc=[16, 16, 24, 16, 16, 8, 16, 8] bytes=120 recall=64.377500

PQ_GREEDY_EVAL tag=it7_b7_plus8 alloc=[16, 16, 24, 16, 16, 8, 8, 16] bytes=120 recall=64.745000

PQ_GREEDY_EVAL tag=it8_b0_plus8 alloc=[24, 16, 24, 16, 16, 16, 8, 8] bytes=128 recall=65.892500

PQ_GREEDY_EVAL tag=it8_b1_plus8 alloc=[16, 24, 24, 16, 16, 16, 8, 8] bytes=128 recall=65.925000

PQ_GREEDY_EVAL tag=it8_b2_plus8 alloc=[16, 16, 32, 16, 16, 16, 8, 8] bytes=128 recall=65.392500

PQ_GREEDY_EVAL tag=it8_b3_plus8 alloc=[16, 16, 24, 24, 16, 16, 8, 8] bytes=128 recall=65.567500

PQ_GREEDY_EVAL tag=it8_b4_plus8 alloc=[16, 16, 24, 16, 24, 16, 8, 8] bytes=128 recall=66.152500

PQ_GREEDY_EVAL tag=it8_b5_plus8 alloc=[16, 16, 24, 16, 16, 24, 8, 8] bytes=128 recall=65.635000

PQ_GREEDY_EVAL tag=it8_b6_plus8 alloc=[16, 16, 24, 16, 16, 16, 16, 8] bytes=128 recall=65.705000

PQ_GREEDY_EVAL tag=it8_b7_plus8 alloc=[16, 16, 24, 16, 16, 16, 8, 16] bytes=128 recall=65.532500

PQ_GREEDY_EVAL tag=it9_b0_plus8 alloc=[24, 16, 24, 16, 24, 16, 8, 8] bytes=136 recall=66.980000

PQ_GREEDY_EVAL tag=it9_b1_plus8 alloc=[16, 24, 24, 16, 24, 16, 8, 8] bytes=136 recall=67.202500

PQ_GREEDY_EVAL tag=it9_b2_plus8 alloc=[16, 16, 32, 16, 24, 16, 8, 8] bytes=136 recall=66.927500

PQ_GREEDY_EVAL tag=it9_b3_plus8 alloc=[16, 16, 24, 24, 24, 16, 8, 8] bytes=136 recall=66.682500

PQ_GREEDY_EVAL tag=it9_b4_plus8 alloc=[16, 16, 24, 16, 32, 16, 8, 8] bytes=136 recall=66.690000

PQ_GREEDY_EVAL tag=it9_b5_plus8 alloc=[16, 16, 24, 16, 24, 24, 8, 8] bytes=136 recall=66.717500

PQ_GREEDY_EVAL tag=it9_b6_plus8 alloc=[16, 16, 24, 16, 24, 16, 16, 8] bytes=136 recall=67.232500

PQ_GREEDY_EVAL tag=it9_b7_plus8 alloc=[16, 16, 24, 16, 24, 16, 8, 16] bytes=136 recall=66.832500

PQ_GREEDY_EVAL tag=it10_b0_plus8 alloc=[24, 16, 24, 16, 24, 16, 16, 8] bytes=144 recall=68.132500

PQ_GREEDY_EVAL tag=it10_b1_plus8 alloc=[16, 24, 24, 16, 24, 16, 16, 8] bytes=144 recall=68.002500

PQ_GREEDY_EVAL tag=it10_b2_plus8 alloc=[16, 16, 32, 16, 24, 16, 16, 8] bytes=144 recall=68.075000

PQ_GREEDY_EVAL tag=it10_b3_plus8 alloc=[16, 16, 24, 24, 24, 16, 16, 8] bytes=144 recall=67.837500

PQ_GREEDY_EVAL tag=it10_b4_plus8 alloc=[16, 16, 24, 16, 32, 16, 16, 8] bytes=144 recall=67.727500

PQ_GREEDY_EVAL tag=it10_b5_plus8 alloc=[16, 16, 24, 16, 24, 24, 16, 8] bytes=144 recall=67.777500

PQ_GREEDY_EVAL tag=it10_b6_plus8 alloc=[16, 16, 24, 16, 24, 16, 24, 8] bytes=144 recall=67.690000

PQ_GREEDY_EVAL tag=it10_b7_plus8 alloc=[16, 16, 24, 16, 24, 16, 16, 16] bytes=144 recall=68.007500

PQ_GREEDY_EVAL tag=it11_b0_plus8 alloc=[32, 16, 24, 16, 24, 16, 16, 8] bytes=152 recall=69.182500

PQ_GREEDY_EVAL tag=it11_b1_plus8 alloc=[24, 24, 24, 16, 24, 16, 16, 8] bytes=152 recall=69.030000

PQ_GREEDY_EVAL tag=it11_b2_plus8 alloc=[24, 16, 32, 16, 24, 16, 16, 8] bytes=152 recall=69.227500

PQ_GREEDY_EVAL tag=it11_b3_plus8 alloc=[24, 16, 24, 24, 24, 16, 16, 8] bytes=152 recall=68.840000

PQ_GREEDY_EVAL tag=it11_b4_plus8 alloc=[24, 16, 24, 16, 32, 16, 16, 8] bytes=152 recall=68.950000

PQ_GREEDY_EVAL tag=it11_b5_plus8 alloc=[24, 16, 24, 16, 24, 24, 16, 8] bytes=152 recall=68.955000

PQ_GREEDY_EVAL tag=it11_b6_plus8 alloc=[24, 16, 24, 16, 24, 16, 24, 8] bytes=152 recall=69.062500

PQ_GREEDY_EVAL tag=it11_b7_plus8 alloc=[24, 16, 24, 16, 24, 16, 16, 16] bytes=152 recall=68.800000

PQ_GREEDY_EVAL tag=it12_b0_plus8 alloc=[32, 16, 32, 16, 24, 16, 16, 8] bytes=160 recall=69.577500

PQ_GREEDY_EVAL tag=it12_b1_plus8 alloc=[24, 24, 32, 16, 24, 16, 16, 8] bytes=160 recall=70.362500

PQ_GREEDY_EVAL tag=it12_b2_plus8 alloc=[24, 16, 40, 16, 24, 16, 16, 8] bytes=160 recall=69.580000

PQ_GREEDY_EVAL tag=it12_b3_plus8 alloc=[24, 16, 32, 24, 24, 16, 16, 8] bytes=160 recall=69.970000

PQ_GREEDY_EVAL tag=it12_b4_plus8 alloc=[24, 16, 32, 16, 32, 16, 16, 8] bytes=160 recall=69.752500

PQ_GREEDY_EVAL tag=it12_b5_plus8 alloc=[24, 16, 32, 16, 24, 24, 16, 8] bytes=160 recall=69.592500

PQ_GREEDY_EVAL tag=it12_b6_plus8 alloc=[24, 16, 32, 16, 24, 16, 24, 8] bytes=160 recall=69.887500

PQ_GREEDY_EVAL tag=it12_b7_plus8 alloc=[24, 16, 32, 16, 24, 16, 16, 16] bytes=160 recall=70.147500

PQ_GREEDY_EVAL tag=it13_b0_plus8 alloc=[32, 24, 32, 16, 24, 16, 16, 8] bytes=168 recall=70.797500

PQ_GREEDY_EVAL tag=it13_b1_plus8 alloc=[24, 32, 32, 16, 24, 16, 16, 8] bytes=168 recall=71.115000

PQ_GREEDY_EVAL tag=it13_b2_plus8 alloc=[24, 24, 40, 16, 24, 16, 16, 8] bytes=168 recall=70.417500

PQ_GREEDY_EVAL tag=it13_b3_plus8 alloc=[24, 24, 32, 24, 24, 16, 16, 8] bytes=168 recall=70.800000

PQ_GREEDY_EVAL tag=it13_b4_plus8 alloc=[24, 24, 32, 16, 32, 16, 16, 8] bytes=168 recall=71.032500

PQ_GREEDY_EVAL tag=it13_b5_plus8 alloc=[24, 24, 32, 16, 24, 24, 16, 8] bytes=168 recall=70.967500

PQ_GREEDY_EVAL tag=it13_b6_plus8 alloc=[24, 24, 32, 16, 24, 16, 24, 8] bytes=168 recall=70.507500

PQ_GREEDY_EVAL tag=it13_b7_plus8 alloc=[24, 24, 32, 16, 24, 16, 16, 16] bytes=168 recall=70.857500

PQ_GREEDY_EVAL tag=it14_b0_plus8 alloc=[32, 32, 32, 16, 24, 16, 16, 8] bytes=176 recall=71.785000

PQ_GREEDY_EVAL tag=it14_b1_plus8 alloc=[24, 40, 32, 16, 24, 16, 16, 8] bytes=176 recall=71.380000

PQ_GREEDY_EVAL tag=it14_b2_plus8 alloc=[24, 32, 40, 16, 24, 16, 16, 8] bytes=176 recall=71.372500

PQ_GREEDY_EVAL tag=it14_b3_plus8 alloc=[24, 32, 32, 24, 24, 16, 16, 8] bytes=176 recall=71.800000

PQ_GREEDY_EVAL tag=it14_b4_plus8 alloc=[24, 32, 32, 16, 32, 16, 16, 8] bytes=176 recall=71.885000

PQ_GREEDY_EVAL tag=it14_b5_plus8 alloc=[24, 32, 32, 16, 24, 24, 16, 8] bytes=176 recall=71.890000

PQ_GREEDY_EVAL tag=it14_b6_plus8 alloc=[24, 32, 32, 16, 24, 16, 24, 8] bytes=176 recall=71.622500

PQ_GREEDY_EVAL tag=it14_b7_plus8 alloc=[24, 32, 32, 16, 24, 16, 16, 16] bytes=176 recall=71.902500

PQ_GREEDY_EVAL tag=it15_b0_plus8 alloc=[32, 32, 32, 16, 24, 16, 16, 16] bytes=184 recall=72.745000

PQ_GREEDY_EVAL tag=it15_b1_plus8 alloc=[24, 40, 32, 16, 24, 16, 16, 16] bytes=184 recall=72.670000

PQ_GREEDY_EVAL tag=it15_b2_plus8 alloc=[24, 32, 40, 16, 24, 16, 16, 16] bytes=184 recall=72.737500

PQ_GREEDY_EVAL tag=it15_b3_plus8 alloc=[24, 32, 32, 24, 24, 16, 16, 16] bytes=184 recall=72.815000

PQ_GREEDY_EVAL tag=it15_b4_plus8 alloc=[24, 32, 32, 16, 32, 16, 16, 16] bytes=184 recall=72.625000

PQ_GREEDY_EVAL tag=it15_b5_plus8 alloc=[24, 32, 32, 16, 24, 24, 16, 16] bytes=184 recall=72.465000

PQ_GREEDY_EVAL tag=it15_b6_plus8 alloc=[24, 32, 32, 16, 24, 16, 24, 16] bytes=184 recall=72.697500

PQ_GREEDY_EVAL tag=it15_b7_plus8 alloc=[24, 32, 32, 16, 24, 16, 16, 24] bytes=184 recall=72.302500

PQ_GREEDY_EVAL tag=it16_b0_plus8 alloc=[32, 32, 32, 24, 24, 16, 16, 16] bytes=192 recall=73.310000

PQ_GREEDY_EVAL tag=it16_b1_plus8 alloc=[24, 40, 32, 24, 24, 16, 16, 16] bytes=192 recall=73.265000

PQ_GREEDY_EVAL tag=it16_b2_plus8 alloc=[24, 32, 40, 24, 24, 16, 16, 16] bytes=192 recall=73.372500

PQ_GREEDY_EVAL tag=it16_b3_plus8 alloc=[24, 32, 32, 32, 24, 16, 16, 16] bytes=192 recall=73.297500

PQ_GREEDY_EVAL tag=it16_b4_plus8 alloc=[24, 32, 32, 24, 32, 16, 16, 16] bytes=192 recall=73.292500

PQ_GREEDY_EVAL tag=it16_b5_plus8 alloc=[24, 32, 32, 24, 24, 24, 16, 16] bytes=192 recall=73.565000

PQ_GREEDY_EVAL tag=it16_b6_plus8 alloc=[24, 32, 32, 24, 24, 16, 24, 16] bytes=192 recall=73.512500

PQ_GREEDY_EVAL tag=it16_b7_plus8 alloc=[24, 32, 32, 24, 24, 16, 16, 24] bytes=192 recall=73.435000

PQ_GREEDY_EVAL tag=it17_b0_plus8 alloc=[32, 32, 32, 24, 24, 24, 16, 16] bytes=200 recall=74.120000

PQ_GREEDY_EVAL tag=it17_b1_plus8 alloc=[24, 40, 32, 24, 24, 24, 16, 16] bytes=200 recall=74.247500

PQ_GREEDY_EVAL tag=it17_b2_plus8 alloc=[24, 32, 40, 24, 24, 24, 16, 16] bytes=200 recall=73.935000

PQ_GREEDY_EVAL tag=it17_b3_plus8 alloc=[24, 32, 32, 32, 24, 24, 16, 16] bytes=200 recall=74.147500

PQ_GREEDY_EVAL tag=it17_b4_plus8 alloc=[24, 32, 32, 24, 32, 24, 16, 16] bytes=200 recall=74.217500

PQ_GREEDY_EVAL tag=it17_b5_plus8 alloc=[24, 32, 32, 24, 24, 32, 16, 16] bytes=200 recall=74.132500

PQ_GREEDY_EVAL tag=it17_b6_plus8 alloc=[24, 32, 32, 24, 24, 24, 24, 16] bytes=200 recall=74.057500

PQ_GREEDY_EVAL tag=it17_b7_plus8 alloc=[24, 32, 32, 24, 24, 24, 16, 24] bytes=200 recall=74.145000

PQ_GREEDY_EVAL tag=it18_b0_plus8 alloc=[32, 40, 32, 24, 24, 24, 16, 16] bytes=208 recall=74.710000

PQ_GREEDY_EVAL tag=it18_b1_plus8 alloc=[24, 48, 32, 24, 24, 24, 16, 16] bytes=208 recall=74.417500

PQ_GREEDY_EVAL tag=it18_b2_plus8 alloc=[24, 40, 40, 24, 24, 24, 16, 16] bytes=208 recall=74.537500

PQ_GREEDY_EVAL tag=it18_b3_plus8 alloc=[24, 40, 32, 32, 24, 24, 16, 16] bytes=208 recall=74.797500

PQ_GREEDY_EVAL tag=it18_b4_plus8 alloc=[24, 40, 32, 24, 32, 24, 16, 16] bytes=208 recall=74.760000

PQ_GREEDY_EVAL tag=it18_b5_plus8 alloc=[24, 40, 32, 24, 24, 32, 16, 16] bytes=208 recall=74.580000

PQ_GREEDY_EVAL tag=it18_b6_plus8 alloc=[24, 40, 32, 24, 24, 24, 24, 16] bytes=208 recall=74.510000

PQ_GREEDY_EVAL tag=it18_b7_plus8 alloc=[24, 40, 32, 24, 24, 24, 16, 24] bytes=208 recall=74.805000

PQ_GREEDY_EVAL tag=it19_b0_plus8 alloc=[32, 40, 32, 24, 24, 24, 16, 24] bytes=216 recall=75.535000

PQ_GREEDY_EVAL tag=it19_b1_plus8 alloc=[24, 48, 32, 24, 24, 24, 16, 24] bytes=216 recall=75.365000

PQ_GREEDY_EVAL tag=it19_b2_plus8 alloc=[24, 40, 40, 24, 24, 24, 16, 24] bytes=216 recall=75.175000

PQ_GREEDY_EVAL tag=it19_b3_plus8 alloc=[24, 40, 32, 32, 24, 24, 16, 24] bytes=216 recall=75.330000

PQ_GREEDY_EVAL tag=it19_b4_plus8 alloc=[24, 40, 32, 24, 32, 24, 16, 24] bytes=216 recall=75.585000

PQ_GREEDY_EVAL tag=it19_b5_plus8 alloc=[24, 40, 32, 24, 24, 32, 16, 24] bytes=216 recall=75.285000

PQ_GREEDY_EVAL tag=it19_b6_plus8 alloc=[24, 40, 32, 24, 24, 24, 24, 24] bytes=216 recall=75.330000

PQ_GREEDY_EVAL tag=it19_b7_plus8 alloc=[24, 40, 32, 24, 24, 24, 16, 32] bytes=216 recall=75.300000

PQ_GREEDY_EVAL tag=it20_b0_plus8 alloc=[32, 40, 32, 24, 32, 24, 16, 24] bytes=224 recall=76.250000

PQ_GREEDY_EVAL tag=it20_b1_plus8 alloc=[24, 48, 32, 24, 32, 24, 16, 24] bytes=224 recall=76.037500

PQ_GREEDY_EVAL tag=it20_b2_plus8 alloc=[24, 40, 40, 24, 32, 24, 16, 24] bytes=224 recall=76.002500

PQ_GREEDY_EVAL tag=it20_b3_plus8 alloc=[24, 40, 32, 32, 32, 24, 16, 24] bytes=224 recall=76.145000

PQ_GREEDY_EVAL tag=it20_b4_plus8 alloc=[24, 40, 32, 24, 40, 24, 16, 24] bytes=224 recall=75.927500

PQ_GREEDY_EVAL tag=it20_b5_plus8 alloc=[24, 40, 32, 24, 32, 32, 16, 24] bytes=224 recall=75.857500

PQ_GREEDY_EVAL tag=it20_b6_plus8 alloc=[24, 40, 32, 24, 32, 24, 24, 24] bytes=224 recall=76.140000

PQ_GREEDY_EVAL tag=it20_b7_plus8 alloc=[24, 40, 32, 24, 32, 24, 16, 32] bytes=224 recall=75.877500

PQ_GREEDY_EVAL tag=it21_b0_plus8 alloc=[40, 40, 32, 24, 32, 24, 16, 24] bytes=232 recall=77.110000

PQ_GREEDY_EVAL tag=it21_b1_plus8 alloc=[32, 48, 32, 24, 32, 24, 16, 24] bytes=232 recall=76.670000

PQ_GREEDY_EVAL tag=it21_b2_plus8 alloc=[32, 40, 40, 24, 32, 24, 16, 24] bytes=232 recall=76.815000

PQ_GREEDY_EVAL tag=it21_b3_plus8 alloc=[32, 40, 32, 32, 32, 24, 16, 24] bytes=232 recall=77.022500

PQ_GREEDY_EVAL tag=it21_b4_plus8 alloc=[32, 40, 32, 24, 40, 24, 16, 24] bytes=232 recall=76.895000

PQ_GREEDY_EVAL tag=it21_b5_plus8 alloc=[32, 40, 32, 24, 32, 32, 16, 24] bytes=232 recall=76.795000

PQ_GREEDY_EVAL tag=it21_b6_plus8 alloc=[32, 40, 32, 24, 32, 24, 24, 24] bytes=232 recall=76.662500

PQ_GREEDY_EVAL tag=it21_b7_plus8 alloc=[32, 40, 32, 24, 32, 24, 16, 32] bytes=232 recall=76.850000

PQ_GREEDY_EVAL tag=it22_b0_plus8 alloc=[48, 40, 32, 24, 32, 24, 16, 24] bytes=240 recall=77.345000

PQ_GREEDY_EVAL tag=it22_b1_plus8 alloc=[40, 48, 32, 24, 32, 24, 16, 24] bytes=240 recall=77.277500

PQ_GREEDY_EVAL tag=it22_b2_plus8 alloc=[40, 40, 40, 24, 32, 24, 16, 24] bytes=240 recall=77.585000

PQ_GREEDY_EVAL tag=it22_b3_plus8 alloc=[40, 40, 32, 32, 32, 24, 16, 24] bytes=240 recall=77.242500

PQ_GREEDY_EVAL tag=it22_b4_plus8 alloc=[40, 40, 32, 24, 40, 24, 16, 24] bytes=240 recall=77.402500

PQ_GREEDY_EVAL tag=it22_b5_plus8 alloc=[40, 40, 32, 24, 32, 32, 16, 24] bytes=240 recall=77.357500

PQ_GREEDY_EVAL tag=it22_b6_plus8 alloc=[40, 40, 32, 24, 32, 24, 24, 24] bytes=240 recall=77.670000

PQ_GREEDY_EVAL tag=it22_b7_plus8 alloc=[40, 40, 32, 24, 32, 24, 16, 32] bytes=240 recall=77.505000

PQ_GREEDY_EVAL tag=it23_b0_plus8 alloc=[48, 40, 32, 24, 32, 24, 24, 24] bytes=248 recall=77.930000

PQ_GREEDY_EVAL tag=it23_b1_plus8 alloc=[40, 48, 32, 24, 32, 24, 24, 24] bytes=248 recall=77.930000

PQ_GREEDY_EVAL tag=it23_b2_plus8 alloc=[40, 40, 40, 24, 32, 24, 24, 24] bytes=248 recall=77.990000

PQ_GREEDY_EVAL tag=it23_b3_plus8 alloc=[40, 40, 32, 32, 32, 24, 24, 24] bytes=248 recall=78.107500

PQ_GREEDY_EVAL tag=it23_b4_plus8 alloc=[40, 40, 32, 24, 40, 24, 24, 24] bytes=248 recall=77.965000

PQ_GREEDY_EVAL tag=it23_b5_plus8 alloc=[40, 40, 32, 24, 32, 32, 24, 24] bytes=248 recall=77.977500

PQ_GREEDY_EVAL tag=it23_b6_plus8 alloc=[40, 40, 32, 24, 32, 24, 32, 24] bytes=248 recall=77.835000

PQ_GREEDY_EVAL tag=it23_b7_plus8 alloc=[40, 40, 32, 24, 32, 24, 24, 32] bytes=248 recall=78.012500

PQ_GREEDY_EVAL tag=it24_b0_plus8 alloc=[48, 40, 32, 32, 32, 24, 24, 24] bytes=256 recall=78.715000

PQ_GREEDY_EVAL tag=it24_b1_plus8 alloc=[40, 48, 32, 32, 32, 24, 24, 24] bytes=256 recall=78.717500

PQ_GREEDY_EVAL tag=it24_b2_plus8 alloc=[40, 40, 40, 32, 32, 24, 24, 24] bytes=256 recall=78.585000

PQ_GREEDY_EVAL tag=it24_b3_plus8 alloc=[40, 40, 32, 40, 32, 24, 24, 24] bytes=256 recall=78.355000

PQ_GREEDY_EVAL tag=it24_b4_plus8 alloc=[40, 40, 32, 32, 40, 24, 24, 24] bytes=256 recall=78.757500

PQ_GREEDY_EVAL tag=it24_b5_plus8 alloc=[40, 40, 32, 32, 32, 32, 24, 24] bytes=256 recall=78.482500

PQ_GREEDY_EVAL tag=it24_b6_plus8 alloc=[40, 40, 32, 32, 32, 24, 32, 24] bytes=256 recall=78.712500

PQ_GREEDY_EVAL tag=it24_b7_plus8 alloc=[40, 40, 32, 32, 32, 24, 24, 32] bytes=256 recall=78.580000

PQ_GREEDY_EVAL tag=it25_b0_plus8 alloc=[48, 40, 32, 32, 40, 24, 24, 24] bytes=264 recall=79.160000

PQ_GREEDY_EVAL tag=it25_b1_plus8 alloc=[40, 48, 32, 32, 40, 24, 24, 24] bytes=264 recall=79.077500

PQ_GREEDY_EVAL tag=it25_b2_plus8 alloc=[40, 40, 40, 32, 40, 24, 24, 24] bytes=264 recall=79.072500

PQ_GREEDY_EVAL tag=it25_b3_plus8 alloc=[40, 40, 32, 40, 40, 24, 24, 24] bytes=264 recall=79.215000

PQ_GREEDY_EVAL tag=it25_b4_plus8 alloc=[40, 40, 32, 32, 48, 24, 24, 24] bytes=264 recall=79.155000

PQ_GREEDY_EVAL tag=it25_b5_plus8 alloc=[40, 40, 32, 32, 40, 32, 24, 24] bytes=264 recall=79.277500

PQ_GREEDY_EVAL tag=it25_b6_plus8 alloc=[40, 40, 32, 32, 40, 24, 32, 24] bytes=264 recall=79.442500

PQ_GREEDY_EVAL tag=it25_b7_plus8 alloc=[40, 40, 32, 32, 40, 24, 24, 32] bytes=264 recall=79.022500

PQ_GREEDY_EVAL tag=it26_b0_plus8 alloc=[48, 40, 32, 32, 40, 24, 32, 24] bytes=272 recall=79.617500

PQ_GREEDY_EVAL tag=it26_b1_plus8 alloc=[40, 48, 32, 32, 40, 24, 32, 24] bytes=272 recall=79.602500

PQ_GREEDY_EVAL tag=it26_b2_plus8 alloc=[40, 40, 40, 32, 40, 24, 32, 24] bytes=272 recall=79.745000

PQ_GREEDY_EVAL tag=it26_b3_plus8 alloc=[40, 40, 32, 40, 40, 24, 32, 24] bytes=272 recall=79.885000

PQ_GREEDY_EVAL tag=it26_b4_plus8 alloc=[40, 40, 32, 32, 48, 24, 32, 24] bytes=272 recall=79.602500

PQ_GREEDY_EVAL tag=it26_b5_plus8 alloc=[40, 40, 32, 32, 40, 32, 32, 24] bytes=272 recall=79.625000

PQ_GREEDY_EVAL tag=it26_b6_plus8 alloc=[40, 40, 32, 32, 40, 24, 40, 24] bytes=272 recall=79.380000

PQ_GREEDY_EVAL tag=it26_b7_plus8 alloc=[40, 40, 32, 32, 40, 24, 32, 32] bytes=272 recall=79.747500

PQ_GREEDY_EVAL tag=it27_b0_plus8 alloc=[48, 40, 32, 40, 40, 24, 32, 24] bytes=280 recall=80.220000

PQ_GREEDY_EVAL tag=it27_b1_plus8 alloc=[40, 48, 32, 40, 40, 24, 32, 24] bytes=280 recall=80.102500

PQ_GREEDY_EVAL tag=it27_b2_plus8 alloc=[40, 40, 40, 40, 40, 24, 32, 24] bytes=280 recall=80.285000

PQ_GREEDY_EVAL tag=it27_b3_plus8 alloc=[40, 40, 32, 48, 40, 24, 32, 24] bytes=280 recall=79.937500

PQ_GREEDY_EVAL tag=it27_b4_plus8 alloc=[40, 40, 32, 40, 48, 24, 32, 24] bytes=280 recall=80.265000

PQ_GREEDY_EVAL tag=it27_b5_plus8 alloc=[40, 40, 32, 40, 40, 32, 32, 24] bytes=280 recall=80.032500

PQ_GREEDY_EVAL tag=it27_b6_plus8 alloc=[40, 40, 32, 40, 40, 24, 40, 24] bytes=280 recall=80.140000

PQ_GREEDY_EVAL tag=it27_b7_plus8 alloc=[40, 40, 32, 40, 40, 24, 32, 32] bytes=280 recall=80.275000

PQ_GREEDY_EVAL tag=it28_b0_plus8 alloc=[48, 40, 40, 40, 40, 24, 32, 24] bytes=288 recall=80.587500

PQ_GREEDY_EVAL tag=it28_b1_plus8 alloc=[40, 48, 40, 40, 40, 24, 32, 24] bytes=288 recall=80.830000

PQ_GREEDY_EVAL tag=it28_b2_plus8 alloc=[40, 40, 48, 40, 40, 24, 32, 24] bytes=288 recall=80.667500

PQ_GREEDY_EVAL tag=it28_b3_plus8 alloc=[40, 40, 40, 48, 40, 24, 32, 24] bytes=288 recall=80.820000

PQ_GREEDY_EVAL tag=it28_b4_plus8 alloc=[40, 40, 40, 40, 48, 24, 32, 24] bytes=288 recall=80.630000

PQ_GREEDY_EVAL tag=it28_b5_plus8 alloc=[40, 40, 40, 40, 40, 32, 32, 24] bytes=288 recall=80.952500

PQ_GREEDY_EVAL tag=it28_b6_plus8 alloc=[40, 40, 40, 40, 40, 24, 40, 24] bytes=288 recall=80.490000

PQ_GREEDY_EVAL tag=it28_b7_plus8 alloc=[40, 40, 40, 40, 40, 24, 32, 32] bytes=288 recall=81.040000

PQ_GREEDY_EVAL tag=it29_b0_plus8 alloc=[48, 40, 40, 40, 40, 24, 32, 32] bytes=296 recall=81.245000

PQ_GREEDY_EVAL tag=it29_b1_plus8 alloc=[40, 48, 40, 40, 40, 24, 32, 32] bytes=296 recall=81.325000

PQ_GREEDY_EVAL tag=it29_b2_plus8 alloc=[40, 40, 48, 40, 40, 24, 32, 32] bytes=296 recall=81.252500

PQ_GREEDY_EVAL tag=it29_b3_plus8 alloc=[40, 40, 40, 48, 40, 24, 32, 32] bytes=296 recall=81.477500

PQ_GREEDY_EVAL tag=it29_b4_plus8 alloc=[40, 40, 40, 40, 48, 24, 32, 32] bytes=296 recall=81.265000

PQ_GREEDY_EVAL tag=it29_b5_plus8 alloc=[40, 40, 40, 40, 40, 32, 32, 32] bytes=296 recall=81.447500

PQ_GREEDY_EVAL tag=it29_b6_plus8 alloc=[40, 40, 40, 40, 40, 24, 40, 32] bytes=296 recall=81.225000

PQ_GREEDY_EVAL tag=it29_b7_plus8 alloc=[40, 40, 40, 40, 40, 24, 32, 40] bytes=296 recall=81.090000

PQ_GREEDY_EVAL tag=it30_b0_plus8 alloc=[48, 40, 40, 48, 40, 24, 32, 32] bytes=304 recall=81.892500

PQ_GREEDY_EVAL tag=it30_b1_plus8 alloc=[40, 48, 40, 48, 40, 24, 32, 32] bytes=304 recall=81.650000

PQ_GREEDY_EVAL tag=it30_b2_plus8 alloc=[40, 40, 48, 48, 40, 24, 32, 32] bytes=304 recall=81.680000

PQ_GREEDY_EVAL tag=it30_b3_plus8 alloc=[40, 40, 40, 56, 40, 24, 32, 32] bytes=304 recall=81.462500

PQ_GREEDY_EVAL tag=it30_b4_plus8 alloc=[40, 40, 40, 48, 48, 24, 32, 32] bytes=304 recall=81.670000

PQ_GREEDY_EVAL tag=it30_b5_plus8 alloc=[40, 40, 40, 48, 40, 32, 32, 32] bytes=304 recall=81.862500

PQ_GREEDY_EVAL tag=it30_b6_plus8 alloc=[40, 40, 40, 48, 40, 24, 40, 32] bytes=304 recall=81.702500

PQ_GREEDY_EVAL tag=it30_b7_plus8 alloc=[40, 40, 40, 48, 40, 24, 32, 40] bytes=304 recall=81.502500

PQ_GREEDY_EVAL tag=it31_b0_plus8 alloc=[56, 40, 40, 48, 40, 24, 32, 32] bytes=312 recall=82.167500

PQ_GREEDY_EVAL tag=it31_b1_plus8 alloc=[48, 48, 40, 48, 40, 24, 32, 32] bytes=312 recall=82.135000

PQ_GREEDY_EVAL tag=it31_b2_plus8 alloc=[48, 40, 48, 48, 40, 24, 32, 32] bytes=312 recall=81.927500

PQ_GREEDY_EVAL tag=it31_b3_plus8 alloc=[48, 40, 40, 56, 40, 24, 32, 32] bytes=312 recall=81.720000

PQ_GREEDY_EVAL tag=it31_b4_plus8 alloc=[48, 40, 40, 48, 48, 24, 32, 32] bytes=312 recall=82.130000

PQ_GREEDY_EVAL tag=it31_b5_plus8 alloc=[48, 40, 40, 48, 40, 32, 32, 32] bytes=312 recall=82.412500

PQ_GREEDY_EVAL tag=it31_b6_plus8 alloc=[48, 40, 40, 48, 40, 24, 40, 32] bytes=312 recall=82.180000

PQ_GREEDY_EVAL tag=it31_b7_plus8 alloc=[48, 40, 40, 48, 40, 24, 32, 40] bytes=312 recall=82.262500

PQ_GREEDY_EVAL tag=it32_b0_plus8 alloc=[56, 40, 40, 48, 40, 32, 32, 32] bytes=320 recall=82.425000

PQ_GREEDY_EVAL tag=it32_b1_plus8 alloc=[48, 48, 40, 48, 40, 32, 32, 32] bytes=320 recall=82.587500

PQ_GREEDY_EVAL tag=it32_b2_plus8 alloc=[48, 40, 48, 48, 40, 32, 32, 32] bytes=320 recall=82.855000

PQ_GREEDY_EVAL tag=it32_b3_plus8 alloc=[48, 40, 40, 56, 40, 32, 32, 32] bytes=320 recall=82.437500

PQ_GREEDY_EVAL tag=it32_b4_plus8 alloc=[48, 40, 40, 48, 48, 32, 32, 32] bytes=320 recall=82.702500

PQ_GREEDY_EVAL tag=it32_b5_plus8 alloc=[48, 40, 40, 48, 40, 40, 32, 32] bytes=320 recall=82.762500

PQ_GREEDY_EVAL tag=it32_b6_plus8 alloc=[48, 40, 40, 48, 40, 32, 40, 32] bytes=320 recall=82.785000

PQ_GREEDY_EVAL tag=it32_b7_plus8 alloc=[48, 40, 40, 48, 40, 32, 32, 40] bytes=320 recall=82.470000

PQ_GREEDY_EVAL tag=it33_b0_plus8 alloc=[56, 40, 48, 48, 40, 32, 32, 32] bytes=328 recall=83.170000

PQ_GREEDY_EVAL tag=it33_b1_plus8 alloc=[48, 48, 48, 48, 40, 32, 32, 32] bytes=328 recall=82.995000

PQ_GREEDY_EVAL tag=it33_b2_plus8 alloc=[48, 40, 56, 48, 40, 32, 32, 32] bytes=328 recall=83.055000

PQ_GREEDY_EVAL tag=it33_b3_plus8 alloc=[48, 40, 48, 56, 40, 32, 32, 32] bytes=328 recall=83.045000

PQ_GREEDY_EVAL tag=it33_b4_plus8 alloc=[48, 40, 48, 48, 48, 32, 32, 32] bytes=328 recall=82.992500

PQ_GREEDY_EVAL tag=it33_b5_plus8 alloc=[48, 40, 48, 48, 40, 40, 32, 32] bytes=328 recall=83.230000

PQ_GREEDY_EVAL tag=it33_b6_plus8 alloc=[48, 40, 48, 48, 40, 32, 40, 32] bytes=328 recall=83.087500

PQ_GREEDY_EVAL tag=it33_b7_plus8 alloc=[48, 40, 48, 48, 40, 32, 32, 40] bytes=328 recall=83.092500

PQ_GREEDY_EVAL tag=it34_b0_plus8 alloc=[56, 40, 48, 48, 40, 40, 32, 32] bytes=336 recall=83.345000

PQ_GREEDY_EVAL tag=it34_b1_plus8 alloc=[48, 48, 48, 48, 40, 40, 32, 32] bytes=336 recall=83.772500

PQ_GREEDY_EVAL tag=it34_b2_plus8 alloc=[48, 40, 56, 48, 40, 40, 32, 32] bytes=336 recall=83.430000

PQ_GREEDY_EVAL tag=it34_b3_plus8 alloc=[48, 40, 48, 56, 40, 40, 32, 32] bytes=336 recall=83.232500

PQ_GREEDY_EVAL tag=it34_b4_plus8 alloc=[48, 40, 48, 48, 48, 40, 32, 32] bytes=336 recall=83.445000

PQ_GREEDY_EVAL tag=it34_b5_plus8 alloc=[48, 40, 48, 48, 40, 48, 32, 32] bytes=336 recall=83.572500

PQ_GREEDY_EVAL tag=it34_b6_plus8 alloc=[48, 40, 48, 48, 40, 40, 40, 32] bytes=336 recall=83.427500

PQ_GREEDY_EVAL tag=it34_b7_plus8 alloc=[48, 40, 48, 48, 40, 40, 32, 40] bytes=336 recall=83.562500

PQ_GREEDY_EVAL tag=it35_b0_plus8 alloc=[56, 48, 48, 48, 40, 40, 32, 32] bytes=344 recall=83.972500

PQ_GREEDY_EVAL tag=it35_b1_plus8 alloc=[48, 56, 48, 48, 40, 40, 32, 32] bytes=344 recall=83.850000

PQ_GREEDY_EVAL tag=it35_b2_plus8 alloc=[48, 48, 56, 48, 40, 40, 32, 32] bytes=344 recall=83.980000

PQ_GREEDY_EVAL tag=it35_b3_plus8 alloc=[48, 48, 48, 56, 40, 40, 32, 32] bytes=344 recall=84.002500

PQ_GREEDY_EVAL tag=it35_b4_plus8 alloc=[48, 48, 48, 48, 48, 40, 32, 32] bytes=344 recall=84.297500

PQ_GREEDY_EVAL tag=it35_b5_plus8 alloc=[48, 48, 48, 48, 40, 48, 32, 32] bytes=344 recall=84.240000

PQ_GREEDY_EVAL tag=it35_b6_plus8 alloc=[48, 48, 48, 48, 40, 40, 40, 32] bytes=344 recall=84.160000

PQ_GREEDY_EVAL tag=it35_b7_plus8 alloc=[48, 48, 48, 48, 40, 40, 32, 40] bytes=344 recall=84.110000

PQ_GREEDY_EVAL tag=it36_b0_plus8 alloc=[56, 48, 48, 48, 48, 40, 32, 32] bytes=352 recall=84.452500

PQ_GREEDY_EVAL tag=it36_b1_plus8 alloc=[48, 56, 48, 48, 48, 40, 32, 32] bytes=352 recall=84.555000

PQ_GREEDY_EVAL tag=it36_b2_plus8 alloc=[48, 48, 56, 48, 48, 40, 32, 32] bytes=352 recall=84.482500

PQ_GREEDY_EVAL tag=it36_b3_plus8 alloc=[48, 48, 48, 56, 48, 40, 32, 32] bytes=352 recall=84.252500

PQ_GREEDY_EVAL tag=it36_b4_plus8 alloc=[48, 48, 48, 48, 56, 40, 32, 32] bytes=352 recall=84.465000

PQ_GREEDY_EVAL tag=it36_b5_plus8 alloc=[48, 48, 48, 48, 48, 48, 32, 32] bytes=352 recall=84.680000

PQ_GREEDY_EVAL tag=it36_b6_plus8 alloc=[48, 48, 48, 48, 48, 40, 40, 32] bytes=352 recall=84.665000

PQ_GREEDY_EVAL tag=it36_b7_plus8 alloc=[48, 48, 48, 48, 48, 40, 32, 40] bytes=352 recall=84.562500

PQ_GREEDY_EVAL tag=it37_b0_plus8 alloc=[56, 48, 48, 48, 48, 48, 32, 32] bytes=360 recall=84.822500

PQ_GREEDY_EVAL tag=it37_b1_plus8 alloc=[48, 56, 48, 48, 48, 48, 32, 32] bytes=360 recall=84.810000

PQ_GREEDY_EVAL tag=it37_b2_plus8 alloc=[48, 48, 56, 48, 48, 48, 32, 32] bytes=360 recall=84.817500

PQ_GREEDY_EVAL tag=it37_b3_plus8 alloc=[48, 48, 48, 56, 48, 48, 32, 32] bytes=360 recall=84.832500

PQ_GREEDY_EVAL tag=it37_b4_plus8 alloc=[48, 48, 48, 48, 56, 48, 32, 32] bytes=360 recall=84.940000

PQ_GREEDY_EVAL tag=it37_b5_plus8 alloc=[48, 48, 48, 48, 48, 56, 32, 32] bytes=360 recall=84.837500

PQ_GREEDY_EVAL tag=it37_b6_plus8 alloc=[48, 48, 48, 48, 48, 48, 40, 32] bytes=360 recall=85.042500

PQ_GREEDY_EVAL tag=it37_b7_plus8 alloc=[48, 48, 48, 48, 48, 48, 32, 40] bytes=360 recall=85.032500

PQ_GREEDY_EVAL tag=it38_b0_plus8 alloc=[56, 48, 48, 48, 48, 48, 40, 32] bytes=368 recall=85.270000

PQ_GREEDY_EVAL tag=it38_b1_plus8 alloc=[48, 56, 48, 48, 48, 48, 40, 32] bytes=368 recall=85.192500

PQ_GREEDY_EVAL tag=it38_b2_plus8 alloc=[48, 48, 56, 48, 48, 48, 40, 32] bytes=368 recall=85.537500

PQ_GREEDY_EVAL tag=it38_b3_plus8 alloc=[48, 48, 48, 56, 48, 48, 40, 32] bytes=368 recall=85.117500

PQ_GREEDY_EVAL tag=it38_b4_plus8 alloc=[48, 48, 48, 48, 56, 48, 40, 32] bytes=368 recall=85.190000

PQ_GREEDY_EVAL tag=it38_b5_plus8 alloc=[48, 48, 48, 48, 48, 56, 40, 32] bytes=368 recall=85.197500

PQ_GREEDY_EVAL tag=it38_b6_plus8 alloc=[48, 48, 48, 48, 48, 48, 48, 32] bytes=368 recall=85.377500

PQ_GREEDY_EVAL tag=it38_b7_plus8 alloc=[48, 48, 48, 48, 48, 48, 40, 40] bytes=368 recall=85.502500

PQ_GREEDY_EVAL tag=it39_b0_plus8 alloc=[56, 48, 56, 48, 48, 48, 40, 32] bytes=376 recall=85.610000

PQ_GREEDY_EVAL tag=it39_b1_plus8 alloc=[48, 56, 56, 48, 48, 48, 40, 32] bytes=376 recall=85.672500

PQ_GREEDY_EVAL tag=it39_b2_plus8 alloc=[48, 48, 64, 48, 48, 48, 40, 32] bytes=376 recall=85.437500

PQ_GREEDY_EVAL tag=it39_b3_plus8 alloc=[48, 48, 56, 56, 48, 48, 40, 32] bytes=376 recall=85.210000

PQ_GREEDY_EVAL tag=it39_b4_plus8 alloc=[48, 48, 56, 48, 56, 48, 40, 32] bytes=376 recall=85.470000

PQ_GREEDY_EVAL tag=it39_b5_plus8 alloc=[48, 48, 56, 48, 48, 56, 40, 32] bytes=376 recall=85.460000

PQ_GREEDY_EVAL tag=it39_b6_plus8 alloc=[48, 48, 56, 48, 48, 48, 48, 32] bytes=376 recall=85.437500

PQ_GREEDY_EVAL tag=it39_b7_plus8 alloc=[48, 48, 56, 48, 48, 48, 40, 40] bytes=376 recall=85.530000

PQ_GREEDY_EVAL tag=it40_b0_plus8 alloc=[56, 56, 56, 48, 48, 48, 40, 32] bytes=384 recall=86.015000

PQ_GREEDY_EVAL tag=it40_b1_plus8 alloc=[48, 64, 56, 48, 48, 48, 40, 32] bytes=384 recall=85.697500

PQ_GREEDY_EVAL tag=it40_b2_plus8 alloc=[48, 56, 64, 48, 48, 48, 40, 32] bytes=384 recall=85.945000

PQ_GREEDY_EVAL tag=it40_b3_plus8 alloc=[48, 56, 56, 56, 48, 48, 40, 32] bytes=384 recall=85.715000

PQ_GREEDY_EVAL tag=it40_b4_plus8 alloc=[48, 56, 56, 48, 56, 48, 40, 32] bytes=384 recall=85.725000

PQ_GREEDY_EVAL tag=it40_b5_plus8 alloc=[48, 56, 56, 48, 48, 56, 40, 32] bytes=384 recall=85.540000

PQ_GREEDY_EVAL tag=it40_b6_plus8 alloc=[48, 56, 56, 48, 48, 48, 48, 32] bytes=384 recall=85.880000

PQ_GREEDY_EVAL tag=it40_b7_plus8 alloc=[48, 56, 56, 48, 48, 48, 40, 40] bytes=384 recall=85.532500

#### Uniform PQ
PQ sweep completed!
Results directory: /tmp/pq_sweep_1779004827

Summary of recall results:
Bytes,Recall
64,48.89
96,59.59
128,65.8275
160,69.5225
192,73.175
224,75.93
256,78.6225
288,80.3775
320,82.4275
352,83.7325
384,85.94




## SQ
### DBPedia Cohere v4
#### Uniform SQ
SQ sweep completed!
Results directory: /tmp/sq_sweep_1779492777

Summary of SQ recall results:
Bytes,Recall
64,27.6475
96,38.5175
128,46.7775
160,52.245
192,56.81
224,60.65
256,64.495
288,66.8975
320,69.135
352,70.9175
384,72.9875

#### Variable SQ

SQ_GREEDY_EVAL tag=init alloc=[8, 8, 8, 8, 8, 8, 8, 8] bytes=64 recall=22.460000

SQ_GREEDY_EVAL tag=it1_b0_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 8] bytes=72 recall=26.482500

SQ_GREEDY_EVAL tag=it1_b1_plus8 alloc=[8, 16, 8, 8, 8, 8, 8, 8] bytes=72 recall=26.025000

SQ_GREEDY_EVAL tag=it1_b2_plus8 alloc=[8, 8, 16, 8, 8, 8, 8, 8] bytes=72 recall=25.890000

SQ_GREEDY_EVAL tag=it1_b3_plus8 alloc=[8, 8, 8, 16, 8, 8, 8, 8] bytes=72 recall=25.740000

SQ_GREEDY_EVAL tag=it1_b4_plus8 alloc=[8, 8, 8, 8, 16, 8, 8, 8] bytes=72 recall=24.922500

SQ_GREEDY_EVAL tag=it1_b5_plus8 alloc=[8, 8, 8, 8, 8, 16, 8, 8] bytes=72 recall=25.322500

SQ_GREEDY_EVAL tag=it1_b6_plus8 alloc=[8, 8, 8, 8, 8, 8, 16, 8] bytes=72 recall=25.002500

SQ_GREEDY_EVAL tag=it1_b7_plus8 alloc=[8, 8, 8, 8, 8, 8, 8, 16] bytes=72 recall=25.235000

SQ_GREEDY_EVAL tag=it2_b0_plus8 alloc=[24, 8, 8, 8, 8, 8, 8, 8] bytes=80 recall=29.837500

SQ_GREEDY_EVAL tag=it2_b1_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 8] bytes=80 recall=29.625000

SQ_GREEDY_EVAL tag=it2_b2_plus8 alloc=[16, 8, 16, 8, 8, 8, 8, 8] bytes=80 recall=29.552500

SQ_GREEDY_EVAL tag=it2_b3_plus8 alloc=[16, 8, 8, 16, 8, 8, 8, 8] bytes=80 recall=29.450000

SQ_GREEDY_EVAL tag=it2_b4_plus8 alloc=[16, 8, 8, 8, 16, 8, 8, 8] bytes=80 recall=28.627500

SQ_GREEDY_EVAL tag=it2_b5_plus8 alloc=[16, 8, 8, 8, 8, 16, 8, 8] bytes=80 recall=29.042500

SQ_GREEDY_EVAL tag=it2_b6_plus8 alloc=[16, 8, 8, 8, 8, 8, 16, 8] bytes=80 recall=28.675000

SQ_GREEDY_EVAL tag=it2_b7_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 16] bytes=80 recall=28.882500

SQ_GREEDY_EVAL tag=it3_b0_plus8 alloc=[32, 8, 8, 8, 8, 8, 8, 8] bytes=88 recall=33.012500

SQ_GREEDY_EVAL tag=it3_b1_plus8 alloc=[24, 16, 8, 8, 8, 8, 8, 8] bytes=88 recall=32.747500

SQ_GREEDY_EVAL tag=it3_b2_plus8 alloc=[24, 8, 16, 8, 8, 8, 8, 8] bytes=88 recall=32.525000

SQ_GREEDY_EVAL tag=it3_b3_plus8 alloc=[24, 8, 8, 16, 8, 8, 8, 8] bytes=88 recall=32.715000

SQ_GREEDY_EVAL tag=it3_b4_plus8 alloc=[24, 8, 8, 8, 16, 8, 8, 8] bytes=88 recall=31.945000

SQ_GREEDY_EVAL tag=it3_b5_plus8 alloc=[24, 8, 8, 8, 8, 16, 8, 8] bytes=88 recall=32.232500

SQ_GREEDY_EVAL tag=it3_b6_plus8 alloc=[24, 8, 8, 8, 8, 8, 16, 8] bytes=88 recall=31.895000

SQ_GREEDY_EVAL tag=it3_b7_plus8 alloc=[24, 8, 8, 8, 8, 8, 8, 16] bytes=88 recall=32.005000

SQ_GREEDY_EVAL tag=it4_b0_plus8 alloc=[40, 8, 8, 8, 8, 8, 8, 8] bytes=96 recall=36.005000

SQ_GREEDY_EVAL tag=it4_b1_plus8 alloc=[32, 16, 8, 8, 8, 8, 8, 8] bytes=96 recall=35.510000

SQ_GREEDY_EVAL tag=it4_b2_plus8 alloc=[32, 8, 16, 8, 8, 8, 8, 8] bytes=96 recall=35.507500

SQ_GREEDY_EVAL tag=it4_b3_plus8 alloc=[32, 8, 8, 16, 8, 8, 8, 8] bytes=96 recall=35.450000

SQ_GREEDY_EVAL tag=it4_b4_plus8 alloc=[32, 8, 8, 8, 16, 8, 8, 8] bytes=96 recall=34.722500

SQ_GREEDY_EVAL tag=it4_b5_plus8 alloc=[32, 8, 8, 8, 8, 16, 8, 8] bytes=96 recall=35.150000

SQ_GREEDY_EVAL tag=it4_b6_plus8 alloc=[32, 8, 8, 8, 8, 8, 16, 8] bytes=96 recall=34.705000

SQ_GREEDY_EVAL tag=it4_b7_plus8 alloc=[32, 8, 8, 8, 8, 8, 8, 16] bytes=96 recall=34.907500

SQ_GREEDY_EVAL tag=it5_b0_plus8 alloc=[48, 8, 8, 8, 8, 8, 8, 8] bytes=104 recall=38.790000

SQ_GREEDY_EVAL tag=it5_b1_plus8 alloc=[40, 16, 8, 8, 8, 8, 8, 8] bytes=104 recall=38.387500

SQ_GREEDY_EVAL tag=it5_b2_plus8 alloc=[40, 8, 16, 8, 8, 8, 8, 8] bytes=104 recall=38.470000

SQ_GREEDY_EVAL tag=it5_b3_plus8 alloc=[40, 8, 8, 16, 8, 8, 8, 8] bytes=104 recall=38.337500

SQ_GREEDY_EVAL tag=it5_b4_plus8 alloc=[40, 8, 8, 8, 16, 8, 8, 8] bytes=104 recall=37.630000

SQ_GREEDY_EVAL tag=it5_b5_plus8 alloc=[40, 8, 8, 8, 8, 16, 8, 8] bytes=104 recall=37.785000

SQ_GREEDY_EVAL tag=it5_b6_plus8 alloc=[40, 8, 8, 8, 8, 8, 16, 8] bytes=104 recall=37.577500

SQ_GREEDY_EVAL tag=it5_b7_plus8 alloc=[40, 8, 8, 8, 8, 8, 8, 16] bytes=104 recall=37.760000

SQ_GREEDY_EVAL tag=it6_b0_plus8 alloc=[56, 8, 8, 8, 8, 8, 8, 8] bytes=112 recall=40.075000

SQ_GREEDY_EVAL tag=it6_b1_plus8 alloc=[48, 16, 8, 8, 8, 8, 8, 8] bytes=112 recall=40.912500

SQ_GREEDY_EVAL tag=it6_b2_plus8 alloc=[48, 8, 16, 8, 8, 8, 8, 8] bytes=112 recall=40.882500

SQ_GREEDY_EVAL tag=it6_b3_plus8 alloc=[48, 8, 8, 16, 8, 8, 8, 8] bytes=112 recall=40.870000

SQ_GREEDY_EVAL tag=it6_b4_plus8 alloc=[48, 8, 8, 8, 16, 8, 8, 8] bytes=112 recall=40.337500

SQ_GREEDY_EVAL tag=it6_b5_plus8 alloc=[48, 8, 8, 8, 8, 16, 8, 8] bytes=112 recall=40.657500

SQ_GREEDY_EVAL tag=it6_b6_plus8 alloc=[48, 8, 8, 8, 8, 8, 16, 8] bytes=112 recall=40.197500

SQ_GREEDY_EVAL tag=it6_b7_plus8 alloc=[48, 8, 8, 8, 8, 8, 8, 16] bytes=112 recall=40.455000

SQ_GREEDY_EVAL tag=it7_b0_plus8 alloc=[56, 16, 8, 8, 8, 8, 8, 8] bytes=120 recall=41.990000

SQ_GREEDY_EVAL tag=it7_b1_plus8 alloc=[48, 24, 8, 8, 8, 8, 8, 8] bytes=120 recall=42.955000

SQ_GREEDY_EVAL tag=it7_b2_plus8 alloc=[48, 16, 16, 8, 8, 8, 8, 8] bytes=120 recall=43.127500

SQ_GREEDY_EVAL tag=it7_b3_plus8 alloc=[48, 16, 8, 16, 8, 8, 8, 8] bytes=120 recall=42.960000

SQ_GREEDY_EVAL tag=it7_b4_plus8 alloc=[48, 16, 8, 8, 16, 8, 8, 8] bytes=120 recall=42.380000

SQ_GREEDY_EVAL tag=it7_b5_plus8 alloc=[48, 16, 8, 8, 8, 16, 8, 8] bytes=120 recall=42.622500

SQ_GREEDY_EVAL tag=it7_b6_plus8 alloc=[48, 16, 8, 8, 8, 8, 16, 8] bytes=120 recall=42.140000

SQ_GREEDY_EVAL tag=it7_b7_plus8 alloc=[48, 16, 8, 8, 8, 8, 8, 16] bytes=120 recall=42.500000

SQ_GREEDY_EVAL tag=it8_b0_plus8 alloc=[56, 16, 16, 8, 8, 8, 8, 8] bytes=128 recall=44.142500

SQ_GREEDY_EVAL tag=it8_b1_plus8 alloc=[48, 24, 16, 8, 8, 8, 8, 8] bytes=128 recall=44.967500

SQ_GREEDY_EVAL tag=it8_b2_plus8 alloc=[48, 16, 24, 8, 8, 8, 8, 8] bytes=128 recall=44.810000

SQ_GREEDY_EVAL tag=it8_b3_plus8 alloc=[48, 16, 16, 16, 8, 8, 8, 8] bytes=128 recall=45.070000

SQ_GREEDY_EVAL tag=it8_b4_plus8 alloc=[48, 16, 16, 8, 16, 8, 8, 8] bytes=128 recall=44.697500

SQ_GREEDY_EVAL tag=it8_b5_plus8 alloc=[48, 16, 16, 8, 8, 16, 8, 8] bytes=128 recall=44.897500

SQ_GREEDY_EVAL tag=it8_b6_plus8 alloc=[48, 16, 16, 8, 8, 8, 16, 8] bytes=128 recall=44.237500

SQ_GREEDY_EVAL tag=it8_b7_plus8 alloc=[48, 16, 16, 8, 8, 8, 8, 16] bytes=128 recall=44.577500

SQ_GREEDY_EVAL tag=it9_b0_plus8 alloc=[56, 16, 16, 16, 8, 8, 8, 8] bytes=136 recall=45.940000

SQ_GREEDY_EVAL tag=it9_b1_plus8 alloc=[48, 24, 16, 16, 8, 8, 8, 8] bytes=136 recall=46.647500

SQ_GREEDY_EVAL tag=it9_b2_plus8 alloc=[48, 16, 24, 16, 8, 8, 8, 8] bytes=136 recall=46.430000

SQ_GREEDY_EVAL tag=it9_b3_plus8 alloc=[48, 16, 16, 24, 8, 8, 8, 8] bytes=136 recall=46.552500

SQ_GREEDY_EVAL tag=it9_b4_plus8 alloc=[48, 16, 16, 16, 16, 8, 8, 8] bytes=136 recall=46.547500

SQ_GREEDY_EVAL tag=it9_b5_plus8 alloc=[48, 16, 16, 16, 8, 16, 8, 8] bytes=136 recall=46.707500

SQ_GREEDY_EVAL tag=it9_b6_plus8 alloc=[48, 16, 16, 16, 8, 8, 16, 8] bytes=136 recall=46.127500

SQ_GREEDY_EVAL tag=it9_b7_plus8 alloc=[48, 16, 16, 16, 8, 8, 8, 16] bytes=136 recall=46.367500

SQ_GREEDY_EVAL tag=it10_b0_plus8 alloc=[56, 16, 16, 16, 8, 16, 8, 8] bytes=144 recall=47.577500

SQ_GREEDY_EVAL tag=it10_b1_plus8 alloc=[48, 24, 16, 16, 8, 16, 8, 8] bytes=144 recall=48.132500

SQ_GREEDY_EVAL tag=it10_b2_plus8 alloc=[48, 16, 24, 16, 8, 16, 8, 8] bytes=144 recall=48.015000

SQ_GREEDY_EVAL tag=it10_b3_plus8 alloc=[48, 16, 16, 24, 8, 16, 8, 8] bytes=144 recall=48.102500

SQ_GREEDY_EVAL tag=it10_b4_plus8 alloc=[48, 16, 16, 16, 16, 16, 8, 8] bytes=144 recall=47.875000

SQ_GREEDY_EVAL tag=it10_b5_plus8 alloc=[48, 16, 16, 16, 8, 24, 8, 8] bytes=144 recall=47.780000

SQ_GREEDY_EVAL tag=it10_b6_plus8 alloc=[48, 16, 16, 16, 8, 16, 16, 8] bytes=144 recall=47.810000

SQ_GREEDY_EVAL tag=it10_b7_plus8 alloc=[48, 16, 16, 16, 8, 16, 8, 16] bytes=144 recall=47.802500

SQ_GREEDY_EVAL tag=it11_b0_plus8 alloc=[56, 24, 16, 16, 8, 16, 8, 8] bytes=152 recall=49.077500

SQ_GREEDY_EVAL tag=it11_b1_plus8 alloc=[48, 32, 16, 16, 8, 16, 8, 8] bytes=152 recall=49.872500

SQ_GREEDY_EVAL tag=it11_b2_plus8 alloc=[48, 24, 24, 16, 8, 16, 8, 8] bytes=152 recall=49.547500

SQ_GREEDY_EVAL tag=it11_b3_plus8 alloc=[48, 24, 16, 24, 8, 16, 8, 8] bytes=152 recall=49.562500

SQ_GREEDY_EVAL tag=it11_b4_plus8 alloc=[48, 24, 16, 16, 16, 16, 8, 8] bytes=152 recall=49.402500

SQ_GREEDY_EVAL tag=it11_b5_plus8 alloc=[48, 24, 16, 16, 8, 24, 8, 8] bytes=152 recall=49.200000

SQ_GREEDY_EVAL tag=it11_b6_plus8 alloc=[48, 24, 16, 16, 8, 16, 16, 8] bytes=152 recall=49.132500

SQ_GREEDY_EVAL tag=it11_b7_plus8 alloc=[48, 24, 16, 16, 8, 16, 8, 16] bytes=152 recall=49.322500

SQ_GREEDY_EVAL tag=it12_b0_plus8 alloc=[56, 32, 16, 16, 8, 16, 8, 8] bytes=160 recall=50.612500

SQ_GREEDY_EVAL tag=it12_b1_plus8 alloc=[48, 40, 16, 16, 8, 16, 8, 8] bytes=160 recall=51.450000

SQ_GREEDY_EVAL tag=it12_b2_plus8 alloc=[48, 32, 24, 16, 8, 16, 8, 8] bytes=160 recall=51.310000

SQ_GREEDY_EVAL tag=it12_b3_plus8 alloc=[48, 32, 16, 24, 8, 16, 8, 8] bytes=160 recall=51.157500

SQ_GREEDY_EVAL tag=it12_b4_plus8 alloc=[48, 32, 16, 16, 16, 16, 8, 8] bytes=160 recall=50.940000

SQ_GREEDY_EVAL tag=it12_b5_plus8 alloc=[48, 32, 16, 16, 8, 24, 8, 8] bytes=160 recall=50.875000

SQ_GREEDY_EVAL tag=it12_b6_plus8 alloc=[48, 32, 16, 16, 8, 16, 16, 8] bytes=160 recall=50.867500

SQ_GREEDY_EVAL tag=it12_b7_plus8 alloc=[48, 32, 16, 16, 8, 16, 8, 16] bytes=160 recall=50.737500

SQ_GREEDY_EVAL tag=it13_b0_plus8 alloc=[56, 40, 16, 16, 8, 16, 8, 8] bytes=168 recall=52.362500

SQ_GREEDY_EVAL tag=it13_b1_plus8 alloc=[48, 48, 16, 16, 8, 16, 8, 8] bytes=168 recall=53.095000

SQ_GREEDY_EVAL tag=it13_b2_plus8 alloc=[48, 40, 24, 16, 8, 16, 8, 8] bytes=168 recall=52.857500

SQ_GREEDY_EVAL tag=it13_b3_plus8 alloc=[48, 40, 16, 24, 8, 16, 8, 8] bytes=168 recall=52.732500

SQ_GREEDY_EVAL tag=it13_b4_plus8 alloc=[48, 40, 16, 16, 16, 16, 8, 8] bytes=168 recall=52.572500

SQ_GREEDY_EVAL tag=it13_b5_plus8 alloc=[48, 40, 16, 16, 8, 24, 8, 8] bytes=168 recall=52.430000

SQ_GREEDY_EVAL tag=it13_b6_plus8 alloc=[48, 40, 16, 16, 8, 16, 16, 8] bytes=168 recall=52.380000

SQ_GREEDY_EVAL tag=it13_b7_plus8 alloc=[48, 40, 16, 16, 8, 16, 8, 16] bytes=168 recall=52.305000

SQ_GREEDY_EVAL tag=it14_b0_plus8 alloc=[56, 48, 16, 16, 8, 16, 8, 8] bytes=176 recall=53.797500

SQ_GREEDY_EVAL tag=it14_b1_plus8 alloc=[48, 56, 16, 16, 8, 16, 8, 8] bytes=176 recall=53.912500

SQ_GREEDY_EVAL tag=it14_b2_plus8 alloc=[48, 48, 24, 16, 8, 16, 8, 8] bytes=176 recall=54.237500

SQ_GREEDY_EVAL tag=it14_b3_plus8 alloc=[48, 48, 16, 24, 8, 16, 8, 8] bytes=176 recall=54.395000

SQ_GREEDY_EVAL tag=it14_b4_plus8 alloc=[48, 48, 16, 16, 16, 16, 8, 8] bytes=176 recall=54.005000

SQ_GREEDY_EVAL tag=it14_b5_plus8 alloc=[48, 48, 16, 16, 8, 24, 8, 8] bytes=176 recall=53.932500

SQ_GREEDY_EVAL tag=it14_b6_plus8 alloc=[48, 48, 16, 16, 8, 16, 16, 8] bytes=176 recall=53.910000

SQ_GREEDY_EVAL tag=it14_b7_plus8 alloc=[48, 48, 16, 16, 8, 16, 8, 16] bytes=176 recall=53.865000

SQ_GREEDY_EVAL tag=it15_b0_plus8 alloc=[56, 48, 16, 24, 8, 16, 8, 8] bytes=184 recall=54.975000

SQ_GREEDY_EVAL tag=it15_b1_plus8 alloc=[48, 56, 16, 24, 8, 16, 8, 8] bytes=184 recall=55.020000

SQ_GREEDY_EVAL tag=it15_b2_plus8 alloc=[48, 48, 24, 24, 8, 16, 8, 8] bytes=184 recall=55.397500

SQ_GREEDY_EVAL tag=it15_b3_plus8 alloc=[48, 48, 16, 32, 8, 16, 8, 8] bytes=184 recall=55.207500

SQ_GREEDY_EVAL tag=it15_b4_plus8 alloc=[48, 48, 16, 24, 16, 16, 8, 8] bytes=184 recall=55.185000

SQ_GREEDY_EVAL tag=it15_b5_plus8 alloc=[48, 48, 16, 24, 8, 24, 8, 8] bytes=184 recall=55.165000

SQ_GREEDY_EVAL tag=it15_b6_plus8 alloc=[48, 48, 16, 24, 8, 16, 16, 8] bytes=184 recall=55.075000

SQ_GREEDY_EVAL tag=it15_b7_plus8 alloc=[48, 48, 16, 24, 8, 16, 8, 16] bytes=184 recall=55.200000

SQ_GREEDY_EVAL tag=it16_b0_plus8 alloc=[56, 48, 24, 24, 8, 16, 8, 8] bytes=192 recall=56.052500

SQ_GREEDY_EVAL tag=it16_b1_plus8 alloc=[48, 56, 24, 24, 8, 16, 8, 8] bytes=192 recall=56.180000

SQ_GREEDY_EVAL tag=it16_b2_plus8 alloc=[48, 48, 32, 24, 8, 16, 8, 8] bytes=192 recall=56.612500

SQ_GREEDY_EVAL tag=it16_b3_plus8 alloc=[48, 48, 24, 32, 8, 16, 8, 8] bytes=192 recall=56.230000

SQ_GREEDY_EVAL tag=it16_b4_plus8 alloc=[48, 48, 24, 24, 16, 16, 8, 8] bytes=192 recall=56.302500

SQ_GREEDY_EVAL tag=it16_b5_plus8 alloc=[48, 48, 24, 24, 8, 24, 8, 8] bytes=192 recall=56.372500

SQ_GREEDY_EVAL tag=it16_b6_plus8 alloc=[48, 48, 24, 24, 8, 16, 16, 8] bytes=192 recall=56.267500

SQ_GREEDY_EVAL tag=it16_b7_plus8 alloc=[48, 48, 24, 24, 8, 16, 8, 16] bytes=192 recall=56.225000

SQ_GREEDY_EVAL tag=it17_b0_plus8 alloc=[56, 48, 32, 24, 8, 16, 8, 8] bytes=200 recall=57.242500

SQ_GREEDY_EVAL tag=it17_b1_plus8 alloc=[48, 56, 32, 24, 8, 16, 8, 8] bytes=200 recall=57.150000

SQ_GREEDY_EVAL tag=it17_b2_plus8 alloc=[48, 48, 40, 24, 8, 16, 8, 8] bytes=200 recall=57.657500

SQ_GREEDY_EVAL tag=it17_b3_plus8 alloc=[48, 48, 32, 32, 8, 16, 8, 8] bytes=200 recall=57.357500

SQ_GREEDY_EVAL tag=it17_b4_plus8 alloc=[48, 48, 32, 24, 16, 16, 8, 8] bytes=200 recall=57.530000

SQ_GREEDY_EVAL tag=it17_b5_plus8 alloc=[48, 48, 32, 24, 8, 24, 8, 8] bytes=200 recall=57.440000

SQ_GREEDY_EVAL tag=it17_b6_plus8 alloc=[48, 48, 32, 24, 8, 16, 16, 8] bytes=200 recall=57.422500

SQ_GREEDY_EVAL tag=it17_b7_plus8 alloc=[48, 48, 32, 24, 8, 16, 8, 16] bytes=200 recall=57.337500

SQ_GREEDY_EVAL tag=it18_b0_plus8 alloc=[56, 48, 40, 24, 8, 16, 8, 8] bytes=208 recall=58.280000

SQ_GREEDY_EVAL tag=it18_b1_plus8 alloc=[48, 56, 40, 24, 8, 16, 8, 8] bytes=208 recall=58.410000

SQ_GREEDY_EVAL tag=it18_b2_plus8 alloc=[48, 48, 48, 24, 8, 16, 8, 8] bytes=208 recall=58.507500

SQ_GREEDY_EVAL tag=it18_b3_plus8 alloc=[48, 48, 40, 32, 8, 16, 8, 8] bytes=208 recall=58.567500

SQ_GREEDY_EVAL tag=it18_b4_plus8 alloc=[48, 48, 40, 24, 16, 16, 8, 8] bytes=208 recall=58.475000

SQ_GREEDY_EVAL tag=it18_b5_plus8 alloc=[48, 48, 40, 24, 8, 24, 8, 8] bytes=208 recall=58.452500

SQ_GREEDY_EVAL tag=it18_b6_plus8 alloc=[48, 48, 40, 24, 8, 16, 16, 8] bytes=208 recall=58.367500

SQ_GREEDY_EVAL tag=it18_b7_plus8 alloc=[48, 48, 40, 24, 8, 16, 8, 16] bytes=208 recall=58.465000

SQ_GREEDY_EVAL tag=it19_b0_plus8 alloc=[56, 48, 40, 32, 8, 16, 8, 8] bytes=216 recall=59.092500

SQ_GREEDY_EVAL tag=it19_b1_plus8 alloc=[48, 56, 40, 32, 8, 16, 8, 8] bytes=216 recall=59.190000

SQ_GREEDY_EVAL tag=it19_b2_plus8 alloc=[48, 48, 48, 32, 8, 16, 8, 8] bytes=216 recall=59.347500

SQ_GREEDY_EVAL tag=it19_b3_plus8 alloc=[48, 48, 40, 40, 8, 16, 8, 8] bytes=216 recall=59.470000

SQ_GREEDY_EVAL tag=it19_b4_plus8 alloc=[48, 48, 40, 32, 16, 16, 8, 8] bytes=216 recall=59.240000

SQ_GREEDY_EVAL tag=it19_b5_plus8 alloc=[48, 48, 40, 32, 8, 24, 8, 8] bytes=216 recall=59.260000

SQ_GREEDY_EVAL tag=it19_b6_plus8 alloc=[48, 48, 40, 32, 8, 16, 16, 8] bytes=216 recall=59.302500

SQ_GREEDY_EVAL tag=it19_b7_plus8 alloc=[48, 48, 40, 32, 8, 16, 8, 16] bytes=216 recall=59.215000

SQ_GREEDY_EVAL tag=it20_b0_plus8 alloc=[56, 48, 40, 40, 8, 16, 8, 8] bytes=224 recall=60.047500

SQ_GREEDY_EVAL tag=it20_b1_plus8 alloc=[48, 56, 40, 40, 8, 16, 8, 8] bytes=224 recall=59.972500

SQ_GREEDY_EVAL tag=it20_b2_plus8 alloc=[48, 48, 48, 40, 8, 16, 8, 8] bytes=224 recall=60.362500

SQ_GREEDY_EVAL tag=it20_b3_plus8 alloc=[48, 48, 40, 48, 8, 16, 8, 8] bytes=224 recall=60.597500

SQ_GREEDY_EVAL tag=it20_b4_plus8 alloc=[48, 48, 40, 40, 16, 16, 8, 8] bytes=224 recall=60.252500

SQ_GREEDY_EVAL tag=it20_b5_plus8 alloc=[48, 48, 40, 40, 8, 24, 8, 8] bytes=224 recall=60.175000

SQ_GREEDY_EVAL tag=it20_b6_plus8 alloc=[48, 48, 40, 40, 8, 16, 16, 8] bytes=224 recall=60.147500

SQ_GREEDY_EVAL tag=it20_b7_plus8 alloc=[48, 48, 40, 40, 8, 16, 8, 16] bytes=224 recall=60.085000

SQ_GREEDY_EVAL tag=it21_b0_plus8 alloc=[56, 48, 40, 48, 8, 16, 8, 8] bytes=232 recall=61.140000

SQ_GREEDY_EVAL tag=it21_b1_plus8 alloc=[48, 56, 40, 48, 8, 16, 8, 8] bytes=232 recall=61.327500

SQ_GREEDY_EVAL tag=it21_b2_plus8 alloc=[48, 48, 48, 48, 8, 16, 8, 8] bytes=232 recall=61.567500

SQ_GREEDY_EVAL tag=it21_b3_plus8 alloc=[48, 48, 40, 56, 8, 16, 8, 8] bytes=232 recall=60.907500

SQ_GREEDY_EVAL tag=it21_b4_plus8 alloc=[48, 48, 40, 48, 16, 16, 8, 8] bytes=232 recall=61.285000

SQ_GREEDY_EVAL tag=it21_b5_plus8 alloc=[48, 48, 40, 48, 8, 24, 8, 8] bytes=232 recall=61.067500

SQ_GREEDY_EVAL tag=it21_b6_plus8 alloc=[48, 48, 40, 48, 8, 16, 16, 8] bytes=232 recall=61.342500

SQ_GREEDY_EVAL tag=it21_b7_plus8 alloc=[48, 48, 40, 48, 8, 16, 8, 16] bytes=232 recall=61.102500

SQ_GREEDY_EVAL tag=it22_b0_plus8 alloc=[56, 48, 48, 48, 8, 16, 8, 8] bytes=240 recall=62.120000

SQ_GREEDY_EVAL tag=it22_b1_plus8 alloc=[48, 56, 48, 48, 8, 16, 8, 8] bytes=240 recall=62.095000

SQ_GREEDY_EVAL tag=it22_b2_plus8 alloc=[48, 48, 56, 48, 8, 16, 8, 8] bytes=240 recall=62.110000

SQ_GREEDY_EVAL tag=it22_b3_plus8 alloc=[48, 48, 48, 56, 8, 16, 8, 8] bytes=240 recall=61.857500

SQ_GREEDY_EVAL tag=it22_b4_plus8 alloc=[48, 48, 48, 48, 16, 16, 8, 8] bytes=240 recall=62.212500

SQ_GREEDY_EVAL tag=it22_b5_plus8 alloc=[48, 48, 48, 48, 8, 24, 8, 8] bytes=240 recall=62.065000

SQ_GREEDY_EVAL tag=it22_b6_plus8 alloc=[48, 48, 48, 48, 8, 16, 16, 8] bytes=240 recall=62.067500

SQ_GREEDY_EVAL tag=it22_b7_plus8 alloc=[48, 48, 48, 48, 8, 16, 8, 16] bytes=240 recall=62.040000

SQ_GREEDY_EVAL tag=it23_b0_plus8 alloc=[56, 48, 48, 48, 16, 16, 8, 8] bytes=248 recall=62.752500

SQ_GREEDY_EVAL tag=it23_b1_plus8 alloc=[48, 56, 48, 48, 16, 16, 8, 8] bytes=248 recall=62.847500

SQ_GREEDY_EVAL tag=it23_b2_plus8 alloc=[48, 48, 56, 48, 16, 16, 8, 8] bytes=248 recall=62.647500

SQ_GREEDY_EVAL tag=it23_b3_plus8 alloc=[48, 48, 48, 56, 16, 16, 8, 8] bytes=248 recall=62.517500

SQ_GREEDY_EVAL tag=it23_b4_plus8 alloc=[48, 48, 48, 48, 24, 16, 8, 8] bytes=248 recall=63.095000

SQ_GREEDY_EVAL tag=it23_b5_plus8 alloc=[48, 48, 48, 48, 16, 24, 8, 8] bytes=248 recall=62.785000

SQ_GREEDY_EVAL tag=it23_b6_plus8 alloc=[48, 48, 48, 48, 16, 16, 16, 8] bytes=248 recall=62.682500

SQ_GREEDY_EVAL tag=it23_b7_plus8 alloc=[48, 48, 48, 48, 16, 16, 8, 16] bytes=248 recall=62.730000

SQ_GREEDY_EVAL tag=it24_b0_plus8 alloc=[56, 48, 48, 48, 24, 16, 8, 8] bytes=256 recall=63.535000

SQ_GREEDY_EVAL tag=it24_b1_plus8 alloc=[48, 56, 48, 48, 24, 16, 8, 8] bytes=256 recall=63.607500

SQ_GREEDY_EVAL tag=it24_b2_plus8 alloc=[48, 48, 56, 48, 24, 16, 8, 8] bytes=256 recall=63.617500

SQ_GREEDY_EVAL tag=it24_b3_plus8 alloc=[48, 48, 48, 56, 24, 16, 8, 8] bytes=256 recall=63.337500

SQ_GREEDY_EVAL tag=it24_b4_plus8 alloc=[48, 48, 48, 48, 32, 16, 8, 8] bytes=256 recall=64.125000

SQ_GREEDY_EVAL tag=it24_b5_plus8 alloc=[48, 48, 48, 48, 24, 24, 8, 8] bytes=256 recall=63.587500

SQ_GREEDY_EVAL tag=it24_b6_plus8 alloc=[48, 48, 48, 48, 24, 16, 16, 8] bytes=256 recall=63.567500

SQ_GREEDY_EVAL tag=it24_b7_plus8 alloc=[48, 48, 48, 48, 24, 16, 8, 16] bytes=256 recall=63.537500

SQ_GREEDY_EVAL tag=it25_b0_plus8 alloc=[56, 48, 48, 48, 32, 16, 8, 8] bytes=264 recall=64.390000

SQ_GREEDY_EVAL tag=it25_b1_plus8 alloc=[48, 56, 48, 48, 32, 16, 8, 8] bytes=264 recall=64.567500

SQ_GREEDY_EVAL tag=it25_b2_plus8 alloc=[48, 48, 56, 48, 32, 16, 8, 8] bytes=264 recall=64.565000

SQ_GREEDY_EVAL tag=it25_b3_plus8 alloc=[48, 48, 48, 56, 32, 16, 8, 8] bytes=264 recall=64.340000

SQ_GREEDY_EVAL tag=it25_b4_plus8 alloc=[48, 48, 48, 48, 40, 16, 8, 8] bytes=264 recall=64.702500

SQ_GREEDY_EVAL tag=it25_b5_plus8 alloc=[48, 48, 48, 48, 32, 24, 8, 8] bytes=264 recall=64.545000

SQ_GREEDY_EVAL tag=it25_b6_plus8 alloc=[48, 48, 48, 48, 32, 16, 16, 8] bytes=264 recall=64.587500

SQ_GREEDY_EVAL tag=it25_b7_plus8 alloc=[48, 48, 48, 48, 32, 16, 8, 16] bytes=264 recall=64.400000

SQ_GREEDY_EVAL tag=it26_b0_plus8 alloc=[56, 48, 48, 48, 40, 16, 8, 8] bytes=272 recall=65.140000

SQ_GREEDY_EVAL tag=it26_b1_plus8 alloc=[48, 56, 48, 48, 40, 16, 8, 8] bytes=272 recall=65.370000

SQ_GREEDY_EVAL tag=it26_b2_plus8 alloc=[48, 48, 56, 48, 40, 16, 8, 8] bytes=272 recall=65.227500

SQ_GREEDY_EVAL tag=it26_b3_plus8 alloc=[48, 48, 48, 56, 40, 16, 8, 8] bytes=272 recall=65.035000

SQ_GREEDY_EVAL tag=it26_b4_plus8 alloc=[48, 48, 48, 48, 48, 16, 8, 8] bytes=272 recall=65.775000

SQ_GREEDY_EVAL tag=it26_b5_plus8 alloc=[48, 48, 48, 48, 40, 24, 8, 8] bytes=272 recall=65.237500

SQ_GREEDY_EVAL tag=it26_b6_plus8 alloc=[48, 48, 48, 48, 40, 16, 16, 8] bytes=272 recall=65.190000

SQ_GREEDY_EVAL tag=it26_b7_plus8 alloc=[48, 48, 48, 48, 40, 16, 8, 16] bytes=272 recall=65.155000

SQ_GREEDY_EVAL tag=it27_b0_plus8 alloc=[56, 48, 48, 48, 48, 16, 8, 8] bytes=280 recall=66.137500

SQ_GREEDY_EVAL tag=it27_b1_plus8 alloc=[48, 56, 48, 48, 48, 16, 8, 8] bytes=280 recall=66.290000

SQ_GREEDY_EVAL tag=it27_b2_plus8 alloc=[48, 48, 56, 48, 48, 16, 8, 8] bytes=280 recall=66.137500

SQ_GREEDY_EVAL tag=it27_b3_plus8 alloc=[48, 48, 48, 56, 48, 16, 8, 8] bytes=280 recall=66.027500

SQ_GREEDY_EVAL tag=it27_b4_plus8 alloc=[48, 48, 48, 48, 56, 16, 8, 8] bytes=280 recall=66.020000

SQ_GREEDY_EVAL tag=it27_b5_plus8 alloc=[48, 48, 48, 48, 48, 24, 8, 8] bytes=280 recall=66.115000

SQ_GREEDY_EVAL tag=it27_b6_plus8 alloc=[48, 48, 48, 48, 48, 16, 16, 8] bytes=280 recall=66.277500

SQ_GREEDY_EVAL tag=it27_b7_plus8 alloc=[48, 48, 48, 48, 48, 16, 8, 16] bytes=280 recall=66.035000

SQ_GREEDY_EVAL tag=it28_b0_plus8 alloc=[56, 56, 48, 48, 48, 16, 8, 8] bytes=288 recall=66.792500

SQ_GREEDY_EVAL tag=it28_b1_plus8 alloc=[48, 64, 48, 48, 48, 16, 8, 8] bytes=288 recall=66.662500

SQ_GREEDY_EVAL tag=it28_b2_plus8 alloc=[48, 56, 56, 48, 48, 16, 8, 8] bytes=288 recall=66.725000

SQ_GREEDY_EVAL tag=it28_b3_plus8 alloc=[48, 56, 48, 56, 48, 16, 8, 8] bytes=288 recall=66.635000

SQ_GREEDY_EVAL tag=it28_b4_plus8 alloc=[48, 56, 48, 48, 56, 16, 8, 8] bytes=288 recall=66.697500

SQ_GREEDY_EVAL tag=it28_b5_plus8 alloc=[48, 56, 48, 48, 48, 24, 8, 8] bytes=288 recall=66.767500

SQ_GREEDY_EVAL tag=it28_b6_plus8 alloc=[48, 56, 48, 48, 48, 16, 16, 8] bytes=288 recall=66.892500

SQ_GREEDY_EVAL tag=it28_b7_plus8 alloc=[48, 56, 48, 48, 48, 16, 8, 16] bytes=288 recall=66.740000

SQ_GREEDY_EVAL tag=it29_b0_plus8 alloc=[56, 56, 48, 48, 48, 16, 16, 8] bytes=296 recall=67.427500

SQ_GREEDY_EVAL tag=it29_b1_plus8 alloc=[48, 64, 48, 48, 48, 16, 16, 8] bytes=296 recall=67.192500

SQ_GREEDY_EVAL tag=it29_b2_plus8 alloc=[48, 56, 56, 48, 48, 16, 16, 8] bytes=296 recall=67.232500

SQ_GREEDY_EVAL tag=it29_b3_plus8 alloc=[48, 56, 48, 56, 48, 16, 16, 8] bytes=296 recall=67.167500

SQ_GREEDY_EVAL tag=it29_b4_plus8 alloc=[48, 56, 48, 48, 56, 16, 16, 8] bytes=296 recall=67.225000

SQ_GREEDY_EVAL tag=it29_b5_plus8 alloc=[48, 56, 48, 48, 48, 24, 16, 8] bytes=296 recall=67.355000

SQ_GREEDY_EVAL tag=it29_b6_plus8 alloc=[48, 56, 48, 48, 48, 16, 24, 8] bytes=296 recall=67.407500

SQ_GREEDY_EVAL tag=it29_b7_plus8 alloc=[48, 56, 48, 48, 48, 16, 16, 16] bytes=296 recall=67.242500

SQ_GREEDY_EVAL tag=it30_b0_plus8 alloc=[64, 56, 48, 48, 48, 16, 16, 8] bytes=304 recall=67.795000

SQ_GREEDY_EVAL tag=it30_b1_plus8 alloc=[56, 64, 48, 48, 48, 16, 16, 8] bytes=304 recall=67.792500

SQ_GREEDY_EVAL tag=it30_b2_plus8 alloc=[56, 56, 56, 48, 48, 16, 16, 8] bytes=304 recall=67.727500

SQ_GREEDY_EVAL tag=it30_b3_plus8 alloc=[56, 56, 48, 56, 48, 16, 16, 8] bytes=304 recall=67.627500

SQ_GREEDY_EVAL tag=it30_b4_plus8 alloc=[56, 56, 48, 48, 56, 16, 16, 8] bytes=304 recall=67.660000

SQ_GREEDY_EVAL tag=it30_b5_plus8 alloc=[56, 56, 48, 48, 48, 24, 16, 8] bytes=304 recall=67.822500

SQ_GREEDY_EVAL tag=it30_b6_plus8 alloc=[56, 56, 48, 48, 48, 16, 24, 8] bytes=304 recall=67.905000

SQ_GREEDY_EVAL tag=it30_b7_plus8 alloc=[56, 56, 48, 48, 48, 16, 16, 16] bytes=304 recall=67.710000

SQ_GREEDY_EVAL tag=it31_b0_plus8 alloc=[64, 56, 48, 48, 48, 16, 24, 8] bytes=312 recall=68.330000

SQ_GREEDY_EVAL tag=it31_b1_plus8 alloc=[56, 64, 48, 48, 48, 16, 24, 8] bytes=312 recall=68.242500

SQ_GREEDY_EVAL tag=it31_b2_plus8 alloc=[56, 56, 56, 48, 48, 16, 24, 8] bytes=312 recall=68.305000

SQ_GREEDY_EVAL tag=it31_b3_plus8 alloc=[56, 56, 48, 56, 48, 16, 24, 8] bytes=312 recall=68.077500

SQ_GREEDY_EVAL tag=it31_b4_plus8 alloc=[56, 56, 48, 48, 56, 16, 24, 8] bytes=312 recall=68.167500

SQ_GREEDY_EVAL tag=it31_b5_plus8 alloc=[56, 56, 48, 48, 48, 24, 24, 8] bytes=312 recall=68.322500

SQ_GREEDY_EVAL tag=it31_b6_plus8 alloc=[56, 56, 48, 48, 48, 16, 32, 8] bytes=312 recall=68.392500

SQ_GREEDY_EVAL tag=it31_b7_plus8 alloc=[56, 56, 48, 48, 48, 16, 24, 16] bytes=312 recall=68.215000

SQ_GREEDY_EVAL tag=it32_b0_plus8 alloc=[64, 56, 48, 48, 48, 16, 32, 8] bytes=320 recall=68.790000

SQ_GREEDY_EVAL tag=it32_b1_plus8 alloc=[56, 64, 48, 48, 48, 16, 32, 8] bytes=320 recall=68.717500

SQ_GREEDY_EVAL tag=it32_b2_plus8 alloc=[56, 56, 56, 48, 48, 16, 32, 8] bytes=320 recall=68.705000

SQ_GREEDY_EVAL tag=it32_b3_plus8 alloc=[56, 56, 48, 56, 48, 16, 32, 8] bytes=320 recall=68.640000

SQ_GREEDY_EVAL tag=it32_b4_plus8 alloc=[56, 56, 48, 48, 56, 16, 32, 8] bytes=320 recall=68.732500

SQ_GREEDY_EVAL tag=it32_b5_plus8 alloc=[56, 56, 48, 48, 48, 24, 32, 8] bytes=320 recall=68.877500

SQ_GREEDY_EVAL tag=it32_b6_plus8 alloc=[56, 56, 48, 48, 48, 16, 40, 8] bytes=320 recall=68.905000

SQ_GREEDY_EVAL tag=it32_b7_plus8 alloc=[56, 56, 48, 48, 48, 16, 32, 16] bytes=320 recall=68.770000

SQ_GREEDY_EVAL tag=it33_b0_plus8 alloc=[64, 56, 48, 48, 48, 16, 40, 8] bytes=328 recall=69.335000

SQ_GREEDY_EVAL tag=it33_b1_plus8 alloc=[56, 64, 48, 48, 48, 16, 40, 8] bytes=328 recall=69.315000

SQ_GREEDY_EVAL tag=it33_b2_plus8 alloc=[56, 56, 56, 48, 48, 16, 40, 8] bytes=328 recall=69.375000

SQ_GREEDY_EVAL tag=it33_b3_plus8 alloc=[56, 56, 48, 56, 48, 16, 40, 8] bytes=328 recall=69.147500

SQ_GREEDY_EVAL tag=it33_b4_plus8 alloc=[56, 56, 48, 48, 56, 16, 40, 8] bytes=328 recall=69.182500

SQ_GREEDY_EVAL tag=it33_b5_plus8 alloc=[56, 56, 48, 48, 48, 24, 40, 8] bytes=328 recall=69.285000

SQ_GREEDY_EVAL tag=it33_b6_plus8 alloc=[56, 56, 48, 48, 48, 16, 48, 8] bytes=328 recall=69.392500

SQ_GREEDY_EVAL tag=it33_b7_plus8 alloc=[56, 56, 48, 48, 48, 16, 40, 16] bytes=328 recall=69.285000

SQ_GREEDY_EVAL tag=it34_b0_plus8 alloc=[64, 56, 48, 48, 48, 16, 48, 8] bytes=336 recall=69.820000

SQ_GREEDY_EVAL tag=it34_b1_plus8 alloc=[56, 64, 48, 48, 48, 16, 48, 8] bytes=336 recall=69.790000

SQ_GREEDY_EVAL tag=it34_b2_plus8 alloc=[56, 56, 56, 48, 48, 16, 48, 8] bytes=336 recall=69.867500

SQ_GREEDY_EVAL tag=it34_b3_plus8 alloc=[56, 56, 48, 56, 48, 16, 48, 8] bytes=336 recall=69.612500

SQ_GREEDY_EVAL tag=it34_b4_plus8 alloc=[56, 56, 48, 48, 56, 16, 48, 8] bytes=336 recall=69.732500

SQ_GREEDY_EVAL tag=it34_b5_plus8 alloc=[56, 56, 48, 48, 48, 24, 48, 8] bytes=336 recall=69.772500

SQ_GREEDY_EVAL tag=it34_b6_plus8 alloc=[56, 56, 48, 48, 48, 16, 56, 8] bytes=336 recall=69.595000

SQ_GREEDY_EVAL tag=it34_b7_plus8 alloc=[56, 56, 48, 48, 48, 16, 48, 16] bytes=336 recall=69.797500

SQ_GREEDY_EVAL tag=it35_b0_plus8 alloc=[64, 56, 56, 48, 48, 16, 48, 8] bytes=344 recall=70.220000

SQ_GREEDY_EVAL tag=it35_b1_plus8 alloc=[56, 64, 56, 48, 48, 16, 48, 8] bytes=344 recall=70.247500

SQ_GREEDY_EVAL tag=it35_b2_plus8 alloc=[56, 56, 64, 48, 48, 16, 48, 8] bytes=344 recall=70.267500

SQ_GREEDY_EVAL tag=it35_b3_plus8 alloc=[56, 56, 56, 56, 48, 16, 48, 8] bytes=344 recall=70.052500

SQ_GREEDY_EVAL tag=it35_b4_plus8 alloc=[56, 56, 56, 48, 56, 16, 48, 8] bytes=344 recall=70.227500

SQ_GREEDY_EVAL tag=it35_b5_plus8 alloc=[56, 56, 56, 48, 48, 24, 48, 8] bytes=344 recall=70.335000

SQ_GREEDY_EVAL tag=it35_b6_plus8 alloc=[56, 56, 56, 48, 48, 16, 56, 8] bytes=344 recall=70.137500

SQ_GREEDY_EVAL tag=it35_b7_plus8 alloc=[56, 56, 56, 48, 48, 16, 48, 16] bytes=344 recall=70.225000

SQ_GREEDY_EVAL tag=it36_b0_plus8 alloc=[64, 56, 56, 48, 48, 24, 48, 8] bytes=352 recall=70.672500

SQ_GREEDY_EVAL tag=it36_b1_plus8 alloc=[56, 64, 56, 48, 48, 24, 48, 8] bytes=352 recall=70.730000

SQ_GREEDY_EVAL tag=it36_b2_plus8 alloc=[56, 56, 64, 48, 48, 24, 48, 8] bytes=352 recall=70.647500

SQ_GREEDY_EVAL tag=it36_b3_plus8 alloc=[56, 56, 56, 56, 48, 24, 48, 8] bytes=352 recall=70.655000

SQ_GREEDY_EVAL tag=it36_b4_plus8 alloc=[56, 56, 56, 48, 56, 24, 48, 8] bytes=352 recall=70.550000

SQ_GREEDY_EVAL tag=it36_b5_plus8 alloc=[56, 56, 56, 48, 48, 32, 48, 8] bytes=352 recall=71.022500

SQ_GREEDY_EVAL tag=it36_b6_plus8 alloc=[56, 56, 56, 48, 48, 24, 56, 8] bytes=352 recall=70.485000

SQ_GREEDY_EVAL tag=it36_b7_plus8 alloc=[56, 56, 56, 48, 48, 24, 48, 16] bytes=352 recall=70.732500

SQ_GREEDY_EVAL tag=it37_b0_plus8 alloc=[64, 56, 56, 48, 48, 32, 48, 8] bytes=360 recall=71.312500

SQ_GREEDY_EVAL tag=it37_b1_plus8 alloc=[56, 64, 56, 48, 48, 32, 48, 8] bytes=360 recall=71.450000

SQ_GREEDY_EVAL tag=it37_b2_plus8 alloc=[56, 56, 64, 48, 48, 32, 48, 8] bytes=360 recall=71.272500

SQ_GREEDY_EVAL tag=it37_b3_plus8 alloc=[56, 56, 56, 56, 48, 32, 48, 8] bytes=360 recall=71.237500

SQ_GREEDY_EVAL tag=it37_b4_plus8 alloc=[56, 56, 56, 48, 56, 32, 48, 8] bytes=360 recall=71.342500

SQ_GREEDY_EVAL tag=it37_b5_plus8 alloc=[56, 56, 56, 48, 48, 40, 48, 8] bytes=360 recall=71.410000

SQ_GREEDY_EVAL tag=it37_b6_plus8 alloc=[56, 56, 56, 48, 48, 32, 56, 8] bytes=360 recall=71.197500

SQ_GREEDY_EVAL tag=it37_b7_plus8 alloc=[56, 56, 56, 48, 48, 32, 48, 16] bytes=360 recall=71.280000

SQ_GREEDY_EVAL tag=it38_b0_plus8 alloc=[64, 64, 56, 48, 48, 32, 48, 8] bytes=368 recall=71.682500

SQ_GREEDY_EVAL tag=it38_b1_plus8 alloc=[56, 72, 56, 48, 48, 32, 48, 8] bytes=368 recall=71.780000

SQ_GREEDY_EVAL tag=it38_b2_plus8 alloc=[56, 64, 64, 48, 48, 32, 48, 8] bytes=368 recall=71.805000

SQ_GREEDY_EVAL tag=it38_b3_plus8 alloc=[56, 64, 56, 56, 48, 32, 48, 8] bytes=368 recall=71.802500

SQ_GREEDY_EVAL tag=it38_b4_plus8 alloc=[56, 64, 56, 48, 56, 32, 48, 8] bytes=368 recall=71.625000

SQ_GREEDY_EVAL tag=it38_b5_plus8 alloc=[56, 64, 56, 48, 48, 40, 48, 8] bytes=368 recall=71.812500

SQ_GREEDY_EVAL tag=it38_b6_plus8 alloc=[56, 64, 56, 48, 48, 32, 56, 8] bytes=368 recall=71.660000

SQ_GREEDY_EVAL tag=it38_b7_plus8 alloc=[56, 64, 56, 48, 48, 32, 48, 16] bytes=368 recall=71.780000

SQ_GREEDY_EVAL tag=it39_b0_plus8 alloc=[64, 64, 56, 48, 48, 40, 48, 8] bytes=376 recall=72.300000

SQ_GREEDY_EVAL tag=it39_b1_plus8 alloc=[56, 72, 56, 48, 48, 40, 48, 8] bytes=376 recall=72.160000

SQ_GREEDY_EVAL tag=it39_b2_plus8 alloc=[56, 64, 64, 48, 48, 40, 48, 8] bytes=376 recall=72.180000

SQ_GREEDY_EVAL tag=it39_b3_plus8 alloc=[56, 64, 56, 56, 48, 40, 48, 8] bytes=376 recall=72.195000

SQ_GREEDY_EVAL tag=it39_b4_plus8 alloc=[56, 64, 56, 48, 56, 40, 48, 8] bytes=376 recall=72.040000

SQ_GREEDY_EVAL tag=it39_b5_plus8 alloc=[56, 64, 56, 48, 48, 48, 48, 8] bytes=376 recall=72.342500

SQ_GREEDY_EVAL tag=it39_b6_plus8 alloc=[56, 64, 56, 48, 48, 40, 56, 8] bytes=376 recall=72.112500

SQ_GREEDY_EVAL tag=it39_b7_plus8 alloc=[56, 64, 56, 48, 48, 40, 48, 16] bytes=376 recall=72.085000

SQ_GREEDY_EVAL tag=it40_b0_plus8 alloc=[64, 64, 56, 48, 48, 48, 48, 8] bytes=384 recall=72.832500

SQ_GREEDY_EVAL tag=it40_b1_plus8 alloc=[56, 72, 56, 48, 48, 48, 48, 8] bytes=384 recall=72.647500

SQ_GREEDY_EVAL tag=it40_b2_plus8 alloc=[56, 64, 64, 48, 48, 48, 48, 8] bytes=384 recall=72.697500

SQ_GREEDY_EVAL tag=it40_b3_plus8 alloc=[56, 64, 56, 56, 48, 48, 48, 8] bytes=384 recall=72.572500

SQ_GREEDY_EVAL tag=it40_b4_plus8 alloc=[56, 64, 56, 48, 56, 48, 48, 8] bytes=384 recall=72.652500

SQ_GREEDY_EVAL tag=it40_b5_plus8 alloc=[56, 64, 56, 48, 48, 56, 48, 8] bytes=384 recall=72.665000

SQ_GREEDY_EVAL tag=it40_b6_plus8 alloc=[56, 64, 56, 48, 48, 48, 56, 8] bytes=384 recall=72.665000

SQ_GREEDY_EVAL tag=it40_b7_plus8 alloc=[56, 64, 56, 48, 48, 48, 48, 16] bytes=384 recall=72.547500



### DBPedia openai-text-large-3
#### Uniform SQ
SQ sweep completed!
Results directory: /tmp/sq_sweep_1779558716

Summary of SQ recall results:
Bytes,Recall
64,36.9
96,47.18
128,54.88
160,59.685
192,63.4
224,66.6125
256,69.32
288,71.2575
320,73.075
352,74.485
384,75.94

#### Variable SQ
SQ_GREEDY_EVAL tag=init alloc=[8, 8, 8, 8, 8, 8, 8, 8] bytes=64 recall=28.630000

SQ_GREEDY_EVAL tag=it1_b0_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 8] bytes=72 recall=32.402500

SQ_GREEDY_EVAL tag=it1_b1_plus8 alloc=[8, 16, 8, 8, 8, 8, 8, 8] bytes=72 recall=32.152500

SQ_GREEDY_EVAL tag=it1_b2_plus8 alloc=[8, 8, 16, 8, 8, 8, 8, 8] bytes=72 recall=32.430000

SQ_GREEDY_EVAL tag=it1_b3_plus8 alloc=[8, 8, 8, 16, 8, 8, 8, 8] bytes=72 recall=31.732500

SQ_GREEDY_EVAL tag=it1_b4_plus8 alloc=[8, 8, 8, 8, 16, 8, 8, 8] bytes=72 recall=31.605000

SQ_GREEDY_EVAL tag=it1_b5_plus8 alloc=[8, 8, 8, 8, 8, 16, 8, 8] bytes=72 recall=31.155000

SQ_GREEDY_EVAL tag=it1_b6_plus8 alloc=[8, 8, 8, 8, 8, 8, 16, 8] bytes=72 recall=31.425000

SQ_GREEDY_EVAL tag=it1_b7_plus8 alloc=[8, 8, 8, 8, 8, 8, 8, 16] bytes=72 recall=31.182500

SQ_GREEDY_EVAL tag=it2_b0_plus8 alloc=[16, 8, 16, 8, 8, 8, 8, 8] bytes=80 recall=35.680000

SQ_GREEDY_EVAL tag=it2_b1_plus8 alloc=[8, 16, 16, 8, 8, 8, 8, 8] bytes=80 recall=35.610000

SQ_GREEDY_EVAL tag=it2_b2_plus8 alloc=[8, 8, 24, 8, 8, 8, 8, 8] bytes=80 recall=35.930000

SQ_GREEDY_EVAL tag=it2_b3_plus8 alloc=[8, 8, 16, 16, 8, 8, 8, 8] bytes=80 recall=35.190000

SQ_GREEDY_EVAL tag=it2_b4_plus8 alloc=[8, 8, 16, 8, 16, 8, 8, 8] bytes=80 recall=35.270000

SQ_GREEDY_EVAL tag=it2_b5_plus8 alloc=[8, 8, 16, 8, 8, 16, 8, 8] bytes=80 recall=34.855000

SQ_GREEDY_EVAL tag=it2_b6_plus8 alloc=[8, 8, 16, 8, 8, 8, 16, 8] bytes=80 recall=35.077500

SQ_GREEDY_EVAL tag=it2_b7_plus8 alloc=[8, 8, 16, 8, 8, 8, 8, 16] bytes=80 recall=34.922500

SQ_GREEDY_EVAL tag=it3_b0_plus8 alloc=[16, 8, 24, 8, 8, 8, 8, 8] bytes=88 recall=38.752500

SQ_GREEDY_EVAL tag=it3_b1_plus8 alloc=[8, 16, 24, 8, 8, 8, 8, 8] bytes=88 recall=38.755000

SQ_GREEDY_EVAL tag=it3_b2_plus8 alloc=[8, 8, 32, 8, 8, 8, 8, 8] bytes=88 recall=38.730000

SQ_GREEDY_EVAL tag=it3_b3_plus8 alloc=[8, 8, 24, 16, 8, 8, 8, 8] bytes=88 recall=38.255000

SQ_GREEDY_EVAL tag=it3_b4_plus8 alloc=[8, 8, 24, 8, 16, 8, 8, 8] bytes=88 recall=38.195000

SQ_GREEDY_EVAL tag=it3_b5_plus8 alloc=[8, 8, 24, 8, 8, 16, 8, 8] bytes=88 recall=37.897500

SQ_GREEDY_EVAL tag=it3_b6_plus8 alloc=[8, 8, 24, 8, 8, 8, 16, 8] bytes=88 recall=38.140000

SQ_GREEDY_EVAL tag=it3_b7_plus8 alloc=[8, 8, 24, 8, 8, 8, 8, 16] bytes=88 recall=37.882500

SQ_GREEDY_EVAL tag=it4_b0_plus8 alloc=[16, 16, 24, 8, 8, 8, 8, 8] bytes=96 recall=41.275000

SQ_GREEDY_EVAL tag=it4_b1_plus8 alloc=[8, 24, 24, 8, 8, 8, 8, 8] bytes=96 recall=41.407500

SQ_GREEDY_EVAL tag=it4_b2_plus8 alloc=[8, 16, 32, 8, 8, 8, 8, 8] bytes=96 recall=41.482500

SQ_GREEDY_EVAL tag=it4_b3_plus8 alloc=[8, 16, 24, 16, 8, 8, 8, 8] bytes=96 recall=40.932500

SQ_GREEDY_EVAL tag=it4_b4_plus8 alloc=[8, 16, 24, 8, 16, 8, 8, 8] bytes=96 recall=40.932500

SQ_GREEDY_EVAL tag=it4_b5_plus8 alloc=[8, 16, 24, 8, 8, 16, 8, 8] bytes=96 recall=40.600000

SQ_GREEDY_EVAL tag=it4_b6_plus8 alloc=[8, 16, 24, 8, 8, 8, 16, 8] bytes=96 recall=40.580000

SQ_GREEDY_EVAL tag=it4_b7_plus8 alloc=[8, 16, 24, 8, 8, 8, 8, 16] bytes=96 recall=40.632500

SQ_GREEDY_EVAL tag=it5_b0_plus8 alloc=[16, 16, 32, 8, 8, 8, 8, 8] bytes=104 recall=43.710000

SQ_GREEDY_EVAL tag=it5_b1_plus8 alloc=[8, 24, 32, 8, 8, 8, 8, 8] bytes=104 recall=43.815000

SQ_GREEDY_EVAL tag=it5_b2_plus8 alloc=[8, 16, 40, 8, 8, 8, 8, 8] bytes=104 recall=43.547500

SQ_GREEDY_EVAL tag=it5_b3_plus8 alloc=[8, 16, 32, 16, 8, 8, 8, 8] bytes=104 recall=43.435000

SQ_GREEDY_EVAL tag=it5_b4_plus8 alloc=[8, 16, 32, 8, 16, 8, 8, 8] bytes=104 recall=43.317500

SQ_GREEDY_EVAL tag=it5_b5_plus8 alloc=[8, 16, 32, 8, 8, 16, 8, 8] bytes=104 recall=43.095000

SQ_GREEDY_EVAL tag=it5_b6_plus8 alloc=[8, 16, 32, 8, 8, 8, 16, 8] bytes=104 recall=43.240000

SQ_GREEDY_EVAL tag=it5_b7_plus8 alloc=[8, 16, 32, 8, 8, 8, 8, 16] bytes=104 recall=42.972500

SQ_GREEDY_EVAL tag=it6_b0_plus8 alloc=[16, 24, 32, 8, 8, 8, 8, 8] bytes=112 recall=45.735000

SQ_GREEDY_EVAL tag=it6_b1_plus8 alloc=[8, 32, 32, 8, 8, 8, 8, 8] bytes=112 recall=46.217500

SQ_GREEDY_EVAL tag=it6_b2_plus8 alloc=[8, 24, 40, 8, 8, 8, 8, 8] bytes=112 recall=45.875000

SQ_GREEDY_EVAL tag=it6_b3_plus8 alloc=[8, 24, 32, 16, 8, 8, 8, 8] bytes=112 recall=45.650000

SQ_GREEDY_EVAL tag=it6_b4_plus8 alloc=[8, 24, 32, 8, 16, 8, 8, 8] bytes=112 recall=45.600000

SQ_GREEDY_EVAL tag=it6_b5_plus8 alloc=[8, 24, 32, 8, 8, 16, 8, 8] bytes=112 recall=45.147500

SQ_GREEDY_EVAL tag=it6_b6_plus8 alloc=[8, 24, 32, 8, 8, 8, 16, 8] bytes=112 recall=45.410000

SQ_GREEDY_EVAL tag=it6_b7_plus8 alloc=[8, 24, 32, 8, 8, 8, 8, 16] bytes=112 recall=45.335000

SQ_GREEDY_EVAL tag=it7_b0_plus8 alloc=[16, 32, 32, 8, 8, 8, 8, 8] bytes=120 recall=47.872500

SQ_GREEDY_EVAL tag=it7_b1_plus8 alloc=[8, 40, 32, 8, 8, 8, 8, 8] bytes=120 recall=48.202500

SQ_GREEDY_EVAL tag=it7_b2_plus8 alloc=[8, 32, 40, 8, 8, 8, 8, 8] bytes=120 recall=47.997500

SQ_GREEDY_EVAL tag=it7_b3_plus8 alloc=[8, 32, 32, 16, 8, 8, 8, 8] bytes=120 recall=47.857500

SQ_GREEDY_EVAL tag=it7_b4_plus8 alloc=[8, 32, 32, 8, 16, 8, 8, 8] bytes=120 recall=47.532500

SQ_GREEDY_EVAL tag=it7_b5_plus8 alloc=[8, 32, 32, 8, 8, 16, 8, 8] bytes=120 recall=47.402500

SQ_GREEDY_EVAL tag=it7_b6_plus8 alloc=[8, 32, 32, 8, 8, 8, 16, 8] bytes=120 recall=47.560000

SQ_GREEDY_EVAL tag=it7_b7_plus8 alloc=[8, 32, 32, 8, 8, 8, 8, 16] bytes=120 recall=47.575000

SQ_GREEDY_EVAL tag=it8_b0_plus8 alloc=[16, 40, 32, 8, 8, 8, 8, 8] bytes=128 recall=49.847500

SQ_GREEDY_EVAL tag=it8_b1_plus8 alloc=[8, 48, 32, 8, 8, 8, 8, 8] bytes=128 recall=49.640000

SQ_GREEDY_EVAL tag=it8_b2_plus8 alloc=[8, 40, 40, 8, 8, 8, 8, 8] bytes=128 recall=49.787500

SQ_GREEDY_EVAL tag=it8_b3_plus8 alloc=[8, 40, 32, 16, 8, 8, 8, 8] bytes=128 recall=49.595000

SQ_GREEDY_EVAL tag=it8_b4_plus8 alloc=[8, 40, 32, 8, 16, 8, 8, 8] bytes=128 recall=49.470000

SQ_GREEDY_EVAL tag=it8_b5_plus8 alloc=[8, 40, 32, 8, 8, 16, 8, 8] bytes=128 recall=49.267500

SQ_GREEDY_EVAL tag=it8_b6_plus8 alloc=[8, 40, 32, 8, 8, 8, 16, 8] bytes=128 recall=49.325000

SQ_GREEDY_EVAL tag=it8_b7_plus8 alloc=[8, 40, 32, 8, 8, 8, 8, 16] bytes=128 recall=49.415000

SQ_GREEDY_EVAL tag=it9_b0_plus8 alloc=[24, 40, 32, 8, 8, 8, 8, 8] bytes=136 recall=51.840000

SQ_GREEDY_EVAL tag=it9_b1_plus8 alloc=[16, 48, 32, 8, 8, 8, 8, 8] bytes=136 recall=51.240000

SQ_GREEDY_EVAL tag=it9_b2_plus8 alloc=[16, 40, 40, 8, 8, 8, 8, 8] bytes=136 recall=51.435000

SQ_GREEDY_EVAL tag=it9_b3_plus8 alloc=[16, 40, 32, 16, 8, 8, 8, 8] bytes=136 recall=51.250000

SQ_GREEDY_EVAL tag=it9_b4_plus8 alloc=[16, 40, 32, 8, 16, 8, 8, 8] bytes=136 recall=51.107500

SQ_GREEDY_EVAL tag=it9_b5_plus8 alloc=[16, 40, 32, 8, 8, 16, 8, 8] bytes=136 recall=50.927500

SQ_GREEDY_EVAL tag=it9_b6_plus8 alloc=[16, 40, 32, 8, 8, 8, 16, 8] bytes=136 recall=50.965000

SQ_GREEDY_EVAL tag=it9_b7_plus8 alloc=[16, 40, 32, 8, 8, 8, 8, 16] bytes=136 recall=50.885000

SQ_GREEDY_EVAL tag=it10_b0_plus8 alloc=[32, 40, 32, 8, 8, 8, 8, 8] bytes=144 recall=53.590000

SQ_GREEDY_EVAL tag=it10_b1_plus8 alloc=[24, 48, 32, 8, 8, 8, 8, 8] bytes=144 recall=53.122500

SQ_GREEDY_EVAL tag=it10_b2_plus8 alloc=[24, 40, 40, 8, 8, 8, 8, 8] bytes=144 recall=53.220000

SQ_GREEDY_EVAL tag=it10_b3_plus8 alloc=[24, 40, 32, 16, 8, 8, 8, 8] bytes=144 recall=53.202500

SQ_GREEDY_EVAL tag=it10_b4_plus8 alloc=[24, 40, 32, 8, 16, 8, 8, 8] bytes=144 recall=52.855000

SQ_GREEDY_EVAL tag=it10_b5_plus8 alloc=[24, 40, 32, 8, 8, 16, 8, 8] bytes=144 recall=52.685000

SQ_GREEDY_EVAL tag=it10_b6_plus8 alloc=[24, 40, 32, 8, 8, 8, 16, 8] bytes=144 recall=52.900000

SQ_GREEDY_EVAL tag=it10_b7_plus8 alloc=[24, 40, 32, 8, 8, 8, 8, 16] bytes=144 recall=52.775000

SQ_GREEDY_EVAL tag=it11_b0_plus8 alloc=[40, 40, 32, 8, 8, 8, 8, 8] bytes=152 recall=55.425000

SQ_GREEDY_EVAL tag=it11_b1_plus8 alloc=[32, 48, 32, 8, 8, 8, 8, 8] bytes=152 recall=54.895000

SQ_GREEDY_EVAL tag=it11_b2_plus8 alloc=[32, 40, 40, 8, 8, 8, 8, 8] bytes=152 recall=54.922500

SQ_GREEDY_EVAL tag=it11_b3_plus8 alloc=[32, 40, 32, 16, 8, 8, 8, 8] bytes=152 recall=54.877500

SQ_GREEDY_EVAL tag=it11_b4_plus8 alloc=[32, 40, 32, 8, 16, 8, 8, 8] bytes=152 recall=54.620000

SQ_GREEDY_EVAL tag=it11_b5_plus8 alloc=[32, 40, 32, 8, 8, 16, 8, 8] bytes=152 recall=54.460000

SQ_GREEDY_EVAL tag=it11_b6_plus8 alloc=[32, 40, 32, 8, 8, 8, 16, 8] bytes=152 recall=54.635000

SQ_GREEDY_EVAL tag=it11_b7_plus8 alloc=[32, 40, 32, 8, 8, 8, 8, 16] bytes=152 recall=54.572500

SQ_GREEDY_EVAL tag=it12_b0_plus8 alloc=[48, 40, 32, 8, 8, 8, 8, 8] bytes=160 recall=56.855000

SQ_GREEDY_EVAL tag=it12_b1_plus8 alloc=[40, 48, 32, 8, 8, 8, 8, 8] bytes=160 recall=56.510000

SQ_GREEDY_EVAL tag=it12_b2_plus8 alloc=[40, 40, 40, 8, 8, 8, 8, 8] bytes=160 recall=56.632500

SQ_GREEDY_EVAL tag=it12_b3_plus8 alloc=[40, 40, 32, 16, 8, 8, 8, 8] bytes=160 recall=56.500000

SQ_GREEDY_EVAL tag=it12_b4_plus8 alloc=[40, 40, 32, 8, 16, 8, 8, 8] bytes=160 recall=56.245000

SQ_GREEDY_EVAL tag=it12_b5_plus8 alloc=[40, 40, 32, 8, 8, 16, 8, 8] bytes=160 recall=56.212500

SQ_GREEDY_EVAL tag=it12_b6_plus8 alloc=[40, 40, 32, 8, 8, 8, 16, 8] bytes=160 recall=56.260000

SQ_GREEDY_EVAL tag=it12_b7_plus8 alloc=[40, 40, 32, 8, 8, 8, 8, 16] bytes=160 recall=56.197500

SQ_GREEDY_EVAL tag=it13_b0_plus8 alloc=[56, 40, 32, 8, 8, 8, 8, 8] bytes=168 recall=57.927500

SQ_GREEDY_EVAL tag=it13_b1_plus8 alloc=[48, 48, 32, 8, 8, 8, 8, 8] bytes=168 recall=57.832500

SQ_GREEDY_EVAL tag=it13_b2_plus8 alloc=[48, 40, 40, 8, 8, 8, 8, 8] bytes=168 recall=57.800000

SQ_GREEDY_EVAL tag=it13_b3_plus8 alloc=[48, 40, 32, 16, 8, 8, 8, 8] bytes=168 recall=57.722500

SQ_GREEDY_EVAL tag=it13_b4_plus8 alloc=[48, 40, 32, 8, 16, 8, 8, 8] bytes=168 recall=57.625000

SQ_GREEDY_EVAL tag=it13_b5_plus8 alloc=[48, 40, 32, 8, 8, 16, 8, 8] bytes=168 recall=57.522500

SQ_GREEDY_EVAL tag=it13_b6_plus8 alloc=[48, 40, 32, 8, 8, 8, 16, 8] bytes=168 recall=57.707500

SQ_GREEDY_EVAL tag=it13_b7_plus8 alloc=[48, 40, 32, 8, 8, 8, 8, 16] bytes=168 recall=57.587500

SQ_GREEDY_EVAL tag=it14_b0_plus8 alloc=[64, 40, 32, 8, 8, 8, 8, 8] bytes=176 recall=59.572500

SQ_GREEDY_EVAL tag=it14_b1_plus8 alloc=[56, 48, 32, 8, 8, 8, 8, 8] bytes=176 recall=59.125000

SQ_GREEDY_EVAL tag=it14_b2_plus8 alloc=[56, 40, 40, 8, 8, 8, 8, 8] bytes=176 recall=59.205000

SQ_GREEDY_EVAL tag=it14_b3_plus8 alloc=[56, 40, 32, 16, 8, 8, 8, 8] bytes=176 recall=58.885000

SQ_GREEDY_EVAL tag=it14_b4_plus8 alloc=[56, 40, 32, 8, 16, 8, 8, 8] bytes=176 recall=58.822500

SQ_GREEDY_EVAL tag=it14_b5_plus8 alloc=[56, 40, 32, 8, 8, 16, 8, 8] bytes=176 recall=58.687500

SQ_GREEDY_EVAL tag=it14_b6_plus8 alloc=[56, 40, 32, 8, 8, 8, 16, 8] bytes=176 recall=58.747500

SQ_GREEDY_EVAL tag=it14_b7_plus8 alloc=[56, 40, 32, 8, 8, 8, 8, 16] bytes=176 recall=58.690000

SQ_GREEDY_EVAL tag=it15_b0_plus8 alloc=[72, 40, 32, 8, 8, 8, 8, 8] bytes=184 recall=60.965000

SQ_GREEDY_EVAL tag=it15_b1_plus8 alloc=[64, 48, 32, 8, 8, 8, 8, 8] bytes=184 recall=60.490000

SQ_GREEDY_EVAL tag=it15_b2_plus8 alloc=[64, 40, 40, 8, 8, 8, 8, 8] bytes=184 recall=60.580000

SQ_GREEDY_EVAL tag=it15_b3_plus8 alloc=[64, 40, 32, 16, 8, 8, 8, 8] bytes=184 recall=60.357500

SQ_GREEDY_EVAL tag=it15_b4_plus8 alloc=[64, 40, 32, 8, 16, 8, 8, 8] bytes=184 recall=60.297500

SQ_GREEDY_EVAL tag=it15_b5_plus8 alloc=[64, 40, 32, 8, 8, 16, 8, 8] bytes=184 recall=60.217500

SQ_GREEDY_EVAL tag=it15_b6_plus8 alloc=[64, 40, 32, 8, 8, 8, 16, 8] bytes=184 recall=60.255000

SQ_GREEDY_EVAL tag=it15_b7_plus8 alloc=[64, 40, 32, 8, 8, 8, 8, 16] bytes=184 recall=60.325000

SQ_GREEDY_EVAL tag=it16_b0_plus8 alloc=[80, 40, 32, 8, 8, 8, 8, 8] bytes=192 recall=62.190000

SQ_GREEDY_EVAL tag=it16_b1_plus8 alloc=[72, 48, 32, 8, 8, 8, 8, 8] bytes=192 recall=61.852500

SQ_GREEDY_EVAL tag=it16_b2_plus8 alloc=[72, 40, 40, 8, 8, 8, 8, 8] bytes=192 recall=61.940000

SQ_GREEDY_EVAL tag=it16_b3_plus8 alloc=[72, 40, 32, 16, 8, 8, 8, 8] bytes=192 recall=61.675000

SQ_GREEDY_EVAL tag=it16_b4_plus8 alloc=[72, 40, 32, 8, 16, 8, 8, 8] bytes=192 recall=61.702500

SQ_GREEDY_EVAL tag=it16_b5_plus8 alloc=[72, 40, 32, 8, 8, 16, 8, 8] bytes=192 recall=61.510000

SQ_GREEDY_EVAL tag=it16_b6_plus8 alloc=[72, 40, 32, 8, 8, 8, 16, 8] bytes=192 recall=61.532500

SQ_GREEDY_EVAL tag=it16_b7_plus8 alloc=[72, 40, 32, 8, 8, 8, 8, 16] bytes=192 recall=61.650000

SQ_GREEDY_EVAL tag=it17_b0_plus8 alloc=[88, 40, 32, 8, 8, 8, 8, 8] bytes=200 recall=63.137500

SQ_GREEDY_EVAL tag=it17_b1_plus8 alloc=[80, 48, 32, 8, 8, 8, 8, 8] bytes=200 recall=62.982500

SQ_GREEDY_EVAL tag=it17_b2_plus8 alloc=[80, 40, 40, 8, 8, 8, 8, 8] bytes=200 recall=62.930000

SQ_GREEDY_EVAL tag=it17_b3_plus8 alloc=[80, 40, 32, 16, 8, 8, 8, 8] bytes=200 recall=62.885000

SQ_GREEDY_EVAL tag=it17_b4_plus8 alloc=[80, 40, 32, 8, 16, 8, 8, 8] bytes=200 recall=62.850000

SQ_GREEDY_EVAL tag=it17_b5_plus8 alloc=[80, 40, 32, 8, 8, 16, 8, 8] bytes=200 recall=62.782500

SQ_GREEDY_EVAL tag=it17_b6_plus8 alloc=[80, 40, 32, 8, 8, 8, 16, 8] bytes=200 recall=62.750000

SQ_GREEDY_EVAL tag=it17_b7_plus8 alloc=[80, 40, 32, 8, 8, 8, 8, 16] bytes=200 recall=62.732500

SQ_GREEDY_EVAL tag=it18_b0_plus8 alloc=[96, 40, 32, 8, 8, 8, 8, 8] bytes=208 recall=64.015000

SQ_GREEDY_EVAL tag=it18_b1_plus8 alloc=[88, 48, 32, 8, 8, 8, 8, 8] bytes=208 recall=63.902500

SQ_GREEDY_EVAL tag=it18_b2_plus8 alloc=[88, 40, 40, 8, 8, 8, 8, 8] bytes=208 recall=63.957500

SQ_GREEDY_EVAL tag=it18_b3_plus8 alloc=[88, 40, 32, 16, 8, 8, 8, 8] bytes=208 recall=63.872500

SQ_GREEDY_EVAL tag=it18_b4_plus8 alloc=[88, 40, 32, 8, 16, 8, 8, 8] bytes=208 recall=63.697500

SQ_GREEDY_EVAL tag=it18_b5_plus8 alloc=[88, 40, 32, 8, 8, 16, 8, 8] bytes=208 recall=63.697500

SQ_GREEDY_EVAL tag=it18_b6_plus8 alloc=[88, 40, 32, 8, 8, 8, 16, 8] bytes=208 recall=63.722500

SQ_GREEDY_EVAL tag=it18_b7_plus8 alloc=[88, 40, 32, 8, 8, 8, 8, 16] bytes=208 recall=63.765000

SQ_GREEDY_EVAL tag=it19_b0_plus8 alloc=[104, 40, 32, 8, 8, 8, 8, 8] bytes=216 recall=64.367500

SQ_GREEDY_EVAL tag=it19_b1_plus8 alloc=[96, 48, 32, 8, 8, 8, 8, 8] bytes=216 recall=64.810000

SQ_GREEDY_EVAL tag=it19_b2_plus8 alloc=[96, 40, 40, 8, 8, 8, 8, 8] bytes=216 recall=64.745000

SQ_GREEDY_EVAL tag=it19_b3_plus8 alloc=[96, 40, 32, 16, 8, 8, 8, 8] bytes=216 recall=64.615000

SQ_GREEDY_EVAL tag=it19_b4_plus8 alloc=[96, 40, 32, 8, 16, 8, 8, 8] bytes=216 recall=64.512500

SQ_GREEDY_EVAL tag=it19_b5_plus8 alloc=[96, 40, 32, 8, 8, 16, 8, 8] bytes=216 recall=64.510000

SQ_GREEDY_EVAL tag=it19_b6_plus8 alloc=[96, 40, 32, 8, 8, 8, 16, 8] bytes=216 recall=64.502500

SQ_GREEDY_EVAL tag=it19_b7_plus8 alloc=[96, 40, 32, 8, 8, 8, 8, 16] bytes=216 recall=64.487500

SQ_GREEDY_EVAL tag=it20_b0_plus8 alloc=[104, 48, 32, 8, 8, 8, 8, 8] bytes=224 recall=65.067500

SQ_GREEDY_EVAL tag=it20_b1_plus8 alloc=[96, 56, 32, 8, 8, 8, 8, 8] bytes=224 recall=65.535000

SQ_GREEDY_EVAL tag=it20_b2_plus8 alloc=[96, 48, 40, 8, 8, 8, 8, 8] bytes=224 recall=65.567500

SQ_GREEDY_EVAL tag=it20_b3_plus8 alloc=[96, 48, 32, 16, 8, 8, 8, 8] bytes=224 recall=65.387500

SQ_GREEDY_EVAL tag=it20_b4_plus8 alloc=[96, 48, 32, 8, 16, 8, 8, 8] bytes=224 recall=65.350000

SQ_GREEDY_EVAL tag=it20_b5_plus8 alloc=[96, 48, 32, 8, 8, 16, 8, 8] bytes=224 recall=65.265000

SQ_GREEDY_EVAL tag=it20_b6_plus8 alloc=[96, 48, 32, 8, 8, 8, 16, 8] bytes=224 recall=65.212500

SQ_GREEDY_EVAL tag=it20_b7_plus8 alloc=[96, 48, 32, 8, 8, 8, 8, 16] bytes=224 recall=65.377500

SQ_GREEDY_EVAL tag=it21_b0_plus8 alloc=[104, 48, 40, 8, 8, 8, 8, 8] bytes=232 recall=65.847500

SQ_GREEDY_EVAL tag=it21_b1_plus8 alloc=[96, 56, 40, 8, 8, 8, 8, 8] bytes=232 recall=66.350000

SQ_GREEDY_EVAL tag=it21_b2_plus8 alloc=[96, 48, 48, 8, 8, 8, 8, 8] bytes=232 recall=66.092500

SQ_GREEDY_EVAL tag=it21_b3_plus8 alloc=[96, 48, 40, 16, 8, 8, 8, 8] bytes=232 recall=66.157500

SQ_GREEDY_EVAL tag=it21_b4_plus8 alloc=[96, 48, 40, 8, 16, 8, 8, 8] bytes=232 recall=66.025000

SQ_GREEDY_EVAL tag=it21_b5_plus8 alloc=[96, 48, 40, 8, 8, 16, 8, 8] bytes=232 recall=65.960000

SQ_GREEDY_EVAL tag=it21_b6_plus8 alloc=[96, 48, 40, 8, 8, 8, 16, 8] bytes=232 recall=66.027500

SQ_GREEDY_EVAL tag=it21_b7_plus8 alloc=[96, 48, 40, 8, 8, 8, 8, 16] bytes=232 recall=66.080000

SQ_GREEDY_EVAL tag=it22_b0_plus8 alloc=[104, 56, 40, 8, 8, 8, 8, 8] bytes=240 recall=66.700000

SQ_GREEDY_EVAL tag=it22_b1_plus8 alloc=[96, 64, 40, 8, 8, 8, 8, 8] bytes=240 recall=66.950000

SQ_GREEDY_EVAL tag=it22_b2_plus8 alloc=[96, 56, 48, 8, 8, 8, 8, 8] bytes=240 recall=66.912500

SQ_GREEDY_EVAL tag=it22_b3_plus8 alloc=[96, 56, 40, 16, 8, 8, 8, 8] bytes=240 recall=66.902500

SQ_GREEDY_EVAL tag=it22_b4_plus8 alloc=[96, 56, 40, 8, 16, 8, 8, 8] bytes=240 recall=66.852500

SQ_GREEDY_EVAL tag=it22_b5_plus8 alloc=[96, 56, 40, 8, 8, 16, 8, 8] bytes=240 recall=66.780000

SQ_GREEDY_EVAL tag=it22_b6_plus8 alloc=[96, 56, 40, 8, 8, 8, 16, 8] bytes=240 recall=66.797500

SQ_GREEDY_EVAL tag=it22_b7_plus8 alloc=[96, 56, 40, 8, 8, 8, 8, 16] bytes=240 recall=66.830000

SQ_GREEDY_EVAL tag=it23_b0_plus8 alloc=[104, 64, 40, 8, 8, 8, 8, 8] bytes=248 recall=67.425000

SQ_GREEDY_EVAL tag=it23_b1_plus8 alloc=[96, 72, 40, 8, 8, 8, 8, 8] bytes=248 recall=67.502500

SQ_GREEDY_EVAL tag=it23_b2_plus8 alloc=[96, 64, 48, 8, 8, 8, 8, 8] bytes=248 recall=67.580000

SQ_GREEDY_EVAL tag=it23_b3_plus8 alloc=[96, 64, 40, 16, 8, 8, 8, 8] bytes=248 recall=67.590000

SQ_GREEDY_EVAL tag=it23_b4_plus8 alloc=[96, 64, 40, 8, 16, 8, 8, 8] bytes=248 recall=67.532500

SQ_GREEDY_EVAL tag=it23_b5_plus8 alloc=[96, 64, 40, 8, 8, 16, 8, 8] bytes=248 recall=67.355000

SQ_GREEDY_EVAL tag=it23_b6_plus8 alloc=[96, 64, 40, 8, 8, 8, 16, 8] bytes=248 recall=67.465000

SQ_GREEDY_EVAL tag=it23_b7_plus8 alloc=[96, 64, 40, 8, 8, 8, 8, 16] bytes=248 recall=67.470000

SQ_GREEDY_EVAL tag=it24_b0_plus8 alloc=[104, 64, 40, 16, 8, 8, 8, 8] bytes=256 recall=67.930000

SQ_GREEDY_EVAL tag=it24_b1_plus8 alloc=[96, 72, 40, 16, 8, 8, 8, 8] bytes=256 recall=68.032500

SQ_GREEDY_EVAL tag=it24_b2_plus8 alloc=[96, 64, 48, 16, 8, 8, 8, 8] bytes=256 recall=68.090000

SQ_GREEDY_EVAL tag=it24_b3_plus8 alloc=[96, 64, 40, 24, 8, 8, 8, 8] bytes=256 recall=68.142500

SQ_GREEDY_EVAL tag=it24_b4_plus8 alloc=[96, 64, 40, 16, 16, 8, 8, 8] bytes=256 recall=68.127500

SQ_GREEDY_EVAL tag=it24_b5_plus8 alloc=[96, 64, 40, 16, 8, 16, 8, 8] bytes=256 recall=67.980000

SQ_GREEDY_EVAL tag=it24_b6_plus8 alloc=[96, 64, 40, 16, 8, 8, 16, 8] bytes=256 recall=68.075000

SQ_GREEDY_EVAL tag=it24_b7_plus8 alloc=[96, 64, 40, 16, 8, 8, 8, 16] bytes=256 recall=68.015000

SQ_GREEDY_EVAL tag=it25_b0_plus8 alloc=[104, 64, 40, 24, 8, 8, 8, 8] bytes=264 recall=68.492500

SQ_GREEDY_EVAL tag=it25_b1_plus8 alloc=[96, 72, 40, 24, 8, 8, 8, 8] bytes=264 recall=68.632500

SQ_GREEDY_EVAL tag=it25_b2_plus8 alloc=[96, 64, 48, 24, 8, 8, 8, 8] bytes=264 recall=68.755000

SQ_GREEDY_EVAL tag=it25_b3_plus8 alloc=[96, 64, 40, 32, 8, 8, 8, 8] bytes=264 recall=68.590000

SQ_GREEDY_EVAL tag=it25_b4_plus8 alloc=[96, 64, 40, 24, 16, 8, 8, 8] bytes=264 recall=68.617500

SQ_GREEDY_EVAL tag=it25_b5_plus8 alloc=[96, 64, 40, 24, 8, 16, 8, 8] bytes=264 recall=68.485000

SQ_GREEDY_EVAL tag=it25_b6_plus8 alloc=[96, 64, 40, 24, 8, 8, 16, 8] bytes=264 recall=68.537500

SQ_GREEDY_EVAL tag=it25_b7_plus8 alloc=[96, 64, 40, 24, 8, 8, 8, 16] bytes=264 recall=68.580000

SQ_GREEDY_EVAL tag=it26_b0_plus8 alloc=[104, 64, 48, 24, 8, 8, 8, 8] bytes=272 recall=69.035000

SQ_GREEDY_EVAL tag=it26_b1_plus8 alloc=[96, 72, 48, 24, 8, 8, 8, 8] bytes=272 recall=69.132500

SQ_GREEDY_EVAL tag=it26_b2_plus8 alloc=[96, 64, 56, 24, 8, 8, 8, 8] bytes=272 recall=69.257500

SQ_GREEDY_EVAL tag=it26_b3_plus8 alloc=[96, 64, 48, 32, 8, 8, 8, 8] bytes=272 recall=69.197500

SQ_GREEDY_EVAL tag=it26_b4_plus8 alloc=[96, 64, 48, 24, 16, 8, 8, 8] bytes=272 recall=69.112500

SQ_GREEDY_EVAL tag=it26_b5_plus8 alloc=[96, 64, 48, 24, 8, 16, 8, 8] bytes=272 recall=69.085000

SQ_GREEDY_EVAL tag=it26_b6_plus8 alloc=[96, 64, 48, 24, 8, 8, 16, 8] bytes=272 recall=69.045000

SQ_GREEDY_EVAL tag=it26_b7_plus8 alloc=[96, 64, 48, 24, 8, 8, 8, 16] bytes=272 recall=69.120000

SQ_GREEDY_EVAL tag=it27_b0_plus8 alloc=[104, 64, 56, 24, 8, 8, 8, 8] bytes=280 recall=69.655000

SQ_GREEDY_EVAL tag=it27_b1_plus8 alloc=[96, 72, 56, 24, 8, 8, 8, 8] bytes=280 recall=69.715000

SQ_GREEDY_EVAL tag=it27_b2_plus8 alloc=[96, 64, 64, 24, 8, 8, 8, 8] bytes=280 recall=69.932500

SQ_GREEDY_EVAL tag=it27_b3_plus8 alloc=[96, 64, 56, 32, 8, 8, 8, 8] bytes=280 recall=69.757500

SQ_GREEDY_EVAL tag=it27_b4_plus8 alloc=[96, 64, 56, 24, 16, 8, 8, 8] bytes=280 recall=69.705000

SQ_GREEDY_EVAL tag=it27_b5_plus8 alloc=[96, 64, 56, 24, 8, 16, 8, 8] bytes=280 recall=69.670000

SQ_GREEDY_EVAL tag=it27_b6_plus8 alloc=[96, 64, 56, 24, 8, 8, 16, 8] bytes=280 recall=69.622500

SQ_GREEDY_EVAL tag=it27_b7_plus8 alloc=[96, 64, 56, 24, 8, 8, 8, 16] bytes=280 recall=69.632500

SQ_GREEDY_EVAL tag=it28_b0_plus8 alloc=[104, 64, 64, 24, 8, 8, 8, 8] bytes=288 recall=70.322500

SQ_GREEDY_EVAL tag=it28_b1_plus8 alloc=[96, 72, 64, 24, 8, 8, 8, 8] bytes=288 recall=70.370000

SQ_GREEDY_EVAL tag=it28_b2_plus8 alloc=[96, 64, 72, 24, 8, 8, 8, 8] bytes=288 recall=70.475000

SQ_GREEDY_EVAL tag=it28_b3_plus8 alloc=[96, 64, 64, 32, 8, 8, 8, 8] bytes=288 recall=70.390000

SQ_GREEDY_EVAL tag=it28_b4_plus8 alloc=[96, 64, 64, 24, 16, 8, 8, 8] bytes=288 recall=70.345000

SQ_GREEDY_EVAL tag=it28_b5_plus8 alloc=[96, 64, 64, 24, 8, 16, 8, 8] bytes=288 recall=70.295000

SQ_GREEDY_EVAL tag=it28_b6_plus8 alloc=[96, 64, 64, 24, 8, 8, 16, 8] bytes=288 recall=70.300000

SQ_GREEDY_EVAL tag=it28_b7_plus8 alloc=[96, 64, 64, 24, 8, 8, 8, 16] bytes=288 recall=70.240000

SQ_GREEDY_EVAL tag=it29_b0_plus8 alloc=[104, 64, 72, 24, 8, 8, 8, 8] bytes=296 recall=70.717500

SQ_GREEDY_EVAL tag=it29_b1_plus8 alloc=[96, 72, 72, 24, 8, 8, 8, 8] bytes=296 recall=70.907500

SQ_GREEDY_EVAL tag=it29_b2_plus8 alloc=[96, 64, 80, 24, 8, 8, 8, 8] bytes=296 recall=70.912500

SQ_GREEDY_EVAL tag=it29_b3_plus8 alloc=[96, 64, 72, 32, 8, 8, 8, 8] bytes=296 recall=70.902500

SQ_GREEDY_EVAL tag=it29_b4_plus8 alloc=[96, 64, 72, 24, 16, 8, 8, 8] bytes=296 recall=70.840000

SQ_GREEDY_EVAL tag=it29_b5_plus8 alloc=[96, 64, 72, 24, 8, 16, 8, 8] bytes=296 recall=70.822500

SQ_GREEDY_EVAL tag=it29_b6_plus8 alloc=[96, 64, 72, 24, 8, 8, 16, 8] bytes=296 recall=70.807500

SQ_GREEDY_EVAL tag=it29_b7_plus8 alloc=[96, 64, 72, 24, 8, 8, 8, 16] bytes=296 recall=70.772500

SQ_GREEDY_EVAL tag=it30_b0_plus8 alloc=[104, 64, 80, 24, 8, 8, 8, 8] bytes=304 recall=71.212500

SQ_GREEDY_EVAL tag=it30_b1_plus8 alloc=[96, 72, 80, 24, 8, 8, 8, 8] bytes=304 recall=71.325000

SQ_GREEDY_EVAL tag=it30_b2_plus8 alloc=[96, 64, 88, 24, 8, 8, 8, 8] bytes=304 recall=71.472500

SQ_GREEDY_EVAL tag=it30_b3_plus8 alloc=[96, 64, 80, 32, 8, 8, 8, 8] bytes=304 recall=71.352500

SQ_GREEDY_EVAL tag=it30_b4_plus8 alloc=[96, 64, 80, 24, 16, 8, 8, 8] bytes=304 recall=71.342500

SQ_GREEDY_EVAL tag=it30_b5_plus8 alloc=[96, 64, 80, 24, 8, 16, 8, 8] bytes=304 recall=71.277500

SQ_GREEDY_EVAL tag=it30_b6_plus8 alloc=[96, 64, 80, 24, 8, 8, 16, 8] bytes=304 recall=71.277500

SQ_GREEDY_EVAL tag=it30_b7_plus8 alloc=[96, 64, 80, 24, 8, 8, 8, 16] bytes=304 recall=71.157500

SQ_GREEDY_EVAL tag=it31_b0_plus8 alloc=[104, 64, 88, 24, 8, 8, 8, 8] bytes=312 recall=71.737500

SQ_GREEDY_EVAL tag=it31_b1_plus8 alloc=[96, 72, 88, 24, 8, 8, 8, 8] bytes=312 recall=71.827500

SQ_GREEDY_EVAL tag=it31_b2_plus8 alloc=[96, 64, 96, 24, 8, 8, 8, 8] bytes=312 recall=71.902500

SQ_GREEDY_EVAL tag=it31_b3_plus8 alloc=[96, 64, 88, 32, 8, 8, 8, 8] bytes=312 recall=71.887500

SQ_GREEDY_EVAL tag=it31_b4_plus8 alloc=[96, 64, 88, 24, 16, 8, 8, 8] bytes=312 recall=71.830000

SQ_GREEDY_EVAL tag=it31_b5_plus8 alloc=[96, 64, 88, 24, 8, 16, 8, 8] bytes=312 recall=71.750000

SQ_GREEDY_EVAL tag=it31_b6_plus8 alloc=[96, 64, 88, 24, 8, 8, 16, 8] bytes=312 recall=71.780000

SQ_GREEDY_EVAL tag=it31_b7_plus8 alloc=[96, 64, 88, 24, 8, 8, 8, 16] bytes=312 recall=71.717500

SQ_GREEDY_EVAL tag=it32_b0_plus8 alloc=[104, 64, 96, 24, 8, 8, 8, 8] bytes=320 recall=72.250000

SQ_GREEDY_EVAL tag=it32_b1_plus8 alloc=[96, 72, 96, 24, 8, 8, 8, 8] bytes=320 recall=72.295000

SQ_GREEDY_EVAL tag=it32_b2_plus8 alloc=[96, 64, 104, 24, 8, 8, 8, 8] bytes=320 recall=72.155000

SQ_GREEDY_EVAL tag=it32_b3_plus8 alloc=[96, 64, 96, 32, 8, 8, 8, 8] bytes=320 recall=72.320000

SQ_GREEDY_EVAL tag=it32_b4_plus8 alloc=[96, 64, 96, 24, 16, 8, 8, 8] bytes=320 recall=72.280000

SQ_GREEDY_EVAL tag=it32_b5_plus8 alloc=[96, 64, 96, 24, 8, 16, 8, 8] bytes=320 recall=72.177500

SQ_GREEDY_EVAL tag=it32_b6_plus8 alloc=[96, 64, 96, 24, 8, 8, 16, 8] bytes=320 recall=72.192500

SQ_GREEDY_EVAL tag=it32_b7_plus8 alloc=[96, 64, 96, 24, 8, 8, 8, 16] bytes=320 recall=72.165000

SQ_GREEDY_EVAL tag=it33_b0_plus8 alloc=[104, 64, 96, 32, 8, 8, 8, 8] bytes=328 recall=72.680000

SQ_GREEDY_EVAL tag=it33_b1_plus8 alloc=[96, 72, 96, 32, 8, 8, 8, 8] bytes=328 recall=72.775000

SQ_GREEDY_EVAL tag=it33_b2_plus8 alloc=[96, 64, 104, 32, 8, 8, 8, 8] bytes=328 recall=72.575000

SQ_GREEDY_EVAL tag=it33_b3_plus8 alloc=[96, 64, 96, 40, 8, 8, 8, 8] bytes=328 recall=72.750000

SQ_GREEDY_EVAL tag=it33_b4_plus8 alloc=[96, 64, 96, 32, 16, 8, 8, 8] bytes=328 recall=72.662500

SQ_GREEDY_EVAL tag=it33_b5_plus8 alloc=[96, 64, 96, 32, 8, 16, 8, 8] bytes=328 recall=72.587500

SQ_GREEDY_EVAL tag=it33_b6_plus8 alloc=[96, 64, 96, 32, 8, 8, 16, 8] bytes=328 recall=72.612500

SQ_GREEDY_EVAL tag=it33_b7_plus8 alloc=[96, 64, 96, 32, 8, 8, 8, 16] bytes=328 recall=72.647500

SQ_GREEDY_EVAL tag=it34_b0_plus8 alloc=[104, 72, 96, 32, 8, 8, 8, 8] bytes=336 recall=72.942500

SQ_GREEDY_EVAL tag=it34_b1_plus8 alloc=[96, 80, 96, 32, 8, 8, 8, 8] bytes=336 recall=73.345000

SQ_GREEDY_EVAL tag=it34_b2_plus8 alloc=[96, 72, 104, 32, 8, 8, 8, 8] bytes=336 recall=72.895000

SQ_GREEDY_EVAL tag=it34_b3_plus8 alloc=[96, 72, 96, 40, 8, 8, 8, 8] bytes=336 recall=73.097500

SQ_GREEDY_EVAL tag=it34_b4_plus8 alloc=[96, 72, 96, 32, 16, 8, 8, 8] bytes=336 recall=73.037500

SQ_GREEDY_EVAL tag=it34_b5_plus8 alloc=[96, 72, 96, 32, 8, 16, 8, 8] bytes=336 recall=73.025000

SQ_GREEDY_EVAL tag=it34_b6_plus8 alloc=[96, 72, 96, 32, 8, 8, 16, 8] bytes=336 recall=73.012500

SQ_GREEDY_EVAL tag=it34_b7_plus8 alloc=[96, 72, 96, 32, 8, 8, 8, 16] bytes=336 recall=72.985000

SQ_GREEDY_EVAL tag=it35_b0_plus8 alloc=[104, 80, 96, 32, 8, 8, 8, 8] bytes=344 recall=73.582500

SQ_GREEDY_EVAL tag=it35_b1_plus8 alloc=[96, 88, 96, 32, 8, 8, 8, 8] bytes=344 recall=73.695000

SQ_GREEDY_EVAL tag=it35_b2_plus8 alloc=[96, 80, 104, 32, 8, 8, 8, 8] bytes=344 recall=73.400000

SQ_GREEDY_EVAL tag=it35_b3_plus8 alloc=[96, 80, 96, 40, 8, 8, 8, 8] bytes=344 recall=73.740000

SQ_GREEDY_EVAL tag=it35_b4_plus8 alloc=[96, 80, 96, 32, 16, 8, 8, 8] bytes=344 recall=73.647500

SQ_GREEDY_EVAL tag=it35_b5_plus8 alloc=[96, 80, 96, 32, 8, 16, 8, 8] bytes=344 recall=73.572500

SQ_GREEDY_EVAL tag=it35_b6_plus8 alloc=[96, 80, 96, 32, 8, 8, 16, 8] bytes=344 recall=73.535000

SQ_GREEDY_EVAL tag=it35_b7_plus8 alloc=[96, 80, 96, 32, 8, 8, 8, 16] bytes=344 recall=73.597500

SQ_GREEDY_EVAL tag=it36_b0_plus8 alloc=[104, 80, 96, 40, 8, 8, 8, 8] bytes=352 recall=73.872500

SQ_GREEDY_EVAL tag=it36_b1_plus8 alloc=[96, 88, 96, 40, 8, 8, 8, 8] bytes=352 recall=74.037500

SQ_GREEDY_EVAL tag=it36_b2_plus8 alloc=[96, 80, 104, 40, 8, 8, 8, 8] bytes=352 recall=73.720000

SQ_GREEDY_EVAL tag=it36_b3_plus8 alloc=[96, 80, 96, 48, 8, 8, 8, 8] bytes=352 recall=73.992500

SQ_GREEDY_EVAL tag=it36_b4_plus8 alloc=[96, 80, 96, 40, 16, 8, 8, 8] bytes=352 recall=73.967500

SQ_GREEDY_EVAL tag=it36_b5_plus8 alloc=[96, 80, 96, 40, 8, 16, 8, 8] bytes=352 recall=73.960000

SQ_GREEDY_EVAL tag=it36_b6_plus8 alloc=[96, 80, 96, 40, 8, 8, 16, 8] bytes=352 recall=73.937500

SQ_GREEDY_EVAL tag=it36_b7_plus8 alloc=[96, 80, 96, 40, 8, 8, 8, 16] bytes=352 recall=73.907500

SQ_GREEDY_EVAL tag=it37_b0_plus8 alloc=[104, 88, 96, 40, 8, 8, 8, 8] bytes=360 recall=74.235000

SQ_GREEDY_EVAL tag=it37_b1_plus8 alloc=[96, 96, 96, 40, 8, 8, 8, 8] bytes=360 recall=74.630000

SQ_GREEDY_EVAL tag=it37_b2_plus8 alloc=[96, 88, 104, 40, 8, 8, 8, 8] bytes=360 recall=74.315000

SQ_GREEDY_EVAL tag=it37_b3_plus8 alloc=[96, 88, 96, 48, 8, 8, 8, 8] bytes=360 recall=74.480000

SQ_GREEDY_EVAL tag=it37_b4_plus8 alloc=[96, 88, 96, 40, 16, 8, 8, 8] bytes=360 recall=74.435000

SQ_GREEDY_EVAL tag=it37_b5_plus8 alloc=[96, 88, 96, 40, 8, 16, 8, 8] bytes=360 recall=74.347500

SQ_GREEDY_EVAL tag=it37_b6_plus8 alloc=[96, 88, 96, 40, 8, 8, 16, 8] bytes=360 recall=74.410000

SQ_GREEDY_EVAL tag=it37_b7_plus8 alloc=[96, 88, 96, 40, 8, 8, 8, 16] bytes=360 recall=74.320000

SQ_GREEDY_EVAL tag=it38_b0_plus8 alloc=[104, 96, 96, 40, 8, 8, 8, 8] bytes=368 recall=74.795000

SQ_GREEDY_EVAL tag=it38_b1_plus8 alloc=[96, 104, 96, 40, 8, 8, 8, 8] bytes=368 recall=74.890000

SQ_GREEDY_EVAL tag=it38_b2_plus8 alloc=[96, 96, 104, 40, 8, 8, 8, 8] bytes=368 recall=74.750000

SQ_GREEDY_EVAL tag=it38_b3_plus8 alloc=[96, 96, 96, 48, 8, 8, 8, 8] bytes=368 recall=74.882500

SQ_GREEDY_EVAL tag=it38_b4_plus8 alloc=[96, 96, 96, 40, 16, 8, 8, 8] bytes=368 recall=74.932500

SQ_GREEDY_EVAL tag=it38_b5_plus8 alloc=[96, 96, 96, 40, 8, 16, 8, 8] bytes=368 recall=74.832500

SQ_GREEDY_EVAL tag=it38_b6_plus8 alloc=[96, 96, 96, 40, 8, 8, 16, 8] bytes=368 recall=74.832500

SQ_GREEDY_EVAL tag=it38_b7_plus8 alloc=[96, 96, 96, 40, 8, 8, 8, 16] bytes=368 recall=74.825000

SQ_GREEDY_EVAL tag=it39_b0_plus8 alloc=[104, 96, 96, 40, 16, 8, 8, 8] bytes=376 recall=75.067500

SQ_GREEDY_EVAL tag=it39_b1_plus8 alloc=[96, 104, 96, 40, 16, 8, 8, 8] bytes=376 recall=75.210000

SQ_GREEDY_EVAL tag=it39_b2_plus8 alloc=[96, 96, 104, 40, 16, 8, 8, 8] bytes=376 recall=75.075000

SQ_GREEDY_EVAL tag=it39_b3_plus8 alloc=[96, 96, 96, 48, 16, 8, 8, 8] bytes=376 recall=75.172500

SQ_GREEDY_EVAL tag=it39_b4_plus8 alloc=[96, 96, 96, 40, 24, 8, 8, 8] bytes=376 recall=75.185000

SQ_GREEDY_EVAL tag=it39_b5_plus8 alloc=[96, 96, 96, 40, 16, 16, 8, 8] bytes=376 recall=75.145000

SQ_GREEDY_EVAL tag=it39_b6_plus8 alloc=[96, 96, 96, 40, 16, 8, 16, 8] bytes=376 recall=75.167500

SQ_GREEDY_EVAL tag=it39_b7_plus8 alloc=[96, 96, 96, 40, 16, 8, 8, 16] bytes=376 recall=75.192500

SQ_GREEDY_EVAL tag=it40_b0_plus8 alloc=[104, 104, 96, 40, 16, 8, 8, 8] bytes=384 recall=75.425000

SQ_GREEDY_EVAL tag=it40_b1_plus8 alloc=[96, 112, 96, 40, 16, 8, 8, 8] bytes=384 recall=75.477500

SQ_GREEDY_EVAL tag=it40_b2_plus8 alloc=[96, 104, 104, 40, 16, 8, 8, 8] bytes=384 recall=75.315000

SQ_GREEDY_EVAL tag=it40_b3_plus8 alloc=[96, 104, 96, 48, 16, 8, 8, 8] bytes=384 recall=75.517500

SQ_GREEDY_EVAL tag=it40_b4_plus8 alloc=[96, 104, 96, 40, 24, 8, 8, 8] bytes=384 recall=75.535000

SQ_GREEDY_EVAL tag=it40_b5_plus8 alloc=[96, 104, 96, 40, 16, 16, 8, 8] bytes=384 recall=75.382500

SQ_GREEDY_EVAL tag=it40_b6_plus8 alloc=[96, 104, 96, 40, 16, 8, 16, 8] bytes=384 recall=75.367500

SQ_GREEDY_EVAL tag=it40_b7_plus8 alloc=[96, 104, 96, 40, 16, 8, 8, 16] bytes=384 recall=75.462500

### DBpedia Cohere v4 stride
#### Uniform
SQ sweep completed!
Results directory: /tmp/sq_sweep_1779798527

Summary of SQ recall results:
Bytes,Recall
64,21.3725
96,32.0025
128,40.955
160,46.88
192,53.43
224,57.53
256,61.3725
288,64.805
320,67.9225
352,70.505
384,72.9875

#### Variable

```

SQ_GREEDY_EVAL tag=init alloc=[8, 8, 8, 8, 8, 8, 8, 8] bytes=64 recall=21.372500

SQ_GREEDY_EVAL tag=it1_b0_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 8] bytes=72 recall=25.502500

SQ_GREEDY_EVAL tag=it1_b1_plus8 alloc=[8, 16, 8, 8, 8, 8, 8, 8] bytes=72 recall=24.672500

SQ_GREEDY_EVAL tag=it1_b2_plus8 alloc=[8, 8, 16, 8, 8, 8, 8, 8] bytes=72 recall=24.725000

SQ_GREEDY_EVAL tag=it1_b3_plus8 alloc=[8, 8, 8, 16, 8, 8, 8, 8] bytes=72 recall=24.312500

SQ_GREEDY_EVAL tag=it1_b4_plus8 alloc=[8, 8, 8, 8, 16, 8, 8, 8] bytes=72 recall=24.892500

SQ_GREEDY_EVAL tag=it1_b5_plus8 alloc=[8, 8, 8, 8, 8, 16, 8, 8] bytes=72 recall=24.047500

SQ_GREEDY_EVAL tag=it1_b6_plus8 alloc=[8, 8, 8, 8, 8, 8, 16, 8] bytes=72 recall=24.280000

SQ_GREEDY_EVAL tag=it1_b7_plus8 alloc=[8, 8, 8, 8, 8, 8, 8, 16] bytes=72 recall=24.112500

SQ_GREEDY_EVAL tag=it2_b0_plus8 alloc=[24, 8, 8, 8, 8, 8, 8, 8] bytes=80 recall=28.295000

SQ_GREEDY_EVAL tag=it2_b1_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 8] bytes=80 recall=28.327500

SQ_GREEDY_EVAL tag=it2_b2_plus8 alloc=[16, 8, 16, 8, 8, 8, 8, 8] bytes=80 recall=28.495000

SQ_GREEDY_EVAL tag=it2_b3_plus8 alloc=[16, 8, 8, 16, 8, 8, 8, 8] bytes=80 recall=28.017500

SQ_GREEDY_EVAL tag=it2_b4_plus8 alloc=[16, 8, 8, 8, 16, 8, 8, 8] bytes=80 recall=28.502500

SQ_GREEDY_EVAL tag=it2_b5_plus8 alloc=[16, 8, 8, 8, 8, 16, 8, 8] bytes=80 recall=27.785000

SQ_GREEDY_EVAL tag=it2_b6_plus8 alloc=[16, 8, 8, 8, 8, 8, 16, 8] bytes=80 recall=27.897500

SQ_GREEDY_EVAL tag=it2_b7_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 16] bytes=80 recall=27.807500

SQ_GREEDY_EVAL tag=it3_b0_plus8 alloc=[24, 8, 8, 8, 16, 8, 8, 8] bytes=88 recall=31.417500

SQ_GREEDY_EVAL tag=it3_b1_plus8 alloc=[16, 16, 8, 8, 16, 8, 8, 8] bytes=88 recall=31.242500

SQ_GREEDY_EVAL tag=it3_b2_plus8 alloc=[16, 8, 16, 8, 16, 8, 8, 8] bytes=88 recall=31.312500

SQ_GREEDY_EVAL tag=it3_b3_plus8 alloc=[16, 8, 8, 16, 16, 8, 8, 8] bytes=88 recall=30.997500

SQ_GREEDY_EVAL tag=it3_b4_plus8 alloc=[16, 8, 8, 8, 24, 8, 8, 8] bytes=88 recall=30.717500

SQ_GREEDY_EVAL tag=it3_b5_plus8 alloc=[16, 8, 8, 8, 16, 16, 8, 8] bytes=88 recall=30.662500

SQ_GREEDY_EVAL tag=it3_b6_plus8 alloc=[16, 8, 8, 8, 16, 8, 16, 8] bytes=88 recall=30.740000

SQ_GREEDY_EVAL tag=it3_b7_plus8 alloc=[16, 8, 8, 8, 16, 8, 8, 16] bytes=88 recall=30.630000

SQ_GREEDY_EVAL tag=it4_b0_plus8 alloc=[32, 8, 8, 8, 16, 8, 8, 8] bytes=96 recall=34.690000

SQ_GREEDY_EVAL tag=it4_b1_plus8 alloc=[24, 16, 8, 8, 16, 8, 8, 8] bytes=96 recall=33.882500

SQ_GREEDY_EVAL tag=it4_b2_plus8 alloc=[24, 8, 16, 8, 16, 8, 8, 8] bytes=96 recall=33.887500

SQ_GREEDY_EVAL tag=it4_b3_plus8 alloc=[24, 8, 8, 16, 16, 8, 8, 8] bytes=96 recall=33.635000

SQ_GREEDY_EVAL tag=it4_b4_plus8 alloc=[24, 8, 8, 8, 24, 8, 8, 8] bytes=96 recall=33.320000

SQ_GREEDY_EVAL tag=it4_b5_plus8 alloc=[24, 8, 8, 8, 16, 16, 8, 8] bytes=96 recall=33.410000

SQ_GREEDY_EVAL tag=it4_b6_plus8 alloc=[24, 8, 8, 8, 16, 8, 16, 8] bytes=96 recall=33.515000

SQ_GREEDY_EVAL tag=it4_b7_plus8 alloc=[24, 8, 8, 8, 16, 8, 8, 16] bytes=96 recall=33.462500

SQ_GREEDY_EVAL tag=it5_b0_plus8 alloc=[40, 8, 8, 8, 16, 8, 8, 8] bytes=104 recall=37.557500

SQ_GREEDY_EVAL tag=it5_b1_plus8 alloc=[32, 16, 8, 8, 16, 8, 8, 8] bytes=104 recall=37.022500

SQ_GREEDY_EVAL tag=it5_b2_plus8 alloc=[32, 8, 16, 8, 16, 8, 8, 8] bytes=104 recall=36.897500

SQ_GREEDY_EVAL tag=it5_b3_plus8 alloc=[32, 8, 8, 16, 16, 8, 8, 8] bytes=104 recall=36.472500

SQ_GREEDY_EVAL tag=it5_b4_plus8 alloc=[32, 8, 8, 8, 24, 8, 8, 8] bytes=104 recall=36.735000

SQ_GREEDY_EVAL tag=it5_b5_plus8 alloc=[32, 8, 8, 8, 16, 16, 8, 8] bytes=104 recall=36.427500

SQ_GREEDY_EVAL tag=it5_b6_plus8 alloc=[32, 8, 8, 8, 16, 8, 16, 8] bytes=104 recall=36.540000

SQ_GREEDY_EVAL tag=it5_b7_plus8 alloc=[32, 8, 8, 8, 16, 8, 8, 16] bytes=104 recall=36.467500

SQ_GREEDY_EVAL tag=it6_b0_plus8 alloc=[48, 8, 8, 8, 16, 8, 8, 8] bytes=112 recall=39.872500

SQ_GREEDY_EVAL tag=it6_b1_plus8 alloc=[40, 16, 8, 8, 16, 8, 8, 8] bytes=112 recall=39.577500

SQ_GREEDY_EVAL tag=it6_b2_plus8 alloc=[40, 8, 16, 8, 16, 8, 8, 8] bytes=112 recall=39.582500

SQ_GREEDY_EVAL tag=it6_b3_plus8 alloc=[40, 8, 8, 16, 16, 8, 8, 8] bytes=112 recall=39.227500

SQ_GREEDY_EVAL tag=it6_b4_plus8 alloc=[40, 8, 8, 8, 24, 8, 8, 8] bytes=112 recall=39.347500

SQ_GREEDY_EVAL tag=it6_b5_plus8 alloc=[40, 8, 8, 8, 16, 16, 8, 8] bytes=112 recall=39.005000

SQ_GREEDY_EVAL tag=it6_b6_plus8 alloc=[40, 8, 8, 8, 16, 8, 16, 8] bytes=112 recall=39.127500

SQ_GREEDY_EVAL tag=it6_b7_plus8 alloc=[40, 8, 8, 8, 16, 8, 8, 16] bytes=112 recall=39.055000

SQ_GREEDY_EVAL tag=it7_b0_plus8 alloc=[56, 8, 8, 8, 16, 8, 8, 8] bytes=120 recall=40.940000

SQ_GREEDY_EVAL tag=it7_b1_plus8 alloc=[48, 16, 8, 8, 16, 8, 8, 8] bytes=120 recall=41.855000

SQ_GREEDY_EVAL tag=it7_b2_plus8 alloc=[48, 8, 16, 8, 16, 8, 8, 8] bytes=120 recall=41.980000

SQ_GREEDY_EVAL tag=it7_b3_plus8 alloc=[48, 8, 8, 16, 16, 8, 8, 8] bytes=120 recall=41.697500

SQ_GREEDY_EVAL tag=it7_b4_plus8 alloc=[48, 8, 8, 8, 24, 8, 8, 8] bytes=120 recall=41.797500

SQ_GREEDY_EVAL tag=it7_b5_plus8 alloc=[48, 8, 8, 8, 16, 16, 8, 8] bytes=120 recall=41.292500

SQ_GREEDY_EVAL tag=it7_b6_plus8 alloc=[48, 8, 8, 8, 16, 8, 16, 8] bytes=120 recall=41.427500

SQ_GREEDY_EVAL tag=it7_b7_plus8 alloc=[48, 8, 8, 8, 16, 8, 8, 16] bytes=120 recall=41.577500

SQ_GREEDY_EVAL tag=it8_b0_plus8 alloc=[56, 8, 16, 8, 16, 8, 8, 8] bytes=128 recall=43.107500

SQ_GREEDY_EVAL tag=it8_b1_plus8 alloc=[48, 16, 16, 8, 16, 8, 8, 8] bytes=128 recall=43.935000

SQ_GREEDY_EVAL tag=it8_b2_plus8 alloc=[48, 8, 24, 8, 16, 8, 8, 8] bytes=128 recall=43.767500

SQ_GREEDY_EVAL tag=it8_b3_plus8 alloc=[48, 8, 16, 16, 16, 8, 8, 8] bytes=128 recall=43.617500

SQ_GREEDY_EVAL tag=it8_b4_plus8 alloc=[48, 8, 16, 8, 24, 8, 8, 8] bytes=128 recall=43.747500

SQ_GREEDY_EVAL tag=it8_b5_plus8 alloc=[48, 8, 16, 8, 16, 16, 8, 8] bytes=128 recall=43.307500

SQ_GREEDY_EVAL tag=it8_b6_plus8 alloc=[48, 8, 16, 8, 16, 8, 16, 8] bytes=128 recall=43.427500

SQ_GREEDY_EVAL tag=it8_b7_plus8 alloc=[48, 8, 16, 8, 16, 8, 8, 16] bytes=128 recall=43.435000

SQ_GREEDY_EVAL tag=it9_b0_plus8 alloc=[56, 16, 16, 8, 16, 8, 8, 8] bytes=136 recall=44.862500

SQ_GREEDY_EVAL tag=it9_b1_plus8 alloc=[48, 24, 16, 8, 16, 8, 8, 8] bytes=136 recall=46.045000

SQ_GREEDY_EVAL tag=it9_b2_plus8 alloc=[48, 16, 24, 8, 16, 8, 8, 8] bytes=136 recall=45.595000

SQ_GREEDY_EVAL tag=it9_b3_plus8 alloc=[48, 16, 16, 16, 16, 8, 8, 8] bytes=136 recall=45.317500

SQ_GREEDY_EVAL tag=it9_b4_plus8 alloc=[48, 16, 16, 8, 24, 8, 8, 8] bytes=136 recall=45.250000

SQ_GREEDY_EVAL tag=it9_b5_plus8 alloc=[48, 16, 16, 8, 16, 16, 8, 8] bytes=136 recall=45.110000

SQ_GREEDY_EVAL tag=it9_b6_plus8 alloc=[48, 16, 16, 8, 16, 8, 16, 8] bytes=136 recall=45.160000

SQ_GREEDY_EVAL tag=it9_b7_plus8 alloc=[48, 16, 16, 8, 16, 8, 8, 16] bytes=136 recall=45.132500

SQ_GREEDY_EVAL tag=it10_b0_plus8 alloc=[56, 24, 16, 8, 16, 8, 8, 8] bytes=144 recall=46.955000

SQ_GREEDY_EVAL tag=it10_b1_plus8 alloc=[48, 32, 16, 8, 16, 8, 8, 8] bytes=144 recall=47.615000

SQ_GREEDY_EVAL tag=it10_b2_plus8 alloc=[48, 24, 24, 8, 16, 8, 8, 8] bytes=144 recall=47.452500

SQ_GREEDY_EVAL tag=it10_b3_plus8 alloc=[48, 24, 16, 16, 16, 8, 8, 8] bytes=144 recall=47.195000

SQ_GREEDY_EVAL tag=it10_b4_plus8 alloc=[48, 24, 16, 8, 24, 8, 8, 8] bytes=144 recall=47.425000

SQ_GREEDY_EVAL tag=it10_b5_plus8 alloc=[48, 24, 16, 8, 16, 16, 8, 8] bytes=144 recall=47.087500

SQ_GREEDY_EVAL tag=it10_b6_plus8 alloc=[48, 24, 16, 8, 16, 8, 16, 8] bytes=144 recall=47.125000

SQ_GREEDY_EVAL tag=it10_b7_plus8 alloc=[48, 24, 16, 8, 16, 8, 8, 16] bytes=144 recall=47.155000

SQ_GREEDY_EVAL tag=it11_b0_plus8 alloc=[56, 32, 16, 8, 16, 8, 8, 8] bytes=152 recall=48.390000

SQ_GREEDY_EVAL tag=it11_b1_plus8 alloc=[48, 40, 16, 8, 16, 8, 8, 8] bytes=152 recall=49.240000

SQ_GREEDY_EVAL tag=it11_b2_plus8 alloc=[48, 32, 24, 8, 16, 8, 8, 8] bytes=152 recall=49.127500

SQ_GREEDY_EVAL tag=it11_b3_plus8 alloc=[48, 32, 16, 16, 16, 8, 8, 8] bytes=152 recall=48.937500

SQ_GREEDY_EVAL tag=it11_b4_plus8 alloc=[48, 32, 16, 8, 24, 8, 8, 8] bytes=152 recall=48.900000

SQ_GREEDY_EVAL tag=it11_b5_plus8 alloc=[48, 32, 16, 8, 16, 16, 8, 8] bytes=152 recall=48.720000

SQ_GREEDY_EVAL tag=it11_b6_plus8 alloc=[48, 32, 16, 8, 16, 8, 16, 8] bytes=152 recall=48.762500

SQ_GREEDY_EVAL tag=it11_b7_plus8 alloc=[48, 32, 16, 8, 16, 8, 8, 16] bytes=152 recall=48.705000

SQ_GREEDY_EVAL tag=it12_b0_plus8 alloc=[56, 40, 16, 8, 16, 8, 8, 8] bytes=160 recall=50.160000

SQ_GREEDY_EVAL tag=it12_b1_plus8 alloc=[48, 48, 16, 8, 16, 8, 8, 8] bytes=160 recall=51.255000

SQ_GREEDY_EVAL tag=it12_b2_plus8 alloc=[48, 40, 24, 8, 16, 8, 8, 8] bytes=160 recall=50.867500

SQ_GREEDY_EVAL tag=it12_b3_plus8 alloc=[48, 40, 16, 16, 16, 8, 8, 8] bytes=160 recall=50.507500

SQ_GREEDY_EVAL tag=it12_b4_plus8 alloc=[48, 40, 16, 8, 24, 8, 8, 8] bytes=160 recall=50.625000

SQ_GREEDY_EVAL tag=it12_b5_plus8 alloc=[48, 40, 16, 8, 16, 16, 8, 8] bytes=160 recall=50.525000

SQ_GREEDY_EVAL tag=it12_b6_plus8 alloc=[48, 40, 16, 8, 16, 8, 16, 8] bytes=160 recall=50.355000

SQ_GREEDY_EVAL tag=it12_b7_plus8 alloc=[48, 40, 16, 8, 16, 8, 8, 16] bytes=160 recall=50.317500

SQ_GREEDY_EVAL tag=it13_b0_plus8 alloc=[56, 48, 16, 8, 16, 8, 8, 8] bytes=168 recall=52.105000

SQ_GREEDY_EVAL tag=it13_b1_plus8 alloc=[48, 56, 16, 8, 16, 8, 8, 8] bytes=168 recall=52.055000

SQ_GREEDY_EVAL tag=it13_b2_plus8 alloc=[48, 48, 24, 8, 16, 8, 8, 8] bytes=168 recall=52.670000

SQ_GREEDY_EVAL tag=it13_b3_plus8 alloc=[48, 48, 16, 16, 16, 8, 8, 8] bytes=168 recall=52.430000

SQ_GREEDY_EVAL tag=it13_b4_plus8 alloc=[48, 48, 16, 8, 24, 8, 8, 8] bytes=168 recall=52.247500

SQ_GREEDY_EVAL tag=it13_b5_plus8 alloc=[48, 48, 16, 8, 16, 16, 8, 8] bytes=168 recall=52.117500

SQ_GREEDY_EVAL tag=it13_b6_plus8 alloc=[48, 48, 16, 8, 16, 8, 16, 8] bytes=168 recall=52.255000

SQ_GREEDY_EVAL tag=it13_b7_plus8 alloc=[48, 48, 16, 8, 16, 8, 8, 16] bytes=168 recall=52.325000

SQ_GREEDY_EVAL tag=it14_b0_plus8 alloc=[56, 48, 24, 8, 16, 8, 8, 8] bytes=176 recall=53.520000

SQ_GREEDY_EVAL tag=it14_b1_plus8 alloc=[48, 56, 24, 8, 16, 8, 8, 8] bytes=176 recall=53.355000

SQ_GREEDY_EVAL tag=it14_b2_plus8 alloc=[48, 48, 32, 8, 16, 8, 8, 8] bytes=176 recall=53.945000

SQ_GREEDY_EVAL tag=it14_b3_plus8 alloc=[48, 48, 24, 16, 16, 8, 8, 8] bytes=176 recall=53.680000

SQ_GREEDY_EVAL tag=it14_b4_plus8 alloc=[48, 48, 24, 8, 24, 8, 8, 8] bytes=176 recall=53.710000

SQ_GREEDY_EVAL tag=it14_b5_plus8 alloc=[48, 48, 24, 8, 16, 16, 8, 8] bytes=176 recall=53.695000

SQ_GREEDY_EVAL tag=it14_b6_plus8 alloc=[48, 48, 24, 8, 16, 8, 16, 8] bytes=176 recall=53.605000

SQ_GREEDY_EVAL tag=it14_b7_plus8 alloc=[48, 48, 24, 8, 16, 8, 8, 16] bytes=176 recall=53.480000

SQ_GREEDY_EVAL tag=it15_b0_plus8 alloc=[56, 48, 32, 8, 16, 8, 8, 8] bytes=184 recall=54.782500

SQ_GREEDY_EVAL tag=it15_b1_plus8 alloc=[48, 56, 32, 8, 16, 8, 8, 8] bytes=184 recall=54.595000

SQ_GREEDY_EVAL tag=it15_b2_plus8 alloc=[48, 48, 40, 8, 16, 8, 8, 8] bytes=184 recall=55.205000

SQ_GREEDY_EVAL tag=it15_b3_plus8 alloc=[48, 48, 32, 16, 16, 8, 8, 8] bytes=184 recall=54.915000

SQ_GREEDY_EVAL tag=it15_b4_plus8 alloc=[48, 48, 32, 8, 24, 8, 8, 8] bytes=184 recall=55.037500

SQ_GREEDY_EVAL tag=it15_b5_plus8 alloc=[48, 48, 32, 8, 16, 16, 8, 8] bytes=184 recall=54.967500

SQ_GREEDY_EVAL tag=it15_b6_plus8 alloc=[48, 48, 32, 8, 16, 8, 16, 8] bytes=184 recall=54.897500

SQ_GREEDY_EVAL tag=it15_b7_plus8 alloc=[48, 48, 32, 8, 16, 8, 8, 16] bytes=184 recall=54.787500

SQ_GREEDY_EVAL tag=it16_b0_plus8 alloc=[56, 48, 40, 8, 16, 8, 8, 8] bytes=192 recall=55.940000

SQ_GREEDY_EVAL tag=it16_b1_plus8 alloc=[48, 56, 40, 8, 16, 8, 8, 8] bytes=192 recall=55.820000

SQ_GREEDY_EVAL tag=it16_b2_plus8 alloc=[48, 48, 48, 8, 16, 8, 8, 8] bytes=192 recall=56.287500

SQ_GREEDY_EVAL tag=it16_b3_plus8 alloc=[48, 48, 40, 16, 16, 8, 8, 8] bytes=192 recall=56.062500

SQ_GREEDY_EVAL tag=it16_b4_plus8 alloc=[48, 48, 40, 8, 24, 8, 8, 8] bytes=192 recall=56.285000

SQ_GREEDY_EVAL tag=it16_b5_plus8 alloc=[48, 48, 40, 8, 16, 16, 8, 8] bytes=192 recall=56.240000

SQ_GREEDY_EVAL tag=it16_b6_plus8 alloc=[48, 48, 40, 8, 16, 8, 16, 8] bytes=192 recall=56.137500

SQ_GREEDY_EVAL tag=it16_b7_plus8 alloc=[48, 48, 40, 8, 16, 8, 8, 16] bytes=192 recall=56.010000

SQ_GREEDY_EVAL tag=it17_b0_plus8 alloc=[56, 48, 48, 8, 16, 8, 8, 8] bytes=200 recall=56.995000

SQ_GREEDY_EVAL tag=it17_b1_plus8 alloc=[48, 56, 48, 8, 16, 8, 8, 8] bytes=200 recall=56.975000

SQ_GREEDY_EVAL tag=it17_b2_plus8 alloc=[48, 48, 56, 8, 16, 8, 8, 8] bytes=200 recall=56.735000

SQ_GREEDY_EVAL tag=it17_b3_plus8 alloc=[48, 48, 48, 16, 16, 8, 8, 8] bytes=200 recall=57.105000

SQ_GREEDY_EVAL tag=it17_b4_plus8 alloc=[48, 48, 48, 8, 24, 8, 8, 8] bytes=200 recall=57.015000

SQ_GREEDY_EVAL tag=it17_b5_plus8 alloc=[48, 48, 48, 8, 16, 16, 8, 8] bytes=200 recall=57.197500

SQ_GREEDY_EVAL tag=it17_b6_plus8 alloc=[48, 48, 48, 8, 16, 8, 16, 8] bytes=200 recall=57.060000

SQ_GREEDY_EVAL tag=it17_b7_plus8 alloc=[48, 48, 48, 8, 16, 8, 8, 16] bytes=200 recall=57.055000

SQ_GREEDY_EVAL tag=it18_b0_plus8 alloc=[56, 48, 48, 8, 16, 16, 8, 8] bytes=208 recall=57.897500

SQ_GREEDY_EVAL tag=it18_b1_plus8 alloc=[48, 56, 48, 8, 16, 16, 8, 8] bytes=208 recall=57.815000

SQ_GREEDY_EVAL tag=it18_b2_plus8 alloc=[48, 48, 56, 8, 16, 16, 8, 8] bytes=208 recall=57.820000

SQ_GREEDY_EVAL tag=it18_b3_plus8 alloc=[48, 48, 48, 16, 16, 16, 8, 8] bytes=208 recall=57.985000

SQ_GREEDY_EVAL tag=it18_b4_plus8 alloc=[48, 48, 48, 8, 24, 16, 8, 8] bytes=208 recall=57.830000

SQ_GREEDY_EVAL tag=it18_b5_plus8 alloc=[48, 48, 48, 8, 16, 24, 8, 8] bytes=208 recall=58.180000

SQ_GREEDY_EVAL tag=it18_b6_plus8 alloc=[48, 48, 48, 8, 16, 16, 16, 8] bytes=208 recall=58.000000

SQ_GREEDY_EVAL tag=it18_b7_plus8 alloc=[48, 48, 48, 8, 16, 16, 8, 16] bytes=208 recall=57.912500

SQ_GREEDY_EVAL tag=it19_b0_plus8 alloc=[56, 48, 48, 8, 16, 24, 8, 8] bytes=216 recall=58.912500

SQ_GREEDY_EVAL tag=it19_b1_plus8 alloc=[48, 56, 48, 8, 16, 24, 8, 8] bytes=216 recall=58.805000

SQ_GREEDY_EVAL tag=it19_b2_plus8 alloc=[48, 48, 56, 8, 16, 24, 8, 8] bytes=216 recall=58.662500

SQ_GREEDY_EVAL tag=it19_b3_plus8 alloc=[48, 48, 48, 16, 16, 24, 8, 8] bytes=216 recall=59.062500

SQ_GREEDY_EVAL tag=it19_b4_plus8 alloc=[48, 48, 48, 8, 24, 24, 8, 8] bytes=216 recall=58.975000

SQ_GREEDY_EVAL tag=it19_b5_plus8 alloc=[48, 48, 48, 8, 16, 32, 8, 8] bytes=216 recall=59.070000

SQ_GREEDY_EVAL tag=it19_b6_plus8 alloc=[48, 48, 48, 8, 16, 24, 16, 8] bytes=216 recall=59.000000

SQ_GREEDY_EVAL tag=it19_b7_plus8 alloc=[48, 48, 48, 8, 16, 24, 8, 16] bytes=216 recall=58.910000

SQ_GREEDY_EVAL tag=it20_b0_plus8 alloc=[56, 48, 48, 8, 16, 32, 8, 8] bytes=224 recall=59.550000

SQ_GREEDY_EVAL tag=it20_b1_plus8 alloc=[48, 56, 48, 8, 16, 32, 8, 8] bytes=224 recall=59.545000

SQ_GREEDY_EVAL tag=it20_b2_plus8 alloc=[48, 48, 56, 8, 16, 32, 8, 8] bytes=224 recall=59.415000

SQ_GREEDY_EVAL tag=it20_b3_plus8 alloc=[48, 48, 48, 16, 16, 32, 8, 8] bytes=224 recall=59.740000

SQ_GREEDY_EVAL tag=it20_b4_plus8 alloc=[48, 48, 48, 8, 24, 32, 8, 8] bytes=224 recall=59.755000

SQ_GREEDY_EVAL tag=it20_b5_plus8 alloc=[48, 48, 48, 8, 16, 40, 8, 8] bytes=224 recall=59.835000

SQ_GREEDY_EVAL tag=it20_b6_plus8 alloc=[48, 48, 48, 8, 16, 32, 16, 8] bytes=224 recall=59.747500

SQ_GREEDY_EVAL tag=it20_b7_plus8 alloc=[48, 48, 48, 8, 16, 32, 8, 16] bytes=224 recall=59.762500

SQ_GREEDY_EVAL tag=it21_b0_plus8 alloc=[56, 48, 48, 8, 16, 40, 8, 8] bytes=232 recall=60.355000

SQ_GREEDY_EVAL tag=it21_b1_plus8 alloc=[48, 56, 48, 8, 16, 40, 8, 8] bytes=232 recall=60.265000

SQ_GREEDY_EVAL tag=it21_b2_plus8 alloc=[48, 48, 56, 8, 16, 40, 8, 8] bytes=232 recall=60.285000

SQ_GREEDY_EVAL tag=it21_b3_plus8 alloc=[48, 48, 48, 16, 16, 40, 8, 8] bytes=232 recall=60.665000

SQ_GREEDY_EVAL tag=it21_b4_plus8 alloc=[48, 48, 48, 8, 24, 40, 8, 8] bytes=232 recall=60.720000

SQ_GREEDY_EVAL tag=it21_b5_plus8 alloc=[48, 48, 48, 8, 16, 48, 8, 8] bytes=232 recall=60.690000

SQ_GREEDY_EVAL tag=it21_b6_plus8 alloc=[48, 48, 48, 8, 16, 40, 16, 8] bytes=232 recall=60.522500

SQ_GREEDY_EVAL tag=it21_b7_plus8 alloc=[48, 48, 48, 8, 16, 40, 8, 16] bytes=232 recall=60.502500

SQ_GREEDY_EVAL tag=it22_b0_plus8 alloc=[56, 48, 48, 8, 24, 40, 8, 8] bytes=240 recall=61.150000

SQ_GREEDY_EVAL tag=it22_b1_plus8 alloc=[48, 56, 48, 8, 24, 40, 8, 8] bytes=240 recall=61.070000

SQ_GREEDY_EVAL tag=it22_b2_plus8 alloc=[48, 48, 56, 8, 24, 40, 8, 8] bytes=240 recall=61.040000

SQ_GREEDY_EVAL tag=it22_b3_plus8 alloc=[48, 48, 48, 16, 24, 40, 8, 8] bytes=240 recall=61.372500

SQ_GREEDY_EVAL tag=it22_b4_plus8 alloc=[48, 48, 48, 8, 32, 40, 8, 8] bytes=240 recall=61.497500

SQ_GREEDY_EVAL tag=it22_b5_plus8 alloc=[48, 48, 48, 8, 24, 48, 8, 8] bytes=240 recall=61.480000

SQ_GREEDY_EVAL tag=it22_b6_plus8 alloc=[48, 48, 48, 8, 24, 40, 16, 8] bytes=240 recall=61.310000

SQ_GREEDY_EVAL tag=it22_b7_plus8 alloc=[48, 48, 48, 8, 24, 40, 8, 16] bytes=240 recall=61.260000

SQ_GREEDY_EVAL tag=it23_b0_plus8 alloc=[56, 48, 48, 8, 32, 40, 8, 8] bytes=248 recall=62.252500

SQ_GREEDY_EVAL tag=it23_b1_plus8 alloc=[48, 56, 48, 8, 32, 40, 8, 8] bytes=248 recall=61.977500

SQ_GREEDY_EVAL tag=it23_b2_plus8 alloc=[48, 48, 56, 8, 32, 40, 8, 8] bytes=248 recall=61.950000

SQ_GREEDY_EVAL tag=it23_b3_plus8 alloc=[48, 48, 48, 16, 32, 40, 8, 8] bytes=248 recall=62.477500

SQ_GREEDY_EVAL tag=it23_b4_plus8 alloc=[48, 48, 48, 8, 40, 40, 8, 8] bytes=248 recall=62.302500

SQ_GREEDY_EVAL tag=it23_b5_plus8 alloc=[48, 48, 48, 8, 32, 48, 8, 8] bytes=248 recall=62.425000

SQ_GREEDY_EVAL tag=it23_b6_plus8 alloc=[48, 48, 48, 8, 32, 40, 16, 8] bytes=248 recall=62.115000

SQ_GREEDY_EVAL tag=it23_b7_plus8 alloc=[48, 48, 48, 8, 32, 40, 8, 16] bytes=248 recall=62.230000

SQ_GREEDY_EVAL tag=it24_b0_plus8 alloc=[56, 48, 48, 16, 32, 40, 8, 8] bytes=256 recall=63.057500

SQ_GREEDY_EVAL tag=it24_b1_plus8 alloc=[48, 56, 48, 16, 32, 40, 8, 8] bytes=256 recall=62.815000

SQ_GREEDY_EVAL tag=it24_b2_plus8 alloc=[48, 48, 56, 16, 32, 40, 8, 8] bytes=256 recall=62.822500

SQ_GREEDY_EVAL tag=it24_b3_plus8 alloc=[48, 48, 48, 24, 32, 40, 8, 8] bytes=256 recall=63.577500

SQ_GREEDY_EVAL tag=it24_b4_plus8 alloc=[48, 48, 48, 16, 40, 40, 8, 8] bytes=256 recall=63.187500

SQ_GREEDY_EVAL tag=it24_b5_plus8 alloc=[48, 48, 48, 16, 32, 48, 8, 8] bytes=256 recall=63.255000

SQ_GREEDY_EVAL tag=it24_b6_plus8 alloc=[48, 48, 48, 16, 32, 40, 16, 8] bytes=256 recall=63.007500

SQ_GREEDY_EVAL tag=it24_b7_plus8 alloc=[48, 48, 48, 16, 32, 40, 8, 16] bytes=256 recall=63.122500

SQ_GREEDY_EVAL tag=it25_b0_plus8 alloc=[56, 48, 48, 24, 32, 40, 8, 8] bytes=264 recall=64.120000

SQ_GREEDY_EVAL tag=it25_b1_plus8 alloc=[48, 56, 48, 24, 32, 40, 8, 8] bytes=264 recall=63.985000

SQ_GREEDY_EVAL tag=it25_b2_plus8 alloc=[48, 48, 56, 24, 32, 40, 8, 8] bytes=264 recall=63.882500

SQ_GREEDY_EVAL tag=it25_b3_plus8 alloc=[48, 48, 48, 32, 32, 40, 8, 8] bytes=264 recall=64.095000

SQ_GREEDY_EVAL tag=it25_b4_plus8 alloc=[48, 48, 48, 24, 40, 40, 8, 8] bytes=264 recall=64.287500

SQ_GREEDY_EVAL tag=it25_b5_plus8 alloc=[48, 48, 48, 24, 32, 48, 8, 8] bytes=264 recall=64.402500

SQ_GREEDY_EVAL tag=it25_b6_plus8 alloc=[48, 48, 48, 24, 32, 40, 16, 8] bytes=264 recall=64.060000

SQ_GREEDY_EVAL tag=it25_b7_plus8 alloc=[48, 48, 48, 24, 32, 40, 8, 16] bytes=264 recall=64.195000

SQ_GREEDY_EVAL tag=it26_b0_plus8 alloc=[56, 48, 48, 24, 32, 48, 8, 8] bytes=272 recall=64.837500

SQ_GREEDY_EVAL tag=it26_b1_plus8 alloc=[48, 56, 48, 24, 32, 48, 8, 8] bytes=272 recall=64.700000

SQ_GREEDY_EVAL tag=it26_b2_plus8 alloc=[48, 48, 56, 24, 32, 48, 8, 8] bytes=272 recall=64.545000

SQ_GREEDY_EVAL tag=it26_b3_plus8 alloc=[48, 48, 48, 32, 32, 48, 8, 8] bytes=272 recall=64.682500

SQ_GREEDY_EVAL tag=it26_b4_plus8 alloc=[48, 48, 48, 24, 40, 48, 8, 8] bytes=272 recall=65.175000

SQ_GREEDY_EVAL tag=it26_b5_plus8 alloc=[48, 48, 48, 24, 32, 56, 8, 8] bytes=272 recall=64.547500

SQ_GREEDY_EVAL tag=it26_b6_plus8 alloc=[48, 48, 48, 24, 32, 48, 16, 8] bytes=272 recall=64.852500

SQ_GREEDY_EVAL tag=it26_b7_plus8 alloc=[48, 48, 48, 24, 32, 48, 8, 16] bytes=272 recall=65.060000

SQ_GREEDY_EVAL tag=it27_b0_plus8 alloc=[56, 48, 48, 24, 40, 48, 8, 8] bytes=280 recall=65.535000

SQ_GREEDY_EVAL tag=it27_b1_plus8 alloc=[48, 56, 48, 24, 40, 48, 8, 8] bytes=280 recall=65.602500

SQ_GREEDY_EVAL tag=it27_b2_plus8 alloc=[48, 48, 56, 24, 40, 48, 8, 8] bytes=280 recall=65.522500

SQ_GREEDY_EVAL tag=it27_b3_plus8 alloc=[48, 48, 48, 32, 40, 48, 8, 8] bytes=280 recall=65.485000

SQ_GREEDY_EVAL tag=it27_b4_plus8 alloc=[48, 48, 48, 24, 48, 48, 8, 8] bytes=280 recall=65.670000

SQ_GREEDY_EVAL tag=it27_b5_plus8 alloc=[48, 48, 48, 24, 40, 56, 8, 8] bytes=280 recall=65.342500

SQ_GREEDY_EVAL tag=it27_b6_plus8 alloc=[48, 48, 48, 24, 40, 48, 16, 8] bytes=280 recall=65.642500

SQ_GREEDY_EVAL tag=it27_b7_plus8 alloc=[48, 48, 48, 24, 40, 48, 8, 16] bytes=280 recall=65.857500

SQ_GREEDY_EVAL tag=it28_b0_plus8 alloc=[56, 48, 48, 24, 40, 48, 8, 16] bytes=288 recall=66.227500

SQ_GREEDY_EVAL tag=it28_b1_plus8 alloc=[48, 56, 48, 24, 40, 48, 8, 16] bytes=288 recall=66.255000

SQ_GREEDY_EVAL tag=it28_b2_plus8 alloc=[48, 48, 56, 24, 40, 48, 8, 16] bytes=288 recall=66.130000

SQ_GREEDY_EVAL tag=it28_b3_plus8 alloc=[48, 48, 48, 32, 40, 48, 8, 16] bytes=288 recall=66.017500

SQ_GREEDY_EVAL tag=it28_b4_plus8 alloc=[48, 48, 48, 24, 48, 48, 8, 16] bytes=288 recall=66.392500

SQ_GREEDY_EVAL tag=it28_b5_plus8 alloc=[48, 48, 48, 24, 40, 56, 8, 16] bytes=288 recall=66.020000

SQ_GREEDY_EVAL tag=it28_b6_plus8 alloc=[48, 48, 48, 24, 40, 48, 16, 16] bytes=288 recall=66.317500

SQ_GREEDY_EVAL tag=it28_b7_plus8 alloc=[48, 48, 48, 24, 40, 48, 8, 24] bytes=288 recall=66.272500

SQ_GREEDY_EVAL tag=it29_b0_plus8 alloc=[56, 48, 48, 24, 48, 48, 8, 16] bytes=296 recall=66.870000

SQ_GREEDY_EVAL tag=it29_b1_plus8 alloc=[48, 56, 48, 24, 48, 48, 8, 16] bytes=296 recall=66.862500

SQ_GREEDY_EVAL tag=it29_b2_plus8 alloc=[48, 48, 56, 24, 48, 48, 8, 16] bytes=296 recall=66.672500

SQ_GREEDY_EVAL tag=it29_b3_plus8 alloc=[48, 48, 48, 32, 48, 48, 8, 16] bytes=296 recall=66.625000

SQ_GREEDY_EVAL tag=it29_b4_plus8 alloc=[48, 48, 48, 24, 56, 48, 8, 16] bytes=296 recall=66.630000

SQ_GREEDY_EVAL tag=it29_b5_plus8 alloc=[48, 48, 48, 24, 48, 56, 8, 16] bytes=296 recall=66.705000

SQ_GREEDY_EVAL tag=it29_b6_plus8 alloc=[48, 48, 48, 24, 48, 48, 16, 16] bytes=296 recall=66.795000

SQ_GREEDY_EVAL tag=it29_b7_plus8 alloc=[48, 48, 48, 24, 48, 48, 8, 24] bytes=296 recall=66.877500

SQ_GREEDY_EVAL tag=it30_b0_plus8 alloc=[56, 48, 48, 24, 48, 48, 8, 24] bytes=304 recall=67.272500

SQ_GREEDY_EVAL tag=it30_b1_plus8 alloc=[48, 56, 48, 24, 48, 48, 8, 24] bytes=304 recall=67.287500

SQ_GREEDY_EVAL tag=it30_b2_plus8 alloc=[48, 48, 56, 24, 48, 48, 8, 24] bytes=304 recall=67.280000

SQ_GREEDY_EVAL tag=it30_b3_plus8 alloc=[48, 48, 48, 32, 48, 48, 8, 24] bytes=304 recall=67.197500

SQ_GREEDY_EVAL tag=it30_b4_plus8 alloc=[48, 48, 48, 24, 56, 48, 8, 24] bytes=304 recall=67.267500

SQ_GREEDY_EVAL tag=it30_b5_plus8 alloc=[48, 48, 48, 24, 48, 56, 8, 24] bytes=304 recall=67.155000

SQ_GREEDY_EVAL tag=it30_b6_plus8 alloc=[48, 48, 48, 24, 48, 48, 16, 24] bytes=304 recall=67.290000

SQ_GREEDY_EVAL tag=it30_b7_plus8 alloc=[48, 48, 48, 24, 48, 48, 8, 32] bytes=304 recall=67.522500

SQ_GREEDY_EVAL tag=it31_b0_plus8 alloc=[56, 48, 48, 24, 48, 48, 8, 32] bytes=312 recall=67.922500

SQ_GREEDY_EVAL tag=it31_b1_plus8 alloc=[48, 56, 48, 24, 48, 48, 8, 32] bytes=312 recall=67.832500

SQ_GREEDY_EVAL tag=it31_b2_plus8 alloc=[48, 48, 56, 24, 48, 48, 8, 32] bytes=312 recall=67.815000

SQ_GREEDY_EVAL tag=it31_b3_plus8 alloc=[48, 48, 48, 32, 48, 48, 8, 32] bytes=312 recall=67.810000

SQ_GREEDY_EVAL tag=it31_b4_plus8 alloc=[48, 48, 48, 24, 56, 48, 8, 32] bytes=312 recall=67.785000

SQ_GREEDY_EVAL tag=it31_b5_plus8 alloc=[48, 48, 48, 24, 48, 56, 8, 32] bytes=312 recall=67.722500

SQ_GREEDY_EVAL tag=it31_b6_plus8 alloc=[48, 48, 48, 24, 48, 48, 16, 32] bytes=312 recall=67.955000

SQ_GREEDY_EVAL tag=it31_b7_plus8 alloc=[48, 48, 48, 24, 48, 48, 8, 40] bytes=312 recall=68.052500

SQ_GREEDY_EVAL tag=it32_b0_plus8 alloc=[56, 48, 48, 24, 48, 48, 8, 40] bytes=320 recall=68.360000

SQ_GREEDY_EVAL tag=it32_b1_plus8 alloc=[48, 56, 48, 24, 48, 48, 8, 40] bytes=320 recall=68.332500

SQ_GREEDY_EVAL tag=it32_b2_plus8 alloc=[48, 48, 56, 24, 48, 48, 8, 40] bytes=320 recall=68.322500

SQ_GREEDY_EVAL tag=it32_b3_plus8 alloc=[48, 48, 48, 32, 48, 48, 8, 40] bytes=320 recall=68.267500

SQ_GREEDY_EVAL tag=it32_b4_plus8 alloc=[48, 48, 48, 24, 56, 48, 8, 40] bytes=320 recall=68.367500

SQ_GREEDY_EVAL tag=it32_b5_plus8 alloc=[48, 48, 48, 24, 48, 56, 8, 40] bytes=320 recall=68.327500

SQ_GREEDY_EVAL tag=it32_b6_plus8 alloc=[48, 48, 48, 24, 48, 48, 16, 40] bytes=320 recall=68.540000

SQ_GREEDY_EVAL tag=it32_b7_plus8 alloc=[48, 48, 48, 24, 48, 48, 8, 48] bytes=320 recall=68.555000

SQ_GREEDY_EVAL tag=it33_b0_plus8 alloc=[56, 48, 48, 24, 48, 48, 8, 48] bytes=328 recall=69.032500

SQ_GREEDY_EVAL tag=it33_b1_plus8 alloc=[48, 56, 48, 24, 48, 48, 8, 48] bytes=328 recall=68.927500

SQ_GREEDY_EVAL tag=it33_b2_plus8 alloc=[48, 48, 56, 24, 48, 48, 8, 48] bytes=328 recall=68.975000

SQ_GREEDY_EVAL tag=it33_b3_plus8 alloc=[48, 48, 48, 32, 48, 48, 8, 48] bytes=328 recall=68.705000

SQ_GREEDY_EVAL tag=it33_b4_plus8 alloc=[48, 48, 48, 24, 56, 48, 8, 48] bytes=328 recall=68.880000

SQ_GREEDY_EVAL tag=it33_b5_plus8 alloc=[48, 48, 48, 24, 48, 56, 8, 48] bytes=328 recall=68.795000

SQ_GREEDY_EVAL tag=it33_b6_plus8 alloc=[48, 48, 48, 24, 48, 48, 16, 48] bytes=328 recall=69.035000

SQ_GREEDY_EVAL tag=it33_b7_plus8 alloc=[48, 48, 48, 24, 48, 48, 8, 56] bytes=328 recall=68.835000

SQ_GREEDY_EVAL tag=it34_b0_plus8 alloc=[56, 48, 48, 24, 48, 48, 16, 48] bytes=336 recall=69.567500

SQ_GREEDY_EVAL tag=it34_b1_plus8 alloc=[48, 56, 48, 24, 48, 48, 16, 48] bytes=336 recall=69.432500

SQ_GREEDY_EVAL tag=it34_b2_plus8 alloc=[48, 48, 56, 24, 48, 48, 16, 48] bytes=336 recall=69.390000

SQ_GREEDY_EVAL tag=it34_b3_plus8 alloc=[48, 48, 48, 32, 48, 48, 16, 48] bytes=336 recall=69.162500

SQ_GREEDY_EVAL tag=it34_b4_plus8 alloc=[48, 48, 48, 24, 56, 48, 16, 48] bytes=336 recall=69.302500

SQ_GREEDY_EVAL tag=it34_b5_plus8 alloc=[48, 48, 48, 24, 48, 56, 16, 48] bytes=336 recall=69.287500

SQ_GREEDY_EVAL tag=it34_b6_plus8 alloc=[48, 48, 48, 24, 48, 48, 24, 48] bytes=336 recall=69.637500

SQ_GREEDY_EVAL tag=it34_b7_plus8 alloc=[48, 48, 48, 24, 48, 48, 16, 56] bytes=336 recall=69.222500

SQ_GREEDY_EVAL tag=it35_b0_plus8 alloc=[56, 48, 48, 24, 48, 48, 24, 48] bytes=344 recall=70.102500

SQ_GREEDY_EVAL tag=it35_b1_plus8 alloc=[48, 56, 48, 24, 48, 48, 24, 48] bytes=344 recall=69.995000

SQ_GREEDY_EVAL tag=it35_b2_plus8 alloc=[48, 48, 56, 24, 48, 48, 24, 48] bytes=344 recall=70.015000

SQ_GREEDY_EVAL tag=it35_b3_plus8 alloc=[48, 48, 48, 32, 48, 48, 24, 48] bytes=344 recall=69.787500

SQ_GREEDY_EVAL tag=it35_b4_plus8 alloc=[48, 48, 48, 24, 56, 48, 24, 48] bytes=344 recall=69.992500

SQ_GREEDY_EVAL tag=it35_b5_plus8 alloc=[48, 48, 48, 24, 48, 56, 24, 48] bytes=344 recall=69.862500

SQ_GREEDY_EVAL tag=it35_b6_plus8 alloc=[48, 48, 48, 24, 48, 48, 32, 48] bytes=344 recall=70.090000

SQ_GREEDY_EVAL tag=it35_b7_plus8 alloc=[48, 48, 48, 24, 48, 48, 24, 56] bytes=344 recall=69.937500

SQ_GREEDY_EVAL tag=it36_b0_plus8 alloc=[64, 48, 48, 24, 48, 48, 24, 48] bytes=352 recall=70.532500

SQ_GREEDY_EVAL tag=it36_b1_plus8 alloc=[56, 56, 48, 24, 48, 48, 24, 48] bytes=352 recall=70.527500

SQ_GREEDY_EVAL tag=it36_b2_plus8 alloc=[56, 48, 56, 24, 48, 48, 24, 48] bytes=352 recall=70.410000

SQ_GREEDY_EVAL tag=it36_b3_plus8 alloc=[56, 48, 48, 32, 48, 48, 24, 48] bytes=352 recall=70.260000

SQ_GREEDY_EVAL tag=it36_b4_plus8 alloc=[56, 48, 48, 24, 56, 48, 24, 48] bytes=352 recall=70.365000

SQ_GREEDY_EVAL tag=it36_b5_plus8 alloc=[56, 48, 48, 24, 48, 56, 24, 48] bytes=352 recall=70.320000

SQ_GREEDY_EVAL tag=it36_b6_plus8 alloc=[56, 48, 48, 24, 48, 48, 32, 48] bytes=352 recall=70.560000

SQ_GREEDY_EVAL tag=it36_b7_plus8 alloc=[56, 48, 48, 24, 48, 48, 24, 56] bytes=352 recall=70.365000

SQ_GREEDY_EVAL tag=it37_b0_plus8 alloc=[64, 48, 48, 24, 48, 48, 32, 48] bytes=360 recall=71.005000

SQ_GREEDY_EVAL tag=it37_b1_plus8 alloc=[56, 56, 48, 24, 48, 48, 32, 48] bytes=360 recall=70.975000

SQ_GREEDY_EVAL tag=it37_b2_plus8 alloc=[56, 48, 56, 24, 48, 48, 32, 48] bytes=360 recall=70.975000

SQ_GREEDY_EVAL tag=it37_b3_plus8 alloc=[56, 48, 48, 32, 48, 48, 32, 48] bytes=360 recall=70.890000

SQ_GREEDY_EVAL tag=it37_b4_plus8 alloc=[56, 48, 48, 24, 56, 48, 32, 48] bytes=360 recall=70.990000

SQ_GREEDY_EVAL tag=it37_b5_plus8 alloc=[56, 48, 48, 24, 48, 56, 32, 48] bytes=360 recall=70.850000

SQ_GREEDY_EVAL tag=it37_b6_plus8 alloc=[56, 48, 48, 24, 48, 48, 40, 48] bytes=360 recall=71.112500

SQ_GREEDY_EVAL tag=it37_b7_plus8 alloc=[56, 48, 48, 24, 48, 48, 32, 56] bytes=360 recall=70.897500

SQ_GREEDY_EVAL tag=it38_b0_plus8 alloc=[64, 48, 48, 24, 48, 48, 40, 48] bytes=368 recall=71.592500

SQ_GREEDY_EVAL tag=it38_b1_plus8 alloc=[56, 56, 48, 24, 48, 48, 40, 48] bytes=368 recall=71.592500

SQ_GREEDY_EVAL tag=it38_b2_plus8 alloc=[56, 48, 56, 24, 48, 48, 40, 48] bytes=368 recall=71.515000

SQ_GREEDY_EVAL tag=it38_b3_plus8 alloc=[56, 48, 48, 32, 48, 48, 40, 48] bytes=368 recall=71.402500

SQ_GREEDY_EVAL tag=it38_b4_plus8 alloc=[56, 48, 48, 24, 56, 48, 40, 48] bytes=368 recall=71.417500

SQ_GREEDY_EVAL tag=it38_b5_plus8 alloc=[56, 48, 48, 24, 48, 56, 40, 48] bytes=368 recall=71.340000

SQ_GREEDY_EVAL tag=it38_b6_plus8 alloc=[56, 48, 48, 24, 48, 48, 48, 48] bytes=368 recall=71.827500

SQ_GREEDY_EVAL tag=it38_b7_plus8 alloc=[56, 48, 48, 24, 48, 48, 40, 56] bytes=368 recall=71.325000

SQ_GREEDY_EVAL tag=it39_b0_plus8 alloc=[64, 48, 48, 24, 48, 48, 48, 48] bytes=376 recall=72.227500

SQ_GREEDY_EVAL tag=it39_b1_plus8 alloc=[56, 56, 48, 24, 48, 48, 48, 48] bytes=376 recall=72.237500

SQ_GREEDY_EVAL tag=it39_b2_plus8 alloc=[56, 48, 56, 24, 48, 48, 48, 48] bytes=376 recall=72.147500

SQ_GREEDY_EVAL tag=it39_b3_plus8 alloc=[56, 48, 48, 32, 48, 48, 48, 48] bytes=376 recall=71.935000

SQ_GREEDY_EVAL tag=it39_b4_plus8 alloc=[56, 48, 48, 24, 56, 48, 48, 48] bytes=376 recall=72.092500

SQ_GREEDY_EVAL tag=it39_b5_plus8 alloc=[56, 48, 48, 24, 48, 56, 48, 48] bytes=376 recall=72.005000

SQ_GREEDY_EVAL tag=it39_b6_plus8 alloc=[56, 48, 48, 24, 48, 48, 56, 48] bytes=376 recall=71.925000

SQ_GREEDY_EVAL tag=it39_b7_plus8 alloc=[56, 48, 48, 24, 48, 48, 48, 56] bytes=376 recall=72.040000

SQ_GREEDY_EVAL tag=it40_b0_plus8 alloc=[64, 56, 48, 24, 48, 48, 48, 48] bytes=384 recall=72.565000

SQ_GREEDY_EVAL tag=it40_b1_plus8 alloc=[56, 64, 48, 24, 48, 48, 48, 48] bytes=384 recall=72.560000

SQ_GREEDY_EVAL tag=it40_b2_plus8 alloc=[56, 56, 56, 24, 48, 48, 48, 48] bytes=384 recall=72.405000

SQ_GREEDY_EVAL tag=it40_b3_plus8 alloc=[56, 56, 48, 32, 48, 48, 48, 48] bytes=384 recall=72.385000

SQ_GREEDY_EVAL tag=it40_b4_plus8 alloc=[56, 56, 48, 24, 56, 48, 48, 48] bytes=384 recall=72.530000

SQ_GREEDY_EVAL tag=it40_b5_plus8 alloc=[56, 56, 48, 24, 48, 56, 48, 48] bytes=384 recall=72.387500

SQ_GREEDY_EVAL tag=it40_b6_plus8 alloc=[56, 56, 48, 24, 48, 48, 56, 48] bytes=384 recall=72.355000

SQ_GREEDY_EVAL tag=it40_b7_plus8 alloc=[56, 56, 48, 24, 48, 48, 48, 56] bytes=384 recall=72.372500

```



### DBpedia Openai text large 3 SQ:
#### Uniform
SQ sweep completed!
Results directory: /tmp/sq_sweep_1779820867

Summary of SQ recall results:

Bytes,Recall

64,27.925

96,38.775

128,46.4175

160,52.065

192,56.3775

224,59.925

256,62.785

288,65.035

320,67.375

352,69.495

384,70.675

#### Variable

SQ_GREEDY_EVAL tag=init alloc=[8, 8, 8, 8, 8, 8, 8, 8] bytes=64 recall=27.925000

  

SQ_GREEDY_EVAL tag=it1_b0_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 8] bytes=72 recall=31.682500

  

SQ_GREEDY_EVAL tag=it1_b1_plus8 alloc=[8, 16, 8, 8, 8, 8, 8, 8] bytes=72 recall=31.365000

  

SQ_GREEDY_EVAL tag=it1_b2_plus8 alloc=[8, 8, 16, 8, 8, 8, 8, 8] bytes=72 recall=31.190000

  

SQ_GREEDY_EVAL tag=it1_b3_plus8 alloc=[8, 8, 8, 16, 8, 8, 8, 8] bytes=72 recall=31.300000

  

SQ_GREEDY_EVAL tag=it1_b4_plus8 alloc=[8, 8, 8, 8, 16, 8, 8, 8] bytes=72 recall=30.857500

  

SQ_GREEDY_EVAL tag=it1_b5_plus8 alloc=[8, 8, 8, 8, 8, 16, 8, 8] bytes=72 recall=31.042500

  

SQ_GREEDY_EVAL tag=it1_b6_plus8 alloc=[8, 8, 8, 8, 8, 8, 16, 8] bytes=72 recall=30.775000

  

SQ_GREEDY_EVAL tag=it1_b7_plus8 alloc=[8, 8, 8, 8, 8, 8, 8, 16] bytes=72 recall=30.655000

  

SQ_GREEDY_EVAL tag=it2_b0_plus8 alloc=[24, 8, 8, 8, 8, 8, 8, 8] bytes=80 recall=34.770000

  

SQ_GREEDY_EVAL tag=it2_b1_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 8] bytes=80 recall=34.915000

  

SQ_GREEDY_EVAL tag=it2_b2_plus8 alloc=[16, 8, 16, 8, 8, 8, 8, 8] bytes=80 recall=34.750000

  

SQ_GREEDY_EVAL tag=it2_b3_plus8 alloc=[16, 8, 8, 16, 8, 8, 8, 8] bytes=80 recall=34.570000

  

SQ_GREEDY_EVAL tag=it2_b4_plus8 alloc=[16, 8, 8, 8, 16, 8, 8, 8] bytes=80 recall=34.207500

  

SQ_GREEDY_EVAL tag=it2_b5_plus8 alloc=[16, 8, 8, 8, 8, 16, 8, 8] bytes=80 recall=34.335000

  

SQ_GREEDY_EVAL tag=it2_b6_plus8 alloc=[16, 8, 8, 8, 8, 8, 16, 8] bytes=80 recall=34.137500

  

SQ_GREEDY_EVAL tag=it2_b7_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 16] bytes=80 recall=34.032500

  

SQ_GREEDY_EVAL tag=it3_b0_plus8 alloc=[24, 16, 8, 8, 8, 8, 8, 8] bytes=88 recall=37.610000

  

SQ_GREEDY_EVAL tag=it3_b1_plus8 alloc=[16, 24, 8, 8, 8, 8, 8, 8] bytes=88 recall=38.157500

  

SQ_GREEDY_EVAL tag=it3_b2_plus8 alloc=[16, 16, 16, 8, 8, 8, 8, 8] bytes=88 recall=37.702500

  

SQ_GREEDY_EVAL tag=it3_b3_plus8 alloc=[16, 16, 8, 16, 8, 8, 8, 8] bytes=88 recall=37.500000

  

SQ_GREEDY_EVAL tag=it3_b4_plus8 alloc=[16, 16, 8, 8, 16, 8, 8, 8] bytes=88 recall=36.930000

  

SQ_GREEDY_EVAL tag=it3_b5_plus8 alloc=[16, 16, 8, 8, 8, 16, 8, 8] bytes=88 recall=37.025000

  

SQ_GREEDY_EVAL tag=it3_b6_plus8 alloc=[16, 16, 8, 8, 8, 8, 16, 8] bytes=88 recall=37.057500

  

SQ_GREEDY_EVAL tag=it3_b7_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 16] bytes=88 recall=36.980000

  

SQ_GREEDY_EVAL tag=it4_b0_plus8 alloc=[24, 24, 8, 8, 8, 8, 8, 8] bytes=96 recall=40.755000

  

SQ_GREEDY_EVAL tag=it4_b1_plus8 alloc=[16, 32, 8, 8, 8, 8, 8, 8] bytes=96 recall=40.627500

  

SQ_GREEDY_EVAL tag=it4_b2_plus8 alloc=[16, 24, 16, 8, 8, 8, 8, 8] bytes=96 recall=40.395000

  

SQ_GREEDY_EVAL tag=it4_b3_plus8 alloc=[16, 24, 8, 16, 8, 8, 8, 8] bytes=96 recall=40.392500

  

SQ_GREEDY_EVAL tag=it4_b4_plus8 alloc=[16, 24, 8, 8, 16, 8, 8, 8] bytes=96 recall=40.107500

  

SQ_GREEDY_EVAL tag=it4_b5_plus8 alloc=[16, 24, 8, 8, 8, 16, 8, 8] bytes=96 recall=40.242500

  

SQ_GREEDY_EVAL tag=it4_b6_plus8 alloc=[16, 24, 8, 8, 8, 8, 16, 8] bytes=96 recall=40.272500

  

SQ_GREEDY_EVAL tag=it4_b7_plus8 alloc=[16, 24, 8, 8, 8, 8, 8, 16] bytes=96 recall=40.100000

  

SQ_GREEDY_EVAL tag=it5_b0_plus8 alloc=[32, 24, 8, 8, 8, 8, 8, 8] bytes=104 recall=43.672500

  

SQ_GREEDY_EVAL tag=it5_b1_plus8 alloc=[24, 32, 8, 8, 8, 8, 8, 8] bytes=104 recall=42.987500

  

SQ_GREEDY_EVAL tag=it5_b2_plus8 alloc=[24, 24, 16, 8, 8, 8, 8, 8] bytes=104 recall=42.890000

  

SQ_GREEDY_EVAL tag=it5_b3_plus8 alloc=[24, 24, 8, 16, 8, 8, 8, 8] bytes=104 recall=42.860000

  

SQ_GREEDY_EVAL tag=it5_b4_plus8 alloc=[24, 24, 8, 8, 16, 8, 8, 8] bytes=104 recall=42.487500

  

SQ_GREEDY_EVAL tag=it5_b5_plus8 alloc=[24, 24, 8, 8, 8, 16, 8, 8] bytes=104 recall=42.492500

  

SQ_GREEDY_EVAL tag=it5_b6_plus8 alloc=[24, 24, 8, 8, 8, 8, 16, 8] bytes=104 recall=42.400000

  

SQ_GREEDY_EVAL tag=it5_b7_plus8 alloc=[24, 24, 8, 8, 8, 8, 8, 16] bytes=104 recall=42.387500

  

SQ_GREEDY_EVAL tag=it6_b0_plus8 alloc=[40, 24, 8, 8, 8, 8, 8, 8] bytes=112 recall=45.597500

  

SQ_GREEDY_EVAL tag=it6_b1_plus8 alloc=[32, 32, 8, 8, 8, 8, 8, 8] bytes=112 recall=45.387500

  

SQ_GREEDY_EVAL tag=it6_b2_plus8 alloc=[32, 24, 16, 8, 8, 8, 8, 8] bytes=112 recall=45.580000

  

SQ_GREEDY_EVAL tag=it6_b3_plus8 alloc=[32, 24, 8, 16, 8, 8, 8, 8] bytes=112 recall=45.470000

  

SQ_GREEDY_EVAL tag=it6_b4_plus8 alloc=[32, 24, 8, 8, 16, 8, 8, 8] bytes=112 recall=45.200000

  

SQ_GREEDY_EVAL tag=it6_b5_plus8 alloc=[32, 24, 8, 8, 8, 16, 8, 8] bytes=112 recall=45.130000

  

SQ_GREEDY_EVAL tag=it6_b6_plus8 alloc=[32, 24, 8, 8, 8, 8, 16, 8] bytes=112 recall=45.300000

  

SQ_GREEDY_EVAL tag=it6_b7_plus8 alloc=[32, 24, 8, 8, 8, 8, 8, 16] bytes=112 recall=45.047500

  

SQ_GREEDY_EVAL tag=it7_b0_plus8 alloc=[48, 24, 8, 8, 8, 8, 8, 8] bytes=120 recall=47.750000

  

SQ_GREEDY_EVAL tag=it7_b1_plus8 alloc=[40, 32, 8, 8, 8, 8, 8, 8] bytes=120 recall=47.177500

  

SQ_GREEDY_EVAL tag=it7_b2_plus8 alloc=[40, 24, 16, 8, 8, 8, 8, 8] bytes=120 recall=47.137500

  

SQ_GREEDY_EVAL tag=it7_b3_plus8 alloc=[40, 24, 8, 16, 8, 8, 8, 8] bytes=120 recall=47.222500

  

SQ_GREEDY_EVAL tag=it7_b4_plus8 alloc=[40, 24, 8, 8, 16, 8, 8, 8] bytes=120 recall=46.895000

  

SQ_GREEDY_EVAL tag=it7_b5_plus8 alloc=[40, 24, 8, 8, 8, 16, 8, 8] bytes=120 recall=46.970000

  

SQ_GREEDY_EVAL tag=it7_b6_plus8 alloc=[40, 24, 8, 8, 8, 8, 16, 8] bytes=120 recall=46.997500

  

SQ_GREEDY_EVAL tag=it7_b7_plus8 alloc=[40, 24, 8, 8, 8, 8, 8, 16] bytes=120 recall=46.890000

  

SQ_GREEDY_EVAL tag=it8_b0_plus8 alloc=[56, 24, 8, 8, 8, 8, 8, 8] bytes=128 recall=50.662500

  

SQ_GREEDY_EVAL tag=it8_b1_plus8 alloc=[48, 32, 8, 8, 8, 8, 8, 8] bytes=128 recall=49.497500

  

SQ_GREEDY_EVAL tag=it8_b2_plus8 alloc=[48, 24, 16, 8, 8, 8, 8, 8] bytes=128 recall=49.477500

  

SQ_GREEDY_EVAL tag=it8_b3_plus8 alloc=[48, 24, 8, 16, 8, 8, 8, 8] bytes=128 recall=49.302500

  

SQ_GREEDY_EVAL tag=it8_b4_plus8 alloc=[48, 24, 8, 8, 16, 8, 8, 8] bytes=128 recall=48.877500

  

SQ_GREEDY_EVAL tag=it8_b5_plus8 alloc=[48, 24, 8, 8, 8, 16, 8, 8] bytes=128 recall=48.892500

  

SQ_GREEDY_EVAL tag=it8_b6_plus8 alloc=[48, 24, 8, 8, 8, 8, 16, 8] bytes=128 recall=48.975000

  

SQ_GREEDY_EVAL tag=it8_b7_plus8 alloc=[48, 24, 8, 8, 8, 8, 8, 16] bytes=128 recall=48.922500

  

SQ_GREEDY_EVAL tag=it9_b0_plus8 alloc=[64, 24, 8, 8, 8, 8, 8, 8] bytes=136 recall=51.972500

  

SQ_GREEDY_EVAL tag=it9_b1_plus8 alloc=[56, 32, 8, 8, 8, 8, 8, 8] bytes=136 recall=51.795000

  

SQ_GREEDY_EVAL tag=it9_b2_plus8 alloc=[56, 24, 16, 8, 8, 8, 8, 8] bytes=136 recall=51.937500

  

SQ_GREEDY_EVAL tag=it9_b3_plus8 alloc=[56, 24, 8, 16, 8, 8, 8, 8] bytes=136 recall=52.017500

  

SQ_GREEDY_EVAL tag=it9_b4_plus8 alloc=[56, 24, 8, 8, 16, 8, 8, 8] bytes=136 recall=51.755000

  

SQ_GREEDY_EVAL tag=it9_b5_plus8 alloc=[56, 24, 8, 8, 8, 16, 8, 8] bytes=136 recall=51.712500

  

SQ_GREEDY_EVAL tag=it9_b6_plus8 alloc=[56, 24, 8, 8, 8, 8, 16, 8] bytes=136 recall=51.785000

  

SQ_GREEDY_EVAL tag=it9_b7_plus8 alloc=[56, 24, 8, 8, 8, 8, 8, 16] bytes=136 recall=51.845000

  

SQ_GREEDY_EVAL tag=it10_b0_plus8 alloc=[64, 24, 8, 16, 8, 8, 8, 8] bytes=144 recall=53.027500

  

SQ_GREEDY_EVAL tag=it10_b1_plus8 alloc=[56, 32, 8, 16, 8, 8, 8, 8] bytes=144 recall=53.082500

  

SQ_GREEDY_EVAL tag=it10_b2_plus8 alloc=[56, 24, 16, 16, 8, 8, 8, 8] bytes=144 recall=53.195000

  

SQ_GREEDY_EVAL tag=it10_b3_plus8 alloc=[56, 24, 8, 24, 8, 8, 8, 8] bytes=144 recall=53.437500

  

SQ_GREEDY_EVAL tag=it10_b4_plus8 alloc=[56, 24, 8, 16, 16, 8, 8, 8] bytes=144 recall=53.055000

  

SQ_GREEDY_EVAL tag=it10_b5_plus8 alloc=[56, 24, 8, 16, 8, 16, 8, 8] bytes=144 recall=53.145000

  

SQ_GREEDY_EVAL tag=it10_b6_plus8 alloc=[56, 24, 8, 16, 8, 8, 16, 8] bytes=144 recall=53.007500

  

SQ_GREEDY_EVAL tag=it10_b7_plus8 alloc=[56, 24, 8, 16, 8, 8, 8, 16] bytes=144 recall=53.110000

  

SQ_GREEDY_EVAL tag=it11_b0_plus8 alloc=[64, 24, 8, 24, 8, 8, 8, 8] bytes=152 recall=54.335000

  

SQ_GREEDY_EVAL tag=it11_b1_plus8 alloc=[56, 32, 8, 24, 8, 8, 8, 8] bytes=152 recall=54.312500

  

SQ_GREEDY_EVAL tag=it11_b2_plus8 alloc=[56, 24, 16, 24, 8, 8, 8, 8] bytes=152 recall=54.535000

  

SQ_GREEDY_EVAL tag=it11_b3_plus8 alloc=[56, 24, 8, 32, 8, 8, 8, 8] bytes=152 recall=54.655000

  

SQ_GREEDY_EVAL tag=it11_b4_plus8 alloc=[56, 24, 8, 24, 16, 8, 8, 8] bytes=152 recall=54.302500

  

SQ_GREEDY_EVAL tag=it11_b5_plus8 alloc=[56, 24, 8, 24, 8, 16, 8, 8] bytes=152 recall=54.350000

  

SQ_GREEDY_EVAL tag=it11_b6_plus8 alloc=[56, 24, 8, 24, 8, 8, 16, 8] bytes=152 recall=54.425000

  

SQ_GREEDY_EVAL tag=it11_b7_plus8 alloc=[56, 24, 8, 24, 8, 8, 8, 16] bytes=152 recall=54.365000

  

SQ_GREEDY_EVAL tag=it12_b0_plus8 alloc=[64, 24, 8, 32, 8, 8, 8, 8] bytes=160 recall=55.407500

  

SQ_GREEDY_EVAL tag=it12_b1_plus8 alloc=[56, 32, 8, 32, 8, 8, 8, 8] bytes=160 recall=55.452500

  

SQ_GREEDY_EVAL tag=it12_b2_plus8 alloc=[56, 24, 16, 32, 8, 8, 8, 8] bytes=160 recall=55.712500

  

SQ_GREEDY_EVAL tag=it12_b3_plus8 alloc=[56, 24, 8, 40, 8, 8, 8, 8] bytes=160 recall=55.637500

  

SQ_GREEDY_EVAL tag=it12_b4_plus8 alloc=[56, 24, 8, 32, 16, 8, 8, 8] bytes=160 recall=55.362500

  

SQ_GREEDY_EVAL tag=it12_b5_plus8 alloc=[56, 24, 8, 32, 8, 16, 8, 8] bytes=160 recall=55.517500

  

SQ_GREEDY_EVAL tag=it12_b6_plus8 alloc=[56, 24, 8, 32, 8, 8, 16, 8] bytes=160 recall=55.435000

  

SQ_GREEDY_EVAL tag=it12_b7_plus8 alloc=[56, 24, 8, 32, 8, 8, 8, 16] bytes=160 recall=55.412500

  

SQ_GREEDY_EVAL tag=it13_b0_plus8 alloc=[64, 24, 16, 32, 8, 8, 8, 8] bytes=168 recall=56.510000

  

SQ_GREEDY_EVAL tag=it13_b1_plus8 alloc=[56, 32, 16, 32, 8, 8, 8, 8] bytes=168 recall=56.562500

  

SQ_GREEDY_EVAL tag=it13_b2_plus8 alloc=[56, 24, 24, 32, 8, 8, 8, 8] bytes=168 recall=57.112500

  

SQ_GREEDY_EVAL tag=it13_b3_plus8 alloc=[56, 24, 16, 40, 8, 8, 8, 8] bytes=168 recall=56.767500

  

SQ_GREEDY_EVAL tag=it13_b4_plus8 alloc=[56, 24, 16, 32, 16, 8, 8, 8] bytes=168 recall=56.575000

  

SQ_GREEDY_EVAL tag=it13_b5_plus8 alloc=[56, 24, 16, 32, 8, 16, 8, 8] bytes=168 recall=56.470000

  

SQ_GREEDY_EVAL tag=it13_b6_plus8 alloc=[56, 24, 16, 32, 8, 8, 16, 8] bytes=168 recall=56.492500

  

SQ_GREEDY_EVAL tag=it13_b7_plus8 alloc=[56, 24, 16, 32, 8, 8, 8, 16] bytes=168 recall=56.560000

  

SQ_GREEDY_EVAL tag=it14_b0_plus8 alloc=[64, 24, 24, 32, 8, 8, 8, 8] bytes=176 recall=57.847500

  

SQ_GREEDY_EVAL tag=it14_b1_plus8 alloc=[56, 32, 24, 32, 8, 8, 8, 8] bytes=176 recall=57.957500

  

SQ_GREEDY_EVAL tag=it14_b2_plus8 alloc=[56, 24, 32, 32, 8, 8, 8, 8] bytes=176 recall=58.120000

  

SQ_GREEDY_EVAL tag=it14_b3_plus8 alloc=[56, 24, 24, 40, 8, 8, 8, 8] bytes=176 recall=57.982500

  

SQ_GREEDY_EVAL tag=it14_b4_plus8 alloc=[56, 24, 24, 32, 16, 8, 8, 8] bytes=176 recall=57.935000

  

SQ_GREEDY_EVAL tag=it14_b5_plus8 alloc=[56, 24, 24, 32, 8, 16, 8, 8] bytes=176 recall=57.955000

  

SQ_GREEDY_EVAL tag=it14_b6_plus8 alloc=[56, 24, 24, 32, 8, 8, 16, 8] bytes=176 recall=58.037500

  

SQ_GREEDY_EVAL tag=it14_b7_plus8 alloc=[56, 24, 24, 32, 8, 8, 8, 16] bytes=176 recall=57.905000

  

SQ_GREEDY_EVAL tag=it15_b0_plus8 alloc=[64, 24, 32, 32, 8, 8, 8, 8] bytes=184 recall=58.757500

  

SQ_GREEDY_EVAL tag=it15_b1_plus8 alloc=[56, 32, 32, 32, 8, 8, 8, 8] bytes=184 recall=58.697500

  

SQ_GREEDY_EVAL tag=it15_b2_plus8 alloc=[56, 24, 40, 32, 8, 8, 8, 8] bytes=184 recall=59.142500

  

SQ_GREEDY_EVAL tag=it15_b3_plus8 alloc=[56, 24, 32, 40, 8, 8, 8, 8] bytes=184 recall=58.742500

  

SQ_GREEDY_EVAL tag=it15_b4_plus8 alloc=[56, 24, 32, 32, 16, 8, 8, 8] bytes=184 recall=58.785000

  

SQ_GREEDY_EVAL tag=it15_b5_plus8 alloc=[56, 24, 32, 32, 8, 16, 8, 8] bytes=184 recall=58.775000

  

SQ_GREEDY_EVAL tag=it15_b6_plus8 alloc=[56, 24, 32, 32, 8, 8, 16, 8] bytes=184 recall=58.890000

  

SQ_GREEDY_EVAL tag=it15_b7_plus8 alloc=[56, 24, 32, 32, 8, 8, 8, 16] bytes=184 recall=58.900000

  

SQ_GREEDY_EVAL tag=it16_b0_plus8 alloc=[64, 24, 40, 32, 8, 8, 8, 8] bytes=192 recall=59.885000

  

SQ_GREEDY_EVAL tag=it16_b1_plus8 alloc=[56, 32, 40, 32, 8, 8, 8, 8] bytes=192 recall=59.805000

  

SQ_GREEDY_EVAL tag=it16_b2_plus8 alloc=[56, 24, 48, 32, 8, 8, 8, 8] bytes=192 recall=60.262500

  

SQ_GREEDY_EVAL tag=it16_b3_plus8 alloc=[56, 24, 40, 40, 8, 8, 8, 8] bytes=192 recall=59.915000

  

SQ_GREEDY_EVAL tag=it16_b4_plus8 alloc=[56, 24, 40, 32, 16, 8, 8, 8] bytes=192 recall=59.785000

  

SQ_GREEDY_EVAL tag=it16_b5_plus8 alloc=[56, 24, 40, 32, 8, 16, 8, 8] bytes=192 recall=59.830000

  

SQ_GREEDY_EVAL tag=it16_b6_plus8 alloc=[56, 24, 40, 32, 8, 8, 16, 8] bytes=192 recall=59.790000

  

SQ_GREEDY_EVAL tag=it16_b7_plus8 alloc=[56, 24, 40, 32, 8, 8, 8, 16] bytes=192 recall=59.832500

  

SQ_GREEDY_EVAL tag=it17_b0_plus8 alloc=[64, 24, 48, 32, 8, 8, 8, 8] bytes=200 recall=61.005000

  

SQ_GREEDY_EVAL tag=it17_b1_plus8 alloc=[56, 32, 48, 32, 8, 8, 8, 8] bytes=200 recall=60.820000

  

SQ_GREEDY_EVAL tag=it17_b2_plus8 alloc=[56, 24, 56, 32, 8, 8, 8, 8] bytes=200 recall=60.947500

  

SQ_GREEDY_EVAL tag=it17_b3_plus8 alloc=[56, 24, 48, 40, 8, 8, 8, 8] bytes=200 recall=60.975000

  

SQ_GREEDY_EVAL tag=it17_b4_plus8 alloc=[56, 24, 48, 32, 16, 8, 8, 8] bytes=200 recall=60.812500

  

SQ_GREEDY_EVAL tag=it17_b5_plus8 alloc=[56, 24, 48, 32, 8, 16, 8, 8] bytes=200 recall=60.795000

  

SQ_GREEDY_EVAL tag=it17_b6_plus8 alloc=[56, 24, 48, 32, 8, 8, 16, 8] bytes=200 recall=60.872500

  

SQ_GREEDY_EVAL tag=it17_b7_plus8 alloc=[56, 24, 48, 32, 8, 8, 8, 16] bytes=200 recall=60.767500

  

SQ_GREEDY_EVAL tag=it18_b0_plus8 alloc=[72, 24, 48, 32, 8, 8, 8, 8] bytes=208 recall=61.835000

  

SQ_GREEDY_EVAL tag=it18_b1_plus8 alloc=[64, 32, 48, 32, 8, 8, 8, 8] bytes=208 recall=61.647500

  

SQ_GREEDY_EVAL tag=it18_b2_plus8 alloc=[64, 24, 56, 32, 8, 8, 8, 8] bytes=208 recall=61.767500

  

SQ_GREEDY_EVAL tag=it18_b3_plus8 alloc=[64, 24, 48, 40, 8, 8, 8, 8] bytes=208 recall=61.537500

  

SQ_GREEDY_EVAL tag=it18_b4_plus8 alloc=[64, 24, 48, 32, 16, 8, 8, 8] bytes=208 recall=61.582500

  

SQ_GREEDY_EVAL tag=it18_b5_plus8 alloc=[64, 24, 48, 32, 8, 16, 8, 8] bytes=208 recall=61.565000

  

SQ_GREEDY_EVAL tag=it18_b6_plus8 alloc=[64, 24, 48, 32, 8, 8, 16, 8] bytes=208 recall=61.505000

  

SQ_GREEDY_EVAL tag=it18_b7_plus8 alloc=[64, 24, 48, 32, 8, 8, 8, 16] bytes=208 recall=61.462500

  

SQ_GREEDY_EVAL tag=it19_b0_plus8 alloc=[80, 24, 48, 32, 8, 8, 8, 8] bytes=216 recall=62.975000

  

SQ_GREEDY_EVAL tag=it19_b1_plus8 alloc=[72, 32, 48, 32, 8, 8, 8, 8] bytes=216 recall=62.567500

  

SQ_GREEDY_EVAL tag=it19_b2_plus8 alloc=[72, 24, 56, 32, 8, 8, 8, 8] bytes=216 recall=62.557500

  

SQ_GREEDY_EVAL tag=it19_b3_plus8 alloc=[72, 24, 48, 40, 8, 8, 8, 8] bytes=216 recall=62.475000

  

SQ_GREEDY_EVAL tag=it19_b4_plus8 alloc=[72, 24, 48, 32, 16, 8, 8, 8] bytes=216 recall=62.342500

  

SQ_GREEDY_EVAL tag=it19_b5_plus8 alloc=[72, 24, 48, 32, 8, 16, 8, 8] bytes=216 recall=62.492500

  

SQ_GREEDY_EVAL tag=it19_b6_plus8 alloc=[72, 24, 48, 32, 8, 8, 16, 8] bytes=216 recall=62.497500

  

SQ_GREEDY_EVAL tag=it19_b7_plus8 alloc=[72, 24, 48, 32, 8, 8, 8, 16] bytes=216 recall=62.340000

  

SQ_GREEDY_EVAL tag=it20_b0_plus8 alloc=[88, 24, 48, 32, 8, 8, 8, 8] bytes=224 recall=64.062500

  

SQ_GREEDY_EVAL tag=it20_b1_plus8 alloc=[80, 32, 48, 32, 8, 8, 8, 8] bytes=224 recall=63.535000

  

SQ_GREEDY_EVAL tag=it20_b2_plus8 alloc=[80, 24, 56, 32, 8, 8, 8, 8] bytes=224 recall=63.527500

  

SQ_GREEDY_EVAL tag=it20_b3_plus8 alloc=[80, 24, 48, 40, 8, 8, 8, 8] bytes=224 recall=63.465000

  

SQ_GREEDY_EVAL tag=it20_b4_plus8 alloc=[80, 24, 48, 32, 16, 8, 8, 8] bytes=224 recall=63.425000

  

SQ_GREEDY_EVAL tag=it20_b5_plus8 alloc=[80, 24, 48, 32, 8, 16, 8, 8] bytes=224 recall=63.465000

  

SQ_GREEDY_EVAL tag=it20_b6_plus8 alloc=[80, 24, 48, 32, 8, 8, 16, 8] bytes=224 recall=63.405000

  

SQ_GREEDY_EVAL tag=it20_b7_plus8 alloc=[80, 24, 48, 32, 8, 8, 8, 16] bytes=224 recall=63.422500

  

SQ_GREEDY_EVAL tag=it21_b0_plus8 alloc=[96, 24, 48, 32, 8, 8, 8, 8] bytes=232 recall=64.960000

  

SQ_GREEDY_EVAL tag=it21_b1_plus8 alloc=[88, 32, 48, 32, 8, 8, 8, 8] bytes=232 recall=64.707500

  

SQ_GREEDY_EVAL tag=it21_b2_plus8 alloc=[88, 24, 56, 32, 8, 8, 8, 8] bytes=232 recall=64.702500

  

SQ_GREEDY_EVAL tag=it21_b3_plus8 alloc=[88, 24, 48, 40, 8, 8, 8, 8] bytes=232 recall=64.740000

  

SQ_GREEDY_EVAL tag=it21_b4_plus8 alloc=[88, 24, 48, 32, 16, 8, 8, 8] bytes=232 recall=64.435000

  

SQ_GREEDY_EVAL tag=it21_b5_plus8 alloc=[88, 24, 48, 32, 8, 16, 8, 8] bytes=232 recall=64.657500

  

SQ_GREEDY_EVAL tag=it21_b6_plus8 alloc=[88, 24, 48, 32, 8, 8, 16, 8] bytes=232 recall=64.545000

  

SQ_GREEDY_EVAL tag=it21_b7_plus8 alloc=[88, 24, 48, 32, 8, 8, 8, 16] bytes=232 recall=64.585000

  

SQ_GREEDY_EVAL tag=it22_b0_plus8 alloc=[104, 24, 48, 32, 8, 8, 8, 8] bytes=240 recall=65.452500

  

SQ_GREEDY_EVAL tag=it22_b1_plus8 alloc=[96, 32, 48, 32, 8, 8, 8, 8] bytes=240 recall=65.412500

  

SQ_GREEDY_EVAL tag=it22_b2_plus8 alloc=[96, 24, 56, 32, 8, 8, 8, 8] bytes=240 recall=65.530000

  

SQ_GREEDY_EVAL tag=it22_b3_plus8 alloc=[96, 24, 48, 40, 8, 8, 8, 8] bytes=240 recall=65.627500

  

SQ_GREEDY_EVAL tag=it22_b4_plus8 alloc=[96, 24, 48, 32, 16, 8, 8, 8] bytes=240 recall=65.375000

  

SQ_GREEDY_EVAL tag=it22_b5_plus8 alloc=[96, 24, 48, 32, 8, 16, 8, 8] bytes=240 recall=65.620000

  

SQ_GREEDY_EVAL tag=it22_b6_plus8 alloc=[96, 24, 48, 32, 8, 8, 16, 8] bytes=240 recall=65.505000

  

SQ_GREEDY_EVAL tag=it22_b7_plus8 alloc=[96, 24, 48, 32, 8, 8, 8, 16] bytes=240 recall=65.427500

  

SQ_GREEDY_EVAL tag=it23_b0_plus8 alloc=[104, 24, 48, 40, 8, 8, 8, 8] bytes=248 recall=66.122500

  

SQ_GREEDY_EVAL tag=it23_b1_plus8 alloc=[96, 32, 48, 40, 8, 8, 8, 8] bytes=248 recall=66.055000

  

SQ_GREEDY_EVAL tag=it23_b2_plus8 alloc=[96, 24, 56, 40, 8, 8, 8, 8] bytes=248 recall=66.125000

  

SQ_GREEDY_EVAL tag=it23_b3_plus8 alloc=[96, 24, 48, 48, 8, 8, 8, 8] bytes=248 recall=66.190000

  

SQ_GREEDY_EVAL tag=it23_b4_plus8 alloc=[96, 24, 48, 40, 16, 8, 8, 8] bytes=248 recall=65.985000

  

SQ_GREEDY_EVAL tag=it23_b5_plus8 alloc=[96, 24, 48, 40, 8, 16, 8, 8] bytes=248 recall=66.017500

  

SQ_GREEDY_EVAL tag=it23_b6_plus8 alloc=[96, 24, 48, 40, 8, 8, 16, 8] bytes=248 recall=65.962500

  

SQ_GREEDY_EVAL tag=it23_b7_plus8 alloc=[96, 24, 48, 40, 8, 8, 8, 16] bytes=248 recall=66.095000

  

SQ_GREEDY_EVAL tag=it24_b0_plus8 alloc=[104, 24, 48, 48, 8, 8, 8, 8] bytes=256 recall=66.732500

  

SQ_GREEDY_EVAL tag=it24_b1_plus8 alloc=[96, 32, 48, 48, 8, 8, 8, 8] bytes=256 recall=66.625000

  

SQ_GREEDY_EVAL tag=it24_b2_plus8 alloc=[96, 24, 56, 48, 8, 8, 8, 8] bytes=256 recall=66.942500

  

SQ_GREEDY_EVAL tag=it24_b3_plus8 alloc=[96, 24, 48, 56, 8, 8, 8, 8] bytes=256 recall=66.732500

  

SQ_GREEDY_EVAL tag=it24_b4_plus8 alloc=[96, 24, 48, 48, 16, 8, 8, 8] bytes=256 recall=66.697500

  

SQ_GREEDY_EVAL tag=it24_b5_plus8 alloc=[96, 24, 48, 48, 8, 16, 8, 8] bytes=256 recall=66.697500

  

SQ_GREEDY_EVAL tag=it24_b6_plus8 alloc=[96, 24, 48, 48, 8, 8, 16, 8] bytes=256 recall=66.657500

  

SQ_GREEDY_EVAL tag=it24_b7_plus8 alloc=[96, 24, 48, 48, 8, 8, 8, 16] bytes=256 recall=66.647500

  

SQ_GREEDY_EVAL tag=it25_b0_plus8 alloc=[104, 24, 56, 48, 8, 8, 8, 8] bytes=264 recall=67.375000

  

SQ_GREEDY_EVAL tag=it25_b1_plus8 alloc=[96, 32, 56, 48, 8, 8, 8, 8] bytes=264 recall=67.232500

  

SQ_GREEDY_EVAL tag=it25_b2_plus8 alloc=[96, 24, 64, 48, 8, 8, 8, 8] bytes=264 recall=67.412500

  

SQ_GREEDY_EVAL tag=it25_b3_plus8 alloc=[96, 24, 56, 56, 8, 8, 8, 8] bytes=264 recall=67.370000

  

SQ_GREEDY_EVAL tag=it25_b4_plus8 alloc=[96, 24, 56, 48, 16, 8, 8, 8] bytes=264 recall=67.332500

  

SQ_GREEDY_EVAL tag=it25_b5_plus8 alloc=[96, 24, 56, 48, 8, 16, 8, 8] bytes=264 recall=67.450000

  

SQ_GREEDY_EVAL tag=it25_b6_plus8 alloc=[96, 24, 56, 48, 8, 8, 16, 8] bytes=264 recall=67.365000

  

SQ_GREEDY_EVAL tag=it25_b7_plus8 alloc=[96, 24, 56, 48, 8, 8, 8, 16] bytes=264 recall=67.372500

  

SQ_GREEDY_EVAL tag=it26_b0_plus8 alloc=[104, 24, 56, 48, 8, 16, 8, 8] bytes=272 recall=67.817500

  

SQ_GREEDY_EVAL tag=it26_b1_plus8 alloc=[96, 32, 56, 48, 8, 16, 8, 8] bytes=272 recall=67.737500

  

SQ_GREEDY_EVAL tag=it26_b2_plus8 alloc=[96, 24, 64, 48, 8, 16, 8, 8] bytes=272 recall=67.975000

  

SQ_GREEDY_EVAL tag=it26_b3_plus8 alloc=[96, 24, 56, 56, 8, 16, 8, 8] bytes=272 recall=67.865000

  

SQ_GREEDY_EVAL tag=it26_b4_plus8 alloc=[96, 24, 56, 48, 16, 16, 8, 8] bytes=272 recall=67.840000

  

SQ_GREEDY_EVAL tag=it26_b5_plus8 alloc=[96, 24, 56, 48, 8, 24, 8, 8] bytes=272 recall=67.647500

  

SQ_GREEDY_EVAL tag=it26_b6_plus8 alloc=[96, 24, 56, 48, 8, 16, 16, 8] bytes=272 recall=67.820000

  

SQ_GREEDY_EVAL tag=it26_b7_plus8 alloc=[96, 24, 56, 48, 8, 16, 8, 16] bytes=272 recall=67.840000

  

SQ_GREEDY_EVAL tag=it27_b0_plus8 alloc=[104, 24, 64, 48, 8, 16, 8, 8] bytes=280 recall=68.315000

  

SQ_GREEDY_EVAL tag=it27_b1_plus8 alloc=[96, 32, 64, 48, 8, 16, 8, 8] bytes=280 recall=68.292500

  

SQ_GREEDY_EVAL tag=it27_b2_plus8 alloc=[96, 24, 72, 48, 8, 16, 8, 8] bytes=280 recall=68.550000

  

SQ_GREEDY_EVAL tag=it27_b3_plus8 alloc=[96, 24, 64, 56, 8, 16, 8, 8] bytes=280 recall=68.307500

  

SQ_GREEDY_EVAL tag=it27_b4_plus8 alloc=[96, 24, 64, 48, 16, 16, 8, 8] bytes=280 recall=68.360000

  

SQ_GREEDY_EVAL tag=it27_b5_plus8 alloc=[96, 24, 64, 48, 8, 24, 8, 8] bytes=280 recall=68.247500

  

SQ_GREEDY_EVAL tag=it27_b6_plus8 alloc=[96, 24, 64, 48, 8, 16, 16, 8] bytes=280 recall=68.382500

  

SQ_GREEDY_EVAL tag=it27_b7_plus8 alloc=[96, 24, 64, 48, 8, 16, 8, 16] bytes=280 recall=68.325000

  

SQ_GREEDY_EVAL tag=it28_b0_plus8 alloc=[104, 24, 72, 48, 8, 16, 8, 8] bytes=288 recall=68.990000

  

SQ_GREEDY_EVAL tag=it28_b1_plus8 alloc=[96, 32, 72, 48, 8, 16, 8, 8] bytes=288 recall=68.817500

  

SQ_GREEDY_EVAL tag=it28_b2_plus8 alloc=[96, 24, 80, 48, 8, 16, 8, 8] bytes=288 recall=69.157500

  

SQ_GREEDY_EVAL tag=it28_b3_plus8 alloc=[96, 24, 72, 56, 8, 16, 8, 8] bytes=288 recall=68.857500

  

SQ_GREEDY_EVAL tag=it28_b4_plus8 alloc=[96, 24, 72, 48, 16, 16, 8, 8] bytes=288 recall=69.010000

  

SQ_GREEDY_EVAL tag=it28_b5_plus8 alloc=[96, 24, 72, 48, 8, 24, 8, 8] bytes=288 recall=68.807500

  

SQ_GREEDY_EVAL tag=it28_b6_plus8 alloc=[96, 24, 72, 48, 8, 16, 16, 8] bytes=288 recall=68.980000

  

SQ_GREEDY_EVAL tag=it28_b7_plus8 alloc=[96, 24, 72, 48, 8, 16, 8, 16] bytes=288 recall=68.965000

  

SQ_GREEDY_EVAL tag=it29_b0_plus8 alloc=[104, 24, 80, 48, 8, 16, 8, 8] bytes=296 recall=69.575000

  

SQ_GREEDY_EVAL tag=it29_b1_plus8 alloc=[96, 32, 80, 48, 8, 16, 8, 8] bytes=296 recall=69.667500

  

SQ_GREEDY_EVAL tag=it29_b2_plus8 alloc=[96, 24, 88, 48, 8, 16, 8, 8] bytes=296 recall=69.737500

  

SQ_GREEDY_EVAL tag=it29_b3_plus8 alloc=[96, 24, 80, 56, 8, 16, 8, 8] bytes=296 recall=69.527500

  

SQ_GREEDY_EVAL tag=it29_b4_plus8 alloc=[96, 24, 80, 48, 16, 16, 8, 8] bytes=296 recall=69.542500

  

SQ_GREEDY_EVAL tag=it29_b5_plus8 alloc=[96, 24, 80, 48, 8, 24, 8, 8] bytes=296 recall=69.310000

  

SQ_GREEDY_EVAL tag=it29_b6_plus8 alloc=[96, 24, 80, 48, 8, 16, 16, 8] bytes=296 recall=69.692500

  

SQ_GREEDY_EVAL tag=it29_b7_plus8 alloc=[96, 24, 80, 48, 8, 16, 8, 16] bytes=296 recall=69.552500

  

SQ_GREEDY_EVAL tag=it30_b0_plus8 alloc=[104, 24, 88, 48, 8, 16, 8, 8] bytes=304 recall=70.190000

  

SQ_GREEDY_EVAL tag=it30_b1_plus8 alloc=[96, 32, 88, 48, 8, 16, 8, 8] bytes=304 recall=69.920000

  

SQ_GREEDY_EVAL tag=it30_b2_plus8 alloc=[96, 24, 96, 48, 8, 16, 8, 8] bytes=304 recall=70.352500

  

SQ_GREEDY_EVAL tag=it30_b3_plus8 alloc=[96, 24, 88, 56, 8, 16, 8, 8] bytes=304 recall=70.040000

  

SQ_GREEDY_EVAL tag=it30_b4_plus8 alloc=[96, 24, 88, 48, 16, 16, 8, 8] bytes=304 recall=69.982500

  

SQ_GREEDY_EVAL tag=it30_b5_plus8 alloc=[96, 24, 88, 48, 8, 24, 8, 8] bytes=304 recall=69.882500

  

SQ_GREEDY_EVAL tag=it30_b6_plus8 alloc=[96, 24, 88, 48, 8, 16, 16, 8] bytes=304 recall=70.150000

  

SQ_GREEDY_EVAL tag=it30_b7_plus8 alloc=[96, 24, 88, 48, 8, 16, 8, 16] bytes=304 recall=70.112500

  

SQ_GREEDY_EVAL tag=it31_b0_plus8 alloc=[104, 24, 96, 48, 8, 16, 8, 8] bytes=312 recall=70.855000

  

SQ_GREEDY_EVAL tag=it31_b1_plus8 alloc=[96, 32, 96, 48, 8, 16, 8, 8] bytes=312 recall=70.582500

  

SQ_GREEDY_EVAL tag=it31_b2_plus8 alloc=[96, 24, 104, 48, 8, 16, 8, 8] bytes=312 recall=70.552500

  

SQ_GREEDY_EVAL tag=it31_b3_plus8 alloc=[96, 24, 96, 56, 8, 16, 8, 8] bytes=312 recall=70.670000

  

SQ_GREEDY_EVAL tag=it31_b4_plus8 alloc=[96, 24, 96, 48, 16, 16, 8, 8] bytes=312 recall=70.595000

  

SQ_GREEDY_EVAL tag=it31_b5_plus8 alloc=[96, 24, 96, 48, 8, 24, 8, 8] bytes=312 recall=70.502500

  

SQ_GREEDY_EVAL tag=it31_b6_plus8 alloc=[96, 24, 96, 48, 8, 16, 16, 8] bytes=312 recall=70.677500

  

SQ_GREEDY_EVAL tag=it31_b7_plus8 alloc=[96, 24, 96, 48, 8, 16, 8, 16] bytes=312 recall=70.657500

  

SQ_GREEDY_EVAL tag=it32_b0_plus8 alloc=[112, 24, 96, 48, 8, 16, 8, 8] bytes=320 recall=71.145000

  

SQ_GREEDY_EVAL tag=it32_b1_plus8 alloc=[104, 32, 96, 48, 8, 16, 8, 8] bytes=320 recall=70.872500

  

SQ_GREEDY_EVAL tag=it32_b2_plus8 alloc=[104, 24, 104, 48, 8, 16, 8, 8] bytes=320 recall=70.962500

  

SQ_GREEDY_EVAL tag=it32_b3_plus8 alloc=[104, 24, 96, 56, 8, 16, 8, 8] bytes=320 recall=71.077500

  

SQ_GREEDY_EVAL tag=it32_b4_plus8 alloc=[104, 24, 96, 48, 16, 16, 8, 8] bytes=320 recall=71.065000

  

SQ_GREEDY_EVAL tag=it32_b5_plus8 alloc=[104, 24, 96, 48, 8, 24, 8, 8] bytes=320 recall=71.000000

  

SQ_GREEDY_EVAL tag=it32_b6_plus8 alloc=[104, 24, 96, 48, 8, 16, 16, 8] bytes=320 recall=71.200000

  

SQ_GREEDY_EVAL tag=it32_b7_plus8 alloc=[104, 24, 96, 48, 8, 16, 8, 16] bytes=320 recall=71.077500

  

SQ_GREEDY_EVAL tag=it33_b0_plus8 alloc=[112, 24, 96, 48, 8, 16, 16, 8] bytes=328 recall=71.550000

  

SQ_GREEDY_EVAL tag=it33_b1_plus8 alloc=[104, 32, 96, 48, 8, 16, 16, 8] bytes=328 recall=71.362500

  

SQ_GREEDY_EVAL tag=it33_b2_plus8 alloc=[104, 24, 104, 48, 8, 16, 16, 8] bytes=328 recall=71.250000

  

SQ_GREEDY_EVAL tag=it33_b3_plus8 alloc=[104, 24, 96, 56, 8, 16, 16, 8] bytes=328 recall=71.525000

  

SQ_GREEDY_EVAL tag=it33_b4_plus8 alloc=[104, 24, 96, 48, 16, 16, 16, 8] bytes=328 recall=71.435000

  

SQ_GREEDY_EVAL tag=it33_b5_plus8 alloc=[104, 24, 96, 48, 8, 24, 16, 8] bytes=328 recall=71.402500

  

SQ_GREEDY_EVAL tag=it33_b6_plus8 alloc=[104, 24, 96, 48, 8, 16, 24, 8] bytes=328 recall=71.515000

  

SQ_GREEDY_EVAL tag=it33_b7_plus8 alloc=[104, 24, 96, 48, 8, 16, 16, 16] bytes=328 recall=71.510000

  

SQ_GREEDY_EVAL tag=it34_b0_plus8 alloc=[120, 24, 96, 48, 8, 16, 16, 8] bytes=336 recall=71.907500

  

SQ_GREEDY_EVAL tag=it34_b1_plus8 alloc=[112, 32, 96, 48, 8, 16, 16, 8] bytes=336 recall=71.750000

  

SQ_GREEDY_EVAL tag=it34_b2_plus8 alloc=[112, 24, 104, 48, 8, 16, 16, 8] bytes=336 recall=71.705000

  

SQ_GREEDY_EVAL tag=it34_b3_plus8 alloc=[112, 24, 96, 56, 8, 16, 16, 8] bytes=336 recall=71.907500

  

SQ_GREEDY_EVAL tag=it34_b4_plus8 alloc=[112, 24, 96, 48, 16, 16, 16, 8] bytes=336 recall=71.775000

  

SQ_GREEDY_EVAL tag=it34_b5_plus8 alloc=[112, 24, 96, 48, 8, 24, 16, 8] bytes=336 recall=71.772500

  

SQ_GREEDY_EVAL tag=it34_b6_plus8 alloc=[112, 24, 96, 48, 8, 16, 24, 8] bytes=336 recall=71.910000

  

SQ_GREEDY_EVAL tag=it34_b7_plus8 alloc=[112, 24, 96, 48, 8, 16, 16, 16] bytes=336 recall=71.807500

  

SQ_GREEDY_EVAL tag=it35_b0_plus8 alloc=[120, 24, 96, 48, 8, 16, 24, 8] bytes=344 recall=72.137500

  

SQ_GREEDY_EVAL tag=it35_b1_plus8 alloc=[112, 32, 96, 48, 8, 16, 24, 8] bytes=344 recall=72.077500

  

SQ_GREEDY_EVAL tag=it35_b2_plus8 alloc=[112, 24, 104, 48, 8, 16, 24, 8] bytes=344 recall=72.070000

  

SQ_GREEDY_EVAL tag=it35_b3_plus8 alloc=[112, 24, 96, 56, 8, 16, 24, 8] bytes=344 recall=72.207500

  

SQ_GREEDY_EVAL tag=it35_b4_plus8 alloc=[112, 24, 96, 48, 16, 16, 24, 8] bytes=344 recall=72.277500

  

SQ_GREEDY_EVAL tag=it35_b5_plus8 alloc=[112, 24, 96, 48, 8, 24, 24, 8] bytes=344 recall=72.230000

  

SQ_GREEDY_EVAL tag=it35_b6_plus8 alloc=[112, 24, 96, 48, 8, 16, 32, 8] bytes=344 recall=72.090000

  

SQ_GREEDY_EVAL tag=it35_b7_plus8 alloc=[112, 24, 96, 48, 8, 16, 24, 16] bytes=344 recall=72.225000

  

SQ_GREEDY_EVAL tag=it36_b0_plus8 alloc=[120, 24, 96, 48, 16, 16, 24, 8] bytes=352 recall=72.510000

  

SQ_GREEDY_EVAL tag=it36_b1_plus8 alloc=[112, 32, 96, 48, 16, 16, 24, 8] bytes=352 recall=72.437500

  

SQ_GREEDY_EVAL tag=it36_b2_plus8 alloc=[112, 24, 104, 48, 16, 16, 24, 8] bytes=352 recall=72.407500

  

SQ_GREEDY_EVAL tag=it36_b3_plus8 alloc=[112, 24, 96, 56, 16, 16, 24, 8] bytes=352 recall=72.515000

  

SQ_GREEDY_EVAL tag=it36_b4_plus8 alloc=[112, 24, 96, 48, 24, 16, 24, 8] bytes=352 recall=72.432500

  

SQ_GREEDY_EVAL tag=it36_b5_plus8 alloc=[112, 24, 96, 48, 16, 24, 24, 8] bytes=352 recall=72.460000

  

SQ_GREEDY_EVAL tag=it36_b6_plus8 alloc=[112, 24, 96, 48, 16, 16, 32, 8] bytes=352 recall=72.395000

  

SQ_GREEDY_EVAL tag=it36_b7_plus8 alloc=[112, 24, 96, 48, 16, 16, 24, 16] bytes=352 recall=72.482500

  

SQ_GREEDY_EVAL tag=it37_b0_plus8 alloc=[120, 24, 96, 56, 16, 16, 24, 8] bytes=360 recall=72.912500

  

SQ_GREEDY_EVAL tag=it37_b1_plus8 alloc=[112, 32, 96, 56, 16, 16, 24, 8] bytes=360 recall=72.777500

  

SQ_GREEDY_EVAL tag=it37_b2_plus8 alloc=[112, 24, 104, 56, 16, 16, 24, 8] bytes=360 recall=72.662500

  

SQ_GREEDY_EVAL tag=it37_b3_plus8 alloc=[112, 24, 96, 64, 16, 16, 24, 8] bytes=360 recall=72.932500

  

SQ_GREEDY_EVAL tag=it37_b4_plus8 alloc=[112, 24, 96, 56, 24, 16, 24, 8] bytes=360 recall=72.725000

  

SQ_GREEDY_EVAL tag=it37_b5_plus8 alloc=[112, 24, 96, 56, 16, 24, 24, 8] bytes=360 recall=72.850000

  

SQ_GREEDY_EVAL tag=it37_b6_plus8 alloc=[112, 24, 96, 56, 16, 16, 32, 8] bytes=360 recall=72.615000

  

SQ_GREEDY_EVAL tag=it37_b7_plus8 alloc=[112, 24, 96, 56, 16, 16, 24, 16] bytes=360 recall=72.732500

  

SQ_GREEDY_EVAL tag=it38_b0_plus8 alloc=[120, 24, 96, 64, 16, 16, 24, 8] bytes=368 recall=73.392500

  

SQ_GREEDY_EVAL tag=it38_b1_plus8 alloc=[112, 32, 96, 64, 16, 16, 24, 8] bytes=368 recall=73.292500

  

SQ_GREEDY_EVAL tag=it38_b2_plus8 alloc=[112, 24, 104, 64, 16, 16, 24, 8] bytes=368 recall=73.090000

  

SQ_GREEDY_EVAL tag=it38_b3_plus8 alloc=[112, 24, 96, 72, 16, 16, 24, 8] bytes=368 recall=73.267500

  

SQ_GREEDY_EVAL tag=it38_b4_plus8 alloc=[112, 24, 96, 64, 24, 16, 24, 8] bytes=368 recall=73.187500

  

SQ_GREEDY_EVAL tag=it38_b5_plus8 alloc=[112, 24, 96, 64, 16, 24, 24, 8] bytes=368 recall=73.262500

  

SQ_GREEDY_EVAL tag=it38_b6_plus8 alloc=[112, 24, 96, 64, 16, 16, 32, 8] bytes=368 recall=73.160000

  

SQ_GREEDY_EVAL tag=it38_b7_plus8 alloc=[112, 24, 96, 64, 16, 16, 24, 16] bytes=368 recall=73.205000

  

SQ_GREEDY_EVAL tag=it39_b0_plus8 alloc=[128, 24, 96, 64, 16, 16, 24, 8] bytes=376 recall=73.550000

  

SQ_GREEDY_EVAL tag=it39_b1_plus8 alloc=[120, 32, 96, 64, 16, 16, 24, 8] bytes=376 recall=73.515000

  

SQ_GREEDY_EVAL tag=it39_b2_plus8 alloc=[120, 24, 104, 64, 16, 16, 24, 8] bytes=376 recall=73.572500

  

SQ_GREEDY_EVAL tag=it39_b3_plus8 alloc=[120, 24, 96, 72, 16, 16, 24, 8] bytes=376 recall=73.672500

  

SQ_GREEDY_EVAL tag=it39_b4_plus8 alloc=[120, 24, 96, 64, 24, 16, 24, 8] bytes=376 recall=73.672500

  

SQ_GREEDY_EVAL tag=it39_b5_plus8 alloc=[120, 24, 96, 64, 16, 24, 24, 8] bytes=376 recall=73.510000

  

SQ_GREEDY_EVAL tag=it39_b6_plus8 alloc=[120, 24, 96, 64, 16, 16, 32, 8] bytes=376 recall=73.482500

  

SQ_GREEDY_EVAL tag=it39_b7_plus8 alloc=[120, 24, 96, 64, 16, 16, 24, 16] bytes=376 recall=73.622500

  

SQ_GREEDY_EVAL tag=it40_b0_plus8 alloc=[128, 24, 96, 64, 24, 16, 24, 8] bytes=384 recall=73.692500

  

SQ_GREEDY_EVAL tag=it40_b1_plus8 alloc=[120, 32, 96, 64, 24, 16, 24, 8] bytes=384 recall=73.767500

  

SQ_GREEDY_EVAL tag=it40_b2_plus8 alloc=[120, 24, 104, 64, 24, 16, 24, 8] bytes=384 recall=73.822500

  

SQ_GREEDY_EVAL tag=it40_b3_plus8 alloc=[120, 24, 96, 72, 24, 16, 24, 8] bytes=384 recall=73.890000

  

SQ_GREEDY_EVAL tag=it40_b4_plus8 alloc=[120, 24, 96, 64, 32, 16, 24, 8] bytes=384 recall=73.915000

  

SQ_GREEDY_EVAL tag=it40_b5_plus8 alloc=[120, 24, 96, 64, 24, 24, 24, 8] bytes=384 recall=73.827500

  

SQ_GREEDY_EVAL tag=it40_b6_plus8 alloc=[120, 24, 96, 64, 24, 16, 32, 8] bytes=384 recall=73.710000

  

SQ_GREEDY_EVAL tag=it40_b7_plus8 alloc=[120, 24, 96, 64, 24, 16, 24, 16] bytes=384 recall=73.775000



### MSMarco Openai text large 3, SQ:
#### Uniform
SQ sweep completed!
Results directory: /tmp/sq_sweep_1779868460

Summary of SQ recall results:

Bytes,Recall

64,35.5552

96,45.6681

128,53.2361

160,58.2966

192,62.0351

224,65.0835

256,67.9666

288,69.8586

320,72.1325

352,73.5467

384,74.9596

#### Variable

SQ_GREEDY_EVAL tag=init alloc=[8, 8, 8, 8, 8, 8, 8, 8] bytes=64 recall=35.555200

  

SQ_GREEDY_EVAL tag=it1_b0_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 8] bytes=72 recall=39.534200

  

SQ_GREEDY_EVAL tag=it1_b1_plus8 alloc=[8, 16, 8, 8, 8, 8, 8, 8] bytes=72 recall=39.334000

  

SQ_GREEDY_EVAL tag=it1_b2_plus8 alloc=[8, 8, 16, 8, 8, 8, 8, 8] bytes=72 recall=38.827900

  

SQ_GREEDY_EVAL tag=it1_b3_plus8 alloc=[8, 8, 8, 16, 8, 8, 8, 8] bytes=72 recall=38.674400

  

SQ_GREEDY_EVAL tag=it1_b4_plus8 alloc=[8, 8, 8, 8, 16, 8, 8, 8] bytes=72 recall=38.240800

  

SQ_GREEDY_EVAL tag=it1_b5_plus8 alloc=[8, 8, 8, 8, 8, 16, 8, 8] bytes=72 recall=38.413300

  

SQ_GREEDY_EVAL tag=it1_b6_plus8 alloc=[8, 8, 8, 8, 8, 8, 16, 8] bytes=72 recall=38.494600

  

SQ_GREEDY_EVAL tag=it1_b7_plus8 alloc=[8, 8, 8, 8, 8, 8, 8, 16] bytes=72 recall=38.359000

  

SQ_GREEDY_EVAL tag=it2_b0_plus8 alloc=[24, 8, 8, 8, 8, 8, 8, 8] bytes=80 recall=42.365900

  

SQ_GREEDY_EVAL tag=it2_b1_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 8] bytes=80 recall=42.776500

  

SQ_GREEDY_EVAL tag=it2_b2_plus8 alloc=[16, 8, 16, 8, 8, 8, 8, 8] bytes=80 recall=42.363000

  

SQ_GREEDY_EVAL tag=it2_b3_plus8 alloc=[16, 8, 8, 16, 8, 8, 8, 8] bytes=80 recall=42.132100

  

SQ_GREEDY_EVAL tag=it2_b4_plus8 alloc=[16, 8, 8, 8, 16, 8, 8, 8] bytes=80 recall=41.713300

  

SQ_GREEDY_EVAL tag=it2_b5_plus8 alloc=[16, 8, 8, 8, 8, 16, 8, 8] bytes=80 recall=41.821100

  

SQ_GREEDY_EVAL tag=it2_b6_plus8 alloc=[16, 8, 8, 8, 8, 8, 16, 8] bytes=80 recall=41.925500

  

SQ_GREEDY_EVAL tag=it2_b7_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 16] bytes=80 recall=41.771300

  

SQ_GREEDY_EVAL tag=it3_b0_plus8 alloc=[24, 16, 8, 8, 8, 8, 8, 8] bytes=88 recall=45.345300

  

SQ_GREEDY_EVAL tag=it3_b1_plus8 alloc=[16, 24, 8, 8, 8, 8, 8, 8] bytes=88 recall=45.512000

  

SQ_GREEDY_EVAL tag=it3_b2_plus8 alloc=[16, 16, 16, 8, 8, 8, 8, 8] bytes=88 recall=45.336200

  

SQ_GREEDY_EVAL tag=it3_b3_plus8 alloc=[16, 16, 8, 16, 8, 8, 8, 8] bytes=88 recall=45.044600

  

SQ_GREEDY_EVAL tag=it3_b4_plus8 alloc=[16, 16, 8, 8, 16, 8, 8, 8] bytes=88 recall=44.707300

  

SQ_GREEDY_EVAL tag=it3_b5_plus8 alloc=[16, 16, 8, 8, 8, 16, 8, 8] bytes=88 recall=44.789100

  

SQ_GREEDY_EVAL tag=it3_b6_plus8 alloc=[16, 16, 8, 8, 8, 8, 16, 8] bytes=88 recall=44.849000

  

SQ_GREEDY_EVAL tag=it3_b7_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 16] bytes=88 recall=44.768800

  

SQ_GREEDY_EVAL tag=it4_b0_plus8 alloc=[24, 24, 8, 8, 8, 8, 8, 8] bytes=96 recall=47.916200

  

SQ_GREEDY_EVAL tag=it4_b1_plus8 alloc=[16, 32, 8, 8, 8, 8, 8, 8] bytes=96 recall=48.141400

  

SQ_GREEDY_EVAL tag=it4_b2_plus8 alloc=[16, 24, 16, 8, 8, 8, 8, 8] bytes=96 recall=47.783000

  

SQ_GREEDY_EVAL tag=it4_b3_plus8 alloc=[16, 24, 8, 16, 8, 8, 8, 8] bytes=96 recall=47.573500

  

SQ_GREEDY_EVAL tag=it4_b4_plus8 alloc=[16, 24, 8, 8, 16, 8, 8, 8] bytes=96 recall=47.203300

  

SQ_GREEDY_EVAL tag=it4_b5_plus8 alloc=[16, 24, 8, 8, 8, 16, 8, 8] bytes=96 recall=47.249700

  

SQ_GREEDY_EVAL tag=it4_b6_plus8 alloc=[16, 24, 8, 8, 8, 8, 16, 8] bytes=96 recall=47.300900

  

SQ_GREEDY_EVAL tag=it4_b7_plus8 alloc=[16, 24, 8, 8, 8, 8, 8, 16] bytes=96 recall=47.234000

  

SQ_GREEDY_EVAL tag=it5_b0_plus8 alloc=[24, 32, 8, 8, 8, 8, 8, 8] bytes=104 recall=50.223100

  

SQ_GREEDY_EVAL tag=it5_b1_plus8 alloc=[16, 40, 8, 8, 8, 8, 8, 8] bytes=104 recall=50.538300

  

SQ_GREEDY_EVAL tag=it5_b2_plus8 alloc=[16, 32, 16, 8, 8, 8, 8, 8] bytes=104 recall=50.180900

  

SQ_GREEDY_EVAL tag=it5_b3_plus8 alloc=[16, 32, 8, 16, 8, 8, 8, 8] bytes=104 recall=49.954700

  

SQ_GREEDY_EVAL tag=it5_b4_plus8 alloc=[16, 32, 8, 8, 16, 8, 8, 8] bytes=104 recall=49.620300

  

SQ_GREEDY_EVAL tag=it5_b5_plus8 alloc=[16, 32, 8, 8, 8, 16, 8, 8] bytes=104 recall=49.698700

  

SQ_GREEDY_EVAL tag=it5_b6_plus8 alloc=[16, 32, 8, 8, 8, 8, 16, 8] bytes=104 recall=49.742000

  

SQ_GREEDY_EVAL tag=it5_b7_plus8 alloc=[16, 32, 8, 8, 8, 8, 8, 16] bytes=104 recall=49.684700

  

SQ_GREEDY_EVAL tag=it6_b0_plus8 alloc=[24, 40, 8, 8, 8, 8, 8, 8] bytes=112 recall=52.374500

  

SQ_GREEDY_EVAL tag=it6_b1_plus8 alloc=[16, 48, 8, 8, 8, 8, 8, 8] bytes=112 recall=52.494000

  

SQ_GREEDY_EVAL tag=it6_b2_plus8 alloc=[16, 40, 16, 8, 8, 8, 8, 8] bytes=112 recall=52.275200

  

SQ_GREEDY_EVAL tag=it6_b3_plus8 alloc=[16, 40, 8, 16, 8, 8, 8, 8] bytes=112 recall=52.125900

  

SQ_GREEDY_EVAL tag=it6_b4_plus8 alloc=[16, 40, 8, 8, 16, 8, 8, 8] bytes=112 recall=51.820900

  

SQ_GREEDY_EVAL tag=it6_b5_plus8 alloc=[16, 40, 8, 8, 8, 16, 8, 8] bytes=112 recall=51.883100

  

SQ_GREEDY_EVAL tag=it6_b6_plus8 alloc=[16, 40, 8, 8, 8, 8, 16, 8] bytes=112 recall=51.929500

  

SQ_GREEDY_EVAL tag=it6_b7_plus8 alloc=[16, 40, 8, 8, 8, 8, 8, 16] bytes=112 recall=51.893600

  

SQ_GREEDY_EVAL tag=it7_b0_plus8 alloc=[24, 48, 8, 8, 8, 8, 8, 8] bytes=120 recall=54.244400

  

SQ_GREEDY_EVAL tag=it7_b1_plus8 alloc=[16, 56, 8, 8, 8, 8, 8, 8] bytes=120 recall=54.519900

  

SQ_GREEDY_EVAL tag=it7_b2_plus8 alloc=[16, 48, 16, 8, 8, 8, 8, 8] bytes=120 recall=54.100400

  

SQ_GREEDY_EVAL tag=it7_b3_plus8 alloc=[16, 48, 8, 16, 8, 8, 8, 8] bytes=120 recall=53.960200

  

SQ_GREEDY_EVAL tag=it7_b4_plus8 alloc=[16, 48, 8, 8, 16, 8, 8, 8] bytes=120 recall=53.679200

  

SQ_GREEDY_EVAL tag=it7_b5_plus8 alloc=[16, 48, 8, 8, 8, 16, 8, 8] bytes=120 recall=53.733500

  

SQ_GREEDY_EVAL tag=it7_b6_plus8 alloc=[16, 48, 8, 8, 8, 8, 16, 8] bytes=120 recall=53.793300

  

SQ_GREEDY_EVAL tag=it7_b7_plus8 alloc=[16, 48, 8, 8, 8, 8, 8, 16] bytes=120 recall=53.711000

  

SQ_GREEDY_EVAL tag=it8_b0_plus8 alloc=[24, 56, 8, 8, 8, 8, 8, 8] bytes=128 recall=56.173500

  

SQ_GREEDY_EVAL tag=it8_b1_plus8 alloc=[16, 64, 8, 8, 8, 8, 8, 8] bytes=128 recall=56.014800

  

SQ_GREEDY_EVAL tag=it8_b2_plus8 alloc=[16, 56, 16, 8, 8, 8, 8, 8] bytes=128 recall=56.035100

  

SQ_GREEDY_EVAL tag=it8_b3_plus8 alloc=[16, 56, 8, 16, 8, 8, 8, 8] bytes=128 recall=55.874900

  

SQ_GREEDY_EVAL tag=it8_b4_plus8 alloc=[16, 56, 8, 8, 16, 8, 8, 8] bytes=128 recall=55.609300

  

SQ_GREEDY_EVAL tag=it8_b5_plus8 alloc=[16, 56, 8, 8, 8, 16, 8, 8] bytes=128 recall=55.653000

  

SQ_GREEDY_EVAL tag=it8_b6_plus8 alloc=[16, 56, 8, 8, 8, 8, 16, 8] bytes=128 recall=55.683500

  

SQ_GREEDY_EVAL tag=it8_b7_plus8 alloc=[16, 56, 8, 8, 8, 8, 8, 16] bytes=128 recall=55.593600

  

SQ_GREEDY_EVAL tag=it9_b0_plus8 alloc=[32, 56, 8, 8, 8, 8, 8, 8] bytes=136 recall=57.866300

  

SQ_GREEDY_EVAL tag=it9_b1_plus8 alloc=[24, 64, 8, 8, 8, 8, 8, 8] bytes=136 recall=57.509000

  

SQ_GREEDY_EVAL tag=it9_b2_plus8 alloc=[24, 56, 16, 8, 8, 8, 8, 8] bytes=136 recall=57.470500

  

SQ_GREEDY_EVAL tag=it9_b3_plus8 alloc=[24, 56, 8, 16, 8, 8, 8, 8] bytes=136 recall=57.369300

  

SQ_GREEDY_EVAL tag=it9_b4_plus8 alloc=[24, 56, 8, 8, 16, 8, 8, 8] bytes=136 recall=57.162900

  

SQ_GREEDY_EVAL tag=it9_b5_plus8 alloc=[24, 56, 8, 8, 8, 16, 8, 8] bytes=136 recall=57.177900

  

SQ_GREEDY_EVAL tag=it9_b6_plus8 alloc=[24, 56, 8, 8, 8, 8, 16, 8] bytes=136 recall=57.202900

  

SQ_GREEDY_EVAL tag=it9_b7_plus8 alloc=[24, 56, 8, 8, 8, 8, 8, 16] bytes=136 recall=57.111300

  

SQ_GREEDY_EVAL tag=it10_b0_plus8 alloc=[40, 56, 8, 8, 8, 8, 8, 8] bytes=144 recall=59.356400

  

SQ_GREEDY_EVAL tag=it10_b1_plus8 alloc=[32, 64, 8, 8, 8, 8, 8, 8] bytes=144 recall=59.087500

  

SQ_GREEDY_EVAL tag=it10_b2_plus8 alloc=[32, 56, 16, 8, 8, 8, 8, 8] bytes=144 recall=59.102100

  

SQ_GREEDY_EVAL tag=it10_b3_plus8 alloc=[32, 56, 8, 16, 8, 8, 8, 8] bytes=144 recall=59.000000

  

SQ_GREEDY_EVAL tag=it10_b4_plus8 alloc=[32, 56, 8, 8, 16, 8, 8, 8] bytes=144 recall=58.703400

  

SQ_GREEDY_EVAL tag=it10_b5_plus8 alloc=[32, 56, 8, 8, 8, 16, 8, 8] bytes=144 recall=58.767200

  

SQ_GREEDY_EVAL tag=it10_b6_plus8 alloc=[32, 56, 8, 8, 8, 8, 16, 8] bytes=144 recall=58.796600

  

SQ_GREEDY_EVAL tag=it10_b7_plus8 alloc=[32, 56, 8, 8, 8, 8, 8, 16] bytes=144 recall=58.743800

  

SQ_GREEDY_EVAL tag=it11_b0_plus8 alloc=[48, 56, 8, 8, 8, 8, 8, 8] bytes=152 recall=60.552000

  

SQ_GREEDY_EVAL tag=it11_b1_plus8 alloc=[40, 64, 8, 8, 8, 8, 8, 8] bytes=152 recall=60.470900

  

SQ_GREEDY_EVAL tag=it11_b2_plus8 alloc=[40, 56, 16, 8, 8, 8, 8, 8] bytes=152 recall=60.428800

  

SQ_GREEDY_EVAL tag=it11_b3_plus8 alloc=[40, 56, 8, 16, 8, 8, 8, 8] bytes=152 recall=60.380500

  

SQ_GREEDY_EVAL tag=it11_b4_plus8 alloc=[40, 56, 8, 8, 16, 8, 8, 8] bytes=152 recall=60.155700

  

SQ_GREEDY_EVAL tag=it11_b5_plus8 alloc=[40, 56, 8, 8, 8, 16, 8, 8] bytes=152 recall=60.191300

  

SQ_GREEDY_EVAL tag=it11_b6_plus8 alloc=[40, 56, 8, 8, 8, 8, 16, 8] bytes=152 recall=60.216600

  

SQ_GREEDY_EVAL tag=it11_b7_plus8 alloc=[40, 56, 8, 8, 8, 8, 8, 16] bytes=152 recall=60.140700

  

SQ_GREEDY_EVAL tag=it12_b0_plus8 alloc=[56, 56, 8, 8, 8, 8, 8, 8] bytes=160 recall=62.175600

  

SQ_GREEDY_EVAL tag=it12_b1_plus8 alloc=[48, 64, 8, 8, 8, 8, 8, 8] bytes=160 recall=61.560700

  

SQ_GREEDY_EVAL tag=it12_b2_plus8 alloc=[48, 56, 16, 8, 8, 8, 8, 8] bytes=160 recall=61.480500

  

SQ_GREEDY_EVAL tag=it12_b3_plus8 alloc=[48, 56, 8, 16, 8, 8, 8, 8] bytes=160 recall=61.516600

  

SQ_GREEDY_EVAL tag=it12_b4_plus8 alloc=[48, 56, 8, 8, 16, 8, 8, 8] bytes=160 recall=61.273500

  

SQ_GREEDY_EVAL tag=it12_b5_plus8 alloc=[48, 56, 8, 8, 8, 16, 8, 8] bytes=160 recall=61.314900

  

SQ_GREEDY_EVAL tag=it12_b6_plus8 alloc=[48, 56, 8, 8, 8, 8, 16, 8] bytes=160 recall=61.332800

  

SQ_GREEDY_EVAL tag=it12_b7_plus8 alloc=[48, 56, 8, 8, 8, 8, 8, 16] bytes=160 recall=61.287100

  

SQ_GREEDY_EVAL tag=it13_b0_plus8 alloc=[64, 56, 8, 8, 8, 8, 8, 8] bytes=168 recall=63.314000

  

SQ_GREEDY_EVAL tag=it13_b1_plus8 alloc=[56, 64, 8, 8, 8, 8, 8, 8] bytes=168 recall=63.161200

  

SQ_GREEDY_EVAL tag=it13_b2_plus8 alloc=[56, 56, 16, 8, 8, 8, 8, 8] bytes=168 recall=63.099900

  

SQ_GREEDY_EVAL tag=it13_b3_plus8 alloc=[56, 56, 8, 16, 8, 8, 8, 8] bytes=168 recall=63.047900

  

SQ_GREEDY_EVAL tag=it13_b4_plus8 alloc=[56, 56, 8, 8, 16, 8, 8, 8] bytes=168 recall=62.829500

  

SQ_GREEDY_EVAL tag=it13_b5_plus8 alloc=[56, 56, 8, 8, 8, 16, 8, 8] bytes=168 recall=62.852000

  

SQ_GREEDY_EVAL tag=it13_b6_plus8 alloc=[56, 56, 8, 8, 8, 8, 16, 8] bytes=168 recall=62.874500

  

SQ_GREEDY_EVAL tag=it13_b7_plus8 alloc=[56, 56, 8, 8, 8, 8, 8, 16] bytes=168 recall=62.867200

  

SQ_GREEDY_EVAL tag=it14_b0_plus8 alloc=[72, 56, 8, 8, 8, 8, 8, 8] bytes=176 recall=64.329200

  

SQ_GREEDY_EVAL tag=it14_b1_plus8 alloc=[64, 64, 8, 8, 8, 8, 8, 8] bytes=176 recall=64.225500

  

SQ_GREEDY_EVAL tag=it14_b2_plus8 alloc=[64, 56, 16, 8, 8, 8, 8, 8] bytes=176 recall=64.178100

  

SQ_GREEDY_EVAL tag=it14_b3_plus8 alloc=[64, 56, 8, 16, 8, 8, 8, 8] bytes=176 recall=64.116500

  

SQ_GREEDY_EVAL tag=it14_b4_plus8 alloc=[64, 56, 8, 8, 16, 8, 8, 8] bytes=176 recall=63.916600

  

SQ_GREEDY_EVAL tag=it14_b5_plus8 alloc=[64, 56, 8, 8, 8, 16, 8, 8] bytes=176 recall=63.950700

  

SQ_GREEDY_EVAL tag=it14_b6_plus8 alloc=[64, 56, 8, 8, 8, 8, 16, 8] bytes=176 recall=63.984500

  

SQ_GREEDY_EVAL tag=it14_b7_plus8 alloc=[64, 56, 8, 8, 8, 8, 8, 16] bytes=176 recall=63.949400

  

SQ_GREEDY_EVAL tag=it15_b0_plus8 alloc=[80, 56, 8, 8, 8, 8, 8, 8] bytes=184 recall=65.481700

  

SQ_GREEDY_EVAL tag=it15_b1_plus8 alloc=[72, 64, 8, 8, 8, 8, 8, 8] bytes=184 recall=65.164800

  

SQ_GREEDY_EVAL tag=it15_b2_plus8 alloc=[72, 56, 16, 8, 8, 8, 8, 8] bytes=184 recall=65.103900

  

SQ_GREEDY_EVAL tag=it15_b3_plus8 alloc=[72, 56, 8, 16, 8, 8, 8, 8] bytes=184 recall=65.094600

  

SQ_GREEDY_EVAL tag=it15_b4_plus8 alloc=[72, 56, 8, 8, 16, 8, 8, 8] bytes=184 recall=64.900000

  

SQ_GREEDY_EVAL tag=it15_b5_plus8 alloc=[72, 56, 8, 8, 8, 16, 8, 8] bytes=184 recall=64.931400

  

SQ_GREEDY_EVAL tag=it15_b6_plus8 alloc=[72, 56, 8, 8, 8, 8, 16, 8] bytes=184 recall=64.950900

  

SQ_GREEDY_EVAL tag=it15_b7_plus8 alloc=[72, 56, 8, 8, 8, 8, 8, 16] bytes=184 recall=64.878400

  

SQ_GREEDY_EVAL tag=it16_b0_plus8 alloc=[88, 56, 8, 8, 8, 8, 8, 8] bytes=192 recall=66.549000

  

SQ_GREEDY_EVAL tag=it16_b1_plus8 alloc=[80, 64, 8, 8, 8, 8, 8, 8] bytes=192 recall=66.263900

  

SQ_GREEDY_EVAL tag=it16_b2_plus8 alloc=[80, 56, 16, 8, 8, 8, 8, 8] bytes=192 recall=66.185800

  

SQ_GREEDY_EVAL tag=it16_b3_plus8 alloc=[80, 56, 8, 16, 8, 8, 8, 8] bytes=192 recall=66.193100

  

SQ_GREEDY_EVAL tag=it16_b4_plus8 alloc=[80, 56, 8, 8, 16, 8, 8, 8] bytes=192 recall=66.026500

  

SQ_GREEDY_EVAL tag=it16_b5_plus8 alloc=[80, 56, 8, 8, 8, 16, 8, 8] bytes=192 recall=66.038800

  

SQ_GREEDY_EVAL tag=it16_b6_plus8 alloc=[80, 56, 8, 8, 8, 8, 16, 8] bytes=192 recall=66.049300

  

SQ_GREEDY_EVAL tag=it16_b7_plus8 alloc=[80, 56, 8, 8, 8, 8, 8, 16] bytes=192 recall=66.002600

  

SQ_GREEDY_EVAL tag=it17_b0_plus8 alloc=[96, 56, 8, 8, 8, 8, 8, 8] bytes=200 recall=67.572100

  

SQ_GREEDY_EVAL tag=it17_b1_plus8 alloc=[88, 64, 8, 8, 8, 8, 8, 8] bytes=200 recall=67.291800

  

SQ_GREEDY_EVAL tag=it17_b2_plus8 alloc=[88, 56, 16, 8, 8, 8, 8, 8] bytes=200 recall=67.218100

  

SQ_GREEDY_EVAL tag=it17_b3_plus8 alloc=[88, 56, 8, 16, 8, 8, 8, 8] bytes=200 recall=67.225400

  

SQ_GREEDY_EVAL tag=it17_b4_plus8 alloc=[88, 56, 8, 8, 16, 8, 8, 8] bytes=200 recall=67.041100

  

SQ_GREEDY_EVAL tag=it17_b5_plus8 alloc=[88, 56, 8, 8, 8, 16, 8, 8] bytes=200 recall=67.100400

  

SQ_GREEDY_EVAL tag=it17_b6_plus8 alloc=[88, 56, 8, 8, 8, 8, 16, 8] bytes=200 recall=67.078800

  

SQ_GREEDY_EVAL tag=it17_b7_plus8 alloc=[88, 56, 8, 8, 8, 8, 8, 16] bytes=200 recall=67.035400

  

SQ_GREEDY_EVAL tag=it18_b0_plus8 alloc=[104, 56, 8, 8, 8, 8, 8, 8] bytes=208 recall=68.012200

  

SQ_GREEDY_EVAL tag=it18_b1_plus8 alloc=[96, 64, 8, 8, 8, 8, 8, 8] bytes=208 recall=68.226600

  

SQ_GREEDY_EVAL tag=it18_b2_plus8 alloc=[96, 56, 16, 8, 8, 8, 8, 8] bytes=208 recall=68.208500

  

SQ_GREEDY_EVAL tag=it18_b3_plus8 alloc=[96, 56, 8, 16, 8, 8, 8, 8] bytes=208 recall=68.193300

  

SQ_GREEDY_EVAL tag=it18_b4_plus8 alloc=[96, 56, 8, 8, 16, 8, 8, 8] bytes=208 recall=68.044000

  

SQ_GREEDY_EVAL tag=it18_b5_plus8 alloc=[96, 56, 8, 8, 8, 16, 8, 8] bytes=208 recall=68.077800

  

SQ_GREEDY_EVAL tag=it18_b6_plus8 alloc=[96, 56, 8, 8, 8, 8, 16, 8] bytes=208 recall=68.067000

  

SQ_GREEDY_EVAL tag=it18_b7_plus8 alloc=[96, 56, 8, 8, 8, 8, 8, 16] bytes=208 recall=68.042600

  

SQ_GREEDY_EVAL tag=it19_b0_plus8 alloc=[104, 64, 8, 8, 8, 8, 8, 8] bytes=216 recall=68.664900

  

SQ_GREEDY_EVAL tag=it19_b1_plus8 alloc=[96, 72, 8, 8, 8, 8, 8, 8] bytes=216 recall=69.160300

  

SQ_GREEDY_EVAL tag=it19_b2_plus8 alloc=[96, 64, 16, 8, 8, 8, 8, 8] bytes=216 recall=68.824400

  

SQ_GREEDY_EVAL tag=it19_b3_plus8 alloc=[96, 64, 8, 16, 8, 8, 8, 8] bytes=216 recall=68.824800

  

SQ_GREEDY_EVAL tag=it19_b4_plus8 alloc=[96, 64, 8, 8, 16, 8, 8, 8] bytes=216 recall=68.681100

  

SQ_GREEDY_EVAL tag=it19_b5_plus8 alloc=[96, 64, 8, 8, 8, 16, 8, 8] bytes=216 recall=68.707600

  

SQ_GREEDY_EVAL tag=it19_b6_plus8 alloc=[96, 64, 8, 8, 8, 8, 16, 8] bytes=216 recall=68.716000

  

SQ_GREEDY_EVAL tag=it19_b7_plus8 alloc=[96, 64, 8, 8, 8, 8, 8, 16] bytes=216 recall=68.681100

  

SQ_GREEDY_EVAL tag=it20_b0_plus8 alloc=[104, 72, 8, 8, 8, 8, 8, 8] bytes=224 recall=69.577100

  

SQ_GREEDY_EVAL tag=it20_b1_plus8 alloc=[96, 80, 8, 8, 8, 8, 8, 8] bytes=224 recall=69.862000

  

SQ_GREEDY_EVAL tag=it20_b2_plus8 alloc=[96, 72, 16, 8, 8, 8, 8, 8] bytes=224 recall=69.750300

  

SQ_GREEDY_EVAL tag=it20_b3_plus8 alloc=[96, 72, 8, 16, 8, 8, 8, 8] bytes=224 recall=69.735700

  

SQ_GREEDY_EVAL tag=it20_b4_plus8 alloc=[96, 72, 8, 8, 16, 8, 8, 8] bytes=224 recall=69.605000

  

SQ_GREEDY_EVAL tag=it20_b5_plus8 alloc=[96, 72, 8, 8, 8, 16, 8, 8] bytes=224 recall=69.620600

  

SQ_GREEDY_EVAL tag=it20_b6_plus8 alloc=[96, 72, 8, 8, 8, 8, 16, 8] bytes=224 recall=69.629500

  

SQ_GREEDY_EVAL tag=it20_b7_plus8 alloc=[96, 72, 8, 8, 8, 8, 8, 16] bytes=224 recall=69.587500

  

SQ_GREEDY_EVAL tag=it21_b0_plus8 alloc=[104, 80, 8, 8, 8, 8, 8, 8] bytes=232 recall=70.258900

  

SQ_GREEDY_EVAL tag=it21_b1_plus8 alloc=[96, 88, 8, 8, 8, 8, 8, 8] bytes=232 recall=70.612800

  

SQ_GREEDY_EVAL tag=it21_b2_plus8 alloc=[96, 80, 16, 8, 8, 8, 8, 8] bytes=232 recall=70.390100

  

SQ_GREEDY_EVAL tag=it21_b3_plus8 alloc=[96, 80, 8, 16, 8, 8, 8, 8] bytes=232 recall=70.371500

  

SQ_GREEDY_EVAL tag=it21_b4_plus8 alloc=[96, 80, 8, 8, 16, 8, 8, 8] bytes=232 recall=70.278700

  

SQ_GREEDY_EVAL tag=it21_b5_plus8 alloc=[96, 80, 8, 8, 8, 16, 8, 8] bytes=232 recall=70.274500

  

SQ_GREEDY_EVAL tag=it21_b6_plus8 alloc=[96, 80, 8, 8, 8, 8, 16, 8] bytes=232 recall=70.293400

  

SQ_GREEDY_EVAL tag=it21_b7_plus8 alloc=[96, 80, 8, 8, 8, 8, 8, 16] bytes=232 recall=70.244700

  

SQ_GREEDY_EVAL tag=it22_b0_plus8 alloc=[104, 88, 8, 8, 8, 8, 8, 8] bytes=240 recall=71.022300

  

SQ_GREEDY_EVAL tag=it22_b1_plus8 alloc=[96, 96, 8, 8, 8, 8, 8, 8] bytes=240 recall=71.291500

  

SQ_GREEDY_EVAL tag=it22_b2_plus8 alloc=[96, 88, 16, 8, 8, 8, 8, 8] bytes=240 recall=71.121100

  

SQ_GREEDY_EVAL tag=it22_b3_plus8 alloc=[96, 88, 8, 16, 8, 8, 8, 8] bytes=240 recall=71.130200

  

SQ_GREEDY_EVAL tag=it22_b4_plus8 alloc=[96, 88, 8, 8, 16, 8, 8, 8] bytes=240 recall=71.001700

  

SQ_GREEDY_EVAL tag=it22_b5_plus8 alloc=[96, 88, 8, 8, 8, 16, 8, 8] bytes=240 recall=71.033500

  

SQ_GREEDY_EVAL tag=it22_b6_plus8 alloc=[96, 88, 8, 8, 8, 8, 16, 8] bytes=240 recall=71.029400

  

SQ_GREEDY_EVAL tag=it22_b7_plus8 alloc=[96, 88, 8, 8, 8, 8, 8, 16] bytes=240 recall=70.987800

  

SQ_GREEDY_EVAL tag=it23_b0_plus8 alloc=[104, 96, 8, 8, 8, 8, 8, 8] bytes=248 recall=71.670300

  

SQ_GREEDY_EVAL tag=it23_b1_plus8 alloc=[96, 104, 8, 8, 8, 8, 8, 8] bytes=248 recall=71.547100

  

SQ_GREEDY_EVAL tag=it23_b2_plus8 alloc=[96, 96, 16, 8, 8, 8, 8, 8] bytes=248 recall=71.780500

  

SQ_GREEDY_EVAL tag=it23_b3_plus8 alloc=[96, 96, 8, 16, 8, 8, 8, 8] bytes=248 recall=71.785200

  

SQ_GREEDY_EVAL tag=it23_b4_plus8 alloc=[96, 96, 8, 8, 16, 8, 8, 8] bytes=248 recall=71.674500

  

SQ_GREEDY_EVAL tag=it23_b5_plus8 alloc=[96, 96, 8, 8, 8, 16, 8, 8] bytes=248 recall=71.679100

  

SQ_GREEDY_EVAL tag=it23_b6_plus8 alloc=[96, 96, 8, 8, 8, 8, 16, 8] bytes=248 recall=71.675900

  

SQ_GREEDY_EVAL tag=it23_b7_plus8 alloc=[96, 96, 8, 8, 8, 8, 8, 16] bytes=248 recall=71.655900

  

SQ_GREEDY_EVAL tag=it24_b0_plus8 alloc=[104, 96, 8, 16, 8, 8, 8, 8] bytes=256 recall=72.143400

  

SQ_GREEDY_EVAL tag=it24_b1_plus8 alloc=[96, 104, 8, 16, 8, 8, 8, 8] bytes=256 recall=72.007400

  

SQ_GREEDY_EVAL tag=it24_b2_plus8 alloc=[96, 96, 16, 16, 8, 8, 8, 8] bytes=256 recall=72.275100

  

SQ_GREEDY_EVAL tag=it24_b3_plus8 alloc=[96, 96, 8, 24, 8, 8, 8, 8] bytes=256 recall=72.222500

  

SQ_GREEDY_EVAL tag=it24_b4_plus8 alloc=[96, 96, 8, 16, 16, 8, 8, 8] bytes=256 recall=72.144400

  

SQ_GREEDY_EVAL tag=it24_b5_plus8 alloc=[96, 96, 8, 16, 8, 16, 8, 8] bytes=256 recall=72.156700

  

SQ_GREEDY_EVAL tag=it24_b6_plus8 alloc=[96, 96, 8, 16, 8, 8, 16, 8] bytes=256 recall=72.154200

  

SQ_GREEDY_EVAL tag=it24_b7_plus8 alloc=[96, 96, 8, 16, 8, 8, 8, 16] bytes=256 recall=72.143100

  

SQ_GREEDY_EVAL tag=it25_b0_plus8 alloc=[104, 96, 16, 16, 8, 8, 8, 8] bytes=264 recall=72.614800

  

SQ_GREEDY_EVAL tag=it25_b1_plus8 alloc=[96, 104, 16, 16, 8, 8, 8, 8] bytes=264 recall=72.508700

  

SQ_GREEDY_EVAL tag=it25_b2_plus8 alloc=[96, 96, 24, 16, 8, 8, 8, 8] bytes=264 recall=72.969100

  

SQ_GREEDY_EVAL tag=it25_b3_plus8 alloc=[96, 96, 16, 24, 8, 8, 8, 8] bytes=264 recall=72.672600

  

SQ_GREEDY_EVAL tag=it25_b4_plus8 alloc=[96, 96, 16, 16, 16, 8, 8, 8] bytes=264 recall=72.645400

  

SQ_GREEDY_EVAL tag=it25_b5_plus8 alloc=[96, 96, 16, 16, 8, 16, 8, 8] bytes=264 recall=72.631800

  

SQ_GREEDY_EVAL tag=it25_b6_plus8 alloc=[96, 96, 16, 16, 8, 8, 16, 8] bytes=264 recall=72.635200

  

SQ_GREEDY_EVAL tag=it25_b7_plus8 alloc=[96, 96, 16, 16, 8, 8, 8, 16] bytes=264 recall=72.604000

  

SQ_GREEDY_EVAL tag=it26_b0_plus8 alloc=[104, 96, 24, 16, 8, 8, 8, 8] bytes=272 recall=73.308500

  

SQ_GREEDY_EVAL tag=it26_b1_plus8 alloc=[96, 104, 24, 16, 8, 8, 8, 8] bytes=272 recall=73.194100

  

SQ_GREEDY_EVAL tag=it26_b2_plus8 alloc=[96, 96, 32, 16, 8, 8, 8, 8] bytes=272 recall=73.422300

  

SQ_GREEDY_EVAL tag=it26_b3_plus8 alloc=[96, 96, 24, 24, 8, 8, 8, 8] bytes=272 recall=73.346600

  

SQ_GREEDY_EVAL tag=it26_b4_plus8 alloc=[96, 96, 24, 16, 16, 8, 8, 8] bytes=272 recall=73.304300

  

SQ_GREEDY_EVAL tag=it26_b5_plus8 alloc=[96, 96, 24, 16, 8, 16, 8, 8] bytes=272 recall=73.313500

  

SQ_GREEDY_EVAL tag=it26_b6_plus8 alloc=[96, 96, 24, 16, 8, 8, 16, 8] bytes=272 recall=73.335700

  

SQ_GREEDY_EVAL tag=it26_b7_plus8 alloc=[96, 96, 24, 16, 8, 8, 8, 16] bytes=272 recall=73.300000

  

SQ_GREEDY_EVAL tag=it27_b0_plus8 alloc=[104, 96, 32, 16, 8, 8, 8, 8] bytes=280 recall=73.740100

  

SQ_GREEDY_EVAL tag=it27_b1_plus8 alloc=[96, 104, 32, 16, 8, 8, 8, 8] bytes=280 recall=73.642000

  

SQ_GREEDY_EVAL tag=it27_b2_plus8 alloc=[96, 96, 40, 16, 8, 8, 8, 8] bytes=280 recall=74.044800

  

SQ_GREEDY_EVAL tag=it27_b3_plus8 alloc=[96, 96, 32, 24, 8, 8, 8, 8] bytes=280 recall=73.778100

  

SQ_GREEDY_EVAL tag=it27_b4_plus8 alloc=[96, 96, 32, 16, 16, 8, 8, 8] bytes=280 recall=73.729500

  

SQ_GREEDY_EVAL tag=it27_b5_plus8 alloc=[96, 96, 32, 16, 8, 16, 8, 8] bytes=280 recall=73.759600

  

SQ_GREEDY_EVAL tag=it27_b6_plus8 alloc=[96, 96, 32, 16, 8, 8, 16, 8] bytes=280 recall=73.751100

  

SQ_GREEDY_EVAL tag=it27_b7_plus8 alloc=[96, 96, 32, 16, 8, 8, 8, 16] bytes=280 recall=73.734500

  

SQ_GREEDY_EVAL tag=it28_b0_plus8 alloc=[104, 96, 40, 16, 8, 8, 8, 8] bytes=288 recall=74.388800

  

SQ_GREEDY_EVAL tag=it28_b1_plus8 alloc=[96, 104, 40, 16, 8, 8, 8, 8] bytes=288 recall=74.272600

  

SQ_GREEDY_EVAL tag=it28_b2_plus8 alloc=[96, 96, 48, 16, 8, 8, 8, 8] bytes=288 recall=74.496400

  

SQ_GREEDY_EVAL tag=it28_b3_plus8 alloc=[96, 96, 40, 24, 8, 8, 8, 8] bytes=288 recall=74.434000

  

SQ_GREEDY_EVAL tag=it28_b4_plus8 alloc=[96, 96, 40, 16, 16, 8, 8, 8] bytes=288 recall=74.349600

  

SQ_GREEDY_EVAL tag=it28_b5_plus8 alloc=[96, 96, 40, 16, 8, 16, 8, 8] bytes=288 recall=74.364600

  

SQ_GREEDY_EVAL tag=it28_b6_plus8 alloc=[96, 96, 40, 16, 8, 8, 16, 8] bytes=288 recall=74.373600

  

SQ_GREEDY_EVAL tag=it28_b7_plus8 alloc=[96, 96, 40, 16, 8, 8, 8, 16] bytes=288 recall=74.345800

  

SQ_GREEDY_EVAL tag=it29_b0_plus8 alloc=[104, 96, 48, 16, 8, 8, 8, 8] bytes=296 recall=74.808300

  

SQ_GREEDY_EVAL tag=it29_b1_plus8 alloc=[96, 104, 48, 16, 8, 8, 8, 8] bytes=296 recall=74.697300

  

SQ_GREEDY_EVAL tag=it29_b2_plus8 alloc=[96, 96, 56, 16, 8, 8, 8, 8] bytes=296 recall=74.917500

  

SQ_GREEDY_EVAL tag=it29_b3_plus8 alloc=[96, 96, 48, 24, 8, 8, 8, 8] bytes=296 recall=74.829900

  

SQ_GREEDY_EVAL tag=it29_b4_plus8 alloc=[96, 96, 48, 16, 16, 8, 8, 8] bytes=296 recall=74.789500

  

SQ_GREEDY_EVAL tag=it29_b5_plus8 alloc=[96, 96, 48, 16, 8, 16, 8, 8] bytes=296 recall=74.814300

  

SQ_GREEDY_EVAL tag=it29_b6_plus8 alloc=[96, 96, 48, 16, 8, 8, 16, 8] bytes=296 recall=74.826200

  

SQ_GREEDY_EVAL tag=it29_b7_plus8 alloc=[96, 96, 48, 16, 8, 8, 8, 16] bytes=296 recall=74.789800

  

SQ_GREEDY_EVAL tag=it30_b0_plus8 alloc=[104, 96, 56, 16, 8, 8, 8, 8] bytes=304 recall=75.208000

  

SQ_GREEDY_EVAL tag=it30_b1_plus8 alloc=[96, 104, 56, 16, 8, 8, 8, 8] bytes=304 recall=75.133400

  

SQ_GREEDY_EVAL tag=it30_b2_plus8 alloc=[96, 96, 64, 16, 8, 8, 8, 8] bytes=304 recall=75.414300

  

SQ_GREEDY_EVAL tag=it30_b3_plus8 alloc=[96, 96, 56, 24, 8, 8, 8, 8] bytes=304 recall=75.224800

  

SQ_GREEDY_EVAL tag=it30_b4_plus8 alloc=[96, 96, 56, 16, 16, 8, 8, 8] bytes=304 recall=75.222500

  

SQ_GREEDY_EVAL tag=it30_b5_plus8 alloc=[96, 96, 56, 16, 8, 16, 8, 8] bytes=304 recall=75.244300

  

SQ_GREEDY_EVAL tag=it30_b6_plus8 alloc=[96, 96, 56, 16, 8, 8, 16, 8] bytes=304 recall=75.207900

  

SQ_GREEDY_EVAL tag=it30_b7_plus8 alloc=[96, 96, 56, 16, 8, 8, 8, 16] bytes=304 recall=75.212600

  

SQ_GREEDY_EVAL tag=it31_b0_plus8 alloc=[104, 96, 64, 16, 8, 8, 8, 8] bytes=312 recall=75.731400

  

SQ_GREEDY_EVAL tag=it31_b1_plus8 alloc=[96, 104, 64, 16, 8, 8, 8, 8] bytes=312 recall=75.625100

  

SQ_GREEDY_EVAL tag=it31_b2_plus8 alloc=[96, 96, 72, 16, 8, 8, 8, 8] bytes=312 recall=75.857200

  

SQ_GREEDY_EVAL tag=it31_b3_plus8 alloc=[96, 96, 64, 24, 8, 8, 8, 8] bytes=312 recall=75.739000

  

SQ_GREEDY_EVAL tag=it31_b4_plus8 alloc=[96, 96, 64, 16, 16, 8, 8, 8] bytes=312 recall=75.707400

  

SQ_GREEDY_EVAL tag=it31_b5_plus8 alloc=[96, 96, 64, 16, 8, 16, 8, 8] bytes=312 recall=75.711600

  

SQ_GREEDY_EVAL tag=it31_b6_plus8 alloc=[96, 96, 64, 16, 8, 8, 16, 8] bytes=312 recall=75.719500

  

SQ_GREEDY_EVAL tag=it31_b7_plus8 alloc=[96, 96, 64, 16, 8, 8, 8, 16] bytes=312 recall=75.697400

  

SQ_GREEDY_EVAL tag=it32_b0_plus8 alloc=[104, 96, 72, 16, 8, 8, 8, 8] bytes=320 recall=76.159900

  

SQ_GREEDY_EVAL tag=it32_b1_plus8 alloc=[96, 104, 72, 16, 8, 8, 8, 8] bytes=320 recall=76.085500

  

SQ_GREEDY_EVAL tag=it32_b2_plus8 alloc=[96, 96, 80, 16, 8, 8, 8, 8] bytes=320 recall=76.338100

  

SQ_GREEDY_EVAL tag=it32_b3_plus8 alloc=[96, 96, 72, 24, 8, 8, 8, 8] bytes=320 recall=76.166300

  

SQ_GREEDY_EVAL tag=it32_b4_plus8 alloc=[96, 96, 72, 16, 16, 8, 8, 8] bytes=320 recall=76.139500

  

SQ_GREEDY_EVAL tag=it32_b5_plus8 alloc=[96, 96, 72, 16, 8, 16, 8, 8] bytes=320 recall=76.142600

  

SQ_GREEDY_EVAL tag=it32_b6_plus8 alloc=[96, 96, 72, 16, 8, 8, 16, 8] bytes=320 recall=76.149400

  

SQ_GREEDY_EVAL tag=it32_b7_plus8 alloc=[96, 96, 72, 16, 8, 8, 8, 16] bytes=320 recall=76.135500

  

SQ_GREEDY_EVAL tag=it33_b0_plus8 alloc=[104, 96, 80, 16, 8, 8, 8, 8] bytes=328 recall=76.641000

  

SQ_GREEDY_EVAL tag=it33_b1_plus8 alloc=[96, 104, 80, 16, 8, 8, 8, 8] bytes=328 recall=76.531700

  

SQ_GREEDY_EVAL tag=it33_b2_plus8 alloc=[96, 96, 88, 16, 8, 8, 8, 8] bytes=328 recall=76.774600

  

SQ_GREEDY_EVAL tag=it33_b3_plus8 alloc=[96, 96, 80, 24, 8, 8, 8, 8] bytes=328 recall=76.643300

  

SQ_GREEDY_EVAL tag=it33_b4_plus8 alloc=[96, 96, 80, 16, 16, 8, 8, 8] bytes=328 recall=76.598700

  

SQ_GREEDY_EVAL tag=it33_b5_plus8 alloc=[96, 96, 80, 16, 8, 16, 8, 8] bytes=328 recall=76.628700

  

SQ_GREEDY_EVAL tag=it33_b6_plus8 alloc=[96, 96, 80, 16, 8, 8, 16, 8] bytes=328 recall=76.622300

  

SQ_GREEDY_EVAL tag=it33_b7_plus8 alloc=[96, 96, 80, 16, 8, 8, 8, 16] bytes=328 recall=76.599600

  

SQ_GREEDY_EVAL tag=it34_b0_plus8 alloc=[104, 96, 88, 16, 8, 8, 8, 8] bytes=336 recall=77.057300

  

SQ_GREEDY_EVAL tag=it34_b1_plus8 alloc=[96, 104, 88, 16, 8, 8, 8, 8] bytes=336 recall=76.973800

  

SQ_GREEDY_EVAL tag=it34_b2_plus8 alloc=[96, 96, 96, 16, 8, 8, 8, 8] bytes=336 recall=77.153700

  

SQ_GREEDY_EVAL tag=it34_b3_plus8 alloc=[96, 96, 88, 24, 8, 8, 8, 8] bytes=336 recall=77.031700

  

SQ_GREEDY_EVAL tag=it34_b4_plus8 alloc=[96, 96, 88, 16, 16, 8, 8, 8] bytes=336 recall=77.021900

  

SQ_GREEDY_EVAL tag=it34_b5_plus8 alloc=[96, 96, 88, 16, 8, 16, 8, 8] bytes=336 recall=77.032800

  

SQ_GREEDY_EVAL tag=it34_b6_plus8 alloc=[96, 96, 88, 16, 8, 8, 16, 8] bytes=336 recall=77.039400

  

SQ_GREEDY_EVAL tag=it34_b7_plus8 alloc=[96, 96, 88, 16, 8, 8, 8, 16] bytes=336 recall=77.016800

  

SQ_GREEDY_EVAL tag=it35_b0_plus8 alloc=[104, 96, 96, 16, 8, 8, 8, 8] bytes=344 recall=77.441500

  

SQ_GREEDY_EVAL tag=it35_b1_plus8 alloc=[96, 104, 96, 16, 8, 8, 8, 8] bytes=344 recall=77.341800

  

SQ_GREEDY_EVAL tag=it35_b2_plus8 alloc=[96, 96, 104, 16, 8, 8, 8, 8] bytes=344 recall=77.302400

  

SQ_GREEDY_EVAL tag=it35_b3_plus8 alloc=[96, 96, 96, 24, 8, 8, 8, 8] bytes=344 recall=77.402100

  

SQ_GREEDY_EVAL tag=it35_b4_plus8 alloc=[96, 96, 96, 16, 16, 8, 8, 8] bytes=344 recall=77.402700

  

SQ_GREEDY_EVAL tag=it35_b5_plus8 alloc=[96, 96, 96, 16, 8, 16, 8, 8] bytes=344 recall=77.404400

  

SQ_GREEDY_EVAL tag=it35_b6_plus8 alloc=[96, 96, 96, 16, 8, 8, 16, 8] bytes=344 recall=77.415900

  

SQ_GREEDY_EVAL tag=it35_b7_plus8 alloc=[96, 96, 96, 16, 8, 8, 8, 16] bytes=344 recall=77.417600

  

SQ_GREEDY_EVAL tag=it36_b0_plus8 alloc=[112, 96, 96, 16, 8, 8, 8, 8] bytes=352 recall=77.721200

  

SQ_GREEDY_EVAL tag=it36_b1_plus8 alloc=[104, 104, 96, 16, 8, 8, 8, 8] bytes=352 recall=77.632200

  

SQ_GREEDY_EVAL tag=it36_b2_plus8 alloc=[104, 96, 104, 16, 8, 8, 8, 8] bytes=352 recall=77.586000

  

SQ_GREEDY_EVAL tag=it36_b3_plus8 alloc=[104, 96, 96, 24, 8, 8, 8, 8] bytes=352 recall=77.702600

  

SQ_GREEDY_EVAL tag=it36_b4_plus8 alloc=[104, 96, 96, 16, 16, 8, 8, 8] bytes=352 recall=77.669900

  

SQ_GREEDY_EVAL tag=it36_b5_plus8 alloc=[104, 96, 96, 16, 8, 16, 8, 8] bytes=352 recall=77.689800

  

SQ_GREEDY_EVAL tag=it36_b6_plus8 alloc=[104, 96, 96, 16, 8, 8, 16, 8] bytes=352 recall=77.701000

  

SQ_GREEDY_EVAL tag=it36_b7_plus8 alloc=[104, 96, 96, 16, 8, 8, 8, 16] bytes=352 recall=77.694700

  

SQ_GREEDY_EVAL tag=it37_b0_plus8 alloc=[120, 96, 96, 16, 8, 8, 8, 8] bytes=360 recall=77.993400

  

SQ_GREEDY_EVAL tag=it37_b1_plus8 alloc=[112, 104, 96, 16, 8, 8, 8, 8] bytes=360 recall=77.920500

  

SQ_GREEDY_EVAL tag=it37_b2_plus8 alloc=[112, 96, 104, 16, 8, 8, 8, 8] bytes=360 recall=77.861300

  

SQ_GREEDY_EVAL tag=it37_b3_plus8 alloc=[112, 96, 96, 24, 8, 8, 8, 8] bytes=360 recall=77.991000

  

SQ_GREEDY_EVAL tag=it37_b4_plus8 alloc=[112, 96, 96, 16, 16, 8, 8, 8] bytes=360 recall=77.952400

  

SQ_GREEDY_EVAL tag=it37_b5_plus8 alloc=[112, 96, 96, 16, 8, 16, 8, 8] bytes=360 recall=77.975100

  

SQ_GREEDY_EVAL tag=it37_b6_plus8 alloc=[112, 96, 96, 16, 8, 8, 16, 8] bytes=360 recall=77.994400

  

SQ_GREEDY_EVAL tag=it37_b7_plus8 alloc=[112, 96, 96, 16, 8, 8, 8, 16] bytes=360 recall=77.974200

  

SQ_GREEDY_EVAL tag=it38_b0_plus8 alloc=[120, 96, 96, 16, 8, 8, 16, 8] bytes=368 recall=78.245700

  

SQ_GREEDY_EVAL tag=it38_b1_plus8 alloc=[112, 104, 96, 16, 8, 8, 16, 8] bytes=368 recall=78.170500

  

SQ_GREEDY_EVAL tag=it38_b2_plus8 alloc=[112, 96, 104, 16, 8, 8, 16, 8] bytes=368 recall=78.135700

  

SQ_GREEDY_EVAL tag=it38_b3_plus8 alloc=[112, 96, 96, 24, 8, 8, 16, 8] bytes=368 recall=78.238500

  

SQ_GREEDY_EVAL tag=it38_b4_plus8 alloc=[112, 96, 96, 16, 16, 8, 16, 8] bytes=368 recall=78.216600

  

SQ_GREEDY_EVAL tag=it38_b5_plus8 alloc=[112, 96, 96, 16, 8, 16, 16, 8] bytes=368 recall=78.237400

  

SQ_GREEDY_EVAL tag=it38_b6_plus8 alloc=[112, 96, 96, 16, 8, 8, 24, 8] bytes=368 recall=78.208600

  

SQ_GREEDY_EVAL tag=it38_b7_plus8 alloc=[112, 96, 96, 16, 8, 8, 16, 16] bytes=368 recall=78.235400

  

SQ_GREEDY_EVAL tag=it39_b0_plus8 alloc=[128, 96, 96, 16, 8, 8, 16, 8] bytes=376 recall=78.509600

  

SQ_GREEDY_EVAL tag=it39_b1_plus8 alloc=[120, 104, 96, 16, 8, 8, 16, 8] bytes=376 recall=78.448300

  

SQ_GREEDY_EVAL tag=it39_b2_plus8 alloc=[120, 96, 104, 16, 8, 8, 16, 8] bytes=376 recall=78.388700

  

SQ_GREEDY_EVAL tag=it39_b3_plus8 alloc=[120, 96, 96, 24, 8, 8, 16, 8] bytes=376 recall=78.489000

  

SQ_GREEDY_EVAL tag=it39_b4_plus8 alloc=[120, 96, 96, 16, 16, 8, 16, 8] bytes=376 recall=78.485200

  

SQ_GREEDY_EVAL tag=it39_b5_plus8 alloc=[120, 96, 96, 16, 8, 16, 16, 8] bytes=376 recall=78.491000

  

SQ_GREEDY_EVAL tag=it39_b6_plus8 alloc=[120, 96, 96, 16, 8, 8, 24, 8] bytes=376 recall=78.466600

  

SQ_GREEDY_EVAL tag=it39_b7_plus8 alloc=[120, 96, 96, 16, 8, 8, 16, 16] bytes=376 recall=78.481500

  

SQ_GREEDY_EVAL tag=it40_b0_plus8 alloc=[136, 96, 96, 16, 8, 8, 16, 8] bytes=384 recall=78.821200

  

SQ_GREEDY_EVAL tag=it40_b1_plus8 alloc=[128, 104, 96, 16, 8, 8, 16, 8] bytes=384 recall=78.722200

  

SQ_GREEDY_EVAL tag=it40_b2_plus8 alloc=[128, 96, 104, 16, 8, 8, 16, 8] bytes=384 recall=78.654700

  

SQ_GREEDY_EVAL tag=it40_b3_plus8 alloc=[128, 96, 96, 24, 8, 8, 16, 8] bytes=384 recall=78.770100

  

SQ_GREEDY_EVAL tag=it40_b4_plus8 alloc=[128, 96, 96, 16, 16, 8, 16, 8] bytes=384 recall=78.750000

  

SQ_GREEDY_EVAL tag=it40_b5_plus8 alloc=[128, 96, 96, 16, 8, 16, 16, 8] bytes=384 recall=78.765600

  

SQ_GREEDY_EVAL tag=it40_b6_plus8 alloc=[128, 96, 96, 16, 8, 8, 24, 8] bytes=384 recall=78.729800

  

SQ_GREEDY_EVAL tag=it40_b7_plus8 alloc=[128, 96, 96, 16, 8, 8, 16, 16] bytes=384 recall=78.757200



### MSMarco Cohere v4, SQ:

  
#### Uniform
==================================================

SQ sweep completed!

Results directory: /tmp/sq_sweep_1779869573

==================================================

  

Summary of SQ recall results:

Bytes,Recall

64,27.3291

96,37.7115

128,46.7073

160,52.4261

192,57.646

224,61.9136

256,65.6278

288,68.3688

320,71.1951

352,73.6701

384,76.1159

#### Variable

SQ_GREEDY_EVAL tag=init alloc=[8, 8, 8, 8, 8, 8, 8, 8] bytes=64 recall=27.329100

SQ_GREEDY_EVAL tag=it1_b0_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 8] bytes=72 recall=31.244600

SQ_GREEDY_EVAL tag=it1_b1_plus8 alloc=[8, 16, 8, 8, 8, 8, 8, 8] bytes=72 recall=30.507000

SQ_GREEDY_EVAL tag=it1_b2_plus8 alloc=[8, 8, 16, 8, 8, 8, 8, 8] bytes=72 recall=30.724800

SQ_GREEDY_EVAL tag=it1_b3_plus8 alloc=[8, 8, 8, 16, 8, 8, 8, 8] bytes=72 recall=30.482200

SQ_GREEDY_EVAL tag=it1_b4_plus8 alloc=[8, 8, 8, 8, 16, 8, 8, 8] bytes=72 recall=30.603900

SQ_GREEDY_EVAL tag=it1_b5_plus8 alloc=[8, 8, 8, 8, 8, 16, 8, 8] bytes=72 recall=30.275800

SQ_GREEDY_EVAL tag=it1_b6_plus8 alloc=[8, 8, 8, 8, 8, 8, 16, 8] bytes=72 recall=30.099900

SQ_GREEDY_EVAL tag=it1_b7_plus8 alloc=[8, 8, 8, 8, 8, 8, 8, 16] bytes=72 recall=30.093400

SQ_GREEDY_EVAL tag=it2_b0_plus8 alloc=[24, 8, 8, 8, 8, 8, 8, 8] bytes=80 recall=34.098900

SQ_GREEDY_EVAL tag=it2_b1_plus8 alloc=[16, 16, 8, 8, 8, 8, 8, 8] bytes=80 recall=34.137800

SQ_GREEDY_EVAL tag=it2_b2_plus8 alloc=[16, 8, 16, 8, 8, 8, 8, 8] bytes=80 recall=34.441500

SQ_GREEDY_EVAL tag=it2_b3_plus8 alloc=[16, 8, 8, 16, 8, 8, 8, 8] bytes=80 recall=34.114800

SQ_GREEDY_EVAL tag=it2_b4_plus8 alloc=[16, 8, 8, 8, 16, 8, 8, 8] bytes=80 recall=34.120600

SQ_GREEDY_EVAL tag=it2_b5_plus8 alloc=[16, 8, 8, 8, 8, 16, 8, 8] bytes=80 recall=33.810300

SQ_GREEDY_EVAL tag=it2_b6_plus8 alloc=[16, 8, 8, 8, 8, 8, 16, 8] bytes=80 recall=33.743400

SQ_GREEDY_EVAL tag=it2_b7_plus8 alloc=[16, 8, 8, 8, 8, 8, 8, 16] bytes=80 recall=33.737000

SQ_GREEDY_EVAL tag=it3_b0_plus8 alloc=[24, 8, 16, 8, 8, 8, 8, 8] bytes=88 recall=36.882200

SQ_GREEDY_EVAL tag=it3_b1_plus8 alloc=[16, 16, 16, 8, 8, 8, 8, 8] bytes=88 recall=37.054400

SQ_GREEDY_EVAL tag=it3_b2_plus8 alloc=[16, 8, 24, 8, 8, 8, 8, 8] bytes=88 recall=37.768800

SQ_GREEDY_EVAL tag=it3_b3_plus8 alloc=[16, 8, 16, 16, 8, 8, 8, 8] bytes=88 recall=37.037400

SQ_GREEDY_EVAL tag=it3_b4_plus8 alloc=[16, 8, 16, 8, 16, 8, 8, 8] bytes=88 recall=37.068900

SQ_GREEDY_EVAL tag=it3_b5_plus8 alloc=[16, 8, 16, 8, 8, 16, 8, 8] bytes=88 recall=36.805600

SQ_GREEDY_EVAL tag=it3_b6_plus8 alloc=[16, 8, 16, 8, 8, 8, 16, 8] bytes=88 recall=36.666600

SQ_GREEDY_EVAL tag=it3_b7_plus8 alloc=[16, 8, 16, 8, 8, 8, 8, 16] bytes=88 recall=36.645800

SQ_GREEDY_EVAL tag=it4_b0_plus8 alloc=[24, 8, 24, 8, 8, 8, 8, 8] bytes=96 recall=40.108600

SQ_GREEDY_EVAL tag=it4_b1_plus8 alloc=[16, 16, 24, 8, 8, 8, 8, 8] bytes=96 recall=40.217800

SQ_GREEDY_EVAL tag=it4_b2_plus8 alloc=[16, 8, 32, 8, 8, 8, 8, 8] bytes=96 recall=40.109300

SQ_GREEDY_EVAL tag=it4_b3_plus8 alloc=[16, 8, 24, 16, 8, 8, 8, 8] bytes=96 recall=40.170800

SQ_GREEDY_EVAL tag=it4_b4_plus8 alloc=[16, 8, 24, 8, 16, 8, 8, 8] bytes=96 recall=40.122600

SQ_GREEDY_EVAL tag=it4_b5_plus8 alloc=[16, 8, 24, 8, 8, 16, 8, 8] bytes=96 recall=39.864500

SQ_GREEDY_EVAL tag=it4_b6_plus8 alloc=[16, 8, 24, 8, 8, 8, 16, 8] bytes=96 recall=39.802400

SQ_GREEDY_EVAL tag=it4_b7_plus8 alloc=[16, 8, 24, 8, 8, 8, 8, 16] bytes=96 recall=39.779500

SQ_GREEDY_EVAL tag=it5_b0_plus8 alloc=[24, 16, 24, 8, 8, 8, 8, 8] bytes=104 recall=42.358700

SQ_GREEDY_EVAL tag=it5_b1_plus8 alloc=[16, 24, 24, 8, 8, 8, 8, 8] bytes=104 recall=42.739800

SQ_GREEDY_EVAL tag=it5_b2_plus8 alloc=[16, 16, 32, 8, 8, 8, 8, 8] bytes=104 recall=42.423400

SQ_GREEDY_EVAL tag=it5_b3_plus8 alloc=[16, 16, 24, 16, 8, 8, 8, 8] bytes=104 recall=42.386800

SQ_GREEDY_EVAL tag=it5_b4_plus8 alloc=[16, 16, 24, 8, 16, 8, 8, 8] bytes=104 recall=42.422800

SQ_GREEDY_EVAL tag=it5_b5_plus8 alloc=[16, 16, 24, 8, 8, 16, 8, 8] bytes=104 recall=42.118600

SQ_GREEDY_EVAL tag=it5_b6_plus8 alloc=[16, 16, 24, 8, 8, 8, 16, 8] bytes=104 recall=42.099100

SQ_GREEDY_EVAL tag=it5_b7_plus8 alloc=[16, 16, 24, 8, 8, 8, 8, 16] bytes=104 recall=42.063600

SQ_GREEDY_EVAL tag=it6_b0_plus8 alloc=[24, 24, 24, 8, 8, 8, 8, 8] bytes=112 recall=44.728100

SQ_GREEDY_EVAL tag=it6_b1_plus8 alloc=[16, 32, 24, 8, 8, 8, 8, 8] bytes=112 recall=44.894300

SQ_GREEDY_EVAL tag=it6_b2_plus8 alloc=[16, 24, 32, 8, 8, 8, 8, 8] bytes=112 recall=44.798100

SQ_GREEDY_EVAL tag=it6_b3_plus8 alloc=[16, 24, 24, 16, 8, 8, 8, 8] bytes=112 recall=44.777100

SQ_GREEDY_EVAL tag=it6_b4_plus8 alloc=[16, 24, 24, 8, 16, 8, 8, 8] bytes=112 recall=44.788800

SQ_GREEDY_EVAL tag=it6_b5_plus8 alloc=[16, 24, 24, 8, 8, 16, 8, 8] bytes=112 recall=44.468800

SQ_GREEDY_EVAL tag=it6_b6_plus8 alloc=[16, 24, 24, 8, 8, 8, 16, 8] bytes=112 recall=44.432100

SQ_GREEDY_EVAL tag=it6_b7_plus8 alloc=[16, 24, 24, 8, 8, 8, 8, 16] bytes=112 recall=44.421500

SQ_GREEDY_EVAL tag=it7_b0_plus8 alloc=[24, 32, 24, 8, 8, 8, 8, 8] bytes=120 recall=46.720800

SQ_GREEDY_EVAL tag=it7_b1_plus8 alloc=[16, 40, 24, 8, 8, 8, 8, 8] bytes=120 recall=46.915500

SQ_GREEDY_EVAL tag=it7_b2_plus8 alloc=[16, 32, 32, 8, 8, 8, 8, 8] bytes=120 recall=46.747000

SQ_GREEDY_EVAL tag=it7_b3_plus8 alloc=[16, 32, 24, 16, 8, 8, 8, 8] bytes=120 recall=46.723100

SQ_GREEDY_EVAL tag=it7_b4_plus8 alloc=[16, 32, 24, 8, 16, 8, 8, 8] bytes=120 recall=46.738700

SQ_GREEDY_EVAL tag=it7_b5_plus8 alloc=[16, 32, 24, 8, 8, 16, 8, 8] bytes=120 recall=46.526400

SQ_GREEDY_EVAL tag=it7_b6_plus8 alloc=[16, 32, 24, 8, 8, 8, 16, 8] bytes=120 recall=46.431100

SQ_GREEDY_EVAL tag=it7_b7_plus8 alloc=[16, 32, 24, 8, 8, 8, 8, 16] bytes=120 recall=46.460200

SQ_GREEDY_EVAL tag=it8_b0_plus8 alloc=[24, 40, 24, 8, 8, 8, 8, 8] bytes=128 recall=48.575500

SQ_GREEDY_EVAL tag=it8_b1_plus8 alloc=[16, 48, 24, 8, 8, 8, 8, 8] bytes=128 recall=49.197900

SQ_GREEDY_EVAL tag=it8_b2_plus8 alloc=[16, 40, 32, 8, 8, 8, 8, 8] bytes=128 recall=48.643000

SQ_GREEDY_EVAL tag=it8_b3_plus8 alloc=[16, 40, 24, 16, 8, 8, 8, 8] bytes=128 recall=48.665500

SQ_GREEDY_EVAL tag=it8_b4_plus8 alloc=[16, 40, 24, 8, 16, 8, 8, 8] bytes=128 recall=48.634200

SQ_GREEDY_EVAL tag=it8_b5_plus8 alloc=[16, 40, 24, 8, 8, 16, 8, 8] bytes=128 recall=48.370300

SQ_GREEDY_EVAL tag=it8_b6_plus8 alloc=[16, 40, 24, 8, 8, 8, 16, 8] bytes=128 recall=48.331400

SQ_GREEDY_EVAL tag=it8_b7_plus8 alloc=[16, 40, 24, 8, 8, 8, 8, 16] bytes=128 recall=48.360500

SQ_GREEDY_EVAL tag=it9_b0_plus8 alloc=[24, 48, 24, 8, 8, 8, 8, 8] bytes=136 recall=50.763500

SQ_GREEDY_EVAL tag=it9_b1_plus8 alloc=[16, 56, 24, 8, 8, 8, 8, 8] bytes=136 recall=49.953700

SQ_GREEDY_EVAL tag=it9_b2_plus8 alloc=[16, 48, 32, 8, 8, 8, 8, 8] bytes=136 recall=50.852400

SQ_GREEDY_EVAL tag=it9_b3_plus8 alloc=[16, 48, 24, 16, 8, 8, 8, 8] bytes=136 recall=50.745300

SQ_GREEDY_EVAL tag=it9_b4_plus8 alloc=[16, 48, 24, 8, 16, 8, 8, 8] bytes=136 recall=50.763500

SQ_GREEDY_EVAL tag=it9_b5_plus8 alloc=[16, 48, 24, 8, 8, 16, 8, 8] bytes=136 recall=50.501000

SQ_GREEDY_EVAL tag=it9_b6_plus8 alloc=[16, 48, 24, 8, 8, 8, 16, 8] bytes=136 recall=50.471500

SQ_GREEDY_EVAL tag=it9_b7_plus8 alloc=[16, 48, 24, 8, 8, 8, 8, 16] bytes=136 recall=50.523100

SQ_GREEDY_EVAL tag=it10_b0_plus8 alloc=[24, 48, 32, 8, 8, 8, 8, 8] bytes=144 recall=52.226400

SQ_GREEDY_EVAL tag=it10_b1_plus8 alloc=[16, 56, 32, 8, 8, 8, 8, 8] bytes=144 recall=51.579900

SQ_GREEDY_EVAL tag=it10_b2_plus8 alloc=[16, 48, 40, 8, 8, 8, 8, 8] bytes=144 recall=52.627100

SQ_GREEDY_EVAL tag=it10_b3_plus8 alloc=[16, 48, 32, 16, 8, 8, 8, 8] bytes=144 recall=52.345600

SQ_GREEDY_EVAL tag=it10_b4_plus8 alloc=[16, 48, 32, 8, 16, 8, 8, 8] bytes=144 recall=52.343100

SQ_GREEDY_EVAL tag=it10_b5_plus8 alloc=[16, 48, 32, 8, 8, 16, 8, 8] bytes=144 recall=52.113800

SQ_GREEDY_EVAL tag=it10_b6_plus8 alloc=[16, 48, 32, 8, 8, 8, 16, 8] bytes=144 recall=52.018300

SQ_GREEDY_EVAL tag=it10_b7_plus8 alloc=[16, 48, 32, 8, 8, 8, 8, 16] bytes=144 recall=52.050300

SQ_GREEDY_EVAL tag=it11_b0_plus8 alloc=[24, 48, 40, 8, 8, 8, 8, 8] bytes=152 recall=53.931400

SQ_GREEDY_EVAL tag=it11_b1_plus8 alloc=[16, 56, 40, 8, 8, 8, 8, 8] bytes=152 recall=53.302600

SQ_GREEDY_EVAL tag=it11_b2_plus8 alloc=[16, 48, 48, 8, 8, 8, 8, 8] bytes=152 recall=54.118300

SQ_GREEDY_EVAL tag=it11_b3_plus8 alloc=[16, 48, 40, 16, 8, 8, 8, 8] bytes=152 recall=53.979100

SQ_GREEDY_EVAL tag=it11_b4_plus8 alloc=[16, 48, 40, 8, 16, 8, 8, 8] bytes=152 recall=54.025100

SQ_GREEDY_EVAL tag=it11_b5_plus8 alloc=[16, 48, 40, 8, 8, 16, 8, 8] bytes=152 recall=53.779700

SQ_GREEDY_EVAL tag=it11_b6_plus8 alloc=[16, 48, 40, 8, 8, 8, 16, 8] bytes=152 recall=53.704700

SQ_GREEDY_EVAL tag=it11_b7_plus8 alloc=[16, 48, 40, 8, 8, 8, 8, 16] bytes=152 recall=53.764500

SQ_GREEDY_EVAL tag=it12_b0_plus8 alloc=[24, 48, 48, 8, 8, 8, 8, 8] bytes=160 recall=55.281400

SQ_GREEDY_EVAL tag=it12_b1_plus8 alloc=[16, 56, 48, 8, 8, 8, 8, 8] bytes=160 recall=54.760900

SQ_GREEDY_EVAL tag=it12_b2_plus8 alloc=[16, 48, 56, 8, 8, 8, 8, 8] bytes=160 recall=54.801000

SQ_GREEDY_EVAL tag=it12_b3_plus8 alloc=[16, 48, 48, 16, 8, 8, 8, 8] bytes=160 recall=55.390000

SQ_GREEDY_EVAL tag=it12_b4_plus8 alloc=[16, 48, 48, 8, 16, 8, 8, 8] bytes=160 recall=55.441700

SQ_GREEDY_EVAL tag=it12_b5_plus8 alloc=[16, 48, 48, 8, 8, 16, 8, 8] bytes=160 recall=55.208200

SQ_GREEDY_EVAL tag=it12_b6_plus8 alloc=[16, 48, 48, 8, 8, 8, 16, 8] bytes=160 recall=55.112000

SQ_GREEDY_EVAL tag=it12_b7_plus8 alloc=[16, 48, 48, 8, 8, 8, 8, 16] bytes=160 recall=55.153000

SQ_GREEDY_EVAL tag=it13_b0_plus8 alloc=[24, 48, 48, 8, 16, 8, 8, 8] bytes=168 recall=56.494400

SQ_GREEDY_EVAL tag=it13_b1_plus8 alloc=[16, 56, 48, 8, 16, 8, 8, 8] bytes=168 recall=56.029800

SQ_GREEDY_EVAL tag=it13_b2_plus8 alloc=[16, 48, 56, 8, 16, 8, 8, 8] bytes=168 recall=56.102900

SQ_GREEDY_EVAL tag=it13_b3_plus8 alloc=[16, 48, 48, 16, 16, 8, 8, 8] bytes=168 recall=56.638300

SQ_GREEDY_EVAL tag=it13_b4_plus8 alloc=[16, 48, 48, 8, 24, 8, 8, 8] bytes=168 recall=56.448300

SQ_GREEDY_EVAL tag=it13_b5_plus8 alloc=[16, 48, 48, 8, 16, 16, 8, 8] bytes=168 recall=56.461600

SQ_GREEDY_EVAL tag=it13_b6_plus8 alloc=[16, 48, 48, 8, 16, 8, 16, 8] bytes=168 recall=56.367800

SQ_GREEDY_EVAL tag=it13_b7_plus8 alloc=[16, 48, 48, 8, 16, 8, 8, 16] bytes=168 recall=56.430200

SQ_GREEDY_EVAL tag=it14_b0_plus8 alloc=[24, 48, 48, 16, 16, 8, 8, 8] bytes=176 recall=57.622200

SQ_GREEDY_EVAL tag=it14_b1_plus8 alloc=[16, 56, 48, 16, 16, 8, 8, 8] bytes=176 recall=57.230700

SQ_GREEDY_EVAL tag=it14_b2_plus8 alloc=[16, 48, 56, 16, 16, 8, 8, 8] bytes=176 recall=57.288400

SQ_GREEDY_EVAL tag=it14_b3_plus8 alloc=[16, 48, 48, 24, 16, 8, 8, 8] bytes=176 recall=57.772100

SQ_GREEDY_EVAL tag=it14_b4_plus8 alloc=[16, 48, 48, 16, 24, 8, 8, 8] bytes=176 recall=57.615600

SQ_GREEDY_EVAL tag=it14_b5_plus8 alloc=[16, 48, 48, 16, 16, 16, 8, 8] bytes=176 recall=57.625100

SQ_GREEDY_EVAL tag=it14_b6_plus8 alloc=[16, 48, 48, 16, 16, 8, 16, 8] bytes=176 recall=57.575100

SQ_GREEDY_EVAL tag=it14_b7_plus8 alloc=[16, 48, 48, 16, 16, 8, 8, 16] bytes=176 recall=57.577700

SQ_GREEDY_EVAL tag=it15_b0_plus8 alloc=[24, 48, 48, 24, 16, 8, 8, 8] bytes=184 recall=58.807400

SQ_GREEDY_EVAL tag=it15_b1_plus8 alloc=[16, 56, 48, 24, 16, 8, 8, 8] bytes=184 recall=58.296600

SQ_GREEDY_EVAL tag=it15_b2_plus8 alloc=[16, 48, 56, 24, 16, 8, 8, 8] bytes=184 recall=58.356400

SQ_GREEDY_EVAL tag=it15_b3_plus8 alloc=[16, 48, 48, 32, 16, 8, 8, 8] bytes=184 recall=58.801900

SQ_GREEDY_EVAL tag=it15_b4_plus8 alloc=[16, 48, 48, 24, 24, 8, 8, 8] bytes=184 recall=58.689500

SQ_GREEDY_EVAL tag=it15_b5_plus8 alloc=[16, 48, 48, 24, 16, 16, 8, 8] bytes=184 recall=58.724400

SQ_GREEDY_EVAL tag=it15_b6_plus8 alloc=[16, 48, 48, 24, 16, 8, 16, 8] bytes=184 recall=58.624900

SQ_GREEDY_EVAL tag=it15_b7_plus8 alloc=[16, 48, 48, 24, 16, 8, 8, 16] bytes=184 recall=58.680100

SQ_GREEDY_EVAL tag=it16_b0_plus8 alloc=[32, 48, 48, 24, 16, 8, 8, 8] bytes=192 recall=60.470800

SQ_GREEDY_EVAL tag=it16_b1_plus8 alloc=[24, 56, 48, 24, 16, 8, 8, 8] bytes=192 recall=59.308900

SQ_GREEDY_EVAL tag=it16_b2_plus8 alloc=[24, 48, 56, 24, 16, 8, 8, 8] bytes=192 recall=59.339700

SQ_GREEDY_EVAL tag=it16_b3_plus8 alloc=[24, 48, 48, 32, 16, 8, 8, 8] bytes=192 recall=59.722100

SQ_GREEDY_EVAL tag=it16_b4_plus8 alloc=[24, 48, 48, 24, 24, 8, 8, 8] bytes=192 recall=59.711500

SQ_GREEDY_EVAL tag=it16_b5_plus8 alloc=[24, 48, 48, 24, 16, 16, 8, 8] bytes=192 recall=59.702600

SQ_GREEDY_EVAL tag=it16_b6_plus8 alloc=[24, 48, 48, 24, 16, 8, 16, 8] bytes=192 recall=59.627800

SQ_GREEDY_EVAL tag=it16_b7_plus8 alloc=[24, 48, 48, 24, 16, 8, 8, 16] bytes=192 recall=59.603600

SQ_GREEDY_EVAL tag=it17_b0_plus8 alloc=[40, 48, 48, 24, 16, 8, 8, 8] bytes=200 recall=61.616800

SQ_GREEDY_EVAL tag=it17_b1_plus8 alloc=[32, 56, 48, 24, 16, 8, 8, 8] bytes=200 recall=60.929800

SQ_GREEDY_EVAL tag=it17_b2_plus8 alloc=[32, 48, 56, 24, 16, 8, 8, 8] bytes=200 recall=60.971300

SQ_GREEDY_EVAL tag=it17_b3_plus8 alloc=[32, 48, 48, 32, 16, 8, 8, 8] bytes=200 recall=61.385100

SQ_GREEDY_EVAL tag=it17_b4_plus8 alloc=[32, 48, 48, 24, 24, 8, 8, 8] bytes=200 recall=61.297700

SQ_GREEDY_EVAL tag=it17_b5_plus8 alloc=[32, 48, 48, 24, 16, 16, 8, 8] bytes=200 recall=61.288800

SQ_GREEDY_EVAL tag=it17_b6_plus8 alloc=[32, 48, 48, 24, 16, 8, 16, 8] bytes=200 recall=61.244600

SQ_GREEDY_EVAL tag=it17_b7_plus8 alloc=[32, 48, 48, 24, 16, 8, 8, 16] bytes=200 recall=61.261500

SQ_GREEDY_EVAL tag=it18_b0_plus8 alloc=[48, 48, 48, 24, 16, 8, 8, 8] bytes=208 recall=62.746800

SQ_GREEDY_EVAL tag=it18_b1_plus8 alloc=[40, 56, 48, 24, 16, 8, 8, 8] bytes=208 recall=62.058000

SQ_GREEDY_EVAL tag=it18_b2_plus8 alloc=[40, 48, 56, 24, 16, 8, 8, 8] bytes=208 recall=62.120800

SQ_GREEDY_EVAL tag=it18_b3_plus8 alloc=[40, 48, 48, 32, 16, 8, 8, 8] bytes=208 recall=62.501000

SQ_GREEDY_EVAL tag=it18_b4_plus8 alloc=[40, 48, 48, 24, 24, 8, 8, 8] bytes=208 recall=62.431400

SQ_GREEDY_EVAL tag=it18_b5_plus8 alloc=[40, 48, 48, 24, 16, 16, 8, 8] bytes=208 recall=62.394800

SQ_GREEDY_EVAL tag=it18_b6_plus8 alloc=[40, 48, 48, 24, 16, 8, 16, 8] bytes=208 recall=62.371100

SQ_GREEDY_EVAL tag=it18_b7_plus8 alloc=[40, 48, 48, 24, 16, 8, 8, 16] bytes=208 recall=62.368300

SQ_GREEDY_EVAL tag=it19_b0_plus8 alloc=[56, 48, 48, 24, 16, 8, 8, 8] bytes=216 recall=63.422800

SQ_GREEDY_EVAL tag=it19_b1_plus8 alloc=[48, 56, 48, 24, 16, 8, 8, 8] bytes=216 recall=63.189700

SQ_GREEDY_EVAL tag=it19_b2_plus8 alloc=[48, 48, 56, 24, 16, 8, 8, 8] bytes=216 recall=63.223200

SQ_GREEDY_EVAL tag=it19_b3_plus8 alloc=[48, 48, 48, 32, 16, 8, 8, 8] bytes=216 recall=63.585800

SQ_GREEDY_EVAL tag=it19_b4_plus8 alloc=[48, 48, 48, 24, 24, 8, 8, 8] bytes=216 recall=63.499600

SQ_GREEDY_EVAL tag=it19_b5_plus8 alloc=[48, 48, 48, 24, 16, 16, 8, 8] bytes=216 recall=63.471500

SQ_GREEDY_EVAL tag=it19_b6_plus8 alloc=[48, 48, 48, 24, 16, 8, 16, 8] bytes=216 recall=63.456700

SQ_GREEDY_EVAL tag=it19_b7_plus8 alloc=[48, 48, 48, 24, 16, 8, 8, 16] bytes=216 recall=63.482700

SQ_GREEDY_EVAL tag=it20_b0_plus8 alloc=[56, 48, 48, 32, 16, 8, 8, 8] bytes=224 recall=64.233200

SQ_GREEDY_EVAL tag=it20_b1_plus8 alloc=[48, 56, 48, 32, 16, 8, 8, 8] bytes=224 recall=63.976200

SQ_GREEDY_EVAL tag=it20_b2_plus8 alloc=[48, 48, 56, 32, 16, 8, 8, 8] bytes=224 recall=64.025600

SQ_GREEDY_EVAL tag=it20_b3_plus8 alloc=[48, 48, 48, 40, 16, 8, 8, 8] bytes=224 recall=64.440000

SQ_GREEDY_EVAL tag=it20_b4_plus8 alloc=[48, 48, 48, 32, 24, 8, 8, 8] bytes=224 recall=64.290300

SQ_GREEDY_EVAL tag=it20_b5_plus8 alloc=[48, 48, 48, 32, 16, 16, 8, 8] bytes=224 recall=64.248700

SQ_GREEDY_EVAL tag=it20_b6_plus8 alloc=[48, 48, 48, 32, 16, 8, 16, 8] bytes=224 recall=64.251000

SQ_GREEDY_EVAL tag=it20_b7_plus8 alloc=[48, 48, 48, 32, 16, 8, 8, 16] bytes=224 recall=64.229900

SQ_GREEDY_EVAL tag=it21_b0_plus8 alloc=[56, 48, 48, 40, 16, 8, 8, 8] bytes=232 recall=65.119600

SQ_GREEDY_EVAL tag=it21_b1_plus8 alloc=[48, 56, 48, 40, 16, 8, 8, 8] bytes=232 recall=64.828800

SQ_GREEDY_EVAL tag=it21_b2_plus8 alloc=[48, 48, 56, 40, 16, 8, 8, 8] bytes=232 recall=64.886000

SQ_GREEDY_EVAL tag=it21_b3_plus8 alloc=[48, 48, 48, 48, 16, 8, 8, 8] bytes=232 recall=65.417900

SQ_GREEDY_EVAL tag=it21_b4_plus8 alloc=[48, 48, 48, 40, 24, 8, 8, 8] bytes=232 recall=65.155600

SQ_GREEDY_EVAL tag=it21_b5_plus8 alloc=[48, 48, 48, 40, 16, 16, 8, 8] bytes=232 recall=65.103900

SQ_GREEDY_EVAL tag=it21_b6_plus8 alloc=[48, 48, 48, 40, 16, 8, 16, 8] bytes=232 recall=65.103200

SQ_GREEDY_EVAL tag=it21_b7_plus8 alloc=[48, 48, 48, 40, 16, 8, 8, 16] bytes=232 recall=65.064600

SQ_GREEDY_EVAL tag=it22_b0_plus8 alloc=[56, 48, 48, 48, 16, 8, 8, 8] bytes=240 recall=66.051300

SQ_GREEDY_EVAL tag=it22_b1_plus8 alloc=[48, 56, 48, 48, 16, 8, 8, 8] bytes=240 recall=65.792800

SQ_GREEDY_EVAL tag=it22_b2_plus8 alloc=[48, 48, 56, 48, 16, 8, 8, 8] bytes=240 recall=65.802700

SQ_GREEDY_EVAL tag=it22_b3_plus8 alloc=[48, 48, 48, 56, 16, 8, 8, 8] bytes=240 recall=65.821900

SQ_GREEDY_EVAL tag=it22_b4_plus8 alloc=[48, 48, 48, 48, 24, 8, 8, 8] bytes=240 recall=66.095800

SQ_GREEDY_EVAL tag=it22_b5_plus8 alloc=[48, 48, 48, 48, 16, 16, 8, 8] bytes=240 recall=66.039100

SQ_GREEDY_EVAL tag=it22_b6_plus8 alloc=[48, 48, 48, 48, 16, 8, 16, 8] bytes=240 recall=66.061900

SQ_GREEDY_EVAL tag=it22_b7_plus8 alloc=[48, 48, 48, 48, 16, 8, 8, 16] bytes=240 recall=66.024900

SQ_GREEDY_EVAL tag=it23_b0_plus8 alloc=[56, 48, 48, 48, 24, 8, 8, 8] bytes=248 recall=66.689400

SQ_GREEDY_EVAL tag=it23_b1_plus8 alloc=[48, 56, 48, 48, 24, 8, 8, 8] bytes=248 recall=66.479200

SQ_GREEDY_EVAL tag=it23_b2_plus8 alloc=[48, 48, 56, 48, 24, 8, 8, 8] bytes=248 recall=66.508000

SQ_GREEDY_EVAL tag=it23_b3_plus8 alloc=[48, 48, 48, 56, 24, 8, 8, 8] bytes=248 recall=66.477800

SQ_GREEDY_EVAL tag=it23_b4_plus8 alloc=[48, 48, 48, 48, 32, 8, 8, 8] bytes=248 recall=67.101300

SQ_GREEDY_EVAL tag=it23_b5_plus8 alloc=[48, 48, 48, 48, 24, 16, 8, 8] bytes=248 recall=66.714900

SQ_GREEDY_EVAL tag=it23_b6_plus8 alloc=[48, 48, 48, 48, 24, 8, 16, 8] bytes=248 recall=66.728200

SQ_GREEDY_EVAL tag=it23_b7_plus8 alloc=[48, 48, 48, 48, 24, 8, 8, 16] bytes=248 recall=66.684000

SQ_GREEDY_EVAL tag=it24_b0_plus8 alloc=[56, 48, 48, 48, 32, 8, 8, 8] bytes=256 recall=67.706400

SQ_GREEDY_EVAL tag=it24_b1_plus8 alloc=[48, 56, 48, 48, 32, 8, 8, 8] bytes=256 recall=67.473100

SQ_GREEDY_EVAL tag=it24_b2_plus8 alloc=[48, 48, 56, 48, 32, 8, 8, 8] bytes=256 recall=67.493000

SQ_GREEDY_EVAL tag=it24_b3_plus8 alloc=[48, 48, 48, 56, 32, 8, 8, 8] bytes=256 recall=67.474900

SQ_GREEDY_EVAL tag=it24_b4_plus8 alloc=[48, 48, 48, 48, 40, 8, 8, 8] bytes=256 recall=67.865500

SQ_GREEDY_EVAL tag=it24_b5_plus8 alloc=[48, 48, 48, 48, 32, 16, 8, 8] bytes=256 recall=67.712900

SQ_GREEDY_EVAL tag=it24_b6_plus8 alloc=[48, 48, 48, 48, 32, 8, 16, 8] bytes=256 recall=67.692700

SQ_GREEDY_EVAL tag=it24_b7_plus8 alloc=[48, 48, 48, 48, 32, 8, 8, 16] bytes=256 recall=67.695700

SQ_GREEDY_EVAL tag=it25_b0_plus8 alloc=[56, 48, 48, 48, 40, 8, 8, 8] bytes=264 recall=68.420800

SQ_GREEDY_EVAL tag=it25_b1_plus8 alloc=[48, 56, 48, 48, 40, 8, 8, 8] bytes=264 recall=68.202400

SQ_GREEDY_EVAL tag=it25_b2_plus8 alloc=[48, 48, 56, 48, 40, 8, 8, 8] bytes=264 recall=68.202600

SQ_GREEDY_EVAL tag=it25_b3_plus8 alloc=[48, 48, 48, 56, 40, 8, 8, 8] bytes=264 recall=68.211200

SQ_GREEDY_EVAL tag=it25_b4_plus8 alloc=[48, 48, 48, 48, 48, 8, 8, 8] bytes=264 recall=68.643300

SQ_GREEDY_EVAL tag=it25_b5_plus8 alloc=[48, 48, 48, 48, 40, 16, 8, 8] bytes=264 recall=68.412800

SQ_GREEDY_EVAL tag=it25_b6_plus8 alloc=[48, 48, 48, 48, 40, 8, 16, 8] bytes=264 recall=68.385800

SQ_GREEDY_EVAL tag=it25_b7_plus8 alloc=[48, 48, 48, 48, 40, 8, 8, 16] bytes=264 recall=68.429900

SQ_GREEDY_EVAL tag=it26_b0_plus8 alloc=[56, 48, 48, 48, 48, 8, 8, 8] bytes=272 recall=69.186500

SQ_GREEDY_EVAL tag=it26_b1_plus8 alloc=[48, 56, 48, 48, 48, 8, 8, 8] bytes=272 recall=68.969100

SQ_GREEDY_EVAL tag=it26_b2_plus8 alloc=[48, 48, 56, 48, 48, 8, 8, 8] bytes=272 recall=69.024800

SQ_GREEDY_EVAL tag=it26_b3_plus8 alloc=[48, 48, 48, 56, 48, 8, 8, 8] bytes=272 recall=68.974500

SQ_GREEDY_EVAL tag=it26_b4_plus8 alloc=[48, 48, 48, 48, 56, 8, 8, 8] bytes=272 recall=69.004200

SQ_GREEDY_EVAL tag=it26_b5_plus8 alloc=[48, 48, 48, 48, 48, 16, 8, 8] bytes=272 recall=69.198000

SQ_GREEDY_EVAL tag=it26_b6_plus8 alloc=[48, 48, 48, 48, 48, 8, 16, 8] bytes=272 recall=69.160200

SQ_GREEDY_EVAL tag=it26_b7_plus8 alloc=[48, 48, 48, 48, 48, 8, 8, 16] bytes=272 recall=69.173800

SQ_GREEDY_EVAL tag=it27_b0_plus8 alloc=[56, 48, 48, 48, 48, 16, 8, 8] bytes=280 recall=69.717000

SQ_GREEDY_EVAL tag=it27_b1_plus8 alloc=[48, 56, 48, 48, 48, 16, 8, 8] bytes=280 recall=69.531800

SQ_GREEDY_EVAL tag=it27_b2_plus8 alloc=[48, 48, 56, 48, 48, 16, 8, 8] bytes=280 recall=69.556300

SQ_GREEDY_EVAL tag=it27_b3_plus8 alloc=[48, 48, 48, 56, 48, 16, 8, 8] bytes=280 recall=69.506900

SQ_GREEDY_EVAL tag=it27_b4_plus8 alloc=[48, 48, 48, 48, 56, 16, 8, 8] bytes=280 recall=69.537700

SQ_GREEDY_EVAL tag=it27_b5_plus8 alloc=[48, 48, 48, 48, 48, 24, 8, 8] bytes=280 recall=69.859700

SQ_GREEDY_EVAL tag=it27_b6_plus8 alloc=[48, 48, 48, 48, 48, 16, 16, 8] bytes=280 recall=69.704000

SQ_GREEDY_EVAL tag=it27_b7_plus8 alloc=[48, 48, 48, 48, 48, 16, 8, 16] bytes=280 recall=69.701900

SQ_GREEDY_EVAL tag=it28_b0_plus8 alloc=[56, 48, 48, 48, 48, 24, 8, 8] bytes=288 recall=70.389300

SQ_GREEDY_EVAL tag=it28_b1_plus8 alloc=[48, 56, 48, 48, 48, 24, 8, 8] bytes=288 recall=70.171200

SQ_GREEDY_EVAL tag=it28_b2_plus8 alloc=[48, 48, 56, 48, 48, 24, 8, 8] bytes=288 recall=70.169600

SQ_GREEDY_EVAL tag=it28_b3_plus8 alloc=[48, 48, 48, 56, 48, 24, 8, 8] bytes=288 recall=70.180700

SQ_GREEDY_EVAL tag=it28_b4_plus8 alloc=[48, 48, 48, 48, 56, 24, 8, 8] bytes=288 recall=70.216800

SQ_GREEDY_EVAL tag=it28_b5_plus8 alloc=[48, 48, 48, 48, 48, 32, 8, 8] bytes=288 recall=70.418300

SQ_GREEDY_EVAL tag=it28_b6_plus8 alloc=[48, 48, 48, 48, 48, 24, 16, 8] bytes=288 recall=70.370800

SQ_GREEDY_EVAL tag=it28_b7_plus8 alloc=[48, 48, 48, 48, 48, 24, 8, 16] bytes=288 recall=70.341500

SQ_GREEDY_EVAL tag=it29_b0_plus8 alloc=[56, 48, 48, 48, 48, 32, 8, 8] bytes=296 recall=70.912500

SQ_GREEDY_EVAL tag=it29_b1_plus8 alloc=[48, 56, 48, 48, 48, 32, 8, 8] bytes=296 recall=70.706200

SQ_GREEDY_EVAL tag=it29_b2_plus8 alloc=[48, 48, 56, 48, 48, 32, 8, 8] bytes=296 recall=70.746400

SQ_GREEDY_EVAL tag=it29_b3_plus8 alloc=[48, 48, 48, 56, 48, 32, 8, 8] bytes=296 recall=70.701100

SQ_GREEDY_EVAL tag=it29_b4_plus8 alloc=[48, 48, 48, 48, 56, 32, 8, 8] bytes=296 recall=70.758900

SQ_GREEDY_EVAL tag=it29_b5_plus8 alloc=[48, 48, 48, 48, 48, 40, 8, 8] bytes=296 recall=70.924600

SQ_GREEDY_EVAL tag=it29_b6_plus8 alloc=[48, 48, 48, 48, 48, 32, 16, 8] bytes=296 recall=70.924400

SQ_GREEDY_EVAL tag=it29_b7_plus8 alloc=[48, 48, 48, 48, 48, 32, 8, 16] bytes=296 recall=70.914200

SQ_GREEDY_EVAL tag=it30_b0_plus8 alloc=[56, 48, 48, 48, 48, 40, 8, 8] bytes=304 recall=71.419800

SQ_GREEDY_EVAL tag=it30_b1_plus8 alloc=[48, 56, 48, 48, 48, 40, 8, 8] bytes=304 recall=71.244400

SQ_GREEDY_EVAL tag=it30_b2_plus8 alloc=[48, 48, 56, 48, 48, 40, 8, 8] bytes=304 recall=71.256600

SQ_GREEDY_EVAL tag=it30_b3_plus8 alloc=[48, 48, 48, 56, 48, 40, 8, 8] bytes=304 recall=71.234800

SQ_GREEDY_EVAL tag=it30_b4_plus8 alloc=[48, 48, 48, 48, 56, 40, 8, 8] bytes=304 recall=71.277800

SQ_GREEDY_EVAL tag=it30_b5_plus8 alloc=[48, 48, 48, 48, 48, 48, 8, 8] bytes=304 recall=71.472900

SQ_GREEDY_EVAL tag=it30_b6_plus8 alloc=[48, 48, 48, 48, 48, 40, 16, 8] bytes=304 recall=71.439800

SQ_GREEDY_EVAL tag=it30_b7_plus8 alloc=[48, 48, 48, 48, 48, 40, 8, 16] bytes=304 recall=71.414900

SQ_GREEDY_EVAL tag=it31_b0_plus8 alloc=[56, 48, 48, 48, 48, 48, 8, 8] bytes=312 recall=71.922600

SQ_GREEDY_EVAL tag=it31_b1_plus8 alloc=[48, 56, 48, 48, 48, 48, 8, 8] bytes=312 recall=71.750600

SQ_GREEDY_EVAL tag=it31_b2_plus8 alloc=[48, 48, 56, 48, 48, 48, 8, 8] bytes=312 recall=71.786500

SQ_GREEDY_EVAL tag=it31_b3_plus8 alloc=[48, 48, 48, 56, 48, 48, 8, 8] bytes=312 recall=71.764000

SQ_GREEDY_EVAL tag=it31_b4_plus8 alloc=[48, 48, 48, 48, 56, 48, 8, 8] bytes=312 recall=71.801400

SQ_GREEDY_EVAL tag=it31_b5_plus8 alloc=[48, 48, 48, 48, 48, 56, 8, 8] bytes=312 recall=71.705700

SQ_GREEDY_EVAL tag=it31_b6_plus8 alloc=[48, 48, 48, 48, 48, 48, 16, 8] bytes=312 recall=71.976200

SQ_GREEDY_EVAL tag=it31_b7_plus8 alloc=[48, 48, 48, 48, 48, 48, 8, 16] bytes=312 recall=71.928100

SQ_GREEDY_EVAL tag=it32_b0_plus8 alloc=[56, 48, 48, 48, 48, 48, 16, 8] bytes=320 recall=72.419800

SQ_GREEDY_EVAL tag=it32_b1_plus8 alloc=[48, 56, 48, 48, 48, 48, 16, 8] bytes=320 recall=72.262300

SQ_GREEDY_EVAL tag=it32_b2_plus8 alloc=[48, 48, 56, 48, 48, 48, 16, 8] bytes=320 recall=72.288400

SQ_GREEDY_EVAL tag=it32_b3_plus8 alloc=[48, 48, 48, 56, 48, 48, 16, 8] bytes=320 recall=72.251000

SQ_GREEDY_EVAL tag=it32_b4_plus8 alloc=[48, 48, 48, 48, 56, 48, 16, 8] bytes=320 recall=72.277700

SQ_GREEDY_EVAL tag=it32_b5_plus8 alloc=[48, 48, 48, 48, 48, 56, 16, 8] bytes=320 recall=72.174200

SQ_GREEDY_EVAL tag=it32_b6_plus8 alloc=[48, 48, 48, 48, 48, 48, 24, 8] bytes=320 recall=72.373200

SQ_GREEDY_EVAL tag=it32_b7_plus8 alloc=[48, 48, 48, 48, 48, 48, 16, 16] bytes=320 recall=72.393300

SQ_GREEDY_EVAL tag=it33_b0_plus8 alloc=[64, 48, 48, 48, 48, 48, 16, 8] bytes=328 recall=72.881700

SQ_GREEDY_EVAL tag=it33_b1_plus8 alloc=[56, 56, 48, 48, 48, 48, 16, 8] bytes=328 recall=72.718500

SQ_GREEDY_EVAL tag=it33_b2_plus8 alloc=[56, 48, 56, 48, 48, 48, 16, 8] bytes=328 recall=72.718800

SQ_GREEDY_EVAL tag=it33_b3_plus8 alloc=[56, 48, 48, 56, 48, 48, 16, 8] bytes=328 recall=72.710900

SQ_GREEDY_EVAL tag=it33_b4_plus8 alloc=[56, 48, 48, 48, 56, 48, 16, 8] bytes=328 recall=72.748700

SQ_GREEDY_EVAL tag=it33_b5_plus8 alloc=[56, 48, 48, 48, 48, 56, 16, 8] bytes=328 recall=72.654400

SQ_GREEDY_EVAL tag=it33_b6_plus8 alloc=[56, 48, 48, 48, 48, 48, 24, 8] bytes=328 recall=72.797600

SQ_GREEDY_EVAL tag=it33_b7_plus8 alloc=[56, 48, 48, 48, 48, 48, 16, 16] bytes=328 recall=72.862900

SQ_GREEDY_EVAL tag=it34_b0_plus8 alloc=[72, 48, 48, 48, 48, 48, 16, 8] bytes=336 recall=73.149700

SQ_GREEDY_EVAL tag=it34_b1_plus8 alloc=[64, 56, 48, 48, 48, 48, 16, 8] bytes=336 recall=73.168900

SQ_GREEDY_EVAL tag=it34_b2_plus8 alloc=[64, 48, 56, 48, 48, 48, 16, 8] bytes=336 recall=73.205900

SQ_GREEDY_EVAL tag=it34_b3_plus8 alloc=[64, 48, 48, 56, 48, 48, 16, 8] bytes=336 recall=73.169900

SQ_GREEDY_EVAL tag=it34_b4_plus8 alloc=[64, 48, 48, 48, 56, 48, 16, 8] bytes=336 recall=73.208900

SQ_GREEDY_EVAL tag=it34_b5_plus8 alloc=[64, 48, 48, 48, 48, 56, 16, 8] bytes=336 recall=73.115900

SQ_GREEDY_EVAL tag=it34_b6_plus8 alloc=[64, 48, 48, 48, 48, 48, 24, 8] bytes=336 recall=73.256300

SQ_GREEDY_EVAL tag=it34_b7_plus8 alloc=[64, 48, 48, 48, 48, 48, 16, 16] bytes=336 recall=73.336400

SQ_GREEDY_EVAL tag=it35_b0_plus8 alloc=[72, 48, 48, 48, 48, 48, 16, 16] bytes=344 recall=73.599100

SQ_GREEDY_EVAL tag=it35_b1_plus8 alloc=[64, 56, 48, 48, 48, 48, 16, 16] bytes=344 recall=73.628400

SQ_GREEDY_EVAL tag=it35_b2_plus8 alloc=[64, 48, 56, 48, 48, 48, 16, 16] bytes=344 recall=73.642000

SQ_GREEDY_EVAL tag=it35_b3_plus8 alloc=[64, 48, 48, 56, 48, 48, 16, 16] bytes=344 recall=73.625600

SQ_GREEDY_EVAL tag=it35_b4_plus8 alloc=[64, 48, 48, 48, 56, 48, 16, 16] bytes=344 recall=73.657600

SQ_GREEDY_EVAL tag=it35_b5_plus8 alloc=[64, 48, 48, 48, 48, 56, 16, 16] bytes=344 recall=73.558900

SQ_GREEDY_EVAL tag=it35_b6_plus8 alloc=[64, 48, 48, 48, 48, 48, 24, 16] bytes=344 recall=73.744600

SQ_GREEDY_EVAL tag=it35_b7_plus8 alloc=[64, 48, 48, 48, 48, 48, 16, 24] bytes=344 recall=73.735800

SQ_GREEDY_EVAL tag=it36_b0_plus8 alloc=[72, 48, 48, 48, 48, 48, 24, 16] bytes=352 recall=73.947000

SQ_GREEDY_EVAL tag=it36_b1_plus8 alloc=[64, 56, 48, 48, 48, 48, 24, 16] bytes=352 recall=74.000100

SQ_GREEDY_EVAL tag=it36_b2_plus8 alloc=[64, 48, 56, 48, 48, 48, 24, 16] bytes=352 recall=74.018800

SQ_GREEDY_EVAL tag=it36_b3_plus8 alloc=[64, 48, 48, 56, 48, 48, 24, 16] bytes=352 recall=74.020300

SQ_GREEDY_EVAL tag=it36_b4_plus8 alloc=[64, 48, 48, 48, 56, 48, 24, 16] bytes=352 recall=74.025600

SQ_GREEDY_EVAL tag=it36_b5_plus8 alloc=[64, 48, 48, 48, 48, 56, 24, 16] bytes=352 recall=73.955700

SQ_GREEDY_EVAL tag=it36_b6_plus8 alloc=[64, 48, 48, 48, 48, 48, 32, 16] bytes=352 recall=74.261500

SQ_GREEDY_EVAL tag=it36_b7_plus8 alloc=[64, 48, 48, 48, 48, 48, 24, 24] bytes=352 recall=74.124900

SQ_GREEDY_EVAL tag=it37_b0_plus8 alloc=[72, 48, 48, 48, 48, 48, 32, 16] bytes=360 recall=74.500700

SQ_GREEDY_EVAL tag=it37_b1_plus8 alloc=[64, 56, 48, 48, 48, 48, 32, 16] bytes=360 recall=74.550900

SQ_GREEDY_EVAL tag=it37_b2_plus8 alloc=[64, 48, 56, 48, 48, 48, 32, 16] bytes=360 recall=74.559300

SQ_GREEDY_EVAL tag=it37_b3_plus8 alloc=[64, 48, 48, 56, 48, 48, 32, 16] bytes=360 recall=74.536100

SQ_GREEDY_EVAL tag=it37_b4_plus8 alloc=[64, 48, 48, 48, 56, 48, 32, 16] bytes=360 recall=74.561600

SQ_GREEDY_EVAL tag=it37_b5_plus8 alloc=[64, 48, 48, 48, 48, 56, 32, 16] bytes=360 recall=74.468500

SQ_GREEDY_EVAL tag=it37_b6_plus8 alloc=[64, 48, 48, 48, 48, 48, 40, 16] bytes=360 recall=74.639800

SQ_GREEDY_EVAL tag=it37_b7_plus8 alloc=[64, 48, 48, 48, 48, 48, 32, 24] bytes=360 recall=74.670800

SQ_GREEDY_EVAL tag=it38_b0_plus8 alloc=[72, 48, 48, 48, 48, 48, 32, 24] bytes=368 recall=74.889700

SQ_GREEDY_EVAL tag=it38_b1_plus8 alloc=[64, 56, 48, 48, 48, 48, 32, 24] bytes=368 recall=74.930700

SQ_GREEDY_EVAL tag=it38_b2_plus8 alloc=[64, 48, 56, 48, 48, 48, 32, 24] bytes=368 recall=74.987100

SQ_GREEDY_EVAL tag=it38_b3_plus8 alloc=[64, 48, 48, 56, 48, 48, 32, 24] bytes=368 recall=74.941300

SQ_GREEDY_EVAL tag=it38_b4_plus8 alloc=[64, 48, 48, 48, 56, 48, 32, 24] bytes=368 recall=74.938100

SQ_GREEDY_EVAL tag=it38_b5_plus8 alloc=[64, 48, 48, 48, 48, 56, 32, 24] bytes=368 recall=74.848900

SQ_GREEDY_EVAL tag=it38_b6_plus8 alloc=[64, 48, 48, 48, 48, 48, 40, 24] bytes=368 recall=75.078800

SQ_GREEDY_EVAL tag=it38_b7_plus8 alloc=[64, 48, 48, 48, 48, 48, 32, 32] bytes=368 recall=75.144300

SQ_GREEDY_EVAL tag=it39_b0_plus8 alloc=[72, 48, 48, 48, 48, 48, 32, 32] bytes=376 recall=75.381100

SQ_GREEDY_EVAL tag=it39_b1_plus8 alloc=[64, 56, 48, 48, 48, 48, 32, 32] bytes=376 recall=75.444400

SQ_GREEDY_EVAL tag=it39_b2_plus8 alloc=[64, 48, 56, 48, 48, 48, 32, 32] bytes=376 recall=75.453700

SQ_GREEDY_EVAL tag=it39_b3_plus8 alloc=[64, 48, 48, 56, 48, 48, 32, 32] bytes=376 recall=75.431900

SQ_GREEDY_EVAL tag=it39_b4_plus8 alloc=[64, 48, 48, 48, 56, 48, 32, 32] bytes=376 recall=75.429400

SQ_GREEDY_EVAL tag=it39_b5_plus8 alloc=[64, 48, 48, 48, 48, 56, 32, 32] bytes=376 recall=75.356300

SQ_GREEDY_EVAL tag=it39_b6_plus8 alloc=[64, 48, 48, 48, 48, 48, 40, 32] bytes=376 recall=75.569100

SQ_GREEDY_EVAL tag=it39_b7_plus8 alloc=[64, 48, 48, 48, 48, 48, 32, 40] bytes=376 recall=75.529800

SQ_GREEDY_EVAL tag=it40_b0_plus8 alloc=[72, 48, 48, 48, 48, 48, 40, 32] bytes=384 recall=75.788400

SQ_GREEDY_EVAL tag=it40_b1_plus8 alloc=[64, 56, 48, 48, 48, 48, 40, 32] bytes=384 recall=75.821900

SQ_GREEDY_EVAL tag=it40_b2_plus8 alloc=[64, 48, 56, 48, 48, 48, 40, 32] bytes=384 recall=75.870900

SQ_GREEDY_EVAL tag=it40_b3_plus8 alloc=[64, 48, 48, 56, 48, 48, 40, 32] bytes=384 recall=75.871200

SQ_GREEDY_EVAL tag=it40_b4_plus8 alloc=[64, 48, 48, 48, 56, 48, 40, 32] bytes=384 recall=75.859200

SQ_GREEDY_EVAL tag=it40_b5_plus8 alloc=[64, 48, 48, 48, 48, 56, 40, 32] bytes=384 recall=75.753900

SQ_GREEDY_EVAL tag=it40_b6_plus8 alloc=[64, 48, 48, 48, 48, 48, 48, 32] bytes=384 recall=76.150700

SQ_GREEDY_EVAL tag=it40_b7_plus8 alloc=[64, 48, 48, 48, 48, 48, 40, 40] bytes=384 recall=75.970300
