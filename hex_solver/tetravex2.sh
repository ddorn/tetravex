#!/bin/sh
python3 hex_gene.py > hex_in
python3 hex_DIMACS.py < hex_in > hex_dim
minisat hex_dim hex_sol
cat hex_in hex_sol > hex_dv
python3 hex_tdg.py < hex_dv

