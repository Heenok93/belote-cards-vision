import random
from typing import List, Dict

from .cards import (
    Card,
    Suit,
    create_deck,
    hand_to_multihot
)

from .scoring import compute_score


# =========================================================
# RANDOM HAND GENERATION
# =========================================================

def generate_random_hand(
    hand_size: int = 8
) -> List[Card]:
    """
    Generate a random valid hand.

    Parameters
    ----------
    hand_size : int
        Number of cards in hand.

    Returns
    -------
    List[Card]
    """

    deck = create_deck()

    return random.sample(deck, hand_size)


# =========================================================
# RANDOM TRUMP GENERATION
# =========================================================

def generate_random_trump() -> Suit:
    """
    Randomly select a trump suit.
    """

    return random.choice(list(Suit))


# =========================================================
# RANDOM BONUS FLAGS
# =========================================================

def generate_random_dix_de_der() -> bool:
    """
    Randomly decide if hand has dix de der.
    """

    return random.choice([True, False])


# =========================================================
# SINGLE TRAINING EXAMPLE
# =========================================================

def generate_training_example() -> Dict:
    """
    Generate one synthetic training example.

    Returns
    -------
    dict
    """

    # -----------------------------------------------------
    # Generate hand
    # -----------------------------------------------------

    cards = generate_random_hand()

    # -----------------------------------------------------
    # Generate trump
    # -----------------------------------------------------

    trump = generate_random_trump()

    # -----------------------------------------------------
    # Generate dix de der
    # -----------------------------------------------------

    dix_de_der = generate_random_dix_de_der()

    # -----------------------------------------------------
    # Compute exact score
    # -----------------------------------------------------

    score = compute_score(
        cards=cards,
        trump_suit=trump,
        dix_de_der=dix_de_der
    )

    # -----------------------------------------------------
    # Return structured example
    # -----------------------------------------------------

    return {
        "cards": cards,
        "trump": trump,
        "dix_de_der": dix_de_der,
        "score": score
    }


# =========================================================
# DATASET GENERATION
# =========================================================

def generate_dataset(
    n_samples: int = 100
) -> List[Dict]:
    """
    Generate a synthetic dataset.

    Parameters
    ----------
    n_samples : int

    Returns
    -------
    List[Dict]
    """

    dataset = []

    for _ in range(n_samples):

        example = generate_training_example()

        dataset.append(example)

    return dataset


# =========================================================
# ML FEATURE ENCODING
# =========================================================

def suit_to_onehot(suit: Suit) -> List[int]:
    """
    Convert trump suit into one-hot vector.

    Example:
        COEUR -> [1,0,0,0]
    """

    suits = list(Suit)

    vector = [0] * len(suits)

    vector[suits.index(suit)] = 1

    return vector


def example_to_features(example: Dict) -> List[int]:
    """
    Convert training example to ML features.

    Features:
        - hand multihot (32)
        - trump onehot (4)
        - dix de der (1)

    Total:
        37 features
    """

    hand_vector = hand_to_multihot(
        example["cards"]
    )

    trump_vector = suit_to_onehot(
        example["trump"]
    )

    dix_vector = [
        int(example["dix_de_der"])
    ]

    return (
        hand_vector +
        trump_vector +
        dix_vector
    )


# =========================================================
# DATASET TO ML MATRICES
# =========================================================

def dataset_to_ml(
    dataset: List[Dict]
):
    """
    Convert dataset into:
        X = features
        y = labels
    """

    X = []
    y = []

    for example in dataset:

        features = example_to_features(example)

        score = example["score"]

        X.append(features)
        y.append(score)

    return X, y


# =========================================================
# DEBUG / EXAMPLE
# =========================================================

if __name__ == "__main__":

    dataset = generate_dataset(100)

    print("Generated examples:")
    print()

    for i, example in enumerate(dataset[:5]):

        print(f"Example {i+1}")
        print("Cards:", example["cards"])
        print("Trump:", example["trump"])
        print("Dix de der:", example["dix_de_der"])
        print("Score:", example["score"])
        print("-" * 50)

    # -----------------------------------------------------
    # ML conversion
    # -----------------------------------------------------

    X, y = dataset_to_ml(dataset)

    print()
    print("ML dataset:")
    print(f"X shape: {len(X)} samples")
    print(f"Feature size: {len(X[0])}")
    print(f"y shape: {len(y)}")