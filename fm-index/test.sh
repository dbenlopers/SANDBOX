#!/bin/bash

src/fm-build.py data/test_data data/test_idx && src/fm-search.py data/test_idx "acgt"
