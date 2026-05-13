/*
 * Copyright (c) Microsoft Corporation.
 * Licensed under the MIT license.
 */

//! BfTree-based data provider for DiskANN async indexes.
//!
//! This crate provides a [`BfTree`](bf_tree::BfTree)-backed implementation of the DiskANN
//! [`DataProvider`](diskann::provider::DataProvider) trait, enabling indexes that can
//! transparently spill to disk for datasets larger than available memory.

pub mod neighbors;
pub mod provider;
pub mod quant;
pub mod vectors;

// Accessors
pub use provider::{
    AsVectorDtype, BfTreePaths, BfTreeProvider, BfTreeProviderParameters, CreateQuantProvider,
    FullAccessor, GraphParams, Hidden, QuantAccessor, StartPoint, VectorDtype,
};

pub use bf_tree::Config;

use diskann::ANNError;

/// Wrapper around [`bf_tree::ConfigError`] that implements [`std::error::Error`].
#[derive(Debug, Clone)]
pub struct ConfigError(pub bf_tree::ConfigError);

impl std::fmt::Display for ConfigError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "BfTree configuration error: {:?}", self.0)
    }
}

impl std::error::Error for ConfigError {}

impl From<ConfigError> for ANNError {
    #[track_caller]
    #[inline(never)]
    fn from(error: ConfigError) -> ANNError {
        ANNError::new(diskann::ANNErrorKind::IndexError, error)
    }
}

trait AsKey {
    fn as_key(&self) -> &[u8];
}

impl AsKey for usize {
    fn as_key(&self) -> &[u8] {
        bytemuck::bytes_of(self)
    }
}
