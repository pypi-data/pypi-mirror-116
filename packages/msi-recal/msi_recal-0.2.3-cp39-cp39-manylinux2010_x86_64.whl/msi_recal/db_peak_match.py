import logging
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

from msi_recal.join_by_mz import join_by_mz
from msi_recal.math import get_centroid_peaks, is_valid_formula_adduct
from msi_recal.mean_spectrum import hybrid_mean_spectrum
from msi_recal.params import RecalParams

logger = logging.getLogger(__name__)


def _spectral_score(ref_ints: np.ndarray, ints: np.ndarray):
    """Calculates a spectral score based on the relative intensities of isotopic peaks."""
    if len(ref_ints) > 1:
        # Sort peaks by decreasing predicted intensity and normalize relative to the first peak
        order = np.argsort(ref_ints)[::-1]
        ints = ints[order[1:]] / ints[order[0]]
        ref_ints = ref_ints[order[1:]] / ref_ints[order[0]]

        ints_ratio_error = np.abs(ints / (ints + ref_ints) - 0.5) * 2
        return 1 - np.average(ints_ratio_error, weights=ref_ints)
    else:
        return 0


def calc_spectral_scores(
    spectrum, db_hits, params: RecalParams, sigma_1: float, limit_of_detection: float
) -> pd.DataFrame:
    """For each DB match, searches for isotopic peaks with the same approximate mass error and
    calculates a spectral score"""

    # Make list of expected isotopic peaks for each DB hit
    spectral_peaks = []

    for db_hit in db_hits.itertuples():
        if 'coverage' in db_hits.columns:
            min_abundance = min(limit_of_detection / db_hit.ints / db_hit.coverage, 0.9)
        else:
            min_abundance = min(limit_of_detection / db_hit.ints, 0.9)
        mol_peaks = get_centroid_peaks(
            db_hit.formula,
            db_hit.adduct,
            db_hit.charge,
            min_abundance,
            params.instrument_model,
        )
        # Recalc error as centroid may be slightly different to monoisotopic peak
        mz_error = db_hit.mz - mol_peaks[0][0]
        for mz, ref_ints in mol_peaks:
            spectral_peaks.append((db_hit[0], mz + mz_error, ref_ints))

    # Search for peaks in the spectrum
    spectral_peaks = pd.DataFrame(spectral_peaks, columns=['hit_index', 'ref_mz', 'ref_ints'])
    spectral_hits = join_by_mz(
        spectral_peaks, 'ref_mz', spectrum, 'mz', params.analyzer, sigma_1, how='left'
    )
    spectral_hits['ints'] = spectral_hits['ints'].fillna(0)

    # Calculate score
    if len(spectral_hits):
        by_hit = spectral_hits.groupby('hit_index')
        spectral_scores = pd.DataFrame(
            {
                'spectral_score': by_hit.apply(
                    lambda grp: _spectral_score(grp.ref_ints.values, grp.ints.values)
                ),
                'n_ref_peaks': by_hit.apply(lambda grp: len(grp)),
            }
        )
    else:
        spectral_scores = pd.DataFrame(
            {'spectral_score': pd.Series(), 'n_ref_peaks': pd.Series(dtype='i')}
        )
    return spectral_scores


def build_dbs(params):
    db_jobs = []
    for db_path in params.db_paths:
        db = load_db(db_path)
        is_targeted = db_path in params.targeted_dbs
        if 'adduct' in db.columns:
            db = db.drop_duplicates(['formula', 'adduct']).assign(
                db=db_path.stem, charge=params.charge
            )
            db_jobs.append((db_path.stem, db, is_targeted))
        else:
            db = db.drop_duplicates('formula')
            for adduct in params.adducts:
                db_name = db_path.stem + adduct
                adduct_db = db.assign(db=db_name, adduct=adduct, charge=params.charge)
                # Remove DB entries that would be invalid (e.g. H2O-Cl)
                adduct_db = adduct_db[
                    [
                        is_valid_formula_adduct(f, a)
                        for f, a in adduct_db[['formula', 'adduct']].itertuples(False, None)
                    ]
                ]
                db_jobs.append((db_name, adduct_db, is_targeted))
    return db_jobs


