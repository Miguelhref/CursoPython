from pydantic import BaseModel

class clientGetDataAmazonAsin(BaseModel):
    storeName: str
    tableName: str