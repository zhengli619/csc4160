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
    
    pass  # Replace with your implementations
