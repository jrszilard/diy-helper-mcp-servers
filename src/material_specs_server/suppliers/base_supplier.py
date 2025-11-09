"""
Base Supplier Interface
Defines the contract for all supplier integrations
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Product:
    """Standard product data structure"""
    id: str
    name: str
    category: str
    subcategory: str
    price: float
    currency: str = "USD"
    supplier: str = ""
    in_stock: bool = True
    quantity_available: Optional[int] = None
    specifications: Dict = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = 0
    store_location: Optional[str] = None
    distance_miles: Optional[float] = None
    manufacturer: Optional[str] = None
    
    def __post_init__(self):
        if self.specifications is None:
            self.specifications = {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "subcategory": self.subcategory,
            "price": self.price,
            "currency": self.currency,
            "supplier": self.supplier,
            "in_stock": self.in_stock,
            "quantity_available": self.quantity_available,
            "specifications": self.specifications,
            "url": self.url,
            "image_url": self.image_url,
            "rating": self.rating,
            "review_count": self.review_count,
            "store_location": self.store_location,
            "distance_miles": self.distance_miles,
            "manufacturer": self.manufacturer
        }


class BaseSupplier(ABC):
    """Abstract base class for supplier integrations"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.name = "Base Supplier"
    
    @abstractmethod
    async def search_products(
        self,
        query: str,
        category: Optional[str] = None,
        zip_code: Optional[str] = None,
        max_price: Optional[float] = None,
        limit: int = 10
    ) -> List[Product]:
        """Search for products"""
        pass
    
    @abstractmethod
    async def get_product_details(self, product_id: str) -> Optional[Product]:
        """Get detailed product information"""
        pass
    
    @abstractmethod
    async def check_availability(
        self,
        product_id: str,
        zip_code: str
    ) -> Dict:
        """Check product availability at nearby stores"""
        pass
    
    def format_price(self, price: float) -> str:
        """Format price as currency"""
        return f"${price:.2f}"