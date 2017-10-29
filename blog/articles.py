# -*- coding: utf-8 -*-

import os
import time
from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route('/articles/write', methods=['GET', 'POST'])
def paste_article():
    if request.method == 'GET':
        return render_template('/articles/articlePaste.html') if session.get('logged_in', False) else redirect('/login')

    title, author, content = request.form['title'], session['nickname'], request.form['content']
    username = session['username']
    time_post = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    post_id = add_article(title, author, content, time_post, username)
    return redirect('/articles/' + str(post_id))


@app.route('/articles/<int:article_id>', methods=['GET', 'POST'])
def set_article(article_id):
    article = get_article(article_id)
    return render_template('/articles/article.html', article=article)


@app.route('/articles/all/<int:page_id>')
def set_articles(page_id=0):
    page_ids = range(max(0, min(page_id-2, articles.count()/10)), min(page_id+3, articles.count()/10)+1)
    _articles = get_articles(page_id)
    return render_template('/articles/articles.html', author="ALL AUTHORS", articles=_articles, pre=max(page_id-1, 0), page_ids=page_ids, next=min(articles.count(), page_id+1))


@app.route('/del/articles', methods=['POST'])
def del_articles():
    orders = request.form.getlist('do_delete')
    orders = map(lambda x: int(x), orders)
    del_articles_by_orders(orders)
    return redirect('/me')