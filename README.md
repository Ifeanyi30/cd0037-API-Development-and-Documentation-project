# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

## API DOCUMENTATION

Base URL: Note that this project is not currently deployed to any online server yet, and the database is also local to the machine it runs on. So the base URL for the API endpoints is `http://localhost:5000` or `http://127.0.0.1:5000`.

### Error Handling

Errors are returned as JSON object in the format below:

    {
        'success': False,
        'error': error.description,
        'status': 422
    }

Error messages to except when a failed call to an endpoint is observed are;

- 400 , Bad request.
- 404 , Not Found.
- 422 , Unprocessable.
- 500 , Internal Server Error.

### API ENDPOINTS

#### GET '/categories'

- General:
    - The endpoint returns a dictionary of all the category ids as keys, and category types as values.
- Sample: `curl http://127.0.0.1:5000/categories`

        {
            "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                "4": "History", 
                "5": "Entertainment", 
                "6": "Sports"
            }
        }

#### GET '/questions'

- General
    - Returns categories (dict), questions (list), total_questions (integer) and current_category (string).
    - The questions returned are paginated, ten questions per page. Use the request argument to specify the page of choice. Non-existent page number returns a 404 error.
- Sample: `curl http://127.0.0.1:5000/questions` or `curl http://127.0.0.1:5000/questions?page=1` to specify page.

        {
            "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                "4": "History", 
                "5": "Entertainment", 
                "6": "Sports"
            }, 
            "current_category": "Science", 
            "questions": [
                {
                "answer": "Muhammad Ali", 
                "category": 4, 
                "difficulty": 1, 
                "id": 9, 
                "question": "What boxer's original name is Cassius Clay?"
                }, 
                {
                "answer": "Apollo 13", 
                "category": 5, 
                "difficulty": 4, 
                "id": 2, 
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                },
                ...
            ], 
            "total_questions": 26
        }

#### POST '/questions'

- General
    - If successful, it returns the JSON format of the question, answer, difficulty, category, success message and status code 200.
    - Sample: `curl -H "Content-Type: application/json" -d '{"question":"Who is the manager of Manchester City Football Club?", "answer":"Pep Guardiola", "difficulty": 2, "category":6}' -X POST http://127.0.0.1:5000/questions`.

            {
                "question":"Who is the manager of Manchester City Football Club?",
                "answer":"Pep Guardiola",
                "category": "Sport",
                "difficulty": 2,
                "success": true,
                "status": 200
            }

#### DELETE '/questions/\<int:question_id\>'

- General
    - Returns the deleted question id, question, category and 'total_question' after deletion.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/1`

        {
            "success": true,
            "status": 200,
            "deleted": 1,
            "question": "How is the president of USA?",
            "total_questions": 20,
            "category": "History"
        }

#### POST '/questions/search'

- General
    - Returns the paginated list of questions ('questions'), and the total question count of the result (total_questions).
    - Uses the request argument 'searchTerm' to post client request to the server.
- Sample: `curl -H 'Content-Type: application/json' -d '{"searchTerm": "first"}' -X POST http://127.0.0.1:5000/questions/search`.

        {
            "questions": [
                {
                    "answer": "Tom Cruise", 
                    "category": 5, 
                    "difficulty": 4, 
                    "id": 4, 
                    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                },
                {
                    "answer": "Uruguay", 
                    "category": 6, 
                    "difficulty": 4, 
                    "id": 11, 
                    "question": "Which country won the first ever soccer World Cup in 1930?"
                }
            ],
            "total_questions": 2
        }

#### GET '/categories/\<int:category_id>/questions'

- General
    - Returns the current_category, questions (list), and the total_question which is the count of the number of questions from that category.
    - The result questions are paginated to 10 questions per page.
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`.

        {
            "current_category": "Art", 
            "questions": [
                {
                "answer": "Escher", 
                "category": 2, 
                "difficulty": 1, 
                "id": 16, 
                "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
                }, 
                {
                "answer": "Mona Lisa", 
                "category": 2, 
                "difficulty": 3, 
                "id": 17, 
                "question": "La Giaconda is better known as what?"
                }, 
                {
                "answer": "One", 
                "category": 2, 
                "difficulty": 4, 
                "id": 18, 
                "question": "How many paintings did Van Gogh sell in his lifetime?"
                }, 
                {
                "answer": "Jackson Pollock", 
                "category": 2, 
                "difficulty": 2, 
                "id": 19, 
                "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
                }, 
                {
                "answer": "North America", 
                "category": 2, 
                "difficulty": 3, 
                "id": 28, 
                "question": "The country 'Ecuador' is in which continent?"
                }
            ], 
            "total_questions": 5
        }
#### POST '/quizzes'

- General
    - It gets a JSON object of the previous_questions list and quiz_category.
    - Randomly selects and returns a question from the chosen category.
- Sample: `curl -X POST http://127.0.0.1:5000/quizzes -H 'Content-Type: application/json' -d '{"quiz_category":{"id": 1, "type": "Science"},"previous_questions":[]}'`

        {
            "question": {
                "answer": "Blood",
                "category": 1,
                "difficulty": 4,
                "id": 22,
                "question": "Hematology is a branch of medicine involving the study of what?"
            }
        }