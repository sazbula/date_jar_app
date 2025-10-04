from app.backend.models import User, Idea


def test_user_idea_relationship(db_session):
    """
    Test that a user can own ideas and they appear in the user's idea list.
    """
    user = User(username="alex", password_hash="hashed123")
    db_session.add(user)
    db_session.commit()

    idea = Idea(title="Movie night", note="Watch Inception", owner=user)
    db_session.add(idea)
    db_session.commit()

    # Check relationship
    assert idea.owner.username == "alex"
    assert len(user.ideas) == 1
    assert user.ideas[0].title == "Movie night"


def test_favorite_relationship(db_session):
    """
    Test many-to-many relationship between users and ideas (favorites).
    """
    user = User(username="bella", password_hash="hashed")
    idea = Idea(title="Go hiking", note="Mountain trail")
    db_session.add_all([user, idea])
    db_session.commit()

    # User favorites an idea
    user.favorites.append(idea)
    db_session.commit()

    # Check both sides of the relationship
    assert idea in user.favorites
    assert user in idea.favorited_by
