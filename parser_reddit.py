import praw
import collections as c
from nltk.sentiment import SentimentIntensityAnalyzer
import datetime as dt

# Reddit API credentials
CLIENT_ID = 'YMND4Oi51pWAgEWQX6oi3A'
SECRET_KEY = '14JDmPPP0BtYeBssmKYyIgBzmIBmsw'
USER_AGENT = 'Ill_Huckleberry9931'
sia = SentimentIntensityAnalyzer()


# Initialize Reddit client
reddit = praw.Reddit(client_id = CLIENT_ID,
                     client_secret = SECRET_KEY,
                     user_agent = USER_AGENT)



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

def search_reddit_for_dog_food(size, breed, start_date="2023-01-01", end_date="2024-03-01"):
    start_timestamp = int(dt.datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(dt.datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    # Formulate the search query based on the dog's size and breed
    search_query = f"best food for {size} {breed} dog"
    
    # Search Reddit for the query
    search_results = reddit.subreddit('dogs').search(search_query, syntax='cloudsearch', time_filter='all', limit=100)
    
    # Initialize a counter for occurrences
    brand_mentions = c.Counter()
    brand_sentiments = c.defaultdict(list)
    
    def search_text_for_brands(text, brand_mentions, brand_sentiments):
        for brand, variations in dog_food_brands.items():
            for variation in variations:
                if variation.lower() in text.lower():
                    brand_mentions[brand] += 1
                    sentiment_score = sia.polarity_scores(text)
                    brand_sentiments[brand].append(sentiment_score['compound'])  # Compound score for overall sentiment

    
    # Search through titles and comments for brand mentions
    for submission in search_results:
        # Check if submission falls within the desired timeframe
        if start_timestamp <= submission.created_utc:
            # Search in title
            search_text_for_brands(submission.title, brand_mentions, brand_sentiments)
            
            # heavy part cause searching through comments
            submission.comments.replace_more(limit=0)  # This line removes the "MoreComments" instances
            for comment in submission.comments.list():
                search_text_for_brands(comment.body, brand_mentions, brand_sentiments)

    for brand in brand_sentiments:
        brand_sentiments[brand] = sum(brand_sentiments[brand]) / len(brand_sentiments[brand]) if brand_sentiments[brand] else 0
    
    sorted_brand_mentions = sorted(brand_mentions.items(), key=lambda x: x[1], reverse=True)
    return sorted_brand_mentions, brand_sentiments

def categorize_sentiment(score):
    if 0.5 < score < 0.6:
        return "good"
    elif score < 0.2:
        return "better not"
    elif score > 0.6:
        return "excellent"
    else:
        return "decent"

    

def getList(brand_mentions, brand_sentiments):
    # Print the brands mentioned and their occurrence times along with average sentiment
    if brand_mentions:
        print("Brand mentions and sentiments based on your search:")
        for brand, count in brand_mentions :
            # Fetch the average sentiment score for the brand, defaulting to 0 if not found
            sentiment_score = brand_sentiments.get(brand, 0)
            sentiment_description = categorize_sentiment(sentiment_score)
            print(f"{brand}: {count} times || Average Sentiment: {sentiment_description}")
    else:
        print("No specific dog food brands mentioned in the search results.")


def find_brand_name(user_input, brands_dict=None):
    # Iterate through each brand and its variations
    if brands_dict is None:
        brands_dict = dog_food_brands
        for brand, variations in brands_dict.items():
            # Check if the user input matches any of the variations (case-insensitive)
            if user_input in [variation.lower() for variation in variations]:
                return brand  # Return the main brand name if a match is found
        return None