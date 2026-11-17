import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")
    
    # a) Check if all scores are percentage based (0-100)

    invalid_scores = False
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print(f"Error: Score {item['score']} for '{item['assignment']}' "
                  f"is outside the valid range 0-100.")
            invalid_scores = True
    if invalid_scores:
        print("Please correct the scores above and run the program again.")
        sys.exit(1)

    # Make sure every row belongs to a known category
    for item in data:
        if item['group'].strip().lower() not in ('formative', 'summative'):
            print(f"Error: Unknown group '{item['group']}' for '{item['assignment']}'. "
                  f"Use 'Formative' or 'Summative'.")
            sys.exit(1)

    formative = [d for d in data if d['group'].strip().lower() == 'formative']
    summative = [d for d in data if d['group'].strip().lower() == 'summative']

    # b) Validate total weights (Total=100, Summative=40, Formative=60)

    formative_weight = sum(d['weight'] for d in formative)
    summative_weight = sum(d['weight'] for d in summative)
    total_weight = formative_weight + summative_weight

    weight_ok = True
    if abs(total_weight - 100) > 1e-9:
        print(f"Error: Total weight is {total_weight:g}, it must be exactly 100.")
        weight_ok = False
    if abs(formative_weight - 60) > 1e-9:
        print(f"Error: Formative weight is {formative_weight:g}, it must be exactly 60.")
        weight_ok = False
    if abs(summative_weight - 40) > 1e-9:
        print(f"Error: Summative weight is {summative_weight:g}, it must be exactly 40.")
        weight_ok = False
    if not weight_ok:
        print("Please fix the weights in your CSV file and run the program again.")
        sys.exit(1)


    # c) Calculate the Final Grade and GPA

    formative_points = sum(d['score'] * d['weight'] / 100 for d in formative)
    summative_points = sum(d['score'] * d['weight'] / 100 for d in summative)
    total_grade = formative_points + summative_points
    gpa = (total_grade / 100) * 5.0

    # Category percentages (points earned out of the category weight)
    formative_pct = formative_points / formative_weight * 100
    summative_pct = summative_points / summative_weight * 100


    # d) Determine Pass/Fail status (>= 50% in BOTH categories)

passed = formative_pct >= 50 and summative_pct >= 50
    status = "PASSED" if passed else "FAILED"

    # e) Check for failed formative assignments (< 50%)
    #          and determine which one(s) have the highest weight for resubmission.


        failed_formatives = [d for d in formative if d['score'] < 50]
    resubmit = []
    if failed_formatives:
        highest = failed_formatives[0]['weight']
        for d in failed_formatives:
            if d['weight'] > highest:
                highest = d['weight']
        for d in failed_formatives:
            if d['weight'] == highest:
                resubmit.append(d)


    # f) Print the final decision (PASSED / FAILED) and resubmission options
    print(f"\nFormative: {formative_points:.2f}/{formative_weight:g} ({formative_pct:.2f}%)")
    print(f"Summative: {summative_points:.2f}/{summative_weight:g} ({summative_pct:.2f}%)")
    print(f"Total Grade: {total_grade:.2f}/100")
    print(f"GPA: {gpa:.4f}")
    print(f"\nFinal Status: {status}")

    if resubmit:
        print("\nEligible for resubmission (failed formative with the highest weight):")
        for d in resubmit:
            print(f"  - {d['assignment']} (score: {d['score']:g}, weight: {d['weight']:g})")
    else:
        print("\nNo failed formative assignments. No resubmission needed.")
    
    pass

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
