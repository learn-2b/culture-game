# 📁 routes/discover.py
from flask import Blueprint, render_template, request, session
import random

discover_bp = Blueprint('discover', __name__)

locations = [
    {
        "image": "/static/images/karak.jpg",
        "question": "ما الأكلة الشعبية المشهورة في الكرك؟",
        "options": ["المنسف", "المسخن", "المقلوبة"],
        "answer": "المنسف"
    },
    {
        "image": "/static/images/jerash.jpg",
        "question": "ما نوع المعلم المشهور في جرش؟",
        "options": ["قلعة", "مسجد", "آثار رومانية"],
        "answer": "آثار رومانية"
    },
    {
        "image": "/static/images/aqaba.jpg",
        "question": "بماذا تشتهر العقبة؟",
        "options": ["الجبال", "السياحة البحرية", "التمور"],
        "answer": "السياحة البحرية"
    }
]

@discover_bp.route('/discover', methods=['GET', 'POST'])
def discover():
    if 'score' not in session:
        session['score'] = 0

    if request.method == 'POST':
        show_answer = request.form.get('show_answer') == 'yes'
        try_again = request.form.get('try_again') == 'yes'
        image = request.form.get('image')
        question = request.form.get('question')
        correct_answer = request.form.get('correct_answer')
        options = request.form.getlist('options')
        user_answer = request.form.get('answer', '')

        if show_answer:
            feedback = f"✅ الإجابة الصحيحة: {correct_answer}<br>👁️ تم عرض الإجابة الصحيحة."
            return render_template('discover.html', image=image, question=question, options=options,
                                   correct_answer=correct_answer, feedback=feedback, show_answer=True)

        if try_again:
            return render_template('discover.html', image=image, question=question, options=options,
                                   correct_answer=correct_answer)

        if user_answer == correct_answer:
            session['score'] += 1
            feedback = f"✅ الإجابة الصحيحة: {correct_answer}<br>🎉 إجابة صحيحة!"
            return render_template('discover.html', image=image, question=question, options=options,
                                   correct_answer=correct_answer, feedback=feedback, correct=True)
        else:
            feedback = "❌ إجابة خاطئة."
            return render_template('discover.html', image=image, question=question, options=options,
                                   correct_answer=correct_answer, feedback=feedback)

    if 'remaining_indexes' not in session:
        session['remaining_indexes'] = random.sample(range(len(locations)), len(locations))

    remaining = session['remaining_indexes']
    if not remaining:
        total = len(locations)
        score = session.get('score', 0)
        return render_template('done.html', message=f"انتهت جميع الأسئلة 🎉<br>مجموع نقاطك: {score}/{total}")

    current_index = remaining.pop(0)
    session['remaining_indexes'] = remaining
    site = locations[current_index]

    return render_template('discover.html',
                           image=site['image'],
                           question=site['question'],
                           options=site['options'],
                           correct_answer=site['answer'])
