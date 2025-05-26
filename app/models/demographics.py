from pydantic import BaseModel, Field

class Demographics(BaseModel):
    age: int = Field(..., description="Age of the participant")
    education: str = Field(..., description="Highest level of education completed")
    familiarity_with_cognitive_science: str = Field(..., description="Self-rated familiarity with cognitive science")