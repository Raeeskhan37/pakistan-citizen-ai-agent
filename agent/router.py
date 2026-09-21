from config.departments import DEPARTMENTS


def detect_department(
    question,
    selected_department="Automatic",
):

    if selected_department != "Automatic":

        return selected_department

    question_lower = question.lower()

    scores = {}

    for department, data in DEPARTMENTS.items():

        score = 0

        for keyword in data["keywords"]:

            if keyword.lower() in question_lower:
                score += 1

        scores[department] = score

    best_department = max(
        scores,
        key=scores.get,
    )

    if scores[best_department] == 0:

        return "General Government Services"

    return best_department
