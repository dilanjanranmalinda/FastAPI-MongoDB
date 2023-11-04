from mongoengine import connect


def connect_db():
    connection = connect(
        host='mongodb+srv://test1234:test1234@atlascluster.xcumlvf.mongodb.net/fastapi?retryWrites=true&w=majority')

    return connection
