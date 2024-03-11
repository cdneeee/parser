'''Map api'''
import requests
#Default is London, Ontario Coords
latiude=42.9849
longitude=-81.2453
#testing commit
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword=dog&location="+str(latiude)+"%2C"+str(longitude)+"&radius=5000&type=pet_store&key=AIzaSyBr5bs5yA1VqS4DTxckkybYVBuTTiDtQII"



headers = {
	"X-RapidAPI-Key": "bcc6ea3e2cmsh3d114520f1f616fp171b15jsnfa2629b3700f",
	"X-RapidAPI-Host": "map-places.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

responseItems=response.json()

rankedPetStores =dict()

print('---------------------')
for items in responseItems['results']:
    if items['business_status']=='OPERATIONAL':
        if items['rating']<1:
            break
        rankedPetStores[items['name']]=str(items['rating'])
        print (items['name'])
        print("rating: "+str(items['rating']))
        print (items['vicinity'])
        print('---------------------')
rankedPetStores=dict(sorted(rankedPetStores.items(), key=lambda x:x[1],reverse=True))

print("We would recomend going here...")
counter=0
for key in list(rankedPetStores.keys()):
    #make sure to have the seperator with no whitespace or else the formating will not be correct
    print(str(key)+", ranked: "+str(rankedPetStores[key])+"/5 stars",sep="")
    counter+=1
    if counter==1:
        break
