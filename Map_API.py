'''Map api'''
import requests
#Default is London, Ontario Coords
latiude=42.9849
longitude=-81.2453
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword=dog&location="+str(latiude)+"%2C"+str(longitude)+"&radius=5000&type=pet_store&key=AIzaSyBr5bs5yA1VqS4DTxckkybYVBuTTiDtQII"

headers = {
	"X-RapidAPI-Key": "bcc6ea3e2cmsh3d114520f1f616fp171b15jsnfa2629b3700f",
	"X-RapidAPI-Host": "map-places.p.rapidapi.com"
}
#dictonary to store all of the near by pet stores and there rating and location
rankedPetStores=dict()

#main sorting method to find all needed data
def mainSort(rankedPetStores):
    #calling the API
    response = requests.get(url, headers=headers)

    #turing the API response into something we can work with
    responseItems=response.json()

    #List to store both the rating and location relative to the store name 
    locationANDrating = []

    for items in responseItems['results']:
        #checking if the pet store is open/operating, if not there is no point to add to the lsit
        if items['business_status']=='OPERATIONAL':
            #checking the rating of the business, again if too low there is no point to recomending it
            if items['rating']<1:
                break 
            #Adding the rating and location to list
            locationANDrating=[items['rating'],items['vicinity']]
            #linking the name for store to its rating and location
            rankedPetStores[items['name']]=locationANDrating
    #Now sorting the list to find the highest ranked store
    rankedPetStores=dict(sorted(rankedPetStores.items(), key=lambda x:x[1],reverse=True))

#new def to output the top three recomended store to the user
def recomendedStore(rankedPetStores):
    print("We would recomend going here...")
    counter=0
    for key in list(rankedPetStores.keys()):
        #make sure to have the seperator with no whitespace or else the formating will not be correct
        print(str(key)+", "+str(rankedPetStores[key]),sep="")
        counter+=1
        if counter==3:
            break
