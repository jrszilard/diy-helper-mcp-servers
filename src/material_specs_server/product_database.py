"""
Product Database Manager
Coordinates searches across multiple suppliers
"""

import asyncio
from typing import List, Dict, Optional
from .suppliers.base_supplier import Product
from .suppliers.home_depot import HomeDepotSupplier


class ProductDatabase:
    """Manages product searches across multiple suppliers"""
    
    def __init__(self):
        self.suppliers = {
            "home_depot": HomeDepotSupplier(),
            # Add more suppliers as they're implemented
            # "lowes": LowesSupplier(),
            # "ferguson": FergusonSupplier(),
        }
    
    async def search_all_suppliers(
        self,
        query: str,
        category: Optional[str] = None,
        zip_code: Optional[str] = None,
        max_price: Optional[float] = None,
        limit_per_supplier: int = 5
    ) -> List[Product]:
        """
        Search across all suppliers and combine results
        """
        # Search all suppliers concurrently
        tasks = [
            supplier.search_products(
                query=query,
                category=category,
                zip_code=zip_code,
                max_price=max_price,
                limit=limit_per_supplier
            )
            for supplier in self.suppliers.values()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results from all suppliers
        all_products = []
        for result in results:
            if isinstance(result, list):
                all_products.extend(result)
            elif isinstance(result, Exception):
                print(f"Supplier error: {result}")
        
        # Remove duplicates (same product from different suppliers)
        unique_products = self._deduplicate_products(all_products)
        
        # Sort by price and rating
        unique_products.sort(
            key=lambda p: (p.price, -p.rating if p.rating else 0)
        )
        
        return unique_products
    
    def _deduplicate_products(self, products: List[Product]) -> List[Product]:
        """Remove duplicate products based on name similarity"""
        # Simple deduplication by name
        # TODO: Implement more sophisticated matching (UPC, manufacturer part number)
        seen_names = set()
        unique = []
        
        for product in products:
            name_key = product.name.lower().strip()
            if name_key not in seen_names:
                seen_names.add(name_key)
                unique.append(product)
        
        return unique
    
    async def get_product_by_id(
        self,
        product_id: str,
        supplier: Optional[str] = None
    ) -> Optional[Product]:
        """Get specific product details"""
        if supplier and supplier in self.suppliers:
            return await self.suppliers[supplier].get_product_details(product_id)
        
        # Try all suppliers if supplier not specified
        for supplier_obj in self.suppliers.values():
            product = await supplier_obj.get_product_details(product_id)
            if product:
                return product
        
        return None
    
    async def find_alternatives(
        self,
        product: Product,
        budget_range: Optional[tuple] = None
    ) -> List[Product]:
        """
        Find alternative products similar to the given product
        
        Args:
            product: Original product
            budget_range: (min_price, max_price) tuple
        """
        # Search for similar products in same category
        alternatives = await self.search_all_suppliers(
            query=f"{product.category} {product.subcategory}",
            category=product.category,
            limit_per_supplier=10
        )
        
        # Filter by budget range if specified
        if budget_range:
            min_price, max_price = budget_range
            alternatives = [
                p for p in alternatives 
                if min_price <= p.price <= max_price
            ]
        
        # Remove the original product
        alternatives = [p for p in alternatives if p.id != product.id]
        
        # Sort by price
        alternatives.sort(key=lambda p: p.price)
        
        return alternatives
    
    async def check_compatibility(
        self,
        product1_id: str,
        product2_id: str
    ) -> Dict:
        """
        Check if two products are compatible
        For MVP: Basic compatibility rules
        TODO: Build comprehensive compatibility database
        """
        product1 = await self.get_product_by_id(product1_id)
        product2 = await self.get_product_by_id(product2_id)
        
        if not product1 or not product2:
            return {"error": "One or both products not found"}
        
        # Basic compatibility checks
        compatibility = {
            "compatible": False,
            "confidence": "low",
            "notes": []
        }
        
        # PEX pipe and fittings
        if "pex" in product1.name.lower() or "pex" in product2.name.lower():
            if "sharkbite" in (product1.name + product2.name).lower():
                compatibility["compatible"] = True
                compatibility["confidence"] = "high"
                compatibility["notes"].append(
                    "SharkBite fittings work with PEX-A, PEX-B, PEX-C, copper, and CPVC"
                )
        
        # Electrical compatibility
        if product1.category == "electrical" and product2.category == "electrical":
            # Check voltage/amperage compatibility
            spec1 = product1.specifications
            spec2 = product2.specifications
            
            if spec1.get("voltage") == spec2.get("voltage"):
                if spec1.get("amperage") == spec2.get("amperage"):
                    compatibility["compatible"] = True
                    compatibility["confidence"] = "medium"
                    compatibility["notes"].append(
                        f"Both rated for {spec1.get('voltage')}V and {spec1.get('amperage')}A"
                    )
        
        return compatibility