from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sa
from app import app, db
# from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
# from app.models import User, Post
from datetime import datetime, timezone
from app.tic_tac_toe import TicTacToe

game = TicTacToe()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', board=game.board)


@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    position = data['position']
    if game.make_move(position):
        winner = game.check_winner()
        winning_combination = game.get_winning_combination()
        return jsonify({'status': 'success', 'winner': winner, 'board': game.board, 'winning_combinations': winning_combination})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid move'})

# @app.route('/player/<playername>')
# def player(playername):
#     user = db.first_or_404(sa.select(User).where(User.username == username))
#     page = request.args.get('page', 1, type=int)
#     query = user.posts.select().order_by(Post.timestamp.desc())
#     posts = db.paginate(query, page=page,
#                         per_page=app.config['POSTS_PER_PAGE'],
#                         error_out=False)
#     next_url = url_for('user', username=user.username, page=posts.next_num) \
#         if posts.has_next else None
#     prev_url = url_for('user', username=user.username, page=posts.prev_num) \
#         if posts.has_prev else None
#     form = EmptyForm()
#     return render_template('user.html', user=user, posts=posts.items,
#                            next_url=next_url, prev_url=prev_url, form=form)

@app.route('/restart', methods=['POST'])
def clear():
    game.reset_board()
    return jsonify({'status': 'success'})