import openai
import base64
from config import OPENAI_API_KEY, OPENAI_MODEL

# OpenAI clientni sozlash
client = openai.OpenAI(api_key=OPENAI_API_KEY)

CALORIE_PROMPT = """
Sen professional dietolog va ovqat tahlilchisisisan. Foydalanuvchi senga ovqat yoki mahsulot rasmini yubordi.

Rasmni diqqat bilan ko'rib, quyidagilarni aniqlang:

1. Taomning/Mahsulotning nomini aniqlang
2. Taxminiy porsiya hajmini belgilang (gramm yoki ml da)
3. Kaloriya miqdorini hisoblang (100g uchun va umumiy porsiya uchun)
4. Asosiy ozuqa moddalarini ko'rsating:
   - Oqsillar (protein)
   - Yog'lar (fat)
   - Uglevodlar (carbohydrates)
   - Tola (fiber) — agar ma'lum bo'lsa
5. Sog'liqqa foydasi yoki zarari haqida qisqa maslahat bering

Javobni quyidagi formatda bering (faqat O'zbek tilida):

🍽️ *Mahsulot:* [nom]
⚖️ *Taxminiy porsiya:* [gramm/ml]

📊 *Kaloriya:*
• 100g uchun: [X] kcal
• Umumiy porsiya: [X] kcal

🧬 *Ozuqa tarkibi (100g uchun):*
• 🥩 Oqsil: [X]g
• 🧈 Yog': [X]g
• 🌾 Uglevod: [X]g
• 🌿 Tola: [X]g

💡 *Dietolog maslahati:*
[Qisqa va foydali maslahat]

⚠️ _Eslatma: Bu taxminiy hisob bo'lib, aniq miqdorlar porsiya hajmiga qarab farq qilishi mumkin._

Agar rasm ovqat yoki mahsulot bo'lmasa, quyidagicha javob bering:
"❌ Kechirasiz, men faqat ovqat va mahsulot rasmlarini tahlil qila olaman. Iltimos, ovqat rasmini yuboring."
"""


async def analyze_food_image(image_bytes: bytes) -> str:
    """
    Rasm baytlarini OpenAI GPT-4o Vision API ga yuboradi
    va kaloriya hisobini qaytaradi.
    """
    try:
        # Rasmni base64 ga o'tkazish
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # GPT-4o Vision ga so'rov (sync, thread pool da)
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}",
                                    "detail": "high"
                                }
                            },
                            {
                                "type": "text",
                                "text": CALORIE_PROMPT
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
        )

        return response.choices[0].message.content

    except openai.AuthenticationError:
        return "❌ OpenAI API kalit xatosi! Iltimos, config.py faylida OPENAI_API_KEY ni tekshiring."
    except openai.RateLimitError:
        return "⏳ OpenAI API limitiga yetildi. Iltimos, bir oz kuting va qayta urinib ko'ring."
    except openai.BadRequestError as e:
        return f"❌ Rasm formati xatosi: {str(e)}\n\nBoshqa rasm yuborib ko'ring."
    except Exception as e:
        return f"❌ Xatolik yuz berdi: {str(e)}\n\nIltimos, qayta urinib ko'ring."


def is_valid_image(mime_type: str) -> bool:
    """Yuklangan fayl rasm ekanligini tekshiradi."""
    valid_types = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif"]
    return mime_type.lower() in valid_types
