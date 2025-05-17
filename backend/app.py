from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone
import humanize

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/comments_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Comment(db.Model):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    presence = db.Column(db.Boolean, default=True)
    comment = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    gif_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    love = db.Column(db.Integer, default=0)
    owner_uuid = db.Column(UUID(as_uuid=True), nullable=True)
    comments = db.Column(db.JSON, default=[])

    def to_dict(self, is_parent=True):
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "presence": self.presence,
            "comment": self.comment,
            "is_admin": self.is_admin,
            "gif_url": self.gif_url,
            "created_at": humanize.naturaltime(datetime.now(timezone.utc) - self.created_at),
            "like": {
                "love": self.love
            },
            "comments": [],
            "is_parent": is_parent
        }


def build_comment_tree(comment, is_parent=True):
    comment_dict = comment.to_dict(is_parent=is_parent)

    if comment.comments:
        child_uuids = comment.comments
        children = Comment.query.filter(Comment.uuid.in_(child_uuids)).order_by(Comment.created_at.asc()).all()
        comment_dict["comments"] = [build_comment_tree(child, is_parent=False) for child in children]

    return comment_dict


@app.route('/api/v2/comment', methods=['POST'])
def create_comment():
    data = request.get_json()

    try:
        new_comment = Comment(
            uuid=uuid.uuid4(),
            name=data['name'],
            presence=data.get('presence', True),
            comment=data['comment'],
            is_admin=data.get('is_admin', False),
            gif_url=data.get('gif_url'),
            created_at=datetime.utcnow(),
            love=0,
            owner_uuid=uuid.UUID(data['owner_uuid']) if data.get('owner_uuid') else None,
            comments=data.get('comments', [])
        )
        db.session.add(new_comment)
        db.session.commit()

        return jsonify({
            "code": 201,
            "data": new_comment.to_dict(),
            "error": None
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 400,
            "data": None,
            "error": str(e)
        }), 400


@app.route('/api/v2/comment', methods=['GET'])
def get_comments_v2():
    per = request.args.get('per', default=10, type=int)
    next_offset = request.args.get('next', default=0, type=int)

    # Only parent comments
    parent_comments_query = Comment.query.filter(
        (Comment.owner_uuid == None)
    ).order_by(Comment.created_at.desc())

    total_count = parent_comments_query.count()

    paginated_comments = parent_comments_query.offset(next_offset).limit(per).all()
    comments_list = [build_comment_tree(c) for c in paginated_comments]

    return jsonify({
        "code": 200,
        "data": {
            "count": total_count,
            "lists": comments_list
        },
        "error": None
    })


if __name__ == '__main__':
    app.run(debug=True)