"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date, datetime

# Core school information system schemas

class Student(BaseModel):
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    email: EmailStr = Field(..., description="Student email")
    grade_level: Optional[int] = Field(None, ge=1, le=12, description="Grade 1-12")
    enrollment_date: Optional[date] = Field(None, description="Enrollment date")
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    is_active: bool = True

class Teacher(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True

class Course(BaseModel):
    code: str = Field(..., description="Course code, e.g., MATH101")
    title: str
    description: Optional[str] = None
    teacher_id: Optional[str] = Field(None, description="Reference to teacher _id")
    credits: Optional[int] = Field(1, ge=0, le=10)
    grade_levels: Optional[List[int]] = Field(default=None, description="Eligible grade levels")

class Enrollment(BaseModel):
    student_id: str = Field(..., description="Reference to student _id")
    course_id: str = Field(..., description="Reference to course _id")
    status: str = Field("enrolled", description="enrolled, waitlisted, completed, dropped")
    term: Optional[str] = Field(None, description="e.g., Fall 2025")

class Announcement(BaseModel):
    title: str
    body: str
    audience: str = Field("all", description="all, students, teachers, parents")
    publish_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    pinned: bool = False

# Example schemas retained (can be used by database viewer)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
