# Calculate the cost and context length of querying documentation
# Copyright 2024, Philipp Tsipman
# MIT License

# SETUP
import tiktoken
import sys

MODEL = "gpt4_turbo"

MODELS = {
    "gpt4_turbo": {"context_length": 128000, "price_per_1k_input": 0.01, "id": "gpt-4-1106-preview"},
    "gpt35_turbo": {"context_length": 16385, "price_per_1k_input": 0.001, "id": "gpt-3.5-turbo-1106"},
    "gpt4": {"context_length": 8192, "price_per_1k_input": 0.03, "id": "gpt-4"},
}

# FUNCTIONS

# read in text file from file path
def read_text_file(file_path: str) -> str:
    """Reads a text file and returns its contents as a string."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# calculate number of tokens in text file
def num_tokens_from_string(string: str, encoding_model: str, context_length: int) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_model)
    num_tokens = len(encoding.encode(string))
    if num_tokens > context_length:
        overage = num_tokens - context_length
        print(f"Warning: {num_tokens:,} tokens exceeds the context length of {context_length:,} by {overage:,} tokens.")
    return num_tokens

# calculate cost of tokens
def cost_of_tokens(num_tokens: int, price: float) -> float:
    """Returns the cost of tokens in USD."""
    cost = (num_tokens / 1000) * price
    return cost

# check if file path is provided
if len(sys.argv) < 2:
    print("Please provide a file path.")
    sys.exit()

# get the file path from the prompt variable
file_path = sys.argv[1]

file = read_text_file(file_path)

num_tokens = num_tokens_from_string(file, MODELS[MODEL]["id"], MODELS[MODEL]["context_length"])

cost = cost_of_tokens(num_tokens, MODELS[MODEL]["price_per_1k_input"])

print(f"{num_tokens:,} tokens")
print(f"${cost:,.2f} per input")

