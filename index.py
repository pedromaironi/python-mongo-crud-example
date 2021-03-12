import pymongo

MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_TIME = 1000

MONGO_URI = 'mongodb://' + MONGO_HOST+':'+MONGO_PORT+'/'

MONGO_BASEDATA = 'escuela'
MONGO_COLLECTION = 'alumnos'

try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME)
    base_data = client[MONGO_BASEDATA]
    collection = base_data[MONGO_COLLECTION]
    for document in collection.find():
        print(document['nombre'] + " " + str(document['calificacion']))
    client.server_info()
    print('Connection successful')
    client.close()
except pymongo.errors.ServerSelectionTimeoutError as errorTime:
    print('Time lose: ' + errorTime)
except pymongo.errors.ConnectionFailure as errorConnection:
    print('Connection: ' + errorConnection)


