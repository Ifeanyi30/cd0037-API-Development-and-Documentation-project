import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):

        response = self.client().get('/categories')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['categories'])
        self.assertEqual(len(response.get_json()['categories']), 6)

    def test_error_get_categories(self):

        response = self.client().post('/categories?page=1')
        self.assertEqual(response.status_code, 405)

    def test_post_categories(self):

        response = self.client().post('/categories', json={'type': 'Science'})
        self.assertEqual(response.status_code, 405)

    def test_get_paginated_questions(self):

        total_questions = Question.query.count()        
        response = self.client().get('/questions?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()['questions']), 10)
        self.assertEqual(response.get_json()['total_questions'], total_questions)
        self.assertEqual(response.get_json()['current_category'], 'Science')

    def test_error_get_page_not_found(self):

        response = self.client().get('/questions?page=100')
        self.assertEqual(response.status_code, 404)

    def test_post_questions(self):

        response = self.client().post('/questions', json={
            'question': '''
            What is the answer to life, the universe, and everything?
            ''',
            'answer': '42',
            'category': 1,
            'difficulty': 1
        })
        self.assertEqual(response.status_code, 200)

    def test_error_post_questions(self):
    
        response = self.client().post('/questions', json={})
        self.assertEqual(response.status_code, 500)

    def test_delete_question(self):

        question = Question.query.limit(1).first()
        question_id = question.id if question else None
        question_count = Question.query.count()        
        response = self.client().delete(f'/questions/{question_id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['deleted'])
        self.assertEqual(
            response.get_json()['total_questions'], question_count - 1
        )

    def test_error_delete_question(self):

        response = self.client().delete('/questions/1000')
        self.assertEqual(response.status_code, 500)

    def test_result_search(self):

        response = self.client().post('/questions/search', json={'searchTerm': 'title'})
        self.assertEqual(response.status_code, 200)

    def test_no_result_search(self):

        response = self.client().post('/questions/search', json={'searchTerm': 'Budapest'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()['questions']), 0)

    def test_get_questions_by_category(self):

        response = self.client().get('/categories/1/questions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()['questions']), 10)
        self.assertEqual(response.get_json()['current_category'], 'Science')
        self.assertTrue(response.get_json()['questions'])

    def test_error_questions_by_category(self):
       
        response = self.client().get('/categories/10/questions')
        self.assertEqual(response.status_code, 400)

    def test_quzzies_questions(self):

        quiz = {
            'previous_questions': [],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        response = self.client().post('/quizzes', json=quiz)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['question'])

    def test_error_quzzies_questions(self):

        quiz = {
            'previous_questions': [],
            'quiz_category': {'id': 7, 'type': 'Science'}
        }
        response = self.client().post('/quizzes', json=quiz)

        self.assertEqual(response.get_json()['question'], None)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()