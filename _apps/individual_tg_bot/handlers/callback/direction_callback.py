import _apps.individual_tg_bot.keyboards.inline.specializations.keyboards as kb
from _apps.individual_tg_bot import text
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery


async def direction_design_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback design"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.design}",
        reply_markup=kb.design_button(),
    )


async def direction_backend_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback backend"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.backend}",
        reply_markup=kb.backend_button(),
    )


async def direction_analyst_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback analyst"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.analyst}",
        reply_markup=kb.analyst_button(),
    )


async def direction_mobile_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback mobile"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.mobile}",
        reply_markup=kb.mobile_button(),
    )


async def direction_marketing_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback marketing"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.marketing}",
        reply_markup=kb.marketing_button(),
    )


async def direction_product_project_manager_callback(
    query: CallbackQuery, state: FSMContext
) -> None:
    """Обработка callback product_project_manager"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.product_project_manager}",
        reply_markup=kb.product_project_manager_button(),
    )


async def direction_sales_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback sales"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.sales}",
        reply_markup=kb.sales_button(),
    )


async def direction_dev_ops_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback dev_ops"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.dev_ops}",
        reply_markup=kb.dev_ops_button(),
    )


async def direction_frontend_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback frontend"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.frontend}",
        reply_markup=kb.frontend_button(),
    )


async def direction_support_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback support"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.support}",
        reply_markup=kb.support_button(),
    )


async def direction_fullstack_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback fullstack"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.fullstack}",
        reply_markup=kb.fullstack_button(),
    )


async def direction_hr_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback hr"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.hr}",
        reply_markup=kb.hr_button(),
    )


async def direction_game_dev_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback game_dev"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.game_dev}",
        reply_markup=kb.game_dev_button(),
    )


async def direction_qa_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback qa"""
    await state.update_data(selected_direction=query.data)
    await query.message.answer(
        text=f"{text.specialization} {text.qa}",
        reply_markup=kb.qa_button(),
    )
