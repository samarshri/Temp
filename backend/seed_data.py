"""
Seed demo data for Student Discussion Forum
Creates sample users, posts, conversations, and messages
"""

import mysql.connector
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# Parse DATABASE_URL from .env
database_url = os.getenv('DATABASE_URL', 'mysql://root:@localhost/forum_db')
parsed = urlparse(database_url)

# Database connection
db_config = {
    'host': parsed.hostname or 'localhost',
    'user': parsed.username or 'root',
    'password': parsed.password or '',
    'database': parsed.path.lstrip('/') or 'forum_db'
}

# Sample data
BRANCHES = ['CSE', 'IT', 'ECE', 'EEE', 'Mechanical', 'Civil']
YEARS = ['1st Year', '2nd Year', '3rd Year', '4th Year']
SECTIONS = ['A', 'B', 'C']

SAMPLE_USERS = [
    {'username': 'alice_tech', 'name': 'Alice Johnson', 'email': 'alice@example.com', 'branch': 'CSE', 'year': '3rd Year', 'section': 'A', 'bio': 'Passionate about AI and Machine Learning', 'skills': '["Python", "TensorFlow", "React"]'},
    {'username': 'bob_codes', 'name': 'Bob Smith', 'email': 'bob@example.com', 'branch': 'IT', 'year': '2nd Year', 'section': 'B', 'bio': 'Full-stack developer | Open source enthusiast', 'skills': '["JavaScript", "Node.js", "MongoDB"]'},
    {'username': 'charlie_dev', 'name': 'Charlie Brown', 'email': 'charlie@example.com', 'branch': 'CSE', 'year': '4th Year', 'section': 'A', 'bio': 'Final year student | Interested in blockchain', 'skills': '["Solidity", "Web3", "Java"]'},
    {'username': 'diana_data', 'name': 'Diana Prince', 'email': 'diana@example.com', 'branch': 'ECE', 'year': '3rd Year', 'section': 'C', 'bio': 'Data science and IoT', 'skills': '["Python", "R", "Arduino"]'},
    {'username': 'eve_design', 'name': 'Eve Adams', 'email': 'eve@example.com', 'branch': 'IT', 'year': '2nd Year', 'section': 'A', 'bio': 'UI/UX Designer | Frontend Developer', 'skills': '["Figma", "CSS", "React"]'},
]

SAMPLE_POSTS = [
    {
        'title': 'Best resources to learn React in 2024?',
        'content': 'Hey everyone! I\'m looking to learn React for an upcoming project. What are your recommended resources? Videos, courses, or documentation?',
        'branch': 'CSE',
        'category': 'Resources',
        'is_question': True,
        'tags': ['React', 'JavaScript', 'Web Development']
    },
    {
        'title': 'Placement drive next week - Tips?',
        'content': 'Amazon is coming for placements next week. Anyone who got placed before, could you share some tips on what to expect in coding rounds?',
        'branch': 'CSE',
        'category': 'Placements',
        'is_question': True,
        'tags': ['Placements', 'Amazon', 'Interview']
    },
    {
        'title': 'ML Project: Sentiment Analysis Complete!',
        'content': 'Just finished my sentiment analysis project using LSTM networks. Achieved 89% accuracy on Twitter data! Would love to hear feedback.',
        'branch': 'CSE',
        'category': 'Projects',
        'is_question': False,
        'tags': ['Machine Learning', 'NLP', 'Project']
    },
    {
        'title': 'Looking for teammates for hackathon',
        'content': 'Hey! Smart India Hackathon is coming up. I\'m looking for 2-3 members interested in building a healthcare solution. Drop a message if interested!',
        'branch': 'IT',
        'category': 'Collaboration',
        'is_question': False,
        'tags': ['Hackathon', 'Team', 'Healthcare']
    },
]

def create_connection():
    """Create database connection"""
    return mysql.connector.connect(**db_config)

