from pydantic import BaseModel


class IPLookupRequest(BaseModel):
    ip_address: str