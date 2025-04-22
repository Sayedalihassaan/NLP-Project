from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI , HTTPException , Depends
from fastapi.security import APIKeyHeader
from src.helper import APP_NAME , VERSION , API_SECRET_KEY
from src.prediction import TextClassifier
from src.schemas import TextRequest , PredictionResponse

# Load the classifier
classifier = TextClassifier()


# Initialize FastAPI App
app = FastAPI(title=APP_NAME , 
              version=VERSION , 
              description= "API For Sentiment Analysis For Twitter Data")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/" , tags=["Healthy"] , description="Healthy Status Checks Endpoint")
async def home() :
    return {
        "app_name" : APP_NAME , 
        "version" : VERSION , 
        "status" : "up & running"
    }




api_key_header = APIKeyHeader(name='X-API-Key')
async def verify_api_key(api_key: str=Depends(api_key_header)):
    if api_key != API_SECRET_KEY:
        raise HTTPException(status_code=403, detail="You are not authorized to use this API")
    return api_key




@app.post("/predict", tags=['Classification'], 
        description='Analyzes the sentiment of provided texts', response_model=PredictionResponse)
async def predict(request: TextRequest, api_key: str=Depends(verify_api_key)):
    
    try:
        predictions = classifier.predict(request.texts)
        return PredictionResponse(predictions=predictions)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
