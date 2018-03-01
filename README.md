# IncAFfeine - Verify IncAF algorithms

[![build status](https://gitlab.cs.uni-duesseldorf.de/neugebauer/incaffeine/badges/master/build.svg)](https://gitlab.cs.uni-duesseldorf.de/neugebauer/incaffeine/commits/master)
[![coverage report](https://gitlab.cs.uni-duesseldorf.de/neugebauer/incaffeine/badges/master/coverage.svg)](https://gitlab.cs.uni-duesseldorf.de/neugebauer/incaffeine/commits/master)

Conduct exhaustive or randomized tests of heuristics or algorithms for decision problems in incomplete argumentation frameworks.

## Setup

To install required python packages, execute:

    pip3 install -r requirements.txt
    
To run the test template, run:

    python3 test_template.py
    
Create your own verification script based on the template and implement a checker function and a reference function to be compared for all generated instances. 