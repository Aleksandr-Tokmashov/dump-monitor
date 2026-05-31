from uuid import UUID

from app.bot import bot


CHAT_ID = UUID("ТУТ_CHAT_ID")


async def send_incident(incident):

    text = f"""
Найдена свалка

Станция: {incident.station_name}

Источник:
{incident.source_url}

Текст:
{incident.text[:1000]}
"""

    await bot.send_message(
        bot_id=bot.state.bot_accounts[0].id,
        chat_id=CHAT_ID,
        body=text,
    )