def seed_users():
    """Create sample users"""
    conn = create_connection()
    cursor = conn.cursor()
    
    print("Creating sample users...")
    user_ids = []
    
    for user_data in SAMPLE_USERS:
        password_hash = generate_password_hash('password123')
        query = """
        INSERT INTO users (username, name, email, password_hash, branch, year, section, bio, skills, reputation_points)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_data['username'],
            user_data['name'],
            user_data['email'],
            password_hash,
            user_data['branch'],
            user_data['year'],
            user_data['section'],
            user_data['bio'],
            user_data['skills'],
            random.randint(50, 500)
        ))
        user_ids.append(cursor.lastrowid)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✓ Created {len(user_ids)} users")
    return user_ids

def seed_posts(user_ids):
    """Create sample posts"""
    conn = create_connection()
    cursor = conn.cursor()
    
    print("Creating sample posts...")
    post_ids = []
    
    for post_data in SAMPLE_POSTS:
        author_id = random.choice(user_ids)
        query = """
        INSERT INTO posts (user_id, title, content, branch, category, is_question, score, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            author_id,
            post_data['title'],
            post_data['content'],
            post_data['branch'],
            post_data['category'],
            post_data['is_question'],
            random.randint(5, 50),
            datetime.now() - timedelta(days=random.randint(1, 30))
        ))
        post_ids.append(cursor.lastrowid)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✓ Created {len(post_ids)} posts")
    return post_ids

def seed_conversations(user_ids):
    """Create sample conversations and messages"""
    conn = create_connection()
    cursor = conn.cursor()
    
    print("Creating sample conversations...")
    
    # Create 3 conversations
    conversations_created = 0
    for i in range(3):
        user1 = user_ids[i]
        user2 = user_ids[i + 1]
        
        # Create conversation
        cursor.execute("INSERT INTO conversations (type) VALUES ('direct')")
        conv_id = cursor.lastrowid
        
        # Add participants
        cursor.execute("INSERT INTO conversation_participants (conversation_id, user_id) VALUES (%s, %s)", (conv_id, user1))
        cursor.execute("INSERT INTO conversation_participants (conversation_id, user_id) VALUES (%s, %s)", (conv_id, user2))
        
        # Add 3-5 messages
        num_messages = random.randint(3, 5)
        for j in range(num_messages):
            sender = user1 if j % 2 == 0 else user2
            content = f"Sample message {j + 1} in conversation {i + 1}"
            timestamp = datetime.now() - timedelta(minutes=random.randint(10, 1000))
            
            cursor.execute(
                "INSERT INTO messages (conversation_id, sender_id, content, created_at) VALUES (%s, %s, %s, %s)",
                (conv_id, sender, content, timestamp)
            )
        
        conversations_created += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✓ Created {conversations_created} conversations with messages")

def seed_follows(user_ids):
    """Create sample follow relationships"""
    conn = create_connection()
    cursor = conn.cursor()
    
    print("Creating follow relationships...")
    follows_created = 0
    
    # Each user follows 2-3 others
    for user_id in user_ids:
        num_follows = random.randint(2, 3)
        others = [uid for uid in user_ids if uid != user_id]
        to_follow = random.sample(others, min(num_follows, len(others)))
        
        for following_id in to_follow:
            try:
                cursor.execute(
                    "INSERT INTO user_follows (follower_id, following_id) VALUES (%s, %s)",
                    (user_id, following_id)
                )
                follows_created += 1
            except:
                pass  # Skip duplicates
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✓ Created {follows_created} follow relationships")

def main():
    print("\n" + "="*60)
    print("Student Discussion Forum - Seed Data Script")
    print("="*60 + "\n")
    
    try:
        user_ids = seed_users()
        post_ids = seed_posts(user_ids)
        seed_conversations(user_ids)
        seed_follows(user_ids)
        
        print("\n" + "="*60)
        print("✓ Demo data seeded successfully!")
        print("="*60)
        print("\nSample login credentials:")
        print("  Username: alice_tech")
        print("  Password: password123")
        print("\n  (All demo users have password: password123)")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error seeding data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
