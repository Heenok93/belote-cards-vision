from .cards import Value


# =========================================================
# GAME CONSTANTS
# =========================================================

DECK_SIZE = 32

BASE_TOTAL_POINTS = 162

DIX_DE_DER_BONUS = 10

BELOTE_REBELOTE_BONUS = 20


# =========================================================
# NON-TRUMP POINTS
# =========================================================

NON_TRUMP_POINTS = {
    Value.AS: 11,
    Value.DIX: 10,
    Value.ROI: 4,
    Value.DAME: 3,
    Value.VALET: 2,
    Value.NEUF: 0,
    Value.HUIT: 0,
    Value.SEPT: 0,
}


# =========================================================
# TRUMP POINTS
# =========================================================

TRUMP_POINTS = {
    Value.VALET: 20,
    Value.NEUF: 14,
    Value.AS: 11,
    Value.DIX: 10,
    Value.ROI: 4,
    Value.DAME: 3,
    Value.HUIT: 0,
    Value.SEPT: 0,
}