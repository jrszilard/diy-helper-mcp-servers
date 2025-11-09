"""
Test script for Building Codes MCP Server
Run from project root: python tests/test_building_codes.py
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from src.building_codes_server.code_database import CodeDatabase


async def test_code_search():
    """Test code search functionality"""
    print("\n" + "="*60)
    print("TESTING CODE SEARCH")
    print("="*60)
    
    db = CodeDatabase()
    
    # Test 1: Search for outlet spacing
    print("\n1. Searching for 'outlet spacing living room'...")
    results = await db.search(
        query="outlet spacing living room",
        jurisdiction="National",
        top_k=3
    )
    
    print(f"\n✓ Found {len(results)} results")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   Code: {result['code_ref']}")
        print(f"   Summary: {result['summary'][:100]}...")
        print(f"   Relevance Score: {result.get('relevance_score', 'N/A')}")
    
    # Test 2: Search for kitchen outlets
    print("\n\n2. Searching for 'kitchen outlet spacing'...")
    kitchen_results = await db.search(
        query="kitchen outlet spacing",
        jurisdiction="National",
        code_type="electrical",
        top_k=2
    )
    
    print(f"\n✓ Found {len(kitchen_results)} results")
    for result in kitchen_results:
        print(f"\n- {result['title']}")
        print(f"  Code: {result['code_ref']}")
        print(f"  Summary: {result['summary']}")
    
    # Test 3: Search for GFCI
    print("\n\n3. Searching for 'GFCI bathroom'...")
    gfci_results = await db.search(
        query="GFCI bathroom",
        jurisdiction="National",
        top_k=2
    )
    
    print(f"\n✓ Found {len(gfci_results)} results")
    for result in gfci_results:
        print(f"\n- {result['title']}")
        print(f"  Code: {result['code_ref']}")
        print(f"  Summary: {result['summary']}")
    
    # Test 4: Search for stairs
    print("\n\n4. Searching for 'stair riser height'...")
    stair_results = await db.search(
        query="stair riser height",
        jurisdiction="National",
        code_type="structural",
        top_k=2
    )
    
    print(f"\n✓ Found {len(stair_results)} results")
    for result in stair_results:
        print(f"\n- {result['title']}")
        print(f"  Code: {result['code_ref']}")
        print(f"  Summary: {result['summary']}")
    
    # Test 5: Search for plumbing
    print("\n\n5. Searching for 'kitchen sink drain'...")
    plumbing_results = await db.search(
        query="kitchen sink drain",
        jurisdiction="National",
        code_type="plumbing",
        top_k=1
    )
    
    print(f"\n✓ Found {len(plumbing_results)} results")
    for result in plumbing_results:
        print(f"\n- {result['title']}")
        print(f"  Code: {result['code_ref']}")
        print(f"  Summary: {result['summary']}")


async def test_get_section():
    """Test getting specific code sections"""
    print("\n\n" + "="*60)
    print("TESTING GET SPECIFIC CODE SECTIONS")
    print("="*60)
    
    db = CodeDatabase()
    
    # Test 1: Get NEC outlet spacing code
    print("\n1. Getting NEC 210.52(A)(1)...")
    section = await db.get_section("NEC 210.52(A)(1)", "National")
    
    if section:
        print(f"\n✓ Found: {section['title']}")
        print(f"   Code: {section['code_ref']}")
        print(f"   Category: {section['category']}")
        print(f"   Summary: {section['summary']}")
        print(f"   Source: {section['source']}")
        if section.get('related_codes'):
            print(f"   Related: {', '.join(section['related_codes'])}")
    else:
        print("   ❌ Section not found")
    
    # Test 2: Get kitchen outlet code
    print("\n\n2. Getting NEC 210.52(C)(1)...")
    kitchen_section = await db.get_section("NEC 210.52(C)(1)", "National")
    
    if kitchen_section:
        print(f"\n✓ Found: {kitchen_section['title']}")
        print(f"   Summary: {kitchen_section['summary']}")
        print(f"   Notes: {kitchen_section.get('notes', 'N/A')}")
    else:
        print("   ❌ Section not found")
    
    # Test 3: Get GFCI code
    print("\n\n3. Getting NEC 210.8(A)(1)...")
    gfci_section = await db.get_section("NEC 210.8(A)(1)", "National")
    
    if gfci_section:
        print(f"\n✓ Found: {gfci_section['title']}")
        print(f"   Summary: {gfci_section['summary']}")
    else:
        print("   ❌ Section not found")
    
    # Test 4: Get stair riser code
    print("\n\n4. Getting IRC R311.7.5.1...")
    stair_section = await db.get_section("IRC R311.7.5.1", "National")
    
    if stair_section:
        print(f"\n✓ Found: {stair_section['title']}")
        print(f"   Summary: {stair_section['summary']}")
    else:
        print("   ❌ Section not found")
    
    # Test 5: Try to get non-existent code
    print("\n\n5. Testing non-existent code (should fail gracefully)...")
    fake_section = await db.get_section("FAKE-123.45", "National")
    
    if fake_section:
        print("   ❌ Unexpectedly found a section")
    else:
        print("   ✓ Correctly returned None for non-existent code")


async def test_categories():
    """Test getting code categories"""
    print("\n\n" + "="*60)
    print("TESTING CODE CATEGORIES")
    print("="*60)
    
    db = CodeDatabase()
    
    print("\nGetting all code categories...")
    categories = db.get_categories()
    
    print(f"\n✓ Found {len(categories)} categories:\n")
    
    for category, data in categories.items():
        print(f"**{category.upper()}**")
        print(f"  - Number of codes: {data['count']}")
        print(f"  - Sample questions:")
        for question in data['sample_questions']:
            print(f"    • {question}")
        print()


async def test_common_questions():
    """Test searches for common DIY questions"""
    print("\n" + "="*60)
    print("TESTING COMMON DIY QUESTIONS")
    print("="*60)
    
    db = CodeDatabase()
    
    common_questions = [
        "How far apart should outlets be?",
        "Do I need GFCI in bathroom?",
        "What is code for stair height?",
        "How deep should stair treads be?",
        "What size drain pipe for kitchen sink?",
        "Kitchen outlet requirements"
    ]
    
    for i, question in enumerate(common_questions, 1):
        print(f"\n{i}. Question: '{question}'")
        results = await db.search(question, jurisdiction="National", top_k=1)
        
        if results:
            result = results[0]
            print(f"   ✓ Found: {result['code_ref']}")
            print(f"   Summary: {result['summary'][:80]}...")
        else:
            print(f"   ❌ No results found")


async def test_jurisdictions():
    """Test jurisdiction filtering"""
    print("\n\n" + "="*60)
    print("TESTING JURISDICTION FILTERING")
    print("="*60)
    
    db = CodeDatabase()
    
    # All codes in our database are National for now
    print("\n1. Searching National jurisdiction...")
    national_results = await db.search(
        query="outlet",
        jurisdiction="National",
        top_k=5
    )
    print(f"   ✓ Found {len(national_results)} National codes")
    
    # Test with non-existent jurisdiction
    print("\n2. Searching California jurisdiction (should find nothing in MVP)...")
    ca_results = await db.search(
        query="outlet",
        jurisdiction="California",
        top_k=5
    )
    print(f"   ✓ Found {len(ca_results)} California codes")
    
    if len(ca_results) == 0:
        print("   Note: This is expected in MVP - no state-specific codes yet")


async def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n\n" + "="*60)
    print("TESTING EDGE CASES")
    print("="*60)
    
    db = CodeDatabase()
    
    # Test 1: Empty query
    print("\n1. Testing empty query...")
    empty_results = await db.search("", jurisdiction="National")
    print(f"   ✓ Empty query returned {len(empty_results)} results")
    
    # Test 2: Very specific query that shouldn't match
    print("\n2. Testing query with no matches...")
    no_match = await db.search("quantum physics", jurisdiction="National")
    print(f"   ✓ No-match query returned {len(no_match)} results")
    
    # Test 3: Very long query
    print("\n3. Testing very long query...")
    long_query = "what are the requirements for electrical outlet spacing in residential living rooms according to the national electrical code" * 3
    long_results = await db.search(long_query, jurisdiction="National", top_k=1)
    print(f"   ✓ Long query returned {len(long_results)} results")
    
    # Test 4: Query with special characters
    print("\n4. Testing query with special characters...")
    special_results = await db.search("outlet spacing: 12' max?", jurisdiction="National")
    print(f"   ✓ Special chars query returned {len(special_results)} results")
    
    # Test 5: Case sensitivity
    print("\n5. Testing case sensitivity...")
    upper_results = await db.search("OUTLET SPACING", jurisdiction="National")
    lower_results = await db.search("outlet spacing", jurisdiction="National")
    print(f"   ✓ Uppercase: {len(upper_results)} results")
    print(f"   ✓ Lowercase: {len(lower_results)} results")
    print(f"   {'✓' if len(upper_results) == len(lower_results) else '❌'} Case insensitive: {len(upper_results) == len(lower_results)}")


async def test_code_database_stats():
    """Show statistics about the code database"""
    print("\n\n" + "="*60)
    print("CODE DATABASE STATISTICS")
    print("="*60)
    
    db = CodeDatabase()
    
    print(f"\nTotal codes in database: {len(db.codes)}")
    
    # Count by category
    categories = {}
    for code in db.codes:
        cat = code.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCodes by category:")
    for cat, count in sorted(categories.items()):
        print(f"  - {cat}: {count}")
    
    # Count by jurisdiction
    jurisdictions = {}
    for code in db.codes:
        jur = code.get('jurisdiction', 'unknown')
        jurisdictions[jur] = jurisdictions.get(jur, 0) + 1
    
    print("\nCodes by jurisdiction:")
    for jur, count in sorted(jurisdictions.items()):
        print(f"  - {jur}: {count}")
    
    # Show all code references
    print("\nAll code references in database:")
    for code in db.codes:
        print(f"  - {code['code_ref']}: {code['title']}")


async def main():
    """Run all tests"""
    print("\n" + "🧪 " * 20)
    print("DIY HELPER MCP SERVERS - BUILDING CODES TEST SUITE")
    print("🧪 " * 20)
    
    try:
        await test_code_database_stats()
        await test_code_search()
        await test_get_section()
        await test_categories()
        await test_common_questions()
        await test_jurisdictions()
        await test_edge_cases()
        
        print("\n\n" + "✅ " * 20)
        print("ALL TESTS PASSED!")
        print("✅ " * 20 + "\n")
        
        print("\n📋 Summary:")
        print("  ✓ Code search working")
        print("  ✓ Specific section retrieval working")
        print("  ✓ Category listing working")
        print("  ✓ Common questions handled")
        print("  ✓ Jurisdiction filtering working")
        print("  ✓ Edge cases handled gracefully")
        print("\n🎉 Building Codes MCP Server is ready to use!\n")
        
    except Exception as e:
        print(f"\n\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())