from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
import random
import uuid
from typing import Dict

app = FastAPI(
    title="Microservices API QA Mock",
    description="A mock backend to simulate an e-commerce microservices environment for QA validation.",
    version="1.0.0"
)

# In-memory storage for users
users_db: Dict[str, dict] = {}

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Full name of the user, 2-50 characters")
    email: EmailStr = Field(..., description="Valid email address")
    age: int = Field(..., ge=18, le=120, description="Age of the user, must be between 18 and 120")

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    age: int

class OrderCheckout(BaseModel):
    user_id: str = Field(..., description="ID of the user placing the order")
    item_id: str = Field(..., min_length=1, description="ID of the item being purchased")
    quantity: int = Field(..., gt=0, description="Number of items to purchase")

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    user_id = str(uuid.uuid4())
    new_user = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }
    users_db[user_id] = new_user
    return new_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/checkout", status_code=status.HTTP_200_OK)
async def process_checkout(order: OrderCheckout):
    # Validate user exists
    if order.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found for checkout")

    # Simulate 20% failure rate for a "flaky" third-party integration
    if random.random() < 0.20:
        raise HTTPException(
            status_code=500, 
            detail="Payment gateway timeout. Please try again."
        )
    
    return {
        "status": "success",
        "message": "Order processed successfully",
        "order_id": str(uuid.uuid4()),
        "total_items": order.quantity
    }
