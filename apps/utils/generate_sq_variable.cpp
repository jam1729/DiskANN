// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.

#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include <cmath>
#include "utils.h"

void block_convert(std::ofstream &writer, int8_t *write_buf, std::ifstream &reader, float *read_buf, size_t npts,
                   size_t ndims, const std::vector<float> &bias, const std::vector<float> &scale,
                   const std::vector<uint8_t> &bit_widths)
{
    reader.read((char *)read_buf, npts * ndims * sizeof(float));

    for (size_t i = 0; i < npts; i++)
    {
        for (size_t d = 0; d < ndims; d++)
        {
            float val = read_buf[d + i * ndims];
            float current_scale = scale[d];
            if (current_scale <= 1e-9f)
            {
                current_scale = 1.0f;
            }

            // 1. Map to continuous range [0, 254] (exact DiskANN SQ formulation)
            float scaled_val = (val - bias[d]) * (254.0f / current_scale);
            int32_t quantized = (int32_t)std::round(scaled_val);
            quantized = std::max(0, std::min(254, quantized));

            // 2. Precision Truncation based on bit width
            uint8_t w = bit_widths[d];
            if (w == 0)
            {
                // Pruned dimension: map to midpoint
                quantized = 128;
            }
            else if (w == 2)
            {
                // 2 bits: 4 levels spaced by 64 (0, 64, 128, 192)
                quantized = (int32_t)std::round(quantized / 64.0f) * 64;
                quantized = std::max(0, std::min(192, quantized));
            }
            else if (w == 4)
            {
                // 4 bits: 16 levels spaced by 16 (0, 16, 32, ..., 240)
                quantized = (int32_t)std::round(quantized / 16.0f) * 16;
                quantized = std::max(0, std::min(240, quantized));
            }
            // If w == 8, keep full 8-bit precision (no truncation)

            // 3. Cast directly to int8_t (exact C++ wrap-around matching float_bin_to_int8.cpp)
            write_buf[d + i * ndims] = (int8_t)quantized;
        }
    }
    writer.write((char *)write_buf, npts * ndims);
}

int main(int argc, char **argv)
{
    if (argc != 4)
    {
        std::cout << "Usage: " << argv[0] << "  input_float.bin  output_int8.bin  sq_calibration.bin" << std::endl;
        exit(-1);
    }

    std::ifstream reader(argv[1], std::ios::binary);
    if (!reader.is_open())
    {
        std::cerr << "Error opening input file: " << argv[1] << std::endl;
        exit(-1);
    }

    uint32_t npts_u32;
    uint32_t ndims_u32;
    reader.read((char *)&npts_u32, sizeof(uint32_t));
    reader.read((char *)&ndims_u32, sizeof(uint32_t));
    size_t npts = npts_u32;
    size_t ndims = ndims_u32;
    std::cout << "Dataset: #pts = " << npts << ", # dims = " << ndims << std::endl;

    // Load calibration file
    std::ifstream cal_reader(argv[3], std::ios::binary);
    if (!cal_reader.is_open())
    {
        std::cerr << "Error opening calibration file: " << argv[3] << std::endl;
        exit(-1);
    }

    uint32_t cal_dims_u32;
    cal_reader.read((char *)&cal_dims_u32, sizeof(uint32_t));
    if (cal_dims_u32 != ndims_u32)
    {
        std::cerr << "Error: Dimension mismatch between input dataset (" << ndims_u32 
                  << ") and calibration file (" << cal_dims_u32 << ")" << std::endl;
        exit(-1);
    }

    std::vector<float> bias(ndims);
    std::vector<float> scale(ndims);
    std::vector<uint8_t> bit_widths(ndims);

    cal_reader.read((char *)bias.data(), ndims * sizeof(float));
    cal_reader.read((char *)scale.data(), ndims * sizeof(float));
    cal_reader.read((char *)bit_widths.data(), ndims * sizeof(uint8_t));
    cal_reader.close();

    size_t blk_size = 131072;
    size_t nblks = ROUND_UP(npts, blk_size) / blk_size;

    std::ofstream writer(argv[2], std::ios::binary);
    if (!writer.is_open())
    {
        std::cerr << "Error opening output file: " << argv[2] << std::endl;
        exit(-1);
    }

    auto read_buf = new float[blk_size * ndims];
    auto write_buf = new int8_t[blk_size * ndims];

    writer.write((char *)(&npts_u32), sizeof(uint32_t));
    writer.write((char *)(&ndims_u32), sizeof(uint32_t));

    for (size_t i = 0; i < nblks; i++)
    {
        size_t cblk_size = std::min(npts - i * blk_size, blk_size);
        block_convert(writer, write_buf, reader, read_buf, cblk_size, ndims, bias, scale, bit_widths);
        std::cout << "Block #" << i << " written" << std::endl;
    }

    delete[] read_buf;
    delete[] write_buf;

    writer.close();
    reader.close();
    std::cout << "Quantization completed successfully." << std::endl;
}
