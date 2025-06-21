# 📁 routes/treasure.py
from flask import Blueprint, render_template, request, session
import random

treasure_bp = Blueprint('treasure', __name__)

treasure_riddles = [
    {
        "text": "أنا نوع من الكتابة الفنية المزخرفة، أستخدم في الزينة والمساجد، فمن أنا؟",
        "answer": "الخط العربي"
    },
    {
        "text": "مدينة أردنية أثرية منحوتة بالصخر الوردي وتُعد من عجائب الدنيا، ما هي؟",
        "answer": "البتراء"
    },
    {
        "text": "أنا أكلة شعبية تتكون من الأرز واللحم والجميد، وأشتهر في الأردن، من أنا؟",
        "answer": "المنسف"
    }
]

@treasure_bp.route('/treasure', methods=['GET', 'POST'])
def treasure():
    if 'score' not in session:
        session['score'] = 0

    if request.method == 'POST':
        user_answer = request.form.get('answer', '').strip().lower()
        correct_answer = request.form.get('correct_answer', '').strip().lower()
        riddle = request.form.get('riddle')
        show_answer = request.form.get('show_answer') == 'yes'
        try_again = request.form.get('try_again') == 'yes'

        if show_answer:
            feedback = f"✅ الإجابة الصحيحة: {correct_answer.title()}<br>👁️ تم عرض الإجابة الصحيحة."
            return render_template('treasure.html', riddle=riddle,
                                   correct_answer=correct_answer, feedback=feedback, show_answer=True)

        if try_again:
            return render_template('treasure.html', riddle=riddle,
                                   correct_answer=correct_answer)

        if user_answer == correct_answer:
            session['score'] += 1
            feedback = f"✅ الإجابة الصحيحة: {correct_answer.title()}<br>🎉 رائع!"
            return render_template('treasure.html', riddle=riddle,
                                   correct_answer=correct_answer, feedback=feedback, correct=True)
        else:
            feedback = "❌ الإجابة خاطئة."
            return render_template('treasure.html', riddle=riddle,
                                   correct_answer=correct_answer, feedback=feedback)

    if 'remaining_riddles' not in session:
        session['remaining_riddles'] = random.sample(range(len(treasure_riddles)), len(treasure_riddles))

    remaining = session['remaining_riddles']
    if not remaining:
        total = len(treasure_riddles)
        score = session.get('score', 0)
        return render_template('done.html', message=f"انتهت جميع الألغاز 🎉<br>مجموع نقاطك: {score}/{total}")

    current_index = remaining.pop(0)
    session['remaining_riddles'] = remaining
    riddle = treasure_riddles[current_index]

    return render_template('treasure.html', riddle=riddle['text'], correct_answer=riddle['answer'])
