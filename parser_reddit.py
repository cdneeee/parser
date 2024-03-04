import praw
import collections as c

# Reddit API credentials
CLIENT_ID = 'YMND4Oi51pWAgEWQX6oi3A'
SECRET_KEY = '14JDmPPP0BtYeBssmKYyIgBzmIBmsw'
USER_AGENT = 'Ill_Huckleberry9931'


# Initialize Reddit client
reddit = praw.Reddit(client_id = CLIENT_ID,
                     client_secret = SECRET_KEY,
                     user_agent = USER_AGENT)

'''def search_reddit_for_dog_food(size, breed):
    # Formulate the search query based on the dog's size and breed
    search_query = f"best food for {size} {breed} dog"
    
    # Search Reddit for the query
    search_results = reddit.subreddit('dogs').search(search_query, limit=10)
    
    # Collect results in a list
    results_list = []
    for submission in search_results:
        results_list.append({
            "title": submission.title,
            "url": submission.url,
            "score": submission.score,
            "subreddit": str(submission.subreddit)
        })
    
    # Sort the list by score in descending order
    sorted_results = sorted(results_list, key=lambda x: x['score'], reverse=True)
    
    # Print the sorted results
    for result in sorted_results:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Score: {result['score']}")
        print(f"Subreddit: {result['subreddit']}")
        print("--------------------------------------------------")

if __name__ == "__main__":
    prompt = "What's the best food for my dog?"
    print(prompt)
    size = input("Enter your dog's size (small, medium, large): ").lower()
    breed = input("Enter your dog's breed: ").lower()
    search_reddit_for_dog_food(size, breed)'''

dog_food_brands = {
    'Purina': ['Purina', 'Purinna', 'Purena', 'Purinia', 'Purna', 'Pur'],
    'Royal Canin': ['Royal Canin', 'Royal Cannin', 'Royal Canine', 'Roya Canin', 'R Canin', 'RC', 'Royal'],
    'Hill\'s Science Diet': ['Hills Science Diet', 'Hill Science Diet', 'Hill\'s Science Diet', 'Hill\'s Science Dite', 'Hills', 'Science Diet', 'Hill\'s'],
    'Blue Buffalo': ['Blue Buffalo', 'Blue Bufflo', 'Blu Buffalo', 'Blue Buffallo', 'BlueBuff', 'BB'],
    'Pedigree': ['Pedigree', 'Pedegree', 'Padigree', 'Pedigrea', 'Pedi'],
    'Iams': ['Iams', 'Iam', 'Iams\'', 'Iams', 'IAM'],
    'Eukanuba': ['Eukanuba', 'Ekanuba', 'Eucanuba', 'Eukanuva', 'Euka'],
    'Acana': ['Acana', 'Akana', 'Accana', 'Acanna', 'AC'],
    'Orijen': ['Orijen', 'Origen', 'Orijin', 'Origjen', 'OJ'],
    'Taste of the Wild': ['Taste of the Wild', 'Taste of teh Wild', 'Tast of the Wild', 'Taste of the Wield', 'TOTW'],
    'Wellness Core': ['Wellness Core', 'Wellness Coar', 'Wellnes Core', 'Wellness Kore', 'Wellness', 'WC'],
    'Merrick': ['Merrick', 'Merick', 'Meric', 'Merric', 'Mer'],
    'Fromm': ['Fromm', 'Froom', 'Frohm', 'From', 'Frm'],
    'Nutro': ['Nutro', 'Nuto', 'Nutroo', 'Nutor', 'NT'],
    'Nutrience':['Nutri', 'Nutrience', 'Nutrince', 'Nurience', 'Nutrien'],
    'Natural Balance': ['Natural Balance', 'Naturall Balance', 'Natural Balnce', 'Natrual Balance', 'NB'],
    'Canidae': ['Canidae', 'Cannidae', 'Canide', 'Kanidae', 'CD'],
    'Zignature': ['Zignature', 'Zignaturee', 'Zignatur', 'Signature', 'Zig'],
    'Diamond Naturals': ['Diamond Naturals', 'Diamond Natural', 'Diamon Naturals', 'Diamond Nturals', 'DN'],
    'Victor': ['Victor', 'Victor', 'Victer', 'Viktor', 'VT'],
    'Nutrish': ['Nutrish', 'Nutrishh', 'Nurtrish', 'Nutrsh', 'Rachael Ray Nutrish', 'RRN'],
    'Stella & Chewy\'s': ['Stella & Chewy\'s', 'Stela & Chewy', 'Stella and Chewys', 'Stella & Chewis', 'S&C', 'Stella Chewy']
    }
# Initialize Reddit client
def search_reddit_for_dog_food(size, breed):
    # Formulate the search query based on the dog's size and breed
    search_query = f"best food for {size} {breed} dog"
    
    # Search Reddit for the query
    search_results = reddit.subreddit('dogs').search(search_query, limit=100)
    
    # Initialize a counter for occurrences
    brand_mentions = c.Counter()
    
    def search_text_for_brands(text, brand_mentions):
        for brand, variations in dog_food_brands.items():
            for variation in variations:
                if variation.lower() in text.lower():
                    brand_mentions[brand] += 1
    
    # Search through titles and comments for brand mentions
    for submission in search_results:
        # Search in title
        search_text_for_brands(submission.title, brand_mentions)
        
        # heavy part cause searching through comments
        submission.comments.replace_more(limit=0)  # This line removes the "MoreComments" instances
        for comment in submission.comments.list():
            search_text_for_brands(comment.body, brand_mentions)

    sorted_brand_mentions = sorted(brand_mentions.items(), key=lambda x: x[1], reverse=True)
    
    # Print the brands mentioned and their occurrence times
    if sorted_brand_mentions:
        print("Brand mentions based on your search:")
        for brand, count in sorted_brand_mentions:
            print(f"{brand}: {count} times")
    else:
        print("No specific dog food brands mentioned in the search results.")

if __name__ == "__main__":
    prompt = "What's the best food for my dog?"
    print(prompt)
    size = input("Enter your dog's size (small, medium, large): ").lower()
    breed = input("Enter your dog's breed: ").lower()
    search_reddit_for_dog_food(size, breed)