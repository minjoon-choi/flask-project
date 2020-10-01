from pybo import db

idea_voter = db.Table(
    "idea_voter",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "idea_id",
        db.Integer,
        db.ForeignKey("idea.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

feedback_voter = db.Table(
    "feedback_voter",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "feedback_id",
        db.Integer,
        db.ForeignKey("feedback.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    companyID = db.Column(db.String(10), unique=True, nullable=False)
    companyName = db.Column(db.String(50), nullable=False)


class Product(db.Model):
    __tablename__ = "product"
    __table_args__ = (db.UniqueConstraint("companyID", "prodID"),)
    id = db.Column(db.Integer, primary_key=True)
    companyID = db.Column(db.String(10), nullable=False)
    prodID = db.Column(db.String(20), nullable=False)
    prodName = db.Column(db.String(100), nullable=False)
    avgqty = db.Column(db.Float(), nullable=True)


class IdeaProd(db.Model):
    __tablename__ = "ideaProd"
    id = db.Column(db.Integer, primary_key=True)
    idea_id = db.Column(db.Integer, db.ForeignKey("idea.id"))
    companyID = db.Column(db.String(10), nullable=False)
    prodID = db.Column(db.String(30), nullable=False)

    ideaStatus = db.Column(db.String(30), nullable=True)
    effectBegin = db.Column(db.DateTime(), nullable=True)
    effectEnd = db.Column(db.DateTime(), nullable=True)
    estSavings = db.Column(db.Float(), nullable=True)
    agentID = db.Column(db.String(150), nullable=False)

    # Relationship
    idea = db.relationship(
        "Idea", backref=db.backref("ideaProd", lazy="dynamic", collection_class=list)
    )
    # companyName과 prodName는 아이디어제안 detail 조회 시 join할 것


class Idea(db.Model):
    __tablename__ = "idea"
    id = db.Column(db.Integer, primary_key=True)
    ideaNum = db.Column(db.String(30), unique=False, nullable=False)
    ideaType = db.Column(db.String(50), nullable=False)
    ideaTitle = db.Column(db.String(200), nullable=False)
    priceBefore = db.Column(db.Float(), nullable=True)
    priceAfter = db.Column(db.Float(), nullable=True)
    content = db.Column(db.Text(), nullable=False)
    regDate = db.Column(db.DateTime(), nullable=False)
    userid = db.Column(db.String(150), nullable=False)
    userName = db.Column(
        db.Integer, db.ForeignKey("user.username", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship("User", backref=db.backref("idea_set"))
    editDate = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship(
        "User", secondary=idea_voter, backref=db.backref("idea_voter_set")
    )


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    idea_id = db.Column(db.Integer, db.ForeignKey("idea.id", ondelete="CASCADE"))
    idea = db.relationship("Idea", backref=db.backref("feedback_set"))
    content = db.Column(db.Text(), nullable=False)
    regDate = db.Column(db.DateTime(), nullable=False)
    userid = db.Column(
        db.Integer, db.ForeignKey("user.userid", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship("User", backref=db.backref("feedback_set"))
    editDate = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship(
        "User", secondary=feedback_voter, backref=db.backref("feedback_voter_set")
    )


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=False, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    usergroup = db.Column(db.String(30), nullable=False)
    userteam = db.Column(db.String(30), nullable=False)
    userid = db.Column(db.String(150), unique=True, nullable=False)


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.userid", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship("User", backref=db.backref("comment_set"))
    content = db.Column(db.Text(), nullable=False)
    regDate = db.Column(db.DateTime(), nullable=False)
    editDate = db.Column(db.DateTime())
    idea_id = db.Column(
        db.Integer, db.ForeignKey("idea.id", ondelete="CASCADE"), nullable=True
    )
    idea = db.relationship("Idea", backref=db.backref("idea_set"))
    feedback_id = db.Column(
        db.Integer, db.ForeignKey("feedback.id", ondelete="CASCADE"), nullable=True
    )
    feedback = db.relationship("Feedback", backref=db.backref("comment_set"))


# when [Target database is not up to date] error occurs
# do > flask db stamp head

# when db re create dosen't work, check
# sql > select * from alembic_version;
