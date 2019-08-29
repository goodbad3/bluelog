from threading import Thread

from flask import url_for, current_app
from flask_mail import Message

from bluelog.extensions import mail

def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)

def send_mail(subject, to, html):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr

def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) +'#comments'

    send_mail(subject='新评论',to=current_app.config['BLUELOG_EMAIL'],
    html='<p>文章<i>"%s"</i>有了新评论 , 点击下面链接去检查:</p>'
         '<p><a href="%s">%s</a></p>'
         '<p><small style="color: #868e96">邮件不需要回复.</small></p>'
         % (post.title, post_url, post_url))

def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id,_external=True) + '#comments'

    send_mail(subject='新回复', to=comment.email,
    html='<p>您评论的文章<i>"%s"</i>有了回复了,点击下面链接去检查: </p>'
         '<p><a href="%s">%s</a></p>'
         '<p><small style="color: #868e96">邮件不需要回复.</small></p>'
    % (comment.post.title, post_url, post_url))
