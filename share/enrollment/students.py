import boto3, botocore
from dataclasses import dataclass

dynamo_db = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

# Delete table if it already exists
try:
    dynamo_db.Table("students").delete()
except botocore.exceptions.ClientError:
    pass

table = dynamo_db.create_table(
    TableName = 'students',
    KeySchema = [ 
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions = [
        {
            "AttributeName": "id",
            "AttributeType": "N"
        }
    ],
    ProvisionedThroughput={
        "ReadCapacityUnits": 10,
        "WriteCapacityUnits": 10,
    },
)

id_counter = 0
@dataclass
class Item:
    username: str
    name: str
    id: int = 0

    def __post_init__(self):
        if self.id == 0:
            global id_counter
            id_counter += 1
            self.id = id_counter

table.put_item(
    Item = Item('jimbo', 'Jimmy Quach').__dict__
)
table.put_item(
    Item = Item('gouri123', 'Gouri Sabale').__dict__
)
table.put_item(
    Item = Item('Kyle', 'Kyle Whynott').__dict__
)
table.put_item(
    Item = Item('krick123', 'Kendrick Ngo').__dict__
)
table.put_item(
    Item = Item('Walker', 'Kade Walker').__dict__
)
table.put_item(
    Item = Item('Alex', 'Alex Paulson').__dict__
)
table.put_item(
    Item = Item('Light', 'Light Godrey').__dict__
)
table.put_item(
    Item = Item('Bob', 'Bob Builder').__dict__
)
table.put_item(
    Item = Item('Sirus', 'Sirus Black').__dict__
)
table.put_item(
    Item = Item('Frank', 'Frank Bank').__dict__
)
table.put_item(
    Item = Item('Jack', 'Jack Black').__dict__
)
table.put_item(
    Item = Item('Aleister', 'Aleister Incant').__dict__
)
table.put_item(
    Item = Item('Vivian', 'Vivian McRoy').__dict__
)
table.put_item(
    Item = Item('Howard', 'Howard Appliances').__dict__
)
table.put_item(
    Item = Item('Rock', 'The Rock').__dict__
)
table.put_item(
    Item = Item('Mick', 'Mike Salmon').__dict__
)
table.put_item(
    Item = Item('Rick', 'Richard Fools').__dict__
)
table.put_item(
    Item = Item('Sielvester', 'Seilvester Cartwile').__dict__
)
table.put_item(
    Item = Item('Dank', 'Dank Memes').__dict__
)
table.put_item(
    Item = Item('Sam', 'Samauel Jackson').__dict__
)
table.put_item(
    Item = Item('Alexa', 'Alexa Alexa').__dict__
)
table.put_item(
    Item = Item('Lily', 'Lily Rooks').__dict__
)
table.put_item(
    Item = Item('Hal', 'Hal Supercomputer').__dict__
)
table.put_item(
    Item = Item('reggie', 'Reggie').__dict__
)