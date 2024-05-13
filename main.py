import json
import pandas as pd

def find_optimal_comax(wall_height, rebar_diameter, rebar_spacing, w1_thickness, w2_thickness):
    with open('comax_data.json', 'r') as f:
        data = json.load(f)
        df = pd.DataFrame(data['COMAX'])

    valid_boxes = df[
        (df['Diameter'] >= rebar_diameter) &
        (df['E'] == rebar_spacing) &
        (df['W1_min'] <= w1_thickness) &
        (df['W1_max'] >= w1_thickness) &
        (df['W2_min'] <= w2_thickness) &
        (df['W2_max'] >= w2_thickness) &
        (df['p'] <= w1_thickness) &
        (df['b'] <= w1_thickness - 30) 
    ]

    if valid_boxes.empty:
        return None, None

    # Choose the first valid COMAX as the best match (this logic can be adjusted if needed)
    best_comax = valid_boxes.iloc[0]

    # Find the best combination of 83cm and 125cm boxes for the wall height
    best_combination = None
    closest_height_diff = float('inf')
    for num_125 in range(int(wall_height / 125) + 1):
        remaining_height = wall_height - num_125 * 125
        num_83 = int(remaining_height / 83)
        total_height = num_125 * 125 + num_83 * 83
        height_diff = abs(wall_height - total_height)

        if height_diff < closest_height_diff:
            closest_height_diff = height_diff
            best_combination = {'num_125': num_125, 'num_83': num_83}

    return best_combination, best_comax

#Get user input
wall_height = float(input("Enter wall height (cm): "))
rebar_diameter = float(input("Enter rebar diameter (mm): "))
rebar_spacing = float(input("Enter rebar spacing (mm): "))
w1_thickness = float(input("Enter wall thickness for W1 (mm): "))
w2_thickness = float(input("Enter wall thickness for W2 (mm): "))

# Find and display the optimal combination and attributes
best_combination, best_comax = find_optimal_comax(wall_height, rebar_diameter, rebar_spacing, w1_thickness, w2_thickness)

if best_combination is not None and best_comax is not None:
    if wall_height < 83:
        print(f"\n1 x 83cm COMAX Type A {best_comax['Attribute']} can be used (cut to size on site).")
    else:
        print(f"\nCOMAX Type A {best_comax['Attribute']} is the best for you.")
        print(f"The best combination for your floor height ({wall_height}cm) is: {int(best_combination['num_125'])} x 125cm COMAX Type A, {int(best_combination['num_83'])} x 83cm COMAX Type A")
else:
    print("\nNo suitable COMAX combinations found. Consider adjusting your wall dimensions or rebar specifications.")