"""
Material Quantity Calculators
Calculate how much material is needed for various projects
"""

import math
from typing import Dict, Optional


class MaterialCalculator:
    """Calculate material quantities for various projects"""
    
    @staticmethod
    def calculate_wire_length(
        circuit_length_feet: float,
        num_circuits: int = 1,
        waste_factor: float = 0.15
    ) -> Dict:
        """
        Calculate electrical wire needed
        
        Args:
            circuit_length_feet: One-way distance in feet
            num_circuits: Number of circuits
            waste_factor: Percentage extra for waste/mistakes (default 15%)
        """
        # Wire needs to go and return, plus waste
        total_feet = circuit_length_feet * 2 * num_circuits
        with_waste = total_feet * (1 + waste_factor)
        
        # Round up to nearest 25 feet (common spool sizes)
        recommended_feet = math.ceil(with_waste / 25) * 25
        
        return {
            "base_feet": total_feet,
            "with_waste": with_waste,
            "recommended_feet": recommended_feet,
            "waste_factor": waste_factor,
            "note": f"Buying {recommended_feet}ft gives you buffer for mistakes and future repairs"
        }
    
    @staticmethod
    def calculate_outlets_needed(
        room_perimeter_feet: float,
        room_type: str = "living"
    ) -> Dict:
        """
        Calculate number of outlets needed per NEC
        
        Args:
            room_perimeter_feet: Total wall perimeter
            room_type: 'living', 'kitchen', 'bathroom', 'garage'
        """
        if room_type == "kitchen":
            # Kitchen countertop: outlet every 4 feet (24 inches from any point)
            # Assuming countertop is 50% of perimeter
            countertop_length = room_perimeter_feet * 0.5
            outlets = math.ceil(countertop_length / 4)
            code_ref = "NEC 210.52(C)(1)"
            note = "Kitchen countertops require outlets every 4 feet maximum"
        
        elif room_type == "bathroom":
            # Bathroom: at least 1 GFCI outlet
            outlets = max(1, math.ceil(room_perimeter_feet / 12))
            code_ref = "NEC 210.52(D)"
            note = "Bathroom requires at least one GFCI outlet, all must be GFCI protected"
        
        else:  # living, bedroom, etc.
            # General rule: outlet every 12 feet (no point more than 6 feet from outlet)
            outlets = math.ceil(room_perimeter_feet / 12)
            code_ref = "NEC 210.52(A)(1)"
            note = "Living spaces require outlets every 12 feet of wall space"
        
        return {
            "outlets_needed": outlets,
            "room_type": room_type,
            "perimeter_feet": room_perimeter_feet,
            "code_reference": code_ref,
            "note": note
        }
    
    @staticmethod
    def calculate_tile_needed(
        area_sq_ft: float,
        tile_size_inches: tuple = (12, 12),
        waste_factor: float = 0.10
    ) -> Dict:
        """
        Calculate tile needed for floor/wall
        
        Args:
            area_sq_ft: Total area to tile
            tile_size_inches: (width, height) in inches
            waste_factor: Extra for cuts/breakage (default 10%)
        """
        # Convert tile size to sq ft
        tile_width_ft = tile_size_inches[0] / 12
        tile_height_ft = tile_size_inches[1] / 12
        tile_area_sq_ft = tile_width_ft * tile_height_ft
        
        # Calculate base tiles needed
        base_tiles = math.ceil(area_sq_ft / tile_area_sq_ft)
        
        # Add waste factor
        total_tiles = math.ceil(base_tiles * (1 + waste_factor))
        
        # Calculate cases (assume 10 tiles per case typically)
        tiles_per_case = 10
        cases_needed = math.ceil(total_tiles / tiles_per_case)
        total_coverage = cases_needed * tiles_per_case * tile_area_sq_ft
        
        return {
            "area_sq_ft": area_sq_ft,
            "tile_size": f"{tile_size_inches[0]}x{tile_size_inches[1]} inches",
            "tiles_needed": total_tiles,
            "cases_needed": cases_needed,
            "total_tiles": cases_needed * tiles_per_case,
            "total_coverage_sq_ft": round(total_coverage, 1),
            "waste_factor": waste_factor,
            "note": f"Ordering {cases_needed} cases gives you {total_tiles - base_tiles} extra tiles for cuts and repairs"
        }
    
    @staticmethod
    def calculate_paint_needed(
        area_sq_ft: float,
        coats: int = 2,
        coverage_per_gallon: int = 350
    ) -> Dict:
        """
        Calculate paint needed
        
        Args:
            area_sq_ft: Total wall/ceiling area
            coats: Number of coats (default 2)
            coverage_per_gallon: Sq ft per gallon (default 350)
        """
        total_area = area_sq_ft * coats
        gallons_needed = total_area / coverage_per_gallon
        
        # Round up to nearest gallon
        gallons_to_buy = math.ceil(gallons_needed)
        
        return {
            "area_sq_ft": area_sq_ft,
            "coats": coats,
            "total_area_to_cover": total_area,
            "gallons_needed": round(gallons_needed, 2),
            "gallons_to_buy": gallons_to_buy,
            "coverage_per_gallon": coverage_per_gallon,
            "note": f"Buy {gallons_to_buy} gallon(s) for {coats} coats"
        }
    
    @staticmethod
    def calculate_lumber_for_deck(
        deck_length_ft: float,
        deck_width_ft: float,
        joist_spacing_inches: int = 16,
        board_width_inches: float = 5.5
    ) -> Dict:
        """
        Calculate lumber needed for deck framing and decking
        
        Args:
            deck_length_ft: Deck length
            deck_width_ft: Deck width
            joist_spacing_inches: Joist spacing (typically 16")
            board_width_inches: Deck board width (typically 5.5" for 2x6)
        """
        area_sq_ft = deck_length_ft * deck_width_ft
        
        # Calculate joists needed
        num_joists = math.ceil((deck_width_ft * 12) / joist_spacing_inches) + 1
        
        # Calculate deck boards needed
        board_width_ft = board_width_inches / 12
        num_boards = math.ceil(deck_length_ft / board_width_ft)
        
        # Calculate posts (assume one every 6-8 feet)
        posts_length = math.ceil(deck_length_ft / 6)
        posts_width = math.ceil(deck_width_ft / 6)
        total_posts = posts_length * posts_width
        
        return {
            "deck_size": f"{deck_length_ft}x{deck_width_ft} feet",
            "area_sq_ft": area_sq_ft,
            "joists": {
                "quantity": num_joists,
                "size": f"2x8x{math.ceil(deck_width_ft)} (or 2x10 for larger spans)",
                "spacing": f"{joist_spacing_inches} inches on center"
            },
            "decking_boards": {
                "quantity": num_boards,
                "size": f"2x6x{math.ceil(deck_width_ft)} or 5/4x6 composite",
                "note": "Add 10% for cuts and waste"
            },
            "posts": {
                "quantity": total_posts,
                "size": "4x4x10 or 4x4x12 depending on height",
                "note": "Actual quantity depends on height and local code"
            },
            "note": "This is a basic estimate. Consult building codes for beam sizes and post spacing based on deck height."
        }
    
    @staticmethod
    def calculate_pex_pipe(
        num_fixtures: int,
        avg_distance_per_fixture: float = 30,
        manifold_system: bool = True
    ) -> Dict:
        """
        Calculate PEX piping needed for plumbing
        
        Args:
            num_fixtures: Number of fixtures (sinks, toilets, etc.)
            avg_distance_per_fixture: Average run length in feet
            manifold_system: True for home-run, False for trunk-and-branch
        """
        if manifold_system:
            # Home-run: each fixture gets dedicated line from manifold
            hot_water_fixtures = math.ceil(num_fixtures * 0.6)  # ~60% need hot
            cold_water_fixtures = num_fixtures
            
            hot_pipe_feet = hot_water_fixtures * avg_distance_per_fixture
            cold_pipe_feet = cold_water_fixtures * avg_distance_per_fixture
        else:
            # Trunk-and-branch: more efficient but more complex
            hot_pipe_feet = (num_fixtures * 0.6) * avg_distance_per_fixture * 0.7
            cold_pipe_feet = num_fixtures * avg_distance_per_fixture * 0.7
        
        # Add 20% waste
        hot_total = math.ceil(hot_pipe_feet * 1.2)
        cold_total = math.ceil(cold_pipe_feet * 1.2)
        
        # Round to coil sizes (100ft or 300ft)
        def round_to_coil(feet):
            if feet <= 100:
                return 100
            elif feet <= 300:
                return 300
            else:
                return math.ceil(feet / 300) * 300
        
        hot_to_buy = round_to_coil(hot_total)
        cold_to_buy = round_to_coil(cold_total)
        
        return {
            "system_type": "Manifold (home-run)" if manifold_system else "Trunk-and-branch",
            "fixtures": num_fixtures,
            "hot_water_pipe": {
                "feet_needed": hot_total,
                "feet_to_buy": hot_to_buy,
                "size": "1/2 inch PEX",
                "color": "Red"
            },
            "cold_water_pipe": {
                "feet_needed": cold_total,
                "feet_to_buy": cold_to_buy,
                "size": "1/2 inch PEX",
                "color": "Blue"
            },
            "note": "Also budget for manifold, fittings, and crimp rings. Consider 3/4 inch for main lines."
        }