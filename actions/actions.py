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
        arr=data.find().sort("Name",-1).limit(5)
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
        arr=data.find().sort('PriceMin', -1).limit(5)
        for value in arr:
            re_msg.append({'name':value['Name'],'image':value['Image'],'photos':value['Image'],'url':str(value['_id']),'ratings':value['avgrate']})
        print(re_msg)
        details={"best_restaurants":re_msg}
        dispatcher.utter_message(text="Đây là những nhà hàng có giá thấp nhất 🤩",json_message={"payload":"cardsCarousel","data":details['best_restaurants']})
        return []
