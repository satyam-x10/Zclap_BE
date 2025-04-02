from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import uuid
import logging
import traceback
import json

# Import the AgentInfo class and run_chat function from your main module
from app import run_chat, AgentInfo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://zclap.vercel.app/","http:localhost:5173"],  # You can restrict to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define data models for API requests
class AgentInfoAPI(BaseModel):
    model: str
    role: str

class ProductInfoAPI(BaseModel):
    name: str
    description: str
    target_audience: str
    key_features: List[str]

class ContentRequest(BaseModel):
    product: ProductInfoAPI
    agents: List[AgentInfoAPI]

class ContentResponse(BaseModel):
    content: str
    request_id: str

# Convert API model to AgentInfo object
def convert_to_agent_info(agent_api, index):
    # If name is not provided, generate one based on index
    role = agent_api.role if agent_api.role else f"Agent{index+1}"
    return AgentInfo(model=agent_api.model, role=role)

# Convert API model to ProductInfo object (using a dynamic class)
class ProductInfo:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

@app.post("/generate", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    try:
        # Generate a unique ID for this request
        request_id = str(uuid.uuid4())
        
        # Log the received data
        logger.info(f"Received request ID: {request_id}")
        logger.info(f"Product data: {request.product}")
        logger.info(f"Agents data: {request.agents}")
        
        # Convert the API models to the format expected by run_chat
        agents = [convert_to_agent_info(agent, i) for i, agent in enumerate(request.agents)]
        
             
        
        # Convert product to object with attributes
        product_info = ProductInfo(**request.product.dict())
        
        try:
            # Run the chat with the converted objects
            result = run_chat(agents, product_info)
            print('result', result)
            single_string = json.dumps(result)
            print(single_string)
            # Return the results
            return ContentResponse(
                content=single_string,
                request_id=request_id
            )
        except Exception as e:
            # If run_chat fails, log the error and return a mock response
            logger.error(f"Error in run_chat: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Mock response in case of failure
            mock_response = {
                "ContentWriter": "The EcoSmart Home Hub is more than just a smart device; it's your gateway to a sustainable future. Imagine effortlessly managing your home's energy consumption while reducing your carbon footprint and saving money.",
                "GraphicDesigner": "Recommend a clean, minimal design with green and blue color palette. Use circular imagery to represent connectivity and sustainability."
            }
            
            return ContentResponse(
                content=mock_response,
                request_id=request_id
            )
            
    except Exception as e:
        # Log the full traceback for easier debugging
        logger.error(f"Unhandled exception: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)