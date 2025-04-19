async def search_ebay(query: str) -> str:
    import httpx
    from bs4 import BeautifulSoup

    url = f"https://www.ebay.com/sch/i.html?_nkw={query}&_sop=12"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".s-item")

        prices = []
        for item in items:
            price_tag = item.select_one(".s-item__price")
            link_tag = item.select_one("a.s-item__link")
            if price_tag and link_tag:
                price = price_tag.get_text(strip=True)
                link = link_tag.get("href")
                prices.append(f"{price} → {link}")
            if len(prices) >= 3:
                break

        if not prices:
            return "Цены на eBay не найдены."

        return "Найдено на eBay:\n" + "\n".join(prices)

    except Exception as e:
        return f"Ошибка при поиске на eBay: {e}"
