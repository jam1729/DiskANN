/*
 * Copyright (c) Microsoft Corporation.
 * Licensed under the MIT license.
 */

use std::{future::Future, sync::Arc};

use diskann::default_post_processor;
use diskann::{
    ANNError, ANNResult,
    graph::{
        AdjacencyList,
        glue::{
            self, DefaultPostProcessor, ExpandBeam, InplaceDeleteStrategy, InsertStrategy,
            PruneStrategy, SearchExt, SearchStrategy,
        },
        workingset,
    },
    provider::{
        Accessor, BuildDistanceComputer, BuildQueryComputer, DelegateNeighbor, ExecutionContext,
        HasId,
    },
    utils::{IntoUsize, VectorRepr},
};
use diskann_utils::future::AsyncFriendly;
use diskann_vector::{PreprocessedDistanceFunction, distance::Metric};

use crate::model::{
    graph::provider::async_::{
        FastMemoryQuantVectorProviderAsync, FastMemoryVectorProviderAsync,
        SimpleNeighborProviderAsync,
        common::{
            CreateVectorStore, Hybrid, NoStore, Panics, Quantized, SetElementHelper, Unseeded,
            VectorStore,
        },
        distances,
        inmem::{
            DefaultProvider, FullPrecisionProvider, FullPrecisionStore, GetFullPrecision,
            PassThrough, Rerank,
        },
        postprocess::{AsDeletionCheck, DeletionCheck, RemoveDeletedIdsAndCopy},
    },
    pq::{self, FixedChunkPQTable},
};

/// The default quant provider.
pub type DefaultQuant = FastMemoryQuantVectorProviderAsync;

impl CreateVectorStore for FixedChunkPQTable {
    type Target = DefaultQuant;
    fn create(
        self,
        max_points: usize,
        metric: Metric,
        _prefetch_lookahead: Option<usize>,
    ) -> Self::Target {
        DefaultQuant::new(metric, max_points, self)
    }
}

impl VectorStore for DefaultQuant {
    fn total(&self) -> usize {
        self.total()
    }

    fn count_for_get_vector(&self) -> usize {
        self.num_get_calls.get()
    }
}

////////////////
// SetElement //
////////////////

/// Assign to PQ vector store.
impl<T> SetElementHelper<T> for DefaultQuant
where
    T: VectorRepr,
{
    fn set_element(&self, id: &u32, element: &[T]) -> ANNResult<()> {
        unsafe { self.set_vector_sync(id.into_usize(), element) }
    }
}

///////////////////
// QuantAccessor //
///////////////////

/// An accessor that retrieves the quantized portion of the [`DefaultProvider`].
///
/// This type implements the following traits:
///
/// * [`Accessor`] for the `DefaultProvider`.
/// * [`BuildQueryComputer`].
pub struct QuantAccessor<'a, V, D, Ctx> {
    provider: &'a DefaultProvider<V, DefaultQuant, D, Ctx>,
}

impl<T, D, Ctx> GetFullPrecision for QuantAccessor<'_, FullPrecisionStore<T>, D, Ctx>
where
    T: VectorRepr,
{
    type Repr = T;
    fn as_full_precision(&self) -> &FastMemoryVectorProviderAsync<T> {
        &self.provider.base_vectors
    }
}

impl<V, D, Ctx> HasId for QuantAccessor<'_, V, D, Ctx> {
    type Id = u32;
}

impl<V, D, Ctx, T> SearchExt<&[T]> for QuantAccessor<'_, V, D, Ctx>
where
    T: VectorRepr,
    V: AsyncFriendly,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    fn starting_points(&self) -> impl Future<Output = ANNResult<Vec<u32>>> {
        std::future::ready(self.provider.starting_points())
    }

    fn start_point_distances<F>(
        &mut self,
        computer: &Self::QueryComputer,
        mut f: F,
    ) -> impl std::future::Future<Output = ANNResult<()>> + Send
    where
        F: FnMut(Self::Id, f32) + Send,
    {
        async move {
            for i in self.provider.starting_points()? {
                // SAFETY: We're accepting the consequences of potential unsynchronized,
                // concurrent mutation.
                let distance = computer.evaluate_similarity(unsafe {
                    self.provider.aux_vectors.get_vector_sync(i.into_usize())
                });

                f(i, distance);
            }
            Ok(())
        }
    }
}

