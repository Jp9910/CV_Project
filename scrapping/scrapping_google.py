import asyncio
import aiohttp

# Scrapping no html do google
class API:
    def __init__(self):
        self.URL = 'https://www.google.ca/imghp'
    
    async def google_http_search(self, query=None) -> dict:
        request_params = {
            'q':query,
            'engine': "google_images",
            'ijn': 0,
            'hl': 'en',
            "tab": "ri",
            "authuser": "0&ogbl"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.URL,params=request_params) as resultado_html:
                # Necessário processar o HTML
                return resultado_html
                
async def main():
    api = API()
    resultado = await api.google_http_search(query="league of legends kindred")
    print(resultado)

# Resolver "Asyncio Event Loop is Closed"
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())