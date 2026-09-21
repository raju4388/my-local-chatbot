import json
import re
from rapidfuzz import fuzz


# -----------------------------------------
# Load questions_answers.json
# -----------------------------------------

with open("questions_answers.json", "r", encoding="utf-8") as file:
    data = json.load(file)


# -----------------------------------------
# Clean user input
# -----------------------------------------

def clean_text(text):

    text = text.lower().strip()

    # Remove punctuation
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text


# -----------------------------------------
# Get answer
# -----------------------------------------

def get_answer(user_question):

    user_question = clean_text(user_question)

    if not user_question:
        return "Please enter a question."


    # =========================================
    # 1. EXACT QUESTION MATCH
    # =========================================

    for item in data:

        question = clean_text(
            item.get("question", "")
        )

        if user_question == question:

            return item["answer"]


    # =========================================
    # 2. EXACT ALTERNATIVE MATCH
    # =========================================

    for item in data:

        alternatives = item.get(
            "alternatives",
            []
        )

        for alternative in alternatives:

            alternative = clean_text(
                alternative
            )

            if user_question == alternative:

                return item["answer"]


    # =========================================
    # 3. EXACT KEYWORD MATCH
    # =========================================

    user_words = set(
        user_question.split()
    )

    for item in data:

        keywords = item.get(
            "keywords",
            []
        )

        for keyword in keywords:

            keyword = clean_text(
                keyword
            )

            if user_question == keyword:

                return item["answer"]


    # =========================================
    # 4. KEYWORD INSIDE SENTENCE
    # =========================================

    for item in data:

        keywords = item.get(
            "keywords",
            []
        )

        for keyword in keywords:

            keyword = clean_text(
                keyword
            )

            if keyword in user_words:

                common_words = {
                    "what",
                    "is",
                    "the",
                    "for",
                    "how",
                    "can",
                    "tell",
                    "me",
                    "about",
                    "exam",
                    "study"
                }

                if keyword not in common_words:

                    return item["answer"]


    # =========================================
    # 5. FUZZY MATCHING
    # =========================================

    best_score = 0

    best_answer = None


    for item in data:

        # -------------------------------------
        # Main question
        # -------------------------------------

        question = clean_text(
            item.get("question", "")
        )

        score = fuzz.token_set_ratio(
            user_question,
            question
        )

        if score > best_score:

            best_score = score

            best_answer = item["answer"]


        # -------------------------------------
        # Alternatives
        # -------------------------------------

        for alternative in item.get(
            "alternatives",
            []
        ):

            alternative = clean_text(
                alternative
            )

            score = fuzz.token_set_ratio(
                user_question,
                alternative
            )

            if score > best_score:

                best_score = score

                best_answer = item["answer"]


    # =========================================
    # 6. Return fuzzy result
    # =========================================

    if best_score >= 55:

        return best_answer


    # =========================================
    # 7. No answer found
    # =========================================

    return (
        "Sorry, I don't know the answer to that question. "
        "Please ask me about AP EAMCET topics such as "
        "syllabus, eligibility, subjects, exam pattern, "
        "application, hall ticket, results, rank, counselling, "
        "colleges or preparation."
    )