impl<'a, V, D, Ctx> QuantAccessor<'a, V, D, Ctx>
where
    V: AsyncFriendly,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    pub(crate) fn new(provider: &'a DefaultProvider<V, DefaultQuant, D, Ctx>) -> Self {
        Self { provider }
    }
}

impl<'a, V, D, Ctx> DelegateNeighbor<'a> for QuantAccessor<'_, V, D, Ctx>
where
    V: AsyncFriendly,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    type Delegate = &'a SimpleNeighborProviderAsync<u32>;
    fn delegate_neighbor(&'a mut self) -> Self::Delegate {
        self.provider.neighbors()
    }
}

impl<V, D, Ctx> Accessor for QuantAccessor<'_, V, D, Ctx>
where
    V: AsyncFriendly,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    /// `ElementRef` has an arbitrarily short lifetime.
    type ElementRef<'a> = &'a [u8];
}

impl<T, V, D, Ctx> BuildQueryComputer<&[T]> for QuantAccessor<'_, V, D, Ctx>
where
    T: VectorRepr,
    V: AsyncFriendly,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    type QueryComputerError = ANNError;
    type QueryComputer = pq::distance::QueryComputer<Arc<FixedChunkPQTable>>;

    fn build_query_computer(
        &self,
        from: &[T],
    ) -> Result<Self::QueryComputer, Self::QueryComputerError> {
        self.provider.aux_vectors.query_computer(from)
    }
}

impl<V, D, Ctx> BuildDistanceComputer for QuantAccessor<'_, V, D, Ctx>
where
    V: AsyncFriendly,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    type DistanceComputerError = ANNError;
    type DistanceComputer = pq::distance::DistanceComputer<Arc<FixedChunkPQTable>>;

    fn build_distance_computer(
        &self,
    ) -> Result<Self::DistanceComputer, Self::DistanceComputerError> {
        Ok(self.provider.aux_vectors.distance_computer())
    }
}

impl<T, V, D, Ctx> ExpandBeam<&[T]> for QuantAccessor<'_, V, D, Ctx>
where
    T: VectorRepr,
    V: AsyncFriendly,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    fn expand_beam<Itr, P, F>(
        &mut self,
        ids: Itr,
        computer: &Self::QueryComputer,
        mut pred: P,
        mut on_neighbors: F,
    ) -> impl std::future::Future<Output = ANNResult<()>> + Send
    where
        Itr: Iterator<Item = Self::Id> + Send,
        P: glue::HybridPredicate<Self::Id> + Send + Sync,
        F: FnMut(f32, Self::Id) + Send,
    {
        let f = move || -> ANNResult<()> {
            let mut neighbors = AdjacencyList::new();
            for n in ids {
                self.provider
                    .neighbor_provider
                    .get_neighbors_sync(n.into_usize(), &mut neighbors)?;
                for i in neighbors.iter().filter(|i| pred.eval_mut(i)) {
                    // SAFETY: We're accepting the consequences of potential unsynchronized,
                    // concurrent mutation.
                    let distance = computer.evaluate_similarity(unsafe {
                        self.provider.aux_vectors.get_vector_sync(i.into_usize())
                    });

                    on_neighbors(distance, *i);
                }
            }
            Ok(())
        };

        std::future::ready(f())
    }
}

//-------------------//
// In-mem Extensions //
//-------------------//

impl<'a, V, D, Ctx> AsDeletionCheck for QuantAccessor<'a, V, D, Ctx>
where
    V: AsyncFriendly,
    D: AsyncFriendly + DeletionCheck,
    Ctx: ExecutionContext,
{
    type Checker = D;
    fn as_deletion_check(&self) -> &D {
        &self.provider.deleted
    }
}

/////////////////////
// Hybrid Accessor //
/////////////////////