def get_db_hits(peaks_df, params: RecalParams, sigma_1: float):
    min_mz = peaks_df.mz.min()
    max_mz = peaks_df.mz.max()

    if 'coverage' in peaks_df.columns:
        limit_of_detection = np.percentile(peaks_df.ints / peaks_df.coverage, 0.1)
        logger.debug(f'Limit of detection (mean spectrum): {limit_of_detection}')
    else:
        limit_of_detection = np.percentile(peaks_df.ints, 0.1)
        logger.debug(f'Limit of detection: {limit_of_detection}')

    with ThreadPoolExecutor() as ex:
        db_jobs = build_dbs(params)

        job_params = [
            (
                peaks_df,
                db_name,
                db,
                is_targeted,
                limit_of_detection,
                max_mz,
                min_mz,
                params,
                sigma_1,
            )
            for db_name, db, is_targeted in db_jobs
        ]
        candidate_dfs = list(ex.map(_calc_db_scores, *zip(*job_params)))

    candidate_df = pd.concat(candidate_dfs, ignore_index=True)
    candidate_df['weight'] /= candidate_df.weight.max()

    return candidate_df.sort_values('mz')


def load_db(db_path):
    if '\t' in open(db_path).readline():
        db = pd.read_csv(db_path, keep_default_na=False, sep='\t')
    else:
        db = pd.read_csv(db_path, keep_default_na=False)
    db = db.drop(columns=['inchi', 'mz'], errors='ignore')
    return db


def _calc_db_scores(
    peaks_df,
    db_name,
    db,
    is_targeted,
    limit_of_detection,
    max_mz,
    min_mz,
    params: RecalParams,
    sigma_1,
):
    db['db_mz'] = [
        get_centroid_peaks(formula, adduct, params.charge, 0.1, params.instrument_model)[0][0]
        for formula, adduct in db[['formula', 'adduct']].itertuples(False, None)
    ]
    db_hits = join_by_mz(db, 'db_mz', peaks_df, 'mz', params.analyzer, sigma_1)
    spectral_scores = calc_spectral_scores(
        peaks_df, db_hits, params, params.jitter_sigma_1, limit_of_detection
    )
    db_hits = db_hits.join(spectral_scores)
    # db_hits = db_hits[db_hits.n_ref_peaks > 1]  # Only count sufficiently abundant hits
    if is_targeted:
        db_hits['spectral_score'] = np.clip(db_hits.spectral_score, 0.1, None)
        filtered = db_hits.sort_values('spectral_score', ascending=False)
    else:
        filtered = db_hits[db_hits.n_ref_peaks > 1]
    filtered = filtered.sort_values('spectral_score', ascending=False).drop_duplicates(
        ['formula', 'adduct']
    )

    # Find the average score, excluding the following cases that don't indicate bad matches:
    # * mols out of m/z range (also excluding the last 2 Da, because those peaks usually
    # won't have good M+1s)
    # * mols with no other isotopic peaks expected above the limit of detection
    n_candidates = np.count_nonzero(db.db_mz.between(min_mz, max_mz - 2))
    # mono_ratio = np.count_nonzero(db_hits.n_ref_peaks <= 1) / len(db_hits)
    db_weight = filtered.spectral_score.sum() / n_candidates  # / mono_ratio
    db_hits['weight'] = db_hits.spectral_score * db_weight
    if is_targeted:
        db_name = db_name + ' (targeted)'
    logger.debug(
        f'{db_name}: {len(filtered)} of {len(db)} formulas in m/z range matched, weight: {db_weight}'
    )
    return db_hits


def get_recal_candidates(peaks_df, params: RecalParams, sigma_1: float):
    mean_spectrum = hybrid_mean_spectrum(
        peaks_df,
        params.analyzer,
        # WORKAROUND: MSIWarp splats each peak across 3 * sigma_1, which can cause low-coverage peaks
        # to be overshadowed by higher-coverage peaks within a much wider range. Reduce sigma_1
        # to compensate. Peaks' individual sigma_1 values will be used for the actual peak shape.
        (params.peak_width_sigma_1 + params.jitter_sigma_1) / 3,
        0,
    )
    db_hits = get_db_hits(mean_spectrum, params, sigma_1)
    recal_candidates = (
        db_hits[db_hits.weight > 0]
        .sort_values('weight', ascending=False)
        .drop_duplicates('mz')
        .sort_values('mz')
    )
    db_hits['used_for_recal'] = db_hits.index.isin(recal_candidates.index)

    return recal_candidates, db_hits, mean_spectrum
