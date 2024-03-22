from parser_reddit import search_reddit_for_dog_food, getList, find_brand_name
from Map_API import rankedPetStores,mainSort,recomendedStore
def main():
    prompt = "What's the best food for my dog?"
    print(prompt)
    size = input("Enter your dog's size (small, medium, large): ").lower()
    breed = input("Enter your dog's breed: ").lower()
   # search_reddit_for_dog_food(size, breed)
    brand_mentions, brand_sentiments = search_reddit_for_dog_food(size, breed)
    getList(brand_mentions, brand_sentiments) #if you want to print output of reddit parsing results
    search = True
    while(search):
        chosen_brand = input("Choose one brand to find the price of by typing it's full or short name: ").lower()
        matched_brand = find_brand_name(chosen_brand)
        if matched_brand:
            #Run amazon and ebay code

            continue
        else:
            print("Sorry, we couldn't find a match for that brand.")
        prompt1 = "Do you want to search for a different brand?"
        print(prompt1)
        answ = input("Y for Yes || N for No")
        if answ.lower() == 'n':
            mainSort(rankedPetStores)
            recomendedStore(rankedPetStores)
            search = False



#TODO let me know if you agree to this structure, do you think that 2 people on price is okay?










if __name__ == "__main__":
   main()
