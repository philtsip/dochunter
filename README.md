# Doc Hunter

### Find and download technical documentation

### using Modal and Playwright

## Motivation

We use a lot of bleeding-edge programming libraries. Out-of-the-box Github Copilot or ChatGPT do not have the most up-to-date information about them. Instead, let's gather the latest technical documentation and pass it to the LLMs as RAG context.

## Requirements

Just one: a [modal.com](https://modal.com) account

## Usage

1. Deploy to Modal in one step `modal deploy dochunter.py` and get the deployment url
2. Then, get the documentation you're looking for by calling: `https://[YOUR_MODAL_ACCOUNT]-doc-hunter-hunt.modal.run/?q=[reference page or list of pages that include links to all of the rest of the documentation]`

For example: `https://[YOUR_MODAL_ACCOUNT]--doc-hunter-hunt-dev.modal.run/?q=https://threlte.xyz/docs/learn/getting-started/introduction,https://threlte.xyz/docs/examples/examples,https://threlte.xyz/docs/reference/core/getting-started,https://threlte.xyz/docs`

You can find some example queries for different libraries here in the `docs` folder
