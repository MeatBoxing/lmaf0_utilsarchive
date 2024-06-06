import aiohttp
import asyncio

async def send_message(token, url, content, channel_id):
    headers = {"Authorization": token}
    data = {"content": content}
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{url}/{channel_id}/messages", headers=headers, json=data) as response:
            if response.status == 429:  # Rate limit exceeded
                retry_after = (await response.json())['retry_after']
                print(f"Token {token}: Rate limited. Waiting for {retry_after} seconds...")
                await asyncio.sleep(retry_after)
                await send_message(token, url, content, channel_id)  # Retry sending message
            else:
                print(f"Token {token}: {await response.text()}")

async def main(content, channel_ids, tokens):
    url = "https://discord.com/api/v9/channels"
    while True:
        tasks = []
        for channel_id in channel_ids:
            for token in tokens:
                tasks.append(send_message(token, url, content, channel_id))

        await asyncio.gather(*tasks)

def read_tokens(filename):
    with open(filename, "r") as file:
        tokens = file.readlines()
        tokens = [token.strip() for token in tokens if token.strip()]
    return tokens

if __name__ == "__main__":
    content = "example"
    channel_ids = ["1", "2", "3"]
    tokens = read_tokens("tokens.txt")
    asyncio.run(main(content, channel_ids, tokens))
