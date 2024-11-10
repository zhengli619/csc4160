import pickle
import json

# Load the model
filename = 'iris_model.sav'
model = pickle.load(open(filename, 'rb'))

def predict(features):
    return model.predict(features).tolist()

def lambda_handler(event, context):
    # TODO: Implement your own lambda_handler logic here
    # You will need to extract the 'values' from the event and call the predict function.
    
   # Initialize response
    response = {
        'statusCode': 200,
        'body': ''
    }   
    if 'body' in event: # it can be an external request via API gateway
        try:
        # 通过 json.loads(event['body']) 将 JSON 格式的 body 转换为 Python 字典格式。
        # 假设 JSON 对象中有 values 键，该键包含我们需要的预测数据。
        # 将 values 值提取出来并赋值给 extract_values，用于预测。
            extract_values = json.loads(event['body'])['values']
        
            A=predict(extract_values)
            response['body'] = json.dumps({'Prediction':A})
            return response
        except:
            response['statusCode'] = 400
            response['body'] = json.dumps({'error': 'KeyError, ValueError', 'message': 'Invalid input or format.'})
            return response
    else:
        response['statusCode'] = 400
        response['body'] = json.dumps({'error': 'No input found'})
        return response

# event={
#   "body": "{\"values\": [[5.1, 3.5, 1.4, 0.2]]}"
# }

    
response = lambda_handler(event, None)
# 我认为我就算不在lambda_function.py中加入实例示例事件event，到最后由于被变成了一个aws lambda function，会被api触发，
# 所以最终会有个event被传入这个py文件中，不用我主动添加示例事件event，也就是说我在lambda_function.py中不写这一行：
# event = {"body": "{\"values\": [[5.1, 3.5, 1.4, 0.2]]}"}
print(response)
