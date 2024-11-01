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

event={
  "body": "{\"values\": [[5.1, 3.5, 1.4, 0.2]]}"
}

    
response = lambda_handler(event, None)
print(response)