/// A hybrid accessor that fetches a mixture of full-precision and quantized vectors during
/// pruning. This allows the application to trade full-precision fetches for accuracy.
///
/// This type implements the following traits:
///
/// * [`Accessor`] for the [`DefaultProvider`].
/// * [`BuildDistanceComputer`] for computing distances among [`distances::pq::Hybrid`]
///   element types.
/// * [`Fill`] for populating a mixture of full-precision and quant vectors.
pub struct HybridAccessor<'a, T, D, Ctx>
where
    T: VectorRepr,
{
    provider: &'a FullPrecisionProvider<T, DefaultQuant, D, Ctx>,

    /// Maximum number of full-precision vectors to use during pruning.
    /// This field is ignored during search, where full-precision vectors are never used.
    max_fp_vecs_per_prune: usize,
}

impl<'a, T, D, Ctx> HybridAccessor<'a, T, D, Ctx>
where
    T: VectorRepr,
{
    fn new(
        provider: &'a FullPrecisionProvider<T, DefaultQuant, D, Ctx>,
        max_fp_vecs_per_prune: usize,
    ) -> Self {
        Self {
            provider,
            max_fp_vecs_per_prune,
        }
    }
}

impl<T, D, Ctx> HasId for HybridAccessor<'_, T, D, Ctx>
where
    T: VectorRepr,
{
    type Id = u32;
}

impl<'a, T, D, Ctx> DelegateNeighbor<'a> for HybridAccessor<'_, T, D, Ctx>
where
    T: VectorRepr,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    type Delegate = &'a SimpleNeighborProviderAsync<u32>;
    fn delegate_neighbor(&'a mut self) -> Self::Delegate {
        self.provider.neighbors()
    }
}

impl<T, D, Ctx> Accessor for HybridAccessor<'_, T, D, Ctx>
where
    T: VectorRepr,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    /// `ElementRef` has an arbitrarily short lifetime.
    type ElementRef<'a> = distances::pq::Hybrid<&'a [T], &'a [u8]>;
}

impl<T, D, Ctx> BuildDistanceComputer for HybridAccessor<'_, T, D, Ctx>
where
    T: VectorRepr,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    type DistanceComputerError = ANNError;
    type DistanceComputer = distances::pq::HybridComputer<T>;

    fn build_distance_computer(
        &self,
    ) -> Result<Self::DistanceComputer, Self::DistanceComputerError> {
        let metric = self.provider.aux_vectors.metric();
        Ok(distances::pq::HybridComputer::new(
            self.provider.aux_vectors.distance_computer(),
            T::distance(metric, Some(self.provider.base_vectors.dim())),
        ))
    }
}

/// Tracks which IDs should use full-precision vectors during hybrid pruning.
///
/// IDs in the set get full-precision distance computations; all others fall back to
/// quantized vectors.
pub struct FullPrecisionTracker(hashbrown::HashSet<u32>);

impl workingset::AsWorkingSet<FullPrecisionTracker> for Unseeded {
    fn as_working_set(&self, capacity: usize) -> FullPrecisionTracker {
        FullPrecisionTracker(hashbrown::HashSet::with_capacity(capacity))
    }
}

// Selective fill — the first `max_fp_vecs_per_prune` candidates receive full-precision
// vectors; the remainder are accessed through the pass-through `MaybeFullPrecision` view.
impl<T, D, Ctx> workingset::Fill<FullPrecisionTracker> for HybridAccessor<'_, T, D, Ctx>
where
    T: VectorRepr,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    type Error = std::convert::Infallible;
    type View<'a>
        = MaybeFullPrecision<'a, T, D, Ctx>
    where
        Self: 'a;

    async fn fill<'a, Itr>(
        &'a mut self,
        state: &'a mut FullPrecisionTracker,
        itr: Itr,
    ) -> Result<Self::View<'a>, Self::Error>
    where
        Itr: ExactSizeIterator<Item = Self::Id> + Clone + Send + Sync,
        Self: 'a,
    {
        state.0.clear();
        state.0.extend(itr.take(self.max_fp_vecs_per_prune));
        Ok(MaybeFullPrecision {
            accessor: self,
            full: state,
        })
    }
}

