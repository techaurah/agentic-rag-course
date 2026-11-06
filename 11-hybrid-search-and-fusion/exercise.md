# Exercise for Lesson 11: Hybrid search and fusion

Test the insurance claim. Build the two single leg baselines and the hybrid, then deliberately break one leg: shuffle the vector leg's ranking (deterministic seed) before fusion, and rerun the stage table. Record fact recall at 5 and the worst question for the broken hybrid against the intact one. Then write the deployment rule this justifies: what property of RRF did the broken leg demonstrate, and what monitoring would tell you in production that one leg had silently degraded to noise?
