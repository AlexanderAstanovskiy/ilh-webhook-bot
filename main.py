def search_ebay(query):
    import requests
    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    search_url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    
    try:
        response = requests.get(search_url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select("li.s-item")
        results = []

        for item in items[:10]:
            title_elem = item.select_one("h3.s-item__title")
            price_elem = item.select_one(".s-item__price")
            link_elem = item.select_one("a.s-item__link")

            if title_elem and price_elem and link_elem:
                title = title_elem.text.strip()
                price = price_elem.text.strip()
                link = link_elem['href']
                results.append(f"{title} — {price}\n{link}")

        if results:
            return "\n\n".join(results)
        else:
            return f"Цены на eBay не найдены.\n{search_url}"
    except Exception as e:
        return f"Ошибка при поиске на eBay: {search_url}"
