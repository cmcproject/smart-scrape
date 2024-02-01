import bittensor as bt
from template.protocol import TwitterScraperStreaming
import json
import asyncio
import sys  # Import the sys module to access command-line arguments

wallet = bt.wallet(name = "validator", hotkey = "default")
if len(sys.argv) > 1:
    uids = [int(sys.argv[1])]  # Set uids from the command-line argument
else:
    print("Error: Please provide a user ID as a command-line argument.")
    sys.exit(1)

message = "tell me about sports"

axon = bt.axon(wallet=wallet)
dendrite = bt.dendrite(wallet=wallet)

# construct the synapse from the protocol using the message and whatever else we need
synapse = TwitterScraperStreaming(messages=message, model="gpt-4-1106-preview", seed=1234)

meta = bt.metagraph(netuid = 22)
axons = [meta.axons[uid] for uid in uids]

async def main():
    async_responses = await dendrite.forward(
        axons=axons, 
        synapse=synapse, 
        deserialize=False,
        timeout=120,
        streaming=True,
    )
    full_response = ""
    for resp in async_responses:
        async for chunk in resp:
            if isinstance(chunk, str):
                bt.logging.trace(chunk)
                full_response += chunk
        bt.logging.debug(f"full_response: {full_response}")
        break
    # responses = await process_async_responses(async_responses, message)
    # for response in responses:
    #     print(response)

if __name__ == "__main__":
    asyncio.run(main())



    