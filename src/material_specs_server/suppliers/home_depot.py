"""
Home Depot Supplier Integration
For MVP: Mock data. Replace with real API when available.
"""

import asyncio
from typing import List, Dict, Optional
from .base_supplier import BaseSupplier, Product


class HomeDepotSupplier(BaseSupplier):
    """Home Depot product supplier"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.name = "Home Depot"
        
        # Mock product database for MVP
        self.mock_products = self._initialize_mock_products()
    
    def _initialize_mock_products(self) -> List[Product]:
        """Initialize mock product database"""
        return [
            # Electrical Wire
            Product(
                id="HD-12345",
                name="Southwire 250 ft. 12/2 Solid Romex SIMpull CU NM-B W/G Wire",
                category="electrical",
                subcategory="wire",
                price=87.43,
                supplier="Home Depot",
                in_stock=True,
                quantity_available=47,
                specifications={
                    "gauge": "12 AWG",
                    "conductors": "2 with ground",
                    "ampacity_60c": "20A",
                    "ampacity_90c": "25A",
                    "voltage_rating": "600V",
                    "length": "250 feet",
                    "insulation": "PVC",
                    "wire_type": "NM-B (Romex)",
                    "material": "Copper"
                },
                url="https://www.homedepot.com/p/12345",
                image_url="https://images.homedepot.com/productImages/12345.jpg",
                rating=4.7,
                review_count=2340,
                manufacturer="Southwire"
            ),
            Product(
                id="HD-12346",
                name="Cerrowire 250 ft. 12/2 NM-B Wire",
                category="electrical",
                subcategory="wire",
                price=79.98,
                supplier="Home Depot",
                in_stock=True,
                quantity_available=23,
                specifications={
                    "gauge": "12 AWG",
                    "conductors": "2 with ground",
                    "ampacity_60c": "20A",
                    "voltage_rating": "600V",
                    "length": "250 feet",
                    "insulation": "PVC",
                    "wire_type": "NM-B",
                    "material": "Copper"
                },
                url="https://www.homedepot.com/p/12346",
                rating=4.5,
                review_count=890,
                manufacturer="Cerrowire"
            ),
            
            # GFCI Outlets
            Product(
                id="HD-20001",
                name="Leviton 15 Amp 125-Volt Duplex Self-Test Tamper-Resistant GFCI Outlet, White",
                category="electrical",
                subcategory="outlets",
                price=16.97,
                supplier="Home Depot",
                in_stock=True,
                quantity_available=156,
                specifications={
                    "amperage": "15A",
                    "voltage": "125V",
                    "type": "GFCI",
                    "color": "White",
                    "features": ["Self-test", "Tamper-resistant", "LED indicator"],
                    "nec_compliant": True
                },
                url="https://www.homedepot.com/p/20001",
                rating=4.8,
                review_count=4523,
                manufacturer="Leviton"
            ),
            Product(
                id="HD-20002",
                name="Eaton 15 Amp 125-Volt Tamper Resistant GFCI Duplex Receptacle, White",
                category="electrical",
                subcategory="outlets",
                price=12.47,
                supplier="Home Depot",
                in_stock=True,
                quantity_available=203,
                specifications={
                    "amperage": "15A",
                    "voltage": "125V",
                    "type": "GFCI",
                    "color": "White",
                    "features": ["Tamper-resistant", "LED indicator"],
                    "nec_compliant": True
                },
                url="https://www.homedepot.com/p/20002",
                rating=4.6,
                review_count=1876,
                manufacturer="Eaton"
            ),
            
            # Circuit Breakers
            Product(
                id="HD-30001",
                name="Square D Homeline 20 Amp Single-Pole GFCI Circuit Breaker",
                category="electrical",
                subcategory="circuit_breakers",
                price=42.98,
                supplier="Home Depot",
                in_stock=True,
                quantity_available=34,
                specifications={
                    "amperage": "20A",
                    "poles": "Single",
                    "type": "GFCI",
                    "compatible_panels": ["Homeline"],
                    "ul_listed": True
                },
                url="https://www.homedepot.com/p/30001",
                rating=4.7,
                review_count=567,
                manufacturer="Square D"
            ),
            
            # PEX Plumbing
            Product(
                id="HD-40001",
                name="SharkBite 1/2 in. Brass Push-to-Connect Coupling",
                category="plumbing",
                subcategory="fittings",
                price=8.97,
                supplier="Home Depot",
                in_stock=True,
                quantity_available=287,
                specifications={
                    "size": "1/2 inch",
                    "material": "Brass",
                    "connection_type": "Push-to-connect",
                    "compatible_with": ["PEX", "Copper", "CPVC"],
                    "max_pressure": "200 PSI",
                    "temp_rating": "200°F"
                },
                url="https://www.homedepot.com/p/40001",
                rating=4.6,
                review_count=3421,
                manufacturer="SharkBite"
            ),
            Product(
                id="HD-40002",
                name="Apollo 100 ft. Coil Red 1/2 in. PEX-A Expansion Pipe",
                category="plumbing",
                subcategory="pipe",
                price=67.98,
                supplier="Home Depot",
                in_stock=True,
                quantity_available=45,
                specifications={
                    "size": "1/2 inch",
                    "material": "PEX-A",
                    "color": "Red (hot water)",
                    "length": "100 feet",
                    "max_pressure": "160 PSI at 73°F",
                    "temp_rating": "200°F",
                    "certifications": ["NSF-61", "NSF-14"]
                },
                url="https://www.homedepot.com/p/40002",
                rating=4.8,
                review_count=892,
                manufacturer="Apollo"
            ),
            
            # Lumber
            Product(
                id="HD-50001",
                name="2 in. x 4 in. x 8 ft. #2 Prime Pressure-Treated Lumber",
                category="lumber",
                subcategory="dimensional_lumber",
                price=8.47,
                supplier="Home Depot",
                in_stock=True,
                quantity_available=342,
                specifications={
                    "dimensions": "2x4x8",
                    "actual_dimensions": "1.5 x 3.5 x 96 inches",
                    "treatment": "Pressure-treated",
                    "grade": "#2 Prime",
                    "species": "Southern Yellow Pine",
                    "use": "Above ground/Ground contact"
                },
                url="https://www.homedepot.com/p/50001",
                rating=4.3,
                review_count=1234,
                manufacturer="Various"
            ),
            Product(
                id="HD-50002",
                name="2 in. x 8 in. x 12 ft. #2 Pressure-Treated Lumber",
                category="lumber",
                subcategory="dimensional_lumber",
                price=22.98,
                supplier="Home Depot",
                in_stock=True,
                quantity_available=156,
                specifications={
                    "dimensions": "2x8x12",
                    "actual_dimensions": "1.5 x 7.25 x 144 inches",
                    "treatment": "Pressure-treated",
                    "grade": "#2",
                    "species": "Southern Yellow Pine",
                    "use": "Ground contact"
                },
                url="https://www.homedepot.com/p/50002",
                rating=4.4,
                review_count=678,
                manufacturer="Various"
            ),
            
            # Tile
            Product(
                id="HD-60001",
                name="MSI Carrara White 12 in. x 12 in. Polished Marble Floor and Wall Tile (10 sq. ft./case)",
                category="flooring",
                subcategory="tile",
                price=31.98,
                supplier="Home Depot",
                in_stock=True,
                quantity_available=67,
                specifications={
                    "size": "12 x 12 inches",
                    "material": "Marble",
                    "finish": "Polished",
                    "coverage": "10 sq ft per case",
                    "pieces_per_case": 10,
                    "thickness": "3/8 inch",
                    "use": "Floor and wall"
                },
                url="https://www.homedepot.com/p/60001",
                rating=4.5,
                review_count=234,
                manufacturer="MSI"
            ),
        ]
    
    async def search_products(
        self,
        query: str,
        category: Optional[str] = None,
        zip_code: Optional[str] = None,
        max_price: Optional[float] = None,
        limit: int = 10
    ) -> List[Product]:
        """
        Search for products
        For MVP: Simple keyword matching on mock data
        TODO: Replace with real Home Depot API
        """
        # Simulate API delay
        await asyncio.sleep(0.1)
        
        query_lower = query.lower()
        results = []
        
        for product in self.mock_products:
            # Filter by category if specified
            if category and product.category != category:
                continue
            
            # Filter by price if specified
            if max_price and product.price > max_price:
                continue
            
            # Simple keyword matching
            searchable = f"{product.name} {product.category} {product.subcategory}".lower()
            
            # Check if any query word matches
            if any(word in searchable for word in query_lower.split()):
                # Add mock store location if zip provided
                if zip_code:
                    product.store_location = "Brighton, MA"
                    product.distance_miles = 2.3
                
                results.append(product)
        
        # Sort by relevance (simple: by price, then rating)
        results.sort(key=lambda p: (p.price, -p.rating if p.rating else 0))
        
        return results[:limit]
    
    async def get_product_details(self, product_id: str) -> Optional[Product]:
        """Get detailed product information"""
        await asyncio.sleep(0.05)
        
        for product in self.mock_products:
            if product.id == product_id:
                return product
        
        return None
    
    async def check_availability(
        self,
        product_id: str,
        zip_code: str
    ) -> Dict:
        """Check product availability at nearby stores"""
        await asyncio.sleep(0.1)
        
        product = await self.get_product_details(product_id)
        
        if not product:
            return {"error": "Product not found"}
        
        # Mock availability data
        return {
            "product_id": product_id,
            "available": product.in_stock,
            "stores": [
                {
                    "name": "Home Depot - Brighton",
                    "address": "201 Everett Ave, Brighton, MA 02134",
                    "distance_miles": 2.3,
                    "quantity": product.quantity_available,
                    "phone": "(617) 555-0123"
                },
                {
                    "name": "Home Depot - Somerville",
                    "address": "75 Mystic Ave, Somerville, MA 02145",
                    "distance_miles": 3.8,
                    "quantity": max(0, product.quantity_available - 20) if product.quantity_available else 0,
                    "phone": "(617) 555-0456"
                }
            ]
        }