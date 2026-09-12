"""Expected positive-volume contacts in the selected V4 reducer core."""

# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Measurements describe the upstream V4 STEP document; its geometry remains
# MIT-licensed upstream material. See ../NOTICE.

# These are exact OCCT intersection volumes at the authored home pose.  They
# expose, rather than excuse, the STEP's positive-volume disc/output clashes.
# A changed, added, or removed overlap fails the exact inventory contract.
EXPECTED_OVERLAPS = {
    ("front-0", "pin-1"): 192.509199,
    ("front-0", "pin-2"): 170.403082,
    ("front-1", "pin-1"): 192.509199,
    ("front-1", "pin-2"): 170.403082,
    ("front-1", "bearing-0"): 901.995432,
    ("front-1", "bearing-1"): 1255.240118,
    ("front-1", "bearing-8"): 1229.219023,
    ("front-1", "bearing-9"): 99.367716,
    ("front-1", "bearing-10"): 171.397246,
    ("front-1", "bearing-11"): 791.354000,
    ("rear-0", "pin-4"): 192.509199,
    ("rear-0", "pin-5"): 170.403082,
    ("rear-1", "pin-4"): 192.509199,
    ("rear-1", "pin-5"): 170.403082,
    ("rear-1", "bearing-2"): 1255.240118,
    ("rear-1", "bearing-3"): 1229.219023,
    ("rear-1", "bearing-4"): 791.354000,
    ("rear-1", "bearing-5"): 99.367716,
    ("rear-1", "bearing-6"): 901.995432,
    ("rear-1", "bearing-7"): 171.397246,
}
