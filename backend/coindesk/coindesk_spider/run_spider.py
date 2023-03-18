import subprocess

tags = ['bitcoin', 'blockchains', 'coinbase', 'crypto', 'dao', 'ether', 'first-mover', 'gaming', 'hacks', 'law', 'metaverse', 'nfts', 'on-chain-data', 'regulation', 'sanctions', 'sec', 'token-governance', 'yuga-labs']

for tag in tags:
    subprocess.Popen(
        ["scrapy", "crawl", "coindesk", f"-a", f"tag={tag}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
