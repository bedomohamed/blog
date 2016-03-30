from app import db


# Model for blog posts ###################################################################
class Post(db.Model):
    __bind_key__ = 'db1'

    id = db.Column(db.Integer, primary_key=True)
    css_class = db.Column(db.String(64), index=True)
    title = db.Column(db.String(128), index=True)
    subtitle = db.Column(db.String(128), index=True)
    icon = db.Column(db.String(128), index=True)
    content = db.Column(db.String(), index=True)
    date = db.Column(db.String(64), index=True)
    month = db.Column(db.String(64), index=True)
    year = db.Column(db.String(32), index=True)

    def __repr__(self):
        return '%d' % self.id


# Model for public blog posts ############################################################
class PublicPost(db.Model):
    __bind_key__ = 'db3'

    pub_id = db.Column(db.Integer, primary_key=True)
    approved = db.Column(db.Integer, index=True)
    pub_css_class = db.Column(db.String(64), index=True)
    pub_title = db.Column(db.String(128), index=True)
    pub_subtitle = db.Column(db.String(128), index=True)
    author = db.Column(db.String(128), index=True)
    pub_icon = db.Column(db.String(128), index=True)
    pub_content = db.Column(db.String(), index=True)
    pub_date = db.Column(db.String(64), index=True)
    pub_month = db.Column(db.String(64), index=True)
    pub_year = db.Column(db.String(32), index=True)

    def __repr__(self):
        return '%d' % self.pub_id


# Model for CSTools Forms DB #############################################################
class Entry(db.Model):
    __bind_key__ = 'db2'

    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(64), index=True)
    contact_name = db.Column(db.String(128), index=True)
    contact_email = db.Column(db.String(128), index=True)
    csr_name = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.String(64), index=True)
    item_numbers = db.Column(db.String(64), index=True)
    notes = db.Column(db.String(128), index=True)
    color = db.Column(db.String(64), index=True)

    def __repr__(self):
        return 'Entry %r' % self.institution


# GIF Display ############################################################################
gif_tags = db.Table('gif_tags', db.metadata,
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                    db.Column('gif_id', db.Integer, db.ForeignKey('gif.id')),
                    info={'bind_key': 'gifs_db'}
                    )


class Gif(db.Model):
    __bind_key__ = 'gifs_db'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256), index=True)
    tags = db.relationship('Tag', secondary=gif_tags, backref=db.backref('tags', lazy='dynamic'))

    def __repr__(self):
        return '%r' % self.url


class Tag(db.Model):
    __bind_key__ = 'gifs_db'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    subreddits = db.relationship('Subreddit', backref='tag', lazy='dynamic')

    def __repr__(self):
        return '%r' % self.name


class Subreddit(db.Model):
    __bind_key__ = 'gifs_db'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    def __repr__(self):
        return '%r' % self.name
