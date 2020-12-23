from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.weather import Weather
from pymongo.database import Database
from pymongo import MongoClient
from rasa_sdk.events import SlotSet,UserUtteranceReverted
import actions.zomatoApi as zomatoApi
import pymongo
import requests
import json
import feedparser

class ActionHelloWorld(Action):
    def name(self):
        return "action_hello_world"
    def run(self, dispatcher, tracker, domain):
        name="Hello "+(tracker.latest_message)['text']
        print("Here oim ")
        print("this is tracker",tracker)
        dispatcher.utter_message(name)
        return []
class RecommendRestaurant(Action):
    def name(self):
        return "RecommendRestaurant"
    def run(self, dispatcher, tracker, domain):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db=client.WeddingRestaurant
        data=db['profilesrestaurants']
        re_msg=[]
        arr=[]
        arr=data.find().limit(5)
        for value in arr:
            re_msg.append({'name':value['Name'],'image':value['Image'],'photos':value['Image'],'url':str(value['_id']),'ratings':value['avgrate']})
        print(re_msg)
        details={"best_restaurants":re_msg}
        dispatcher.utter_message(text="Đây là một số nhà hàng gợi ý cho bạn  🤩",json_message={"payload":"cardsCarousel","data":details['best_restaurants']})
        return []
class RecommendNewRestaurant(Action):
    def name(self):
        return "RecommendNewRestaurant"
    def run(self, dispatcher, tracker, domain):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db=client.WeddingRestaurant
        data=db['profilesrestaurants']
        re_msg=[]
        arr=[]
        arr=data.find().sort("Name",-1)
        for value in arr:
            re_msg.append({'name':value['Name'],'image':value['Image'],'photos':value['Image'],'url':str(value['_id']),'ratings':value['avgrate']})
        print(re_msg)
        details={"best_restaurants":re_msg}
        dispatcher.utter_message(text="Đây là một số nhà hàng gợi ý cho bạn  🤩",json_message={"payload":"cardsCarousel","data":details['best_restaurants']})
        return []
class RecommendRestaurantCapacity(Action):
    def name(self):
        return "RecommendRestaurantCapacity"
    def run(self, dispatcher, tracker, domain):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db=client.WeddingRestaurant
        data=db['profilesrestaurants']
        re_msg=[]
        arr=[]
        arr=data.find().sort("Capacity",-1).limit(5)
        for value in arr:
            re_msg.append({'name':value['Name'],'image':value['Image'],'photos':value['Image'],'url':str(value['_id']),'ratings':value['avgrate']})
        details={"best_restaurants":re_msg}
        dispatcher.utter_message(text="Đây là top 5 nhà hàng có sức chứa lớn nhất   🤩",json_message={"payload":"cardsCarousel","data":details['best_restaurants']})
        return []
class RecommendRestaurantRating(Action):
    def name(self):
        return "RecommendRestaurantRating"
    def run(self, dispatcher, tracker, domain):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db=client.WeddingRestaurant
        data=db['profilesrestaurants']
        re_msg=[]
        arr=[]
        arr=data.find().sort("avgrate",-1).limit(5)
        for value in arr:
            re_msg.append({'name':value['Name'],'image':value['Image'],'photos':value['Image'],'url':str(value['_id']),'ratings':value['avgrate']})
        details={"best_restaurants":re_msg}
        dispatcher.utter_message(text="Đây là top 5 nhà hàng đánh giá tốt nhất   🤩",json_message={"payload":"cardsCarousel","data":details['best_restaurants']})
        return []
class RestaurantHigh(Action):
    def name(self):
        return "RestaurantHigh"
    def run(self, dispatcher, tracker, domain):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db=client.WeddingRestaurant
        data=db['profilesrestaurants']
        re_msg=[]
        arr=[]
        arr=data.find().sort("PriceMax",-1).limit(5)
        for value in arr:
            re_msg.append({'name':value['Name'],'image':value['Image'],'photos':value['Image'],'url':str(value['_id']),'ratings':value['avgrate']})
        print(re_msg)
        details={"best_restaurants":re_msg}
        dispatcher.utter_message(text="Đây là những nhà hàng có giá cao nhất 🤩",json_message={"payload":"cardsCarousel","data":details['best_restaurants']})
        return []
