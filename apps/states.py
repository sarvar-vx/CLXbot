from aiogram.fsm.state import State, StatesGroup

class FeedbackState(StatesGroup):
    feedback_message = State()