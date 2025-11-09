"""
Simple test - uses direct file imports
"""

import asyncio
import os
import sys

# Print current directory
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Adding to path: {current_dir}")
sys.path.insert(0, current_dir)

# Try importing
print("\nAttempting imports...")

try:
    from src.material_specs_server.calculators import MaterialCalculator
    print("✓ Successfully imported MaterialCalculator")
    
    from src.material_specs_server.product_database import ProductDatabase
    print("✓ Successfully imported ProductDatabase")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check that all __init__.py files exist")
    print("2. Check your directory structure")
    print("3. Try: python -c 'import sys; print(sys.path)'")
    sys.exit(1)


async def quick_test():
    """Quick test of basic functionality"""
    print("\n" + "="*60)
    print("RUNNING QUICK TEST")
    print("="*60)
    
    # Test calculator
    print("\nTesting MaterialCalculator...")
    calc = MaterialCalculator()
    result = calc.calculate_wire_length(50, num_circuits=1)
    print(f"✓ Wire calculation works: {result['recommended_feet']} feet recommended")
    
    # Test database
    print("\nTesting ProductDatabase...")
    db = ProductDatabase()
    products = await db.search_all_suppliers("wire", limit_per_supplier=2)
    print(f"✓ Product search works: found {len(products)} products")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(quick_test())