class RestaurantLow(Action):
    def name(self):
        return "RestaurantLow"
    def run(self, dispatcher, tracker, domain):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db=client.WeddingRestaurant
        data=db['profilesrestaurants']
        re_msg=[]
        arr=[]
        arr=data.find().sort("PriceMax").limit(5)
        for value in arr:
            re_msg.append({'name':value['Name'],'image':value['Image'],'photos':value['Image'],'url':str(value['_id']),'ratings':value['avgrate']})
        print(re_msg)
        details={"best_restaurants":re_msg}
        dispatcher.utter_message(text="Đây là những nhà hàng có giá thấp nhất 🤩",json_message={"payload":"cardsCarousel","data":details['best_restaurants']})
        return []
class ActionSearchBestRestaurants(Action):
    def name(self) -> Text:
        return "action_search_best_restaurants"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print()
        print("======Inside Action Search Best Restaurants====")
        print()

        ## extract the required slots
        location=tracker.get_slot("location")
        cuisine=tracker.get_slot("cuisine")
        lat=tracker.get_slot("latitude")
        lon=tracker.get_slot("longitude")
        entity_id=tracker.get_slot("location_id")
        entity_type=tracker.get_slot("location_type")
        city_id=tracker.get_slot("city_id")

        ## extract the entities
        locationEntity=next(tracker.get_latest_entity_values("location"), None)
        cuisineEntity=next(tracker.get_latest_entity_values("cuisine"), None)
        user_locationEntity=next(tracker.get_latest_entity_values("user_location"), None)
        latEntity=next(tracker.get_latest_entity_values("latitude"), None)
        lonEntity=next(tracker.get_latest_entity_values("longitude"), None)

        ## if we latitude & longitude entities are found, set it to slot
        if(latEntity and lonEntity):
            lat=latEntity
            lon=lonEntity

        ## if user wants to search the best restaurants in his current location
        if(user_locationEntity or (latEntity and lonEntity) ):
            ##check if we already have the user location coordinates stoed in slots
            if(lat==None and lon==None):
                dispatcher.utter_message(text="Sure, please allow me to access your location 🧐",json_message={"payload":"location"})
              
                return []
            else:
                locationEntities=zomatoApi.getLocationDetailsbyCoordinates(lat,lon)
                location=locationEntities["title"]
                city_id=locationEntities["city_id"]
                entity_id=locationEntities["entity_id"]
                entity_type=locationEntities["entity_type"]
                
                ## store the user provided details to slot
                SlotSet("location", locationEntities["title"])
                SlotSet("city_id", locationEntities["city_id"])
                SlotSet("location_id", locationEntities["entity_id"])
                SlotSet("location_type", locationEntities["entity_type"])

        ## if user wants to search best restaurants by location name
        if(locationEntity):
            locationEntities=zomatoApi.getLocationDetailsbyName(locationEntity)
            entity_id=locationEntities["entity_id"]
            entity_type=locationEntities["entity_type"]
            city_id=locationEntities["city_id"]

        print("Entities: ",entity_id," ",entity_type," ",city_id," ",locationEntity)
        
        ## search the best restaurts by calling zomatoApi api
        restaurants=zomatoApi.getLocationDetails(entity_id,entity_type)
        
        if(len(restaurants)>0):
            print(restaurants)
            if(tracker.get_latest_input_channel()=="slack"):
                more_restaurants=None
                if len(restaurants["best_restaurants"])>5:
                    restData=getResto_Slack(restaurants["best_restaurants"][:5],show_more_results=True)
                    more_restaurants=restaurants["best_restaurants"][5:]
                    dispatcher.utter_message(text="Here are few top rated restaurants that I have found 🤩",json_message=restData)
                else:
                    restData=getResto_Slack(restaurants["best_restaurants"],show_more_results=False)

                    dispatcher.utter_message(text="Here are few top rated restaurants that I have found 🤩",json_message=restData)
                return [SlotSet("more_restaurants", more_restaurants)]    
            else:
                if len(restaurants["best_restaurants"])>5:
                    dispatcher.utter_message(text="Here are few top rated restaurants that I have found 🤩",json_message={"payload":"cardsCarousel","data":restaurants["best_restaurants"][:5]})
                    return [SlotSet("more_restaurants", restaurants["best_restaurants"][5:])]    
                else:
                    dispatcher.utter_message(text="Here are few top rated restaurants that I have found 🤩",json_message={"payload":"cardsCarousel","data":restaurants["best_restaurants"]})
                    return [SlotSet("more_restaurants", None)]    
        else:    
            dispatcher.utter_message("Sorry we couldn't find any restaurants that serves {} cuisine in {} 😞".format(cuisine,location))
            return [UserUtteranceReverted()] 
        