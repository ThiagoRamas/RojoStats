from telegram import Bot
from telegram.error import BadRequest, TelegramError

from config import TELEGRAM_CHANNEL, TELEGRAM_TOKEN


class TelegramServiceError(Exception):
    """Error producido al publicar o editar mensajes en Telegram."""


async def publicar_o_actualizar_mensaje(
    texto: str,
    message_id: int | None,
) -> int:
    """
    Publica un mensaje nuevo o edita el mensaje existente.

    Devuelve el message_id utilizado.
    """

    bot = Bot(token=TELEGRAM_TOKEN)

    try:
        if message_id is None:
            resultado = await bot.send_message(
                chat_id=TELEGRAM_CHANNEL,
                text=texto,
                parse_mode="HTML",
            )

            print(f"Canal utilizado: {resultado.chat.title}")
            print(f"ID del canal: {resultado.chat.id}")
            print(f"Mensaje nuevo: {resultado.message_id}")

            return resultado.message_id

        try:
            resultado = await bot.edit_message_text(
                chat_id=TELEGRAM_CHANNEL,
                message_id=message_id,
                text=texto,
                parse_mode="HTML",
            )

            print(f"Canal utilizado: {resultado.chat.title}")
            print(f"ID del canal: {resultado.chat.id}")
            print(f"Mensaje editado: {resultado.message_id}")
            print("Texto confirmado por Telegram:")
            print(resultado.text)

        except BadRequest as error:
            if "Message is not modified" in str(error):
                print("Telegram informa que el mensaje no cambió.")
            else:
                raise

        return message_id

    except TelegramError as error:
        raise TelegramServiceError(
            f"No se pudo actualizar Telegram: {error}"
        ) from error