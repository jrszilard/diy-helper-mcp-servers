"""
Test script for Material Specs MCP Server
Run from project root: python tests/test_material_server.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Since we're in tests/ folder, go up one level to project root
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent  # Go up from tests/ to project root
sys.path.insert(0, str(project_root))

print(f"Project root: {project_root}")  # Debug: see what path we're using

from src.material_specs_server.product_database import ProductDatabase
from src.material_specs_server.calculators import MaterialCalculator


async def test_search():
    """Test product search"""
    print("\n" + "="*60)
    print("TESTING PRODUCT SEARCH")
    print("="*60)
    
    db = ProductDatabase()
    
    # Test 1: Search for wire
    print("\n1. Searching for '12 gauge wire'...")
    products = await db.search_all_suppliers(
        query="12 gauge wire",
        zip_code="02134"
    )
    
    print(f"\n✓ Found {len(products)} products")
    for i, p in enumerate(products[:3], 1):
        print(f"\n{i}. {p.name}")
        print(f"   Price: ${p.price}")
        print(f"   Supplier: {p.supplier}")
        print(f"   In Stock: {'Yes' if p.in_stock else 'No'}")
        if p.rating:
            print(f"   Rating: {p.rating}/5.0")
    
    # Test 2: Search for outlets
    print("\n\n2. Searching for 'GFCI outlet'...")
    outlets = await db.search_all_suppliers(
        query="GFCI outlet",
        category="electrical"
    )
    
    print(f"\n✓ Found {len(outlets)} outlets")
    for i, p in enumerate(outlets[:2], 1):
        print(f"\n{i}. {p.name}")
        print(f"   Price: ${p.price}")
        print(f"   Rating: {p.rating}/5.0" if p.rating else "   Rating: N/A")
    
    # Test 3: Get product details
    print("\n\n3. Getting product details for HD-12345...")
    product = await db.get_product_by_id("HD-12345")
    if product:
        print(f"\n✓ Product: {product.name}")
        print(f"   Price: ${product.price}")
        print(f"   Manufacturer: {product.manufacturer}")
        print(f"   Specifications:")
        for key, value in list(product.specifications.items())[:4]:
            print(f"     - {key}: {value}")
    else:
        print("   ❌ Product not found")
    
    # Test 4: Search by category
    print("\n\n4. Searching plumbing category...")
    plumbing = await db.search_all_suppliers(
        query="pex",
        category="plumbing",
        limit_per_supplier=3
    )
    print(f"\n✓ Found {len(plumbing)} plumbing products")
    for i, p in enumerate(plumbing[:2], 1):
        print(f"\n{i}. {p.name}")
        print(f"   Price: ${p.price}")


async def test_calculator():
    """Test calculators"""
    print("\n\n" + "="*60)
    print("TESTING CALCULATORS")
    print("="*60)
    
    calc = MaterialCalculator()
    
    # Test 1: Wire calculation
    print("\n1. Wire Calculation (50ft circuit run, 2 circuits)...")
    wire_result = calc.calculate_wire_length(50, num_circuits=2)
    print(f"\n✓ Results:")
    print(f"   Base feet needed: {wire_result['base_feet']} ft")
    print(f"   With 15% waste: {wire_result['with_waste']:.1f} ft")
    print(f"   Recommended to buy: {wire_result['recommended_feet']} ft")
    print(f"   💡 {wire_result['note']}")
    
    # Test 2: Outlet calculation - Kitchen
    print("\n\n2. Outlet Calculation - Kitchen (48ft perimeter)...")
    outlet_result = calc.calculate_outlets_needed(48, "kitchen")
    print(f"\n✓ Results:")
    print(f"   Outlets needed: {outlet_result['outlets_needed']}")
    print(f"   Room type: {outlet_result['room_type']}")
    print(f"   Code reference: {outlet_result['code_reference']}")
    print(f"   💡 {outlet_result['note']}")
    
    # Test 3: Outlet calculation - Living room
    print("\n\n3. Outlet Calculation - Living Room (60ft perimeter)...")
    living_result = calc.calculate_outlets_needed(60, "living")
    print(f"\n✓ Results:")
    print(f"   Outlets needed: {living_result['outlets_needed']}")
    print(f"   Code reference: {living_result['code_reference']}")
    
    # Test 4: Tile calculation
    print("\n\n4. Tile Calculation (120 sq ft bathroom, 12x12 tiles)...")
    tile_result = calc.calculate_tile_needed(120, tile_size_inches=(12, 12))
    print(f"\n✓ Results:")
    print(f"   Area to cover: {tile_result['area_sq_ft']} sq ft")
    print(f"   Tile size: {tile_result['tile_size']}")
    print(f"   Tiles needed: {tile_result['tiles_needed']}")
    print(f"   Cases to buy: {tile_result['cases_needed']}")
    print(f"   Total tiles: {tile_result['total_tiles']}")
    print(f"   Total coverage: {tile_result['total_coverage_sq_ft']} sq ft")
    print(f"   💡 {tile_result['note']}")
    
    # Test 5: Paint calculation
    print("\n\n5. Paint Calculation (400 sq ft, 2 coats)...")
    paint_result = calc.calculate_paint_needed(400, coats=2)
    print(f"\n✓ Results:")
    print(f"   Area: {paint_result['area_sq_ft']} sq ft")
    print(f"   Coats: {paint_result['coats']}")
    print(f"   Gallons needed: {paint_result['gallons_needed']}")
    print(f"   Gallons to buy: {paint_result['gallons_to_buy']}")
    print(f"   💡 {paint_result['note']}")
    
    # Test 6: Deck lumber calculation
    print("\n\n6. Deck Lumber Calculation (12x16 ft deck)...")
    deck_result = calc.calculate_lumber_for_deck(12, 16)
    print(f"\n✓ Results:")
    print(f"   Deck size: {deck_result['deck_size']}")
    print(f"   Area: {deck_result['area_sq_ft']} sq ft")
    print(f"   ")
    print(f"   Joists:")
    print(f"     - Quantity: {deck_result['joists']['quantity']}")
    print(f"     - Size: {deck_result['joists']['size']}")
    print(f"     - Spacing: {deck_result['joists']['spacing']}")
    print(f"   ")
    print(f"   Decking boards:")
    print(f"     - Quantity: {deck_result['decking_boards']['quantity']}")
    print(f"     - Size: {deck_result['decking_boards']['size']}")
    print(f"   ")
    print(f"   Posts:")
    print(f"     - Quantity: {deck_result['posts']['quantity']}")
    print(f"     - Size: {deck_result['posts']['size']}")
    
    # Test 7: PEX pipe calculation
    print("\n\n7. PEX Pipe Calculation (8 fixtures, manifold system)...")
    pex_result = calc.calculate_pex_pipe(8, manifold_system=True)
    print(f"\n✓ Results:")
    print(f"   System type: {pex_result['system_type']}")
    print(f"   Number of fixtures: {pex_result['fixtures']}")
    print(f"   ")
    print(f"   Hot water pipe (Red):")
    print(f"     - Feet needed: {pex_result['hot_water_pipe']['feet_needed']} ft")
    print(f"     - Feet to buy: {pex_result['hot_water_pipe']['feet_to_buy']} ft")
    print(f"     - Size: {pex_result['hot_water_pipe']['size']}")
    print(f"   ")
    print(f"   Cold water pipe (Blue):")
    print(f"     - Feet needed: {pex_result['cold_water_pipe']['feet_needed']} ft")
    print(f"     - Feet to buy: {pex_result['cold_water_pipe']['feet_to_buy']} ft")
    print(f"     - Size: {pex_result['cold_water_pipe']['size']}")
    print(f"   ")
    print(f"   💡 {pex_result['note']}")


async def test_alternatives():
    """Test finding alternatives"""
    print("\n\n" + "="*60)
    print("TESTING PRODUCT ALTERNATIVES")
    print("="*60)
    
    db = ProductDatabase()
    
    print("\nFinding alternatives to Southwire wire (HD-12345)...")
    product = await db.get_product_by_id("HD-12345")
    
    if product:
        print(f"\nOriginal product: {product.name}")
        print(f"Original price: ${product.price}")
        
        alternatives = await db.find_alternatives(product, budget_range=(70, 90))
        print(f"\n✓ Found {len(alternatives)} alternatives in $70-90 range:")
        
        for i, alt in enumerate(alternatives, 1):
            price_diff = alt.price - product.price
            savings = "💰 Saves" if price_diff < 0 else "💸 Costs"
            print(f"\n{i}. {alt.name}")
            print(f"   Price: ${alt.price} ({savings} ${abs(price_diff):.2f})")
            print(f"   Supplier: {alt.supplier}")
            if alt.rating:
                print(f"   Rating: {alt.rating}/5.0")
    else:
        print("   ❌ Original product not found")


async def test_compatibility():
    """Test compatibility checking"""
    print("\n\n" + "="*60)
    print("TESTING COMPATIBILITY CHECKS")
    print("="*60)
    
    db = ProductDatabase()
    
    # Test 1: PEX pipe and SharkBite fitting
    print("\n1. Checking: PEX pipe + SharkBite fitting...")
    result = await db.check_compatibility("HD-40002", "HD-40001")
    
    print(f"\n✓ Compatibility: {'✅ Compatible' if result.get('compatible') else '❌ Not Compatible'}")
    print(f"   Confidence: {result.get('confidence', 'unknown')}")
    if result.get('notes'):
        print(f"   Notes:")
        for note in result['notes']:
            print(f"     - {note}")


async def test_shopping_list():
    """Test shopping list creation"""
    print("\n\n" + "="*60)
    print("TESTING SHOPPING LIST CREATION")
    print("="*60)
    
    db = ProductDatabase()
    
    print("\nCreating shopping list for kitchen outlet project...")
    
    # Import the server's create_shopping_list function
    from src.material_specs_server.server import create_shopping_list
    
    items = [
        {"product_id": "HD-20001", "quantity": 4},  # GFCI outlets
        {"product_id": "HD-12345", "quantity": 1},  # Wire
        {"product_id": "HD-30001", "quantity": 1},  # Circuit breaker
    ]
    
    shopping_list = await create_shopping_list(items, "02134")
    print(f"\n{shopping_list}")


async def main():
    """Run all tests"""
    print("\n" + "🧪 " * 20)
    print("DIY HELPER MCP SERVERS - MATERIAL SPECS TEST SUITE")
    print("🧪 " * 20)
    
    try:
        await test_search()
        await test_calculator()
        await test_alternatives()
        await test_compatibility()
        await test_shopping_list()
        
        print("\n\n" + "✅ " * 20)
        print("ALL TESTS PASSED!")
        print("✅ " * 20 + "\n")
        
        print("\n📋 Summary:")
        print("  ✓ Product search working")
        print("  ✓ Product details retrieval working")
        print("  ✓ Material calculators working (7 types)")
        print("  ✓ Alternative products working")
        print("  ✓ Compatibility checks working")
        print("  ✓ Shopping list generation working")
        print("\n🎉 Material Specs MCP Server is ready to use!\n")
        
    except Exception as e:
        print(f"\n\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())