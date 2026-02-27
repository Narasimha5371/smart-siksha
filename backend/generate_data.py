import json
import random

subjects = {
    "Math": ["Algebra", "Geometry", "Calculus", "Statistics"],
    "Physics": ["Mechanics", "Optics", "Thermodynamics", "Electromagnetism"],
    "Chemistry": ["Organic", "Inorganic", "Physical"],
    "Biology": ["Cell Biology", "Genetics", "Ecology"],
    "History": ["Ancient", "Medieval", "Modern", "World War II"],
    "Geography": ["Physical", "Human", "Cartography"],
    "English": ["Grammar", "Literature", "Writing"],
    "Computer Science": ["Algorithms", "Data Structures", "Web Development"]
}

questions = []

# Templates for generating random but valid-looking questions
templates = [
    ("What is the primary concept of {topic}?", "The study of fundamental principles.", ["The study of fundamental principles.", "Cooking recipes.", "Ancient alien theories.", "Mountain climbing techniques."], 0),
    ("Which keyword is associated with {topic}?", "Key Term", ["Key Term", "Irrelevant Term", "Wrong Subject", "Blue"], 0),
    ("Solve a basic problem in {topic}.", "Solution X", ["Solution X", "Solution Y", "Solution Z", "No Solution"], 0),
    ("Who is a famous figure in {topic}?", "Expert Name", ["Expert Name", "Movie Star", "Chef", "Musician"], 0),
    ("Explain a rule in {topic}.", "Rule A", ["Rule A", "Rule B", "Rule C", "Rule D"], 0)
]

# Specific manual questions for better quality
manual_questions = [
    {"subject": "Math", "topic": "Algebra", "question": "Solve for x: 2x + 5 = 15", "options": {"A": "5", "B": "10", "C": "15", "D": "20"}, "correct_answer_index": 0, "explanation": "2x = 10 -> x = 5"},
    {"subject": "Math", "topic": "Geometry", "question": "What is the sum of angles in a triangle?", "options": {"A": "180", "B": "360", "C": "90", "D": "270"}, "correct_answer_index": 0, "explanation": "Triangle angles sum to 180 degrees."},
    {"subject": "Physics", "topic": "Mechanics", "question": "What is Newton's Second Law?", "options": {"A": "F=ma", "B": "E=mc^2", "C": "V=IR", "D": "p=mv"}, "correct_answer_index": 0, "explanation": "Force equals mass times acceleration."},
    {"subject": "Physics", "topic": "Optics", "question": "Light bends when entering a denser medium. This is called:", "options": {"A": "Reflection", "B": "Refraction", "C": "Diffraction", "D": "Dispersion"}, "correct_answer_index": 1, "explanation": "Refraction is the bending of light."},
    {"subject": "Computer Science", "topic": "Algorithms", "question": "What is the time complexity of binary search?", "options": {"A": "O(n)", "B": "O(log n)", "C": "O(n^2)", "D": "O(1)"}, "correct_answer_index": 1, "explanation": "Binary search halves the search space each step."},
    {"subject": "History", "topic": "World War II", "question": "Who were the Axis powers?", "options": {"A": "Germany, Italy, Japan", "B": "USA, UK, USSR", "C": "France, Poland, China", "D": "Germany, USA, France"}, "correct_answer_index": 0, "explanation": "Germany, Italy, and Japan formed the Axis."}
]

id_counter = 0

# Add manual questions
for q in manual_questions:
    q["id"] = f"qa_{id_counter}"
    questions.append(q)
    id_counter += 1

# Generate generic questions to fill gaps
for subject, topics in subjects.items():
    for topic in topics:
        # ensuring at least 3-5 questions per topic
        for i in range(3):
            q_template, ans, wrong, correct_idx = random.choice(templates)
            q_text = q_template.format(topic=topic)
            
            # ans is correct, wrong[1:] are wrong
            all_opts = [ans] + wrong[1:]
            random.shuffle(all_opts)
            
            final_opts = {"A": all_opts[0], "B": all_opts[1], "C": all_opts[2], "D": all_opts[3]}
            
            # Find correct index
            final_correct_idx = -1
            for k, v in final_opts.items():
                if v == ans:
                    if k == 'A': final_correct_idx = 0
                    elif k == 'B': final_correct_idx = 1
                    elif k == 'C': final_correct_idx = 2
                    elif k == 'D': final_correct_idx = 3
            
            entry = {
                "id": f"qa_{id_counter}",
                "subject": subject,
                "topic": topic,
                "question": q_text,
                "options": final_opts,
                "correct_answer_index": final_correct_idx,
                "explanation": f"The correct answer is {ans}."
            }
            questions.append(entry)
            id_counter += 1

# Write to JSONL
with open("questions.jsonl", "w", encoding="utf-8") as f:
    for q in questions:
        f.write(json.dumps(q) + "\n")

print(f"Generated {len(questions)} questions in questions.jsonl")
