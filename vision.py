async def analyze_image(update):

    text = (
        "🧠 Görsel analiz sistemi aktif.\n\n"
        "Yakında:\n"
        "• kıyafet analizi\n"
        "• kumaş tahmini\n"
        "• mankene giydirme\n"
        "• AI redesign\n"
        "özellikleri eklenecek."
    )

    await update.message.reply_text(text)
