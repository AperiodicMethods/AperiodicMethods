"""Settings for plots."""

# Default sizes for figures
FIGSIZE1 = (6, 5)
FIGSIZE2 = (12, 5)

# Colors for simulation types
AP_COLOR = '#0043ad'   # OLD: '#0043ad'
CB_COLOR = '#750896'   # OLD: '#1c8c00'

# Colors for aperiodic parameters
KN_COLOR = '#5f0e99'

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

# Save setting
SAVE_EXT = '.pdf'

# Define default measure labels
LABELS = {
    'specparam' : 'Aperiodic Exponent',
    'irasa' : 'Aperiodic Exponent',

    'hurst' : 'Hurst Exponent',
    'dfa' : 'DFA Exponent',

    'lempelziv' : 'Lempel Ziv Complexity',
    'hjorth_complexity' : 'Hjorth Complexity',

    'app_entropy' : 'Approximate Entropy',
}
