import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None): 
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, origins='*', supports_credentials=True)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS'
        )
        response.headers.add('Set-Cookie', 'SameSite=None; Secure')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():

        try:
            categories = Category.query.all()
            formatted_cats = {
                category.id: category.type for category in categories
            }

            return jsonify({
                'categories': formatted_cats
            })
        except:
            abort(405)

    @app.route('/questions', methods=['GET', 'POST'])
    def questions():

        method = request.method
        if method == 'GET':
            page = request.args.get('page', 1, type=int)
            try:
                questions = Question.query\
                    .paginate(
                        page=page, per_page=QUESTIONS_PER_PAGE
                    ).items

                return jsonify({
                    'questions': [
                        question.format() for question in questions
                    ],
                    'total_questions': Question.query.count(),
                    'current_category': 'Science',
                    'categories': {
                        category.id: category.type
                        for category in Category.query.all()
                    }
                }), 200
            except:
                abort(404)
        elif method == 'POST' and len(request.get_json()) == 4:
            post_question = request.get_json()['question']
            post_answer = request.get_json()['answer']
            post_category = request.get_json()['category']
            post_difficulty = request.get_json()['difficulty']
            try:
                question = Question(
                    question=post_question,
                    answer=post_answer,
                    category=post_category,
                    difficulty=post_difficulty
                )
                category_type = Category.query\
                    .filter_by(id=question.category).first().type
 
                question.insert()
                return jsonify({
                    'question': question.question,
                    'answer': question.answer,
                    'category': category_type,
                    'difficulty': question.difficulty,
                    'success': True,
                    'status': 200
                }), 200
            except:
                question.rollback()
                abort(400)
            finally:
                question.close()
        else:
            abort(500)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.get(question_id)
        if question is not None:
            try:
                question.delete()
                return jsonify({
                    'success': True,
                    'status': 200,
                    'deleted': question_id,
                    'question': question.question,
                    'total_questions': Question.query.count(),
                    'category': question.category
                }), 200
            except:
                abort(500)
            finally:
                question.close()
        else:
            abort(500)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():

        page = request.args.get('page', 1, type=int)
        searchTerm = request.get_json()['searchTerm']

        try:
            questions = Question.query.filter(
                func.lower(Question.question).ilike(
                    '%' + str(searchTerm).lower() + '%'
                )
            ).paginate(page=page, per_page=QUESTIONS_PER_PAGE).items
            return jsonify({
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
            }), 200
        except:
            abort(400)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_by_category(category_id):

        try:
            page = request.args.get('page', 1, type=int)
            category = Category.query.get(category_id)
            questions = Question.query.filter_by(category=category.id)\
                .paginate(page=page, per_page=QUESTIONS_PER_PAGE).items
            return jsonify({
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'current_category': category.type
            }), 200
        except:
            abort(400)

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():

        category_id = request.get_json()['quiz_category']['id']
        previous_questions = request.get_json()['previous_questions']

        questions = []

        try:
            if category_id == 0:
                questions = Question.query.order_by(func.random()).limit(5)
            else:
                questions = Question.query.filter_by(category=category_id)\
                    .limit(5)

            current_questions = [
                question.format()
                for question in questions
                if question.id not in previous_questions
            ]

            question = random.choice(current_questions)\
                if len(current_questions) > 0 else None

            return jsonify({
                'question': question,
            }), 200

        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                'success': False,
                'error': error.description,
                'status': 404
            }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
                'success': False,
                'error': error.description,
                'status': 405
            }), 405   # Method Not Allowed

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                'success': False,
                'error': error.description,
                'status': 422
            }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                'success': False,
                'error': error.description,
                'status': 400
            }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
                'success': False,
                'error': error.description,
                'status': 500
            }), 500

    return app