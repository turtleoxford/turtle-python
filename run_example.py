import sys
import subprocess
from pathlib import Path
from os.path import join

# Mapping from chapter code to example directory
CHAPTER_PATHS = {
    "01": "examples/examples_1_drawing_and_counting_loops",
    "02": "examples/examples_2_functions_simple_recursion",
    "03": "examples/examples_3_further_commands_structures",
    "04": "examples/examples_4_smooth_movement_bouncing",
    "05": "examples/examples_5_user_input_interaction_games",
    "06": "examples/examples_6_file_directory_handling",
    "07": "examples/examples_7_cellular_models",
    "08": "examples/examples_8_other_models",
    "09": "examples/examples_9_self_similarity_chaos",
    "10": "examples/examples_10_computer_science_logic",
}

# Mapping from chapter and letter code to example filename (without .py extension)
EXAMPLE_MAP = {
    "01": {
        "a": "simple_drawing_with_pauses",
        "b": "smiley_face",
        "c": "plough",
        "d": "olympic_rings",
        "e": "for_loop",
        "f": "spinning_triangle",
        "g": "circling_circles",
        "h": "nested_for_loops",
        # i, j skipped
    },
    "02": {
        "a": "spiral_of_colours",
        "b": "simple_function",
        "c": "function_with_parameter",
        "d": "resizable_face",
        "e": "polygons",
        "f": "stars",
        "g": "polygon_rings",
        "h": "simple_triangle",
        "i": "triangle_function",
        "j": "triangle_function_with_limit",
        "k": "recursive_triangle",
        "l": "recursive_factorials",
    },
    "03": {
        "a": "text_arrow",
        "b": "cycling_colours",
        "c": "analogue_clock",
        "d": "digital_clock",
        "e": "flashlights",
        # f skipped
        "g": "3d_colour_effects",
        "h": "standard_string_functions",
        "i": "user_defined_strings",
        "j": "list_functions",
        "k": "mathematical_functions",
        "l": "trigonometric_graphs",
    },
    "04": {
        "a": "moving_ball_var",
        "b": "bouncing_ball_var",
        "c": "moving_ball_turtle",
        "d": "bouncing_ball_turtle",
        "e": "bouncing_face",
        "f": "multiple_bouncing_balls",
        "g": "bouncing_triangle",
        "h": "multiple_bouncing_shapes",
        "i": "movement_under_gravity",
        "j": "solar_system",
    },
    "05": {
        "a": "asking_for_typed_input",
        "b": "mouse_reaction_game",
        "c": "typing_game",
        # d skipped
        "e": "iteration_game",
        "f": "throwing_sponges",
        "g": "arcade_shooting_game",
        "h" : "colouring_cells",
        "i": "snake",
        "j": "mouse_drawing",
    },
    "06": {
        "a": "writing_reading_text_file",
        "b": "renaming_deleting_files",
        "c": "file_searching",
        "d": "saving_csv_file",
        "e": "reading_csv_file",
        "f": "random_sentences",
        "g": "file_commands",
        "h": "directory_commands",
    },
    "07": {
        "a": "tipping_point_epidemic",
        "b": "spread_of_disease",
        "c": "game_of_life",
        "d": "game_of_life_user_setup",
        "e": "game_of_life_lists",
        "f": "1d_cellular_automata",
        # g, h skipped
        "i": "schellings_segregation_model",
        "j": "iterated_prisoners_dilemma",
    },
    "08": {
        # a, b skipped
        "c": "launching_rocket_into_orbit",
        "d": "brownian_motion",
        "e": "cheetahs_gazelles",
        "f": "sex_ratio_evolution",
        "g": "flocking_behaviour",
        "h": "town_road_simulation",
        # i skipped
        "j": "two_slit_interference",
    },
    "09": {
        "a": "recursion_factory",
        "b": "recursive_tree",
        "c": "koch_snowflake",
        "d": "square_koch_fractal_curves",
        "e": "sierpinski_triangle_deletion",
        "f": "sierpinski_triangle_random_dots",
        # g, h skipped
        "i": "ifs_background",
        # j, k skipped
        "l": "logistic_equation",
        "m": "logistic_spider",
        # n, o skipped
    },
    "10": {
        "a": "tower_of_hanoi_recursion",
        "b": "binary_search_guessing_game",
        "c": "square_roots_iteration",
        "d": "fibonacci_recursion_iteration",
        "e": "comparison_sorting_methods",
        "f": "comparison_sorting_methods_strings",
        "g": "tic_tac_toe",
        "h": "nim_learning_program",
        "i": "knights_tour_program",
        "j": "turing_machine_simulator",
    },
}


def main():
    if len(sys.argv) < 2:
        print("Usage: run <code>")
        print("\nAvailable example codes:")
        has_examples = False
        for chapter in sorted(EXAMPLE_MAP.keys()):
            if EXAMPLE_MAP[chapter]:
                for letter in sorted(EXAMPLE_MAP[chapter].keys()):
                    filename = EXAMPLE_MAP[chapter][letter] + ".py"
                    full_path = join(CHAPTER_PATHS[chapter], filename)
                    print(f"  {chapter}{letter} -> {full_path}")
                    has_examples = True
        if not has_examples:
            print("  (No examples mapped yet)")
        sys.exit(1)

    code = sys.argv[1].lower()
    
    # Pad single digit codes
    if len(code) == 2 and code[0].isdigit() and code[1].isalpha():
        code = f"0{code}"
    
    # Extract chapter and letter
    if len(code) >= 3:
        chapter = code[:2]
        letter = code[2]
    else:
        print(f"Error: Invalid code format '{code}'. Expected format: <digit><digit><letter> (e.g., 01a, 1a)")
        sys.exit(1)
    
    if chapter not in EXAMPLE_MAP:
        print(f"Error: Unknown chapter '{chapter}'")
        print("\nAvailable chapters:")
        for ch in sorted(EXAMPLE_MAP.keys()):
            print(f"  {ch}")
        sys.exit(1)
    
    if letter not in EXAMPLE_MAP[chapter]:
        print(f"Error: Unknown example '{letter}' in chapter {chapter}")
        print(f"\nAvailable examples in chapter {chapter}:")
        if EXAMPLE_MAP[chapter]:
            for ltr in sorted(EXAMPLE_MAP[chapter].keys()):
                print(f"  {chapter}{ltr}")
        else:
            print("  (No examples in this chapter yet)")
        sys.exit(1)
    
    filename = EXAMPLE_MAP[chapter][letter] + ".py"
    full_path = join(CHAPTER_PATHS[chapter], filename)
    example_path = Path(__file__).parent / full_path
    
    if not example_path.exists():
        print(f"Error: Example file not found: {example_path}")
        sys.exit(1)
    
    print(f"Running: {example_path}")
    try:
        subprocess.run([sys.executable, str(example_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nExample exited with error code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n\nExample interrupted by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
