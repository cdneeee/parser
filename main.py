from parser_reddit import search_reddit_for_dog_food, getList
def main():
    prompt = "What's the best food for my dog?"
    print(prompt)
    size = input("Enter your dog's size (small, medium, large): ").lower()
    breed = input("Enter your dog's breed: ").lower()
   # search_reddit_for_dog_food(size, breed)
    brand_mentions, brand_sentiments = search_reddit_for_dog_food(size, breed)
    getList(brand_mentions, brand_sentiments) #if you want to print output of reddit parsing results
    '''for brand in list in range(5):   #Uncomment to run
        runUrScript(brand)
        print(f"Top {list.index(brand)} - {brand} average price per kg: {urscripts Aleks + Santiago}, what people say about this brand: {ur script Aidan}")'''


#TODO let me know if you agree to this structure, do you think that 2 people on price is okay?










if __name__ == "__main__":
   main()
