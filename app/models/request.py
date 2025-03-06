from pydantic import BaseModel
from typing import List, Optional

class RequestStatus(BaseModel):
    request_id: str
    status: str  # "processing" or "completed"
    data: List[dict]  # List of product image details
