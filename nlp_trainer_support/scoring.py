from __future__ import annotations

import json


def _load_payload(value):
    if isinstance(value, str):
        return json.loads(value)
    return value or {}


def _normalise_text(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def _keyword_score(answer: str, keywords: list[str]) -> tuple[float, list[str]]:
    answer_normalised = _normalise_text(answer)
    hits = [keyword for keyword in keywords if _normalise_text(keyword) in answer_normalised]
    if not keywords:
        return 0.0, hits
    return len(hits) / len(keywords), hits


def score_submission(exercise, response: dict, mode: str) -> dict:
    content = _load_payload(exercise["content_json"] if "content_json" in exercise.keys() else exercise["content"])
    scoring = _load_payload(exercise["scoring_json"] if "scoring_json" in exercise.keys() else exercise["scoring"])
    exercise_type = exercise["exercise_type"]
    max_score = float(exercise["max_score"])
    requires_review = bool(exercise["requires_manual_review"])
    model_answer = content.get("model_answer", "")

    if exercise_type == "multiple_choice":
        selected = response.get("selected", "")
        is_correct = selected == scoring.get("correct_option")
        score = max_score if is_correct else 0.0
        feedback = "Correct." if is_correct else "Niet correct."
        return _result(score, max_score, feedback, model_answer, requires_review=False)

    if exercise_type == "multi_select":
        selected = set(response.get("selected", []))
        correct = set(scoring.get("correct_options", []))
        if not selected and not correct:
            ratio = 1.0
        elif not selected and correct:
            ratio = 0.0
        else:
            ratio = len(selected & correct) / len(selected | correct)
        score = round(max_score * ratio, 2)
        feedback = f"Je overlap met de juiste set is {round(ratio * 100)}%."
        return _result(score, max_score, feedback, model_answer, requires_review=False)

    if exercise_type == "match_pairs":
        submitted = response.get("matches", {})
        correct_matches = scoring.get("correct_matches", {})
        total = max(len(correct_matches), 1)
        correct_count = sum(1 for left, right in correct_matches.items() if submitted.get(left) == right)
        score = round(max_score * (correct_count / total), 2)
        feedback = f"Je had {correct_count} van de {total} koppelingen correct."
        return _result(score, max_score, feedback, model_answer, requires_review=False)

    if exercise_type == "short_answer":
        answer = response.get("answer", "")
        ratio, hits = _keyword_score(answer, scoring.get("keywords", []))
        score = round(max_score * ratio, 2)
        threshold = float(scoring.get("threshold", 0.4))
        feedback = (
            f"Je antwoord raakte {len(hits)} relevante kernwoorden. "
            f"Drempel voor een sterk antwoord: {int(threshold * 100)}%."
        )
        return _result(score, max_score, feedback, model_answer, requires_review=False)

    if exercise_type == "study_card":
        answer = _normalise_text(response.get("answer", ""))
        feedback = (
            "Je antwoord is opgeslagen. Vergelijk het met het modelantwoord en bepaal daarna of je deze vraag later nog eens wilt oefenen."
            if answer
            else "Vul eerst een antwoord in om deze studiekaart als voltooid te markeren."
        )
        score = None if answer else 0.0
        return _result(score, max_score, feedback, model_answer, requires_review=False)

    if exercise_type == "text_analysis":
        selected = response.get("selected", "")
        follow_up = response.get("follow_up", "")
        option_score = 0.5 if selected == scoring.get("correct_option") else 0.0
        ratio, hits = _keyword_score(follow_up, scoring.get("follow_up_keywords", []))
        follow_score = 0.5 * ratio
        score = round(max_score * (option_score + follow_score), 2)
        feedback = (
            f"Patroonherkenning: {'goed' if option_score else 'nog niet goed'}. "
            f"Je follow-up raakte {len(hits)} relevante aanknopingspunten."
        )
        return _result(score, max_score, feedback, model_answer, requires_review=False)

    if exercise_type in {"reflection", "case_review"}:
        review_message = (
            "Je antwoord is opgeslagen. Een trainer kan dit nu van feedback en een score voorzien."
            if mode == "exam" or requires_review
            else "Je antwoord is opgeslagen."
        )
        return _result(None, max_score, review_message, model_answer, requires_review=True)

    return _result(0.0, max_score, "Onbekend oefentype.", model_answer, requires_review=requires_review)


def _result(
    score: float | None,
    max_score: float,
    feedback: str,
    model_answer: str,
    requires_review: bool,
) -> dict:
    passed = None if score is None else score >= (0.7 * max_score)
    return {
        "auto_score": score,
        "max_score": max_score,
        "feedback": feedback,
        "model_answer": model_answer,
        "requires_review": requires_review,
        "passed": passed,
    }
