from app.models import Base
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Table, ForeignKey


likes_table = Table('likes', Base.metadata,
    Column('review_id', String(60), ForeignKey('reviews.id', ondelete='CASCADE')),
    Column('user_id', String(60), ForeignKey('users.id', ondelete='CASCADE'))
)

dislikes_table = Table('dislikes', Base.metadata,
    Column('reviews_id', String(60), ForeignKey('reviews.id', ondelete='CASCADE')),
    Column('users_id', String(60), ForeignKey('users.id', ondelete='CASCADE'))
)


class Review(BaseModel, Base):
    """The Review model"""

    __tablename__ = "reviews"
    title = Column(String(60))
    content = Column(String(1500))
    reviewer_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    workspace_id = Column(String(60), ForeignKey("workspaces.id"), nullable=False)
    liked_users = relationship("User", secondary=likes_table, back_populates="liked_reviews")
    disliked_users = relationship("User", secondary=dislikes_table, back_populates="disliked_reviews")
