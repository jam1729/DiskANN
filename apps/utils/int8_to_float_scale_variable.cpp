// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.

#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include "utils.h"

void block_convert(std::ofstream &writer, float *write_buf, std::ifstream &reader, int8_t *read_buf, size_t npts,
                   size_t ndims, const std::vector<float> &bias, const std::vector<float> &scale)
{
    reader.read((char *)read_buf, npts * ndims * sizeof(int8_t));

    for (size_t i = 0; i < npts; i++)
    {
        for (size_t d = 0; d < ndims; d++)
        {
            // 1. Cast the signed byte to unsigned uint8_t to reverse C++ wrap-around
            uint8_t y_unsigned = (uint8_t)read_buf[d + i * ndims];

            // 2. Reconstruct the float using our direct scale and bias formula
            write_buf[d + i * ndims] = (((float)y_unsigned / 254.0f) * scale[d]) + bias[d];
        }
    }
    writer.write((char *)write_buf, npts * ndims * sizeof(float));
}

int main(int argc, char **argv)
{
    if (argc != 4)
    {
        std::cout << "Usage: " << argv[0] << "  input-int8.bin  output-float.bin  sq_calibration.bin" << std::endl;
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
    std::vector<uint8_t> bit_widths(ndims); // Read but not needed for dequantization

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

    auto read_buf = new int8_t[blk_size * ndims];
    auto write_buf = new float[blk_size * ndims];

    writer.write((char *)(&npts_u32), sizeof(uint32_t));
    writer.write((char *)(&ndims_u32), sizeof(uint32_t));

    for (size_t i = 0; i < nblks; i++)
    {
        size_t cblk_size = std::min(npts - i * blk_size, blk_size);
        block_convert(writer, write_buf, reader, read_buf, cblk_size, ndims, bias, scale);
        std::cout << "Block #" << i << " written" << std::endl;
    }

    delete[] read_buf;
    delete[] write_buf;

    writer.close();
    reader.close();
    std::cout << "Dequantization completed successfully." << std::endl;
}
