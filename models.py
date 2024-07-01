from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Define the Message model to represent messages in the database
class Message(db.Model):
    # Primary key column
    id = db.Column(db.Integer, primary_key=True)
    # Column to store the first name, cannot be null
    first_name = db.Column(db.String(50), nullable=False)
    # Column to store the last name, cannot be null
    last_name = db.Column(db.String(50), nullable=False)
    # Column to store the email address, cannot be null
    email = db.Column(db.String(100), nullable=False)
    # Column to store the phone number, cannot be null
    phone_number = db.Column(db.String(20), nullable=False)
    # Column to store the subject of the message, cannot be null
    subject = db.Column(db.String(100), nullable=False)
    # Column to store the message content, cannot be null
    message = db.Column(db.Text, nullable=False)

    # Define the string representation of the model instance
    def __repr__(self):
        return f'<Message {self.first_name} {self.last_name}>'
