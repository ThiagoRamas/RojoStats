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
    Publica un mensaje nuevo o edita el existente.

    Devuelve el message_id del mensaje utilizado.
    """

    bot = Bot(token=TELEGRAM_TOKEN)

    try:
        if message_id is None:
            resultado = await bot.send_message(
                chat_id=TELEGRAM_CHANNEL,
                text=texto,
                parse_mode="HTML",
            )

            return resultado.message_id

        try:
            await bot.edit_message_text(
                chat_id=TELEGRAM_CHANNEL,
                message_id=message_id,
                text=texto,
                parse_mode="HTML",
            )

        except BadRequest as error:
            if "Message is not modified" not in str(error):
                raise

        return message_id

    except TelegramError as error:
        raise TelegramServiceError(
            f"No se pudo actualizar Telegram: {error}"
        ) from error