import boto3
from boto3.dynamodb.types import TypeDeserializer
import datetime
deserializer = TypeDeserializer()

class DataFetch():
    def __init__(self, device_id, data_limit):
        self.client = boto3.client('dynamodb', region_name='us-west-2')
        self.device_id = device_id
        self.data_limit = data_limit

    def get_data(self):
        response = self.client.query(
            TableName = 'basement_pi_table',
            KeyConditionExpression = 'device_id = :device_id',
            ExpressionAttributeValues = {
                ':device_id' : {'S' : f'{self.device_id}'}
            },
            Limit = self.data_limit,
            ScanIndexForward = False
        )

        self.stream_arr = []
        for msg in response['Items']:
            doc = msg['payload']['M']
            des_doc = {k: deserializer.deserialize(v) for k, v in doc.items()}
            self.stream_arr.append(des_doc[f'{self.stream_name}'])

    def return_data(self, stream_name):
        self.stream_name = stream_name
        self.get_data()
        return self.stream_arr  

# data = DataFetch('basement_pi_sensor_002', 10)
# # print(type(data.return_data('time')[-1]))
# date_time_obj = datetime.datetime.strptime(data.return_data('time')[-1], '%Y-%m-%d %H:%M:%S.%f')
# new_time = date_time_obj + datetime.timedelta(seconds=10)
# new_time = new_time.strftime('%Y-%m-%d %H:%M:%S.%f')
# print(new_time)
# print(data.return_data('temperature'))