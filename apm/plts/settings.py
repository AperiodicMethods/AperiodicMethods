"""Settings for plots."""

## FIGSIZE SETTINGS

# Default sizes for figures
FIGSIZE1 = (6, 5)
FIGSIZE2 = (12, 5)

## COLOR SETTINGS - SIMULATIONS

# Colors for simulation types
AP_COLOR = '#0043ad'   #
CB_COLOR = '#750896'   # OLD: '#1c8c00'

# Colors for aperiodic parameters
KN_COLOR = '#9073fa'   # OLD: '#5f0e99'

# Colors for periodic parameters
CF_COLOR = '#acc918'
PW_COLOR = '#28a103'
BW_COLOR = '#0fd197'

# Collect colors
COLORS = {
    'AP' : AP_COLOR,
    'CM' : CB_COLOR,
    'KN' : KN_COLOR,
    'CF' : CF_COLOR,
    'PW' : PW_COLOR,
    'BW' : BW_COLOR,
}

## COLOR SETTINGS - METHODS

FIT_COLOR = '#2655b5'
SP_COLOR = '#d1291d'
IR_COLOR = '#36a118'

METHOD_COLORS = {
    'specparam' : SP_COLOR,
    'irasa' : IR_COLOR,
}

## SAVE SETTINGS

# Save setting
EXT = '.pdf'

## LABELS

# Define default measure labels
LABELS = {

    # Exponent measures
    'specparam' : 'Aperiodic Exponent',
    'irasa' : 'Aperiodic Exponent',

    # Autocorrelation Measures
    'autocorr' : 'Autocorrelation',
    'autocorr_decay_time' : 'AC Decay Time',

    # Fluctuation measures
    'hurst' : 'Hurst Exponent',
    'dfa' : 'DFA Exponent',

    # Fractal Dimension Measures
    'correlation_dimension' : 'Correlation Dimension',
    'higuchi_fd' : 'Higuchi Fractal Dimension',
    'katz_fd' : 'Katz Fractal Dimension',
    'petrosian_fd' : 'Petrosian Fractal Dimension',

    # Complexity Measures
    'hjorth_activity' : 'Hjorth Activity',
    'hjorth_mobility' : 'Hjorth Mobility',
    'hjorth_complexity' : 'Hjorth Complexity',
    'lempelziv' : 'Lempel Ziv Complexity',
    'lyapunov' : 'Lyapunov Exponent',

    # Entropy measures
    'app_entropy' : 'Approximate Entropy',
    'sample_entropy' : 'Sample Entropy',
    'perm_entropy' : 'Permutation Entropy',
    'wperm_entropy' : 'Weighted Permuation Entropy',

    # Multiscale entropy measures
    'multi_app_entropy' : 'Multiscale Approximate Entropy',
    'multi_sample_entropy' : 'Multiscale Sample Entropy',
    'multi_perm_entropy' : 'Multiscale Permutation Entropy',
    'multi_wperm_entropy' : 'Multiscale WPermutation Entropy',
}

## ABBREVIATIONS

# Define default measure abbreviations
ABBRS =  {

    # Exponent measures
    'specparam' : 'Exp(SP)',
    'irasa' : 'Exp(IR)',

    # Autocorrelation Measures
    'autocorr' : 'AC',
    'autocorr_decay_time' : 'ACD',

    # Fluctuation measures
    'hurst' : 'HE',
    'dfa' : 'DFA',

    # Fractal Dimension Measures
    'correlation_dimension' : 'CD',
    'higuchi_fd' : 'HFD',
    'katz_fd' : 'KFD',
    'petrosian_fd' : 'PFD',

    # Complexity Measures
    'hjorth_activity' : 'HJA',
    'hjorth_mobility' : 'HJM',
    'hjorth_complexity' : 'HJC',
    'lempelziv' : 'LZC',
    'lyapunov' : 'LLE',

    # Entropy measures
    'app_entropy' : 'ApEn',
    'sample_entropy' : 'SampEn',
    'perm_entropy' : 'PeEn',
    'wperm_entropy' : 'wPeEn',

    # Multiscale entropy measures
    'multi_app_entropy' : 'mApEn',
    'multi_sample_entropy' : 'mSampEn',
    'multi_perm_entropy' : 'mPeEn',
    'multi_wperm_entropy' : 'mwPeEn',
}