pub struct MaybeFullPrecision<'a, T, D, Ctx>
where
    T: VectorRepr,
{
    accessor: &'a HybridAccessor<'a, T, D, Ctx>,
    full: &'a FullPrecisionTracker,
}

impl<T, D, Ctx> workingset::View<u32> for MaybeFullPrecision<'_, T, D, Ctx>
where
    T: VectorRepr,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    type ElementRef<'a> = distances::pq::Hybrid<&'a [T], &'a [u8]>;
    type Element<'a>
        = distances::pq::Hybrid<&'a [T], &'a [u8]>
    where
        Self: 'a;

    fn get(&self, id: u32) -> Option<Self::Element<'_>> {
        let provider = &self.accessor.provider;
        let element = if self.full.0.contains(&id) {
            // SAFETY: This is unsound. We assume no concurrent writes to this slot, but
            // this invariant is not enforced. See `get_vector_sync` for details.
            unsafe {
                distances::pq::Hybrid::Full(provider.base_vectors.get_vector_sync(id.into_usize()))
            }
        } else {
            // SAFETY: This is unsound. We assume no concurrent writes to this slot, but
            // this invariant is not enforced. See `get_vector_sync` for details.
            unsafe {
                distances::pq::Hybrid::Quant(provider.aux_vectors.get_vector_sync(id.into_usize()))
            }
        };
        Some(element)
    }
}

// Pass-through fill — returns `&Self` which directly accesses the underlying provider.
impl<V, D, Ctx> workingset::Fill<PassThrough> for QuantAccessor<'_, V, D, Ctx>
where
    V: AsyncFriendly,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    type Error = std::convert::Infallible;
    type View<'a>
        = &'a Self
    where
        Self: 'a;

    async fn fill<'a, Itr>(
        &'a mut self,
        _state: &'a mut PassThrough,
        _itr: Itr,
    ) -> Result<Self::View<'a>, Self::Error>
    where
        Itr: ExactSizeIterator<Item = Self::Id> + Clone + Send + Sync,
        Self: 'a,
    {
        Ok(self)
    }
}

// Pass-through view — reads PQ codes directly from the provider.
impl<V, D, Ctx> workingset::View<u32> for &QuantAccessor<'_, V, D, Ctx>
where
    V: AsyncFriendly,
    D: AsyncFriendly,
    Ctx: ExecutionContext,
{
    type ElementRef<'a> = &'a [u8];
    type Element<'a>
        = &'a [u8]
    where
        Self: 'a;

    fn get(&self, id: u32) -> Option<&[u8]> {
        // SAFETY: This is unsound. We assume no concurrent writes to this slot, but
        // this invariant is not enforced. See `get_vector_sync` for details.
        Some(unsafe { self.provider.aux_vectors.get_vector_sync(id.into_usize()) })
    }
}

////////////////
// Strategies //
////////////////

////////////
// Hybrid //
////////////

/// Perform a search entirely in the quantized space.
impl<T, D, Ctx> SearchStrategy<FullPrecisionProvider<T, DefaultQuant, D, Ctx>, &[T]> for Hybrid
where
    T: VectorRepr,
    D: AsyncFriendly + DeletionCheck,
    Ctx: ExecutionContext,
{
    type QueryComputer = pq::distance::QueryComputer<Arc<FixedChunkPQTable>>;
    type SearchAccessor<'a> = QuantAccessor<'a, FullPrecisionStore<T>, D, Ctx>;
    type SearchAccessorError = Panics;

    fn search_accessor<'a>(
        &'a self,
        provider: &'a FullPrecisionProvider<T, DefaultQuant, D, Ctx>,
        _context: &'a Ctx,
    ) -> Result<Self::SearchAccessor<'a>, Self::SearchAccessorError> {
        Ok(QuantAccessor::new(provider))
    }
}

/// Starting points are filtered out of the final results and results are reranked using
/// the full-precision data.
impl<T, D, Ctx> DefaultPostProcessor<FullPrecisionProvider<T, DefaultQuant, D, Ctx>, &[T]>
    for Hybrid
where
    T: VectorRepr,
    D: AsyncFriendly + DeletionCheck,
    Ctx: ExecutionContext,
{
    default_post_processor!(glue::Pipeline<glue::FilterStartPoints, Rerank>);
}

