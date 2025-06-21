# 📁 routes/guess_who.py
from flask import Blueprint, render_template, request, session
import random

guess_who_bp = Blueprint('guess_who', __name__)

characters = [
    {
        "name": "ابن سينا",
        "hints": ["أنا طبيب وفيلسوف مسلم.", "كتبت كتاب القانون في الطب.", "ولدت في بخارى."]
    },
    {
        "name": "الخنساء",
        "hints": ["أنا شاعرة عربية شهيرة.", "اشتهرت برثاء أخيها صخر.", "عشت في الجاهلية وصدر الإسلام."]
    },
    {
        "name": "جابر بن حيان",
        "hints": ["أنا عالم كيمياء عربي.", "لقّبت بـ \"أبو الكيمياء\".", "ألفت كتبًا كثيرة في الصيدلة والتجارب."]
    }
]

@guess_who_bp.route('/guess-who', methods=['GET', 'POST'])
def guess_who():
    if 'score' not in session:
        session['score'] = 0

    if request.method == 'POST':
        user_answer = request.form.get('answer', '').strip().lower()
        correct_answer = request.form.get('correct_answer', '').strip().lower()
        show_answer = request.form.get('show_answer') == 'yes'
        try_again = request.form.get('try_again') == 'yes'
        hints = [request.form.get('hint1'), request.form.get('hint2'), request.form.get('hint3')]

        if show_answer:
            feedback = f"✅ الإجابة الصحيحة: {correct_answer.title()}<br>👁️ تم عرض الإجابة الصحيحة."
            return render_template('guess_who.html', hint1=hints[0], hint2=hints[1], hint3=hints[2],
                                   correct_answer=correct_answer, feedback=feedback, show_answer=True)

        if try_again:
            return render_template('guess_who.html', hint1=hints[0], hint2=hints[1], hint3=hints[2],
                                   correct_answer=correct_answer)

        if user_answer == correct_answer:
            session['score'] += 1
            feedback = f"✅ الإجابة الصحيحة: {correct_answer.title()}<br>🎉 إجابة صحيحة!"
            return render_template('guess_who.html', hint1=hints[0], hint2=hints[1], hint3=hints[2],
                                   correct_answer=correct_answer, feedback=feedback, correct=True)
        else:
            feedback = "❌ إجابة خاطئة."
            return render_template('guess_who.html', hint1=hints[0], hint2=hints[1], hint3=hints[2],
                                   correct_answer=correct_answer, feedback=feedback)

    if 'remaining_characters' not in session:
        session['remaining_characters'] = random.sample(range(len(characters)), len(characters))

    remaining = session['remaining_characters']
    if not remaining:
        total = len(characters)
        score = session.get('score', 0)
        return render_template('done.html', message=f"انتهت جميع الشخصيات 🎉<br>مجموع نقاطك: {score}/{total}")

    current_index = remaining.pop(0)
    session['remaining_characters'] = remaining
    character = characters[current_index]

    return render_template('guess_who.html',
                           hint1=character['hints'][0],
                           hint2=character['hints'][1],
                           hint3=character['hints'][2],
                           correct_answer=character['name'])
