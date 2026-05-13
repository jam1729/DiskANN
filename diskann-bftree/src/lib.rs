/*
 * Copyright (c) Microsoft Corporation.
 * Licensed under the MIT license.
 */

//! BfTree-based data provider for DiskANN async indexes.
//!
//! This crate provides a [`BfTree`](bf_tree::BfTree)-backed implementation of the DiskANN
//! [`DataProvider`](diskann::provider::DataProvider) trait, enabling indexes that can
//! transparently spill to disk for datasets larger than available memory.

pub mod provider;