impl<T, D, Ctx> PruneStrategy<FullPrecisionProvider<T, DefaultQuant, D, Ctx>> for Hybrid
where
    T: VectorRepr,
    D: AsyncFriendly + DeletionCheck,
    Ctx: ExecutionContext,
{
    type DistanceComputer<'a> = distances::pq::HybridComputer<T>;
    type PruneAccessor<'a> = HybridAccessor<'a, T, D, Ctx>;
    type PruneAccessorError = diskann::error::Infallible;
    type WorkingSet = FullPrecisionTracker;

    fn create_working_set(&self, capacity: usize) -> Self::WorkingSet {
        FullPrecisionTracker(hashbrown::HashSet::with_capacity(capacity))
    }

    fn prune_accessor<'a>(
        &'a self,
        provider: &'a FullPrecisionProvider<T, DefaultQuant, D, Ctx>,
        _context: &'a Ctx,
    ) -> Result<Self::PruneAccessor<'a>, Self::PruneAccessorError> {
        Ok(HybridAccessor::new(
            provider,
            self.max_fp_vecs_per_prune.unwrap_or(usize::MAX),
        ))
    }
}

impl<T, D, Ctx> InsertStrategy<FullPrecisionProvider<T, DefaultQuant, D, Ctx>, &[T]> for Hybrid
where
    T: VectorRepr,
    D: AsyncFriendly + DeletionCheck,
    Ctx: ExecutionContext,
{
    type PruneStrategy = Self;
    fn prune_strategy(&self) -> Self::PruneStrategy {
        *self
    }
}

impl<T, D, Ctx, B> glue::MultiInsertStrategy<FullPrecisionProvider<T, DefaultQuant, D, Ctx>, B>
    for Hybrid
where
    T: VectorRepr,
    D: AsyncFriendly + DeletionCheck,
    Ctx: ExecutionContext,
    B: glue::Batch,
    Self: for<'a> InsertStrategy<
            FullPrecisionProvider<T, DefaultQuant, D, Ctx>,
            B::Element<'a>,
            PruneStrategy = Self,
        >,
{
    type Seed = Unseeded;
    type WorkingSet = FullPrecisionTracker;
    type FinishError = diskann::error::Infallible;
    type InsertStrategy = Self;

    fn insert_strategy(&self) -> Self::InsertStrategy {
        *self
    }

    fn finish<Itr>(
        &self,
        _provider: &FullPrecisionProvider<T, DefaultQuant, D, Ctx>,
        _ctx: &Ctx,
        _batch: &std::sync::Arc<B>,
        _ids: Itr,
    ) -> impl std::future::Future<Output = Result<Self::Seed, Self::FinishError>> + Send
    where
        Itr: ExactSizeIterator<Item = u32> + Send,
    {
        std::future::ready(Ok(Unseeded))
    }
}

/// Inplace Delete
impl<T, D, Ctx> InplaceDeleteStrategy<FullPrecisionProvider<T, DefaultQuant, D, Ctx>> for Hybrid
where
    T: VectorRepr,
    D: AsyncFriendly + DeletionCheck,
    Ctx: ExecutionContext,
{
    type DeleteElementError = Panics;
    type DeleteElement<'a> = &'a [T];
    type DeleteElementGuard = Box<[T]>;
    type PruneStrategy = Self;
    type DeleteSearchAccessor<'a> = QuantAccessor<'a, FullPrecisionStore<T>, D, Ctx>;
    type SearchPostProcessor = Rerank;
    type SearchStrategy = Self;
    fn search_strategy(&self) -> Self::SearchStrategy {
        *self
    }

    fn prune_strategy(&self) -> Self::PruneStrategy {
        *self
    }

    fn search_post_processor(&self) -> Self::SearchPostProcessor {
        Rerank
    }

    async fn get_delete_element<'a>(
        &'a self,
        provider: &'a FullPrecisionProvider<T, DefaultQuant, D, Ctx>,
        _context: &'a Ctx,
        id: u32,
    ) -> Result<Self::DeleteElementGuard, Self::DeleteElementError> {
        Ok(unsafe { provider.base_vectors.get_vector_sync(id.into_usize()) }.into())
    }
}

