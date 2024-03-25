import requests
import json

# finding product name (title), price, cost of shipping (shippingCost), link and sometimes (if it works) cost per kg

def ebay_analyze (brandName):
# set up the request parameters
  params = {
    'api_key': 'FD3E858FE6B8404EA7920B6F99093FB8',
      'ebay_domain': 'ebay.ca',
      'search_term': 'dog food',
      'type': 'search',
      'authorized_sellers': 'false',
      'max_page': '2',
      'sort_by': 'best_match',
      'output': 'json',
      'customer_location': 'ca'
    }

    # make the http GET request to Countdown API
  api_result = requests.get('https://api.countdownapi.com/request', params)
    
  #dictionary for product cost to weight ratio
  TitlesAndCostsPerKG = {}
  TitlesAndCosts = {}
  TitlesAndWeights = {}  
    
  #putting both strings in lower case to make search case-insensitive

  #product finding
  productRequest = brandName 
  productRequest = productRequest.lower()

  responseString = json.dumps(api_result.json()) 
  responseStringLower = responseString.lower()  
  
  #to amend the search criteria for each go 
  lowerBoundForSearch = 0
  searchNumber = 1
  
  search = 1
  
  while(search != -1):
    #searching the response to find searched dog food
    search = responseStringLower.find(productRequest, lowerBoundForSearch)
    lowerBoundForSearch = search + 200 #setting a lower bound for the next search loop 
    
    #if the search finds nothing
    if search == -1:
      print('This dog food was not found in the Ebay search')
      found = 0

    #if the search finds something
    else: 
      found = 1
      #finding the whole title of the dog food
      titlePos = responseString.find('"title": ', search - 40) + 10 
      endTitle = responseString.find('", "epid": ', search)
      title = responseString[titlePos: endTitle]
      
      #finding the price
      moneyPos = responseString.find('$', search) 
      price = responseString[moneyPos + 1: responseString.find('"}], "price": ', search)] 
      price = float(price)
      
      TitlesAndCosts.update({title: price})
      
      #finding the link
      linkPos = responseString.find('https', search)
      link = responseString[linkPos : responseString.find('", "image": ', search)]
      
      #finding the shipping cost
      shippingPos = responseString.find('"shipping_cost": ', search)
      #sponsored = responseString.find(', "sponsored": ', search)
      #rating = responseString.find(', "rating": ', search)
      
      #next = min(sponsored, rating)
      
      shippingCost = responseString[shippingPos + 15 : shippingPos + 22]
      print(shippingCost)
      def weightFromTitle(self, shippingCost):
        words = title.split()
        for word in words:
            if word.isdigit():
                return float(word)
        return 0.0
      
      
      #the total cost to the customer is the sum of the shown price and the shipping fees
      totalCost = round(price + shippingCost, 2)

      #printing results
      '''
      print('\n' + title)
      print('Price: $' + str(price))
      print('Shipping Cost: $' + str(shippingCost))
      print('Total cost: $' + str(totalCost))
      print('found at: ' + link)'''
      
      #finding the weight
      
      #finding the position of the weight unit, if there is one
      kgPos = title.lower().find('kg')
      lbPos = title.lower().find('lb')
      ozPos = title.lower().find('oz')
      poundPos = title.lower().find('pound')
      canPos = title.lower().find('can')
      
      #will use this dictionary to do conversion
      units = {1: kgPos, 2: lbPos, 3: ozPos,4 : poundPos, 5 : 5}
      
    
      #using a reversed to string to find the numbers nearest to the end  
      reverseTitle = title [::-1]
      
      #finding the positions of each digit 0-9
      numberPositions = []
      for x in range(10):
        numberPositions.append(len(title) - reverseTitle.find(str(x)) - 1)
        
        #if not found, it has position -1
        if numberPositions[x] == len(title):
          numberPositions[x] = -1
        
      
      #making a list to find only the positions of existing digits in the 
      existingNumberPositions = []
      for x in range(10):
        
        #only adding existing numbers in the title string
        if numberPositions[x] != -1:
          existingNumberPositions.append(numberPositions[x])
          
      #if nothing is found return 0   
      if len(existingNumberPositions) == 0:
        existingNumberPositions.append(0)
        
      # finding weight in grams if its denoted in grams 
      # only finding 'g' after a number  
      gPos = title.lower().find('g', title.find(str(max(existingNumberPositions))), title.find(str(max(existingNumberPositions))) + 1)
      
      #adding to dictionary 
      units.update({6: gPos}) 
      
      #finding the unit that is in use
      unitInUse = max(zip(units.values(), units.keys()))[1] 

      #weight reading system is very delicate 
      
      #making it robust to spaces and slashes
      
      #finding where the number is 
      weightString = title[min(existingNumberPositions): max(existingNumberPositions)+1]
      
      #finding the position of a space or a slash
      findingSpace = weightString.find(' ')
      findingSlashes = weightString.find('/')
      
      #if it has found a space eg 123454423 46kg
      if findingSpace != -1:
        weightString = weightString[findingSpace + 1: len(weightString)]
      
      #if it has found a / eg 12/11 pounds
      if findingSlashes != -1: 
        weightString = weightString[findingSlashes + 1: len(weightString)]
      
      #using try-catch block to see if the weight could be read. tell user if it cannot be read    
      try:
        weightNumber = float(weightString)

      except ValueError:
        weightNumber = -1
        pricePerKG = -1
        print("No weight could be read")
      
      #if the weight reading system does work
      else:  
        # if there are no mentions of cans
        if canPos == -1:
          #depending on the units used, the cost per kg changes
          match unitInUse: 
            #kg  
            case 1:
              pricePerKG = price / weightNumber
              #print('The price per Kg is: $' + str(round(pricePerKG, 2)))
            #lb  
            case 2 :
              weightNumber = 0.453592 * weightNumber #conversion to kg
              pricePerKG = price / weightNumber
              #print('The price per Kg is: $' + str(round(pricePerKG, 2)))
              
            #oz  
            case 3:
              weightNumber = 0.0283495 * weightNumber #conversion to kg
              pricePerKG = price / weightNumber
              #print('The price per Kg is: $' + str(round(pricePerKG, 2)))
              
            #pound  
            case 4:
              weightNumber = 0.453592 * weightNumber #conversion to kg
              pricePerKG = price / weightNumber
              #print('The price per Kg is: $' + str(round(pricePerKG, 2)))
              
            case 5: 
              pricePerKG = -1
              weightNumber = -1
              #print('there are no units')
            #grams
            case 6: 
              weightNumber = 0.001 * weightNumber
              pricePerKG = price / weightNumber
              #print('The price per Kg is: $' + str(round(pricePerKG, 2)))
              
        #if theres is a mention of can, the weight reading system doesn't work (would probably need to import chat gpt)
        else: 
          pricePerKG = -1 
          weightNumber = -1
          print('weight could not be read')
      
      TitlesAndCostsPerKG.update({title : pricePerKG})
      TitlesAndWeights.update({title: weightNumber})
  
  #sorting title and costs dictionary 
  sortedTitlesAndCostsPerKG = sorted(TitlesAndCostsPerKG.items(), key=lambda x:x[1])
  SortedCosts = dict(sortedTitlesAndCostsPerKG)     
  
  #printing results
  if(found == 1):
    print("Top 5 best value for "+brandName+" dog food by price/kg")
  for i in SortedCosts: 
    n = 1
    if (SortedCosts.values[i] != -1 and TitlesAndCosts != -1):
      print("%d - $%4.2f/kg (%4.2f for %4.2f kg)", n, SortedCosts.values[i], TitlesAndCosts.get(SortedCosts.keys[i]), TitlesAndWeights.get(SortedCosts.keys[i]))
      n = n + 1
  
 
  
  
  
    
  
  
  









