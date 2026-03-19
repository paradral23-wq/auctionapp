from aiogram.fsm.state import State, StatesGroup


class CustomBidFSM(StatesGroup):
    waiting_for_amount = State()



class CreateLotFSM(StatesGroup):
    entering_title      = State()
    entering_price      = State()
    choosing_step       = State()
    entering_step       = State()
    choosing_duration   = State()
    entering_duration   = State()
    entering_desc       = State()
    uploading_photo     = State()
    choosing_start_time = State()
    entering_start_time = State()
    confirming          = State()
    entering_topic_id   = State()


class CustomBidFSM(StatesGroup):
    waiting_for_amount = State()
