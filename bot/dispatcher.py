from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler

from bot.handlers import commands, commons, queries, students, teacher
from bot import states

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

dispatcher = Dispatcher(bot, None, workers=0)

dispatcher.add_handler(CommandHandler("start", commands.start))
dispatcher.add_handler(MessageHandler(Filters.text("📖 Darslar"), students.get_lessons))
dispatcher.add_handler(MessageHandler(Filters.text("📝️️️️️️ Guruhni o'zgartirish"), teacher.get_groups))
dispatcher.add_handler(MessageHandler(Filters.text("🔐 Tasodifiy ishtirokchilarni tanlash"), teacher.get_random_student))

dispatcher.add_handler(ConversationHandler(
    entry_points=[MessageHandler(Filters.text("🔖 Natijalar"), students.get_results)],
    states={
        states.GET_RESULT_DETAILS: [
            MessageHandler(Filters.all, students.get_result_details),
            CallbackQueryHandler(students.get_result_details)
        ]
    },
    fallbacks=[CommandHandler("start", commands.start)]
))

dispatcher.add_handler(ConversationHandler(
    entry_points=[MessageHandler(Filters.text("❓ Savollar"), students.get_question_set)],
    states={
        states.QUESTION_SINGLE: [
            MessageHandler(Filters.all, students.question_single),
            CallbackQueryHandler(students.question_single)
        ],
        states.QUESTION_NOTIFY: [
            MessageHandler(Filters.all, students.notify_question_start),
        ],
        states.GET_ANSWER: [MessageHandler(Filters.all, students.get_answer)]
    },
    fallbacks=[CommandHandler("start", commands.start)]
))

dispatcher.add_handler(ConversationHandler(
    entry_points=[MessageHandler(Filters.text("✏️ Bajarilmagan topshiriqlar"), students.get_uncompleted_tasks)],
    states={
        states.GET_TASK: [MessageHandler(Filters.all, students.get_task), CallbackQueryHandler(students.get_task)],
        states.GET_TASK_ANSWER: [MessageHandler(Filters.all, students.get_task_answer)]
    },
    fallbacks=[CommandHandler("start", commands.start)]
))

dispatcher.add_handler(ConversationHandler(
    entry_points=[MessageHandler(Filters.text("📖 Topshiriqlar"), teacher.get_tasks)],
    states={
        states.TEACHER_GET_LESSON_FOR_TASK: [
            MessageHandler(Filters.all, teacher.get_lesson_for_task),
            CallbackQueryHandler(teacher.get_lesson_for_task)
        ],
        states.TEACHER_GET_TASK: [
            MessageHandler(Filters.all, teacher.get_task_students),
            CallbackQueryHandler(teacher.get_task_students)
        ],
        states.TEACHER_GET_TASK_DETAILS: [
            MessageHandler(Filters.all, teacher.get_task_details),
            CallbackQueryHandler(teacher.get_task_details)
        ],
        states.TEACHER_CONFIRM_TASK: [
            MessageHandler(Filters.all, teacher.confirm_task),
            CallbackQueryHandler(teacher.confirm_task)
        ]
    },
    fallbacks=[CommandHandler("start", commands.start)]
))

dispatcher.add_handler(CallbackQueryHandler(queries.handle_callback_query))
dispatcher.add_handler(MessageHandler(Filters.text, commons.echo))
