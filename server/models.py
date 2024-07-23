from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if name == '':
            raise ValueError("Invalid name")
        
        for author in Author.query.all():
            if author.name == name:
                raise ValueError("Name taken")
            
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError("Invalid number length")

        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title') 
    def validate_title(self, key, title):
        if title == '':
            raise ValueError("Invalid title")

        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content too short")

        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary too long")
        
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either Fiction or Non-Fiction")

        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        for phrase in clickbait:
            if phrase in title:
                return title
        raise ValueError("Title not clickbait-y enough")

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
