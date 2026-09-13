"""
Sukoon — Adaptive difficulty engine.

IMPORTANT: This is a deliberately transparent, rule-based engine — NOT a
trained medical AI model. It is designed to be explainable to a caregiver
or judge in one sentence, and is architected so the `decide()` function
could later be swapped for a trained model without touching any caller.

Rules (difficulty is an integer 1-5):
  - High accuracy (>=0.85) AND fast response (<= FAST_MS)   -> increase
  - Low accuracy (<0.5) OR very slow response (> SLOW_MS)    -> decrease
  - Otherwise                                                 -> maintain

Difficulty is clamped to [1, 5].
"""
from dataclasses import dataclass

FAST_MS = 4000
SLOW_MS = 12000
HIGH_ACCURACY = 0.85
LOW_ACCURACY = 0.5

MIN_DIFFICULTY = 1
MAX_DIFFICULTY = 5


@dataclass
class AdaptiveResult:
    new_difficulty: int
    direction: str  # "increased" | "maintained" | "reduced"
    explanation_en: str
    explanation_as: str


def decide(current_difficulty: int, accuracy: float, avg_response_time_ms: int) -> AdaptiveResult:
    current_difficulty = max(MIN_DIFFICULTY, min(MAX_DIFFICULTY, current_difficulty))

    if accuracy >= HIGH_ACCURACY and avg_response_time_ms <= FAST_MS:
        new_difficulty = min(MAX_DIFFICULTY, current_difficulty + 1)
        direction = "increased" if new_difficulty > current_difficulty else "maintained"
        explanation_en = (
            "Activity difficulty increased — recent accuracy was high "
            f"({accuracy*100:.0f}%) and responses were quick. This keeps the activity "
            "appropriately challenging."
        )
        explanation_as = (
            "কাৰ্যকলাপৰ কঠিনতা বৃদ্ধি কৰা হ'ল — শুদ্ধতা উচ্চ আছিল আৰু সঁহাৰি দ্ৰুত আছিল।"
        )
    elif accuracy < LOW_ACCURACY or avg_response_time_ms > SLOW_MS:
        new_difficulty = max(MIN_DIFFICULTY, current_difficulty - 1)
        direction = "reduced" if new_difficulty < current_difficulty else "maintained"
        explanation_en = (
            "Activity difficulty reduced based on recent performance, to keep the "
            "activity comfortable and encouraging rather than frustrating."
        )
        explanation_as = (
            "শেহতীয়া কাৰ্যক্ষমতাৰ ওপৰত ভিত্তি কৰি কাৰ্যকলাপৰ কঠিনতা হ্ৰাস কৰা হ'ল।"
        )
    else:
        new_difficulty = current_difficulty
        direction = "maintained"
        explanation_en = (
            "Activity difficulty kept the same — recent performance has been steady."
        )
        explanation_as = "কাৰ্যকলাপৰ কঠিনতা একেই ৰখা হ'ল — শেহতীয়া কাৰ্যক্ষমতা স্থিৰ আছে।"

    return AdaptiveResult(
        new_difficulty=new_difficulty,
        direction=direction,
        explanation_en=explanation_en,
        explanation_as=explanation_as,
    )
