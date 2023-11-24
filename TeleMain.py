from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
from test import *

# /start 명령어 핸들러
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='봇이 초기화되었습니다.')
def message_handler_def(update, context):
    # 텔레그램 메시지 관련 로직
    message_text = update.message.text.split('\n')
    chat_id = update.message.chat_id
    result = []
    try:
        if('■상암지역' in message_text[0]):
            set_text_1(message_text)
        if('/비교명령' in message_text[0]):
            indexes = [index for index, s in enumerate(get_text_1()) if '➖' in s]
            message_text[1] = f"({message_text[1]})"
            for i, index in enumerate(indexes):
                if(message_text[1] in get_text_1()[index:(indexes[i+1] if i+1 < len(indexes) else None)][0]):
                    print(get_text_1()[index:(indexes[i+1] if i+1 < len(indexes) else None)][0], "의 비교를 시작합니다.")
                    response = text_compare(get_text_1()[index:(indexes[i+1] if i+1 < len(indexes) else None)], '\n'.join(message_text[2:]))
                    print(get_text_1()[index:(indexes[i+1] if i+1 < len(indexes) else None)][0], "의 비교를 무사히 종료합니다.")
                    result.append(f"{get_text_1()[index:(indexes[i+1] if i+1 < len(indexes) else None)][0]}\n최종 중복값 제거 리스트:\n{response}\n\n")
            context.bot.send_message(chat_id=chat_id, text=f"{''.join(result)}")
            print(f"전체 비교가 완료되었습니다.")
        else:
            raise Exception
    except Exception as e:
        if '/' in message_text[0]:
            context.bot.send_message(chat_id=chat_id, text=f"올바르지 않은 명령어입니다.\nex> '/비교명령\n[요일]\n텍스트리스트'으로 보내주세요.")

def document_handler_def(update, context):
    document = update.message.document
    print(document.file_name.strip())

    if '우주팀' in document.file_name.strip():
        file = context.bot.get_file(document.file_id)
        file.download('상암지역 우주팀 12월 만남캘린더.xlsm')  # 파일 저장
        print(f'"{document.file_name}" 파일을 받았습니다.')
    else:
        print('파일 이름에 "우주팀"이 포함되어 있지 않습니다.')

    if '상승팀' in document.file_name.strip():
        file = context.bot.get_file(document.file_id)
        file.download('상암지역 상승팀 12월 만남캘린더.xlsm')  # 파일 저장
        print(f'"{document.file_name}" 파일을 받았습니다.')
        # update.message.reply_text(f'"{document.file_name}" 파일을 받았습니다.')
    else:
        print('파일 이름에 "상승팀"이 포함되어 있지 않습니다.')
        # update.message.reply_text('파일 이름에 "상암지역"이 포함되어 있지 않습니다.')

    if '번개팀' in document.file_name.strip():
        file = context.bot.get_file(document.file_id)
        file.download('상암지역 번개팀 12월 만남캘린더.xlsm')  # 파일 저장
        print(f'"{document.file_name}" 파일을 받았습니다.')
    else:
        print('파일 이름에 "번개팀"이 포함되어 있지 않습니다.')

    if '이행팀' in document.file_name.strip():
        file = context.bot.get_file(document.file_id)
        file.download('상암지역 이행팀 12월 만남캘린더.xlsx')  # 파일 저장
        print(f'"{document.file_name}" 파일을 받았습니다.')
    else:
        print('파일 이름에 "이행팀"이 포함되어 있지 않습니다.')

    if '천심팀' in document.file_name.strip():
        file = context.bot.get_file(document.file_id)
        file.download('상암지역 천심팀 12월 만남캘린더.xlsm')  # 파일 저장
        print(f'"{document.file_name}" 파일을 받았습니다.')
    else:
        print('파일 이름에 "천심팀"이 포함되어 있지 않습니다.')

def start_bot():
    bot = Bot(token='6987559664:AAG3phMvUFBNUlZ_NTuyXKxLwxnWM63HHN0')  # 봇 객체 생성
    updater = Updater(bot=bot)  # Updater에 bot 객체 전달
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))  # /start 명령어 핸들러 등록
    message_handler = MessageHandler(Filters.text & (~Filters.command), message_handler_def)
    document_handler = MessageHandler(Filters.document, document_handler_def)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(document_handler)
    updater.start_polling()
    updater.idle()

start_bot()