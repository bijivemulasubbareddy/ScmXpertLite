from pymongo import MongoClient

# MONGO_URI = "mongodb://localhost:27017"
# MONGO_URI = MongoClient("mongodb://localhost:27017")
# MONGO_URI = mongodb+srv://subbareddy:Subbu@3322@cluster0.yjrvgmv.mongodb.net/test
class settingsL:

    MONGO_URI = MongoClient("mongodb+srv://subbareddy:Subbu@3322@cluster0.yjrvgmv.mongodb.net/?retryWrites=true&w=majority")


settings=settingsL()