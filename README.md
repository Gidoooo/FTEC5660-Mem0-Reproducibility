# FTEC5660 Individual Project 2 - Mem0

This is my reproducibility project for FTEC5660. I chose Mem0 to test how AI agents use memory to answer questions.

## My Experiment

I used the LOCOMO dataset with 5 conversation sessions and 9 questions.

I compared two settings:
- Top-10: Use 10 memories.
- Top-20: Use 20 memories.

I used Mem0 Cloud and DeepSeek to run the experiment.

## Results

| | Top-10 | Top-20 |
|---|---|---|
| Correct Answers | 9/9 | 9/9 |
| Accuracy | 100% | 100% |

Both settings got the same results. In this small test, using more memories did not improve accuracy.

## How to Run

Install the required packages:

    python3.11 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Create a `.env` file with your Mem0 and DeepSeek API keys.

Use the LOCOMO subset in `datasets/locomo/formal_subset.json`.

Run:

    export SSL_CERT_FILE=$(python -m certifi)

    python -m benchmarks.locomo.run \
      --project-name formal_topk_01 \
      --dataset-path datasets/locomo/formal_subset.json \
      --conversations 0 \
      --categories 1,2 \
      --max-questions 9 \
      --backend cloud \
      --provider openai \
      --answerer-model deepseek-flash \
      --judge-model deepseek-flash \
      --top-k 20 \
      --top-k-cutoffs 10,20 \
      --max-workers 1 \
      --rpm 10

## Problems

Docker did not work on my Mac, so I used Mem0 Cloud. I also made some small code changes to connect DeepSeek and fix the API connection.

## References

Paper: https://arxiv.org/abs/2504.19413

Original code: https://github.com/mem0ai/mem0

Benchmark: https://github.com/mem0ai/memory-benchmarks
