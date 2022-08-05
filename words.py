import pymongo as pm
import datetime

fh = open("Vocabulary_set.csv", "r")
wd_list = fh.readlines()

wd_list.pop(0)

vocab_list = []

for rawstring in wd_list:
    word, definition = rawstring.split(",", 1)
    definition = definition.rstrip()
    vocab_list.append(
        {
            'word': word,
            'definition': definition
        }
    )

client = pm.MongoClient("mongodb://localhost:27017/")

db = client["vocab"]

vocab_collection = db["vocab_list"]

## we drop each time we run the script to keep doing tests
vocab_collection.drop()

vocab_dict = {
    "word": "cryptic",
    "definition": "With a hidden meaning"
}

result = vocab_collection.insert_one(vocab_dict)


dbs = client.list_database_names()

if "vocab" in dbs:
    print("The vocab exists in the database")

result = vocab_collection.insert_many(vocab_list)

query = vocab_collection.find_one()
print(query)

## no filter
for row_query in vocab_collection.find({}):
    print(row_query)

## adding some filters to only get the words (by exclusion)
filter_dict = {
    "_id": 0,
    "definition": 0
}
input("Enter to continue...")

for row_query in vocab_collection.find({},filter_dict):
    print(row_query)

## looking for a word inside the collection
query = vocab_collection.find_one(
    {"word": "arcane"}
)

print("Query result: \n",query)

input("Enter to continue...")

##doing some updates

updater = vocab_collection.update_one(
    {
        "word" : "eulogy"
    },
    {
        "$set": {
            "definition" : "a speech or piece of writing containing great praise"
        }
    }
)

print("count of modifications: ", updater.modified_count)
query = vocab_collection.find_one(
    {
        "word" : "eulogy"
    }
)

print("Query result of changing the definition of a word: \n",query)

update_dict = {
    "$set": {
        "last updated at UTC " : datetime.datetime.utcnow().strftime("%Y-%m-%d%H%M%SZ")
    }
}

updater = vocab_collection.update_many(
    {},
    update_dict
)

for row_query in vocab_collection.find({}):
    print(row_query)
    
print("count of modifications: ", updater.modified_count)