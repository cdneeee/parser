import requests

class amazon_pricing:
    def __init__(self):
        self.api_key = "463d9dd1dbmsh61ff4cf1128730ap1cce80jsn5fcf93b563f8"
        self.api_host = "real-time-amazon-data.p.rapidapi.com"
        self.url = "https://real-time-amazon-data.p.rapidapi.com/search"
        self.num_results = 100

    def amazonSearch(self, brand):
        querystring = {
            "query": f"{brand} dog food", # the search
            "page": "1", # first page
            "country": "US", # set to US for now for more results
            "sort_by": "RELEVANCE", # most popular
            "category_id": "aps",
            "brand": brand, # CHANGE THIS TO TAKE BRAND NAME FROM REDDIT PARSER
            "min_price": "1" # minimum price set to $1 to avoid priceless listings
        }
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }
        response = requests.get(self.url, headers=headers, params=querystring)
        data = response.json()
        top_results = data["data"]["products"][:self.num_results]
        prices = []
        weights = []
        for product in top_results:
            price_str = product.get('product_price')
            weight_str = product.get('product_title')
            if price_str is not None and weight_str is not None:
                price = float(price_str.replace('$', ''))
                weight = self.weightFromTitle(weight_str)
                if price > 0 and weight > 0 and weight < 100:  # Exclude zero price per kg values and outliers
                    prices.append(price)
                    weights.append(weight)
        return prices, weights

    def weightFromTitle(self, title):
        words = title.split()
        for word in words:
            if word.isdigit():
                return float(word)
        return 0.0

    def amazonOutput(self):
        brand = input("Enter the brand of dog food: ").strip().lower()
        prices, weights = self.amazonSearch(brand)
        if not prices or not weights:
            print("No valid prices or weights found.")
            return
        price_per_kg = [price / weight for price, weight in zip(prices, weights)]
        sorted_results = sorted(zip(price_per_kg, prices, weights))
        print(f"Top 5 best value for {brand} dog food by price/kg:")
        for i, (price_per_kg, price, weight) in enumerate(sorted_results[:5], start=1):
            print(f"{i} - ${price_per_kg:.2f}/kg (${price:.2f} for {weight:.2f} kg)")

if __name__ == "__main__":
    analyzer = amazon_pricing()
    analyzer.amazonOutput()