///////////////
// Quantized //
///////////////

/// Perform a search entirely in the quantized space.
///
/// Starting points are filtered out of the final results.
impl<T, D, Ctx> SearchStrategy<DefaultProvider<NoStore, DefaultQuant, D, Ctx>, &[T]> for Quantized
where
    T: VectorRepr,
    D: AsyncFriendly + DeletionCheck,
    Ctx: ExecutionContext,
{
    type QueryComputer = pq::distance::QueryComputer<Arc<FixedChunkPQTable>>;
    type SearchAccessor<'a> = QuantAccessor<'a, NoStore, D, Ctx>;
    type SearchAccessorError = Panics;

    fn search_accessor<'a>(
        &'a self,
        provider: &'a DefaultProvider<NoStore, DefaultQuant, D, Ctx>,
        _context: &'a Ctx,
    ) -> Result<Self::SearchAccessor<'a>, Self::SearchAccessorError> {
        Ok(QuantAccessor::new(provider))
    }
}

impl<T, D, Ctx> DefaultPostProcessor<DefaultProvider<NoStore, DefaultQuant, D, Ctx>, &[T]>
    for Quantized
where
    T: VectorRepr,
    D: AsyncFriendly + DeletionCheck,
    Ctx: ExecutionContext,
{
    default_post_processor!(glue::Pipeline<glue::FilterStartPoints, RemoveDeletedIdsAndCopy>);
}

impl<D, Ctx> PruneStrategy<DefaultProvider<NoStore, DefaultQuant, D, Ctx>> for Quantized
where
    D: AsyncFriendly + DeletionCheck,
    Ctx: ExecutionContext,
{
    type DistanceComputer<'a> = pq::distance::DistanceComputer<Arc<FixedChunkPQTable>>;
    type PruneAccessor<'a> = QuantAccessor<'a, NoStore, D, Ctx>;
    type PruneAccessorError = diskann::error::Infallible;
    type WorkingSet = PassThrough;

    fn create_working_set(&self, _capacity: usize) -> Self::WorkingSet {
        PassThrough
    }

    fn prune_accessor<'a>(
        &'a self,
        provider: &'a DefaultProvider<NoStore, DefaultQuant, D, Ctx>,
        _context: &'a Ctx,
    ) -> Result<Self::PruneAccessor<'a>, Self::PruneAccessorError> {
        Ok(QuantAccessor::new(provider))
    }
}

impl<T, D, Ctx> InsertStrategy<DefaultProvider<NoStore, DefaultQuant, D, Ctx>, &[T]> for Quantized
where
    T: VectorRepr,
    D: AsyncFriendly + DeletionCheck,
    Ctx: ExecutionContext,
{
    type PruneStrategy = Self;
    fn prune_strategy(&self) -> Self::PruneStrategy {
        *self
    }
}

impl<D, Ctx, B> glue::MultiInsertStrategy<DefaultProvider<NoStore, DefaultQuant, D, Ctx>, B>
    for Quantized
where
    D: AsyncFriendly + DeletionCheck,
    Ctx: ExecutionContext,
    B: glue::Batch,
    Self: for<'a> InsertStrategy<
            DefaultProvider<NoStore, DefaultQuant, D, Ctx>,
            B::Element<'a>,
            PruneStrategy = Self,
        >,
{
    type Seed = PassThrough;
    type WorkingSet = PassThrough;
    type FinishError = diskann::error::Infallible;
    type InsertStrategy = Self;

    fn insert_strategy(&self) -> Self::InsertStrategy {
        *self
    }

    fn finish<Itr>(
        &self,
        _provider: &DefaultProvider<NoStore, DefaultQuant, D, Ctx>,
        _ctx: &Ctx,
        _batch: &std::sync::Arc<B>,
        _ids: Itr,
    ) -> impl std::future::Future<Output = Result<Self::Seed, Self::FinishError>> + Send
    where
        Itr: ExactSizeIterator<Item = u32> + Send,
    {
        std::future::ready(Ok(PassThrough))
    }
}
