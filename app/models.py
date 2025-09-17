from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from decimal import Decimal


# Enums for various status fields
class ContentStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class InquiryStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class ServiceCategory(str, Enum):
    AI_ML = "ai_ml"
    BLOCKCHAIN = "blockchain"
    IOT = "iot"
    DATA_ANALYTICS = "data_analytics"
    RISK_PLANNING = "risk_planning"
    GROWTH_STRATEGY = "growth_strategy"


class SubsidiaryType(str, Enum):
    LAOCTA_TECHLABS = "laocta_techlabs"
    INTEGRAL_IOT = "integral_iot"
    CHAINTUM = "chaintum"


# User and Authentication Models
class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=100)
    email: str = Field(unique=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    full_name: str = Field(max_length=200)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    blog_posts: List["BlogPost"] = Relationship(back_populates="author")


# Website Content Models
class Page(SQLModel, table=True):
    __tablename__ = "pages"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    slug: str = Field(unique=True, max_length=200)
    content: str = Field(default="")
    meta_description: str = Field(default="", max_length=500)
    meta_keywords: str = Field(default="", max_length=500)
    status: ContentStatus = Field(default=ContentStatus.DRAFT)
    is_homepage: bool = Field(default=False)
    sort_order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # SEO and additional metadata
    seo_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))


class Service(SQLModel, table=True):
    __tablename__ = "services"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    slug: str = Field(unique=True, max_length=200)
    description: str = Field(max_length=1000)
    detailed_description: str = Field(default="")
    category: ServiceCategory
    icon: str = Field(default="", max_length=100)  # Icon class or name
    image_url: str = Field(default="", max_length=500)
    features: List[str] = Field(default=[], sa_column=Column(JSON))
    examples: List[str] = Field(default=[], sa_column=Column(JSON))
    is_featured: bool = Field(default=False)
    sort_order: int = Field(default=0)
    status: ContentStatus = Field(default=ContentStatus.PUBLISHED)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Additional metadata
    extra_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))


class Subsidiary(SQLModel, table=True):
    __tablename__ = "subsidiaries"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    slug: str = Field(unique=True, max_length=200)
    subsidiary_type: SubsidiaryType
    tagline: str = Field(default="", max_length=300)
    description: str = Field(max_length=1000)
    detailed_description: str = Field(default="")
    logo_url: str = Field(default="", max_length=500)
    website_url: str = Field(default="", max_length=500)
    contact_email: str = Field(default="", max_length=255)
    contact_phone: str = Field(default="", max_length=50)
    focus_areas: List[str] = Field(default=[], sa_column=Column(JSON))
    key_services: List[str] = Field(default=[], sa_column=Column(JSON))
    is_active: bool = Field(default=True)
    sort_order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Social media and additional info
    social_links: Dict[str, str] = Field(default={}, sa_column=Column(JSON))
    additional_info: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))


class BlogPost(SQLModel, table=True):
    __tablename__ = "blog_posts"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    slug: str = Field(unique=True, max_length=200)
    excerpt: str = Field(default="", max_length=500)
    content: str = Field(default="")
    featured_image_url: str = Field(default="", max_length=500)
    author_id: Optional[int] = Field(default=None, foreign_key="users.id")
    category: str = Field(default="general", max_length=100)
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    status: ContentStatus = Field(default=ContentStatus.DRAFT)
    is_featured: bool = Field(default=False)
    view_count: int = Field(default=0)
    published_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # SEO metadata
    meta_description: str = Field(default="", max_length=500)
    meta_keywords: str = Field(default="", max_length=500)
    seo_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))

    # Relationships
    author: Optional[User] = Relationship(back_populates="blog_posts")


# Contact and Lead Management
class ContactInquiry(SQLModel, table=True):
    __tablename__ = "contact_inquiries"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    email: str = Field(max_length=255)
    phone: str = Field(default="", max_length=50)
    company: str = Field(default="", max_length=200)
    subject: str = Field(max_length=300)
    message: str = Field(default="")
    service_interest: Optional[str] = Field(default=None, max_length=100)
    subsidiary_interest: Optional[str] = Field(default=None, max_length=100)
    status: InquiryStatus = Field(default=InquiryStatus.NEW)
    priority: str = Field(default="medium", max_length=20)  # low, medium, high, urgent
    source: str = Field(default="website", max_length=100)  # website, referral, etc.
    ip_address: str = Field(default="", max_length=45)
    user_agent: str = Field(default="", max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    responded_at: Optional[datetime] = Field(default=None)

    # Additional metadata for lead scoring
    lead_score: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=5)
    notes: str = Field(default="")
    extra_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))


# Company Information
class CompanyInfo(SQLModel, table=True):
    __tablename__ = "company_info"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    company_name: str = Field(default="GMW Tech Group", max_length=200)
    tagline: str = Field(default="Driving Africa's Digital Transformation with AI, Blockchain & IoT", max_length=500)
    mission: str = Field(default="")
    vision: str = Field(default="")
    description: str = Field(default="")
    founded_year: Optional[int] = Field(default=None)

    # Contact Information
    primary_email: str = Field(default="", max_length=255)
    primary_phone: str = Field(default="", max_length=50)
    secondary_phone: str = Field(default="", max_length=50)

    # Address Information
    address_line1: str = Field(default="", max_length=200)
    address_line2: str = Field(default="", max_length=200)
    city: str = Field(default="", max_length=100)
    state: str = Field(default="", max_length=100)
    country: str = Field(default="", max_length=100)
    postal_code: str = Field(default="", max_length=20)

    # Map coordinates
    latitude: Optional[Decimal] = Field(default=None, decimal_places=6, max_digits=9)
    longitude: Optional[Decimal] = Field(default=None, decimal_places=6, max_digits=9)

    # Social Media Links
    social_links: Dict[str, str] = Field(default={}, sa_column=Column(JSON))

    # Business Hours and Additional Info
    business_hours: Dict[str, str] = Field(default={}, sa_column=Column(JSON))
    certifications: List[str] = Field(default=[], sa_column=Column(JSON))
    awards: List[str] = Field(default=[], sa_column=Column(JSON))

    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Analytics and Performance Tracking
class PageView(SQLModel, table=True):
    __tablename__ = "page_views"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    page_path: str = Field(max_length=500)
    page_title: str = Field(default="", max_length=200)
    user_ip: str = Field(default="", max_length=45)
    user_agent: str = Field(default="", max_length=500)
    referrer: str = Field(default="", max_length=500)
    session_id: str = Field(default="", max_length=100)
    device_type: str = Field(default="", max_length=50)  # desktop, tablet, mobile
    browser: str = Field(default="", max_length=100)
    operating_system: str = Field(default="", max_length=100)
    country: str = Field(default="", max_length=100)
    city: str = Field(default="", max_length=100)
    viewed_at: datetime = Field(default_factory=datetime.utcnow)

    # Additional analytics data
    time_on_page: Optional[int] = Field(default=None)  # seconds
    bounce: bool = Field(default=False)
    conversion: bool = Field(default=False)


class SiteAnalytics(SQLModel, table=True):
    __tablename__ = "site_analytics"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(index=True)
    page_views: int = Field(default=0)
    unique_visitors: int = Field(default=0)
    bounce_rate: Decimal = Field(default=Decimal("0"), decimal_places=4, max_digits=6)
    avg_session_duration: Decimal = Field(default=Decimal("0"), decimal_places=2, max_digits=8)
    new_contacts: int = Field(default=0)
    conversion_rate: Decimal = Field(default=Decimal("0"), decimal_places=4, max_digits=6)

    # Traffic sources
    organic_traffic: int = Field(default=0)
    direct_traffic: int = Field(default=0)
    referral_traffic: int = Field(default=0)
    social_traffic: int = Field(default=0)

    # Device breakdown
    desktop_users: int = Field(default=0)
    mobile_users: int = Field(default=0)
    tablet_users: int = Field(default=0)

    # Popular content
    top_pages: List[str] = Field(default=[], sa_column=Column(JSON))
    top_services: List[str] = Field(default=[], sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=datetime.utcnow)


# Website Settings and Configuration
class SiteConfiguration(SQLModel, table=True):
    __tablename__ = "site_configuration"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(unique=True, max_length=100)
    value: str = Field(default="")
    value_type: str = Field(default="string", max_length=20)  # string, int, bool, json
    description: str = Field(default="", max_length=500)
    category: str = Field(default="general", max_length=50)
    is_public: bool = Field(default=False)  # Can be exposed to frontend
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Newsletter Subscription
class NewsletterSubscriber(SQLModel, table=True):
    __tablename__ = "newsletter_subscribers"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, max_length=255)
    name: str = Field(default="", max_length=200)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    verification_token: str = Field(default="", max_length=100)
    interests: List[str] = Field(default=[], sa_column=Column(JSON))
    subscribed_at: datetime = Field(default_factory=datetime.utcnow)
    unsubscribed_at: Optional[datetime] = Field(default=None)
    last_email_sent: Optional[datetime] = Field(default=None)

    # Subscriber metadata
    source: str = Field(default="website", max_length=100)
    ip_address: str = Field(default="", max_length=45)
    user_agent: str = Field(default="", max_length=500)


# Non-persistent schemas for validation and API
class ContactInquiryCreate(SQLModel, table=False):
    name: str = Field(max_length=200)
    email: str = Field(max_length=255)
    phone: str = Field(default="", max_length=50)
    company: str = Field(default="", max_length=200)
    subject: str = Field(max_length=300)
    message: str = Field(default="")
    service_interest: Optional[str] = Field(default=None, max_length=100)
    subsidiary_interest: Optional[str] = Field(default=None, max_length=100)


class NewsletterSubscriberCreate(SQLModel, table=False):
    email: str = Field(max_length=255)
    name: str = Field(default="", max_length=200)
    interests: List[str] = Field(default=[])


class BlogPostCreate(SQLModel, table=False):
    title: str = Field(max_length=200)
    slug: str = Field(max_length=200)
    excerpt: str = Field(default="", max_length=500)
    content: str = Field(default="")
    featured_image_url: str = Field(default="", max_length=500)
    category: str = Field(default="general", max_length=100)
    tags: List[str] = Field(default=[])
    meta_description: str = Field(default="", max_length=500)
    meta_keywords: str = Field(default="", max_length=500)


class BlogPostUpdate(SQLModel, table=False):
    title: Optional[str] = Field(default=None, max_length=200)
    excerpt: Optional[str] = Field(default=None, max_length=500)
    content: Optional[str] = Field(default=None)
    featured_image_url: Optional[str] = Field(default=None, max_length=500)
    category: Optional[str] = Field(default=None, max_length=100)
    tags: Optional[List[str]] = Field(default=None)
    status: Optional[ContentStatus] = Field(default=None)
    is_featured: Optional[bool] = Field(default=None)
    meta_description: Optional[str] = Field(default=None, max_length=500)
    meta_keywords: Optional[str] = Field(default=None, max_length=500)


class ServiceCreate(SQLModel, table=False):
    title: str = Field(max_length=200)
    slug: str = Field(max_length=200)
    description: str = Field(max_length=1000)
    detailed_description: str = Field(default="")
    category: ServiceCategory
    icon: str = Field(default="", max_length=100)
    image_url: str = Field(default="", max_length=500)
    features: List[str] = Field(default=[])
    examples: List[str] = Field(default=[])


class ServiceUpdate(SQLModel, table=False):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    detailed_description: Optional[str] = Field(default=None)
    category: Optional[ServiceCategory] = Field(default=None)
    icon: Optional[str] = Field(default=None, max_length=100)
    image_url: Optional[str] = Field(default=None, max_length=500)
    features: Optional[List[str]] = Field(default=None)
    examples: Optional[List[str]] = Field(default=None)
    is_featured: Optional[bool] = Field(default=None)
    status: Optional[ContentStatus] = Field(default=None)


class PageAnalytics(SQLModel, table=False):
    page_path: str
    views: int
    unique_visitors: int
    avg_time_on_page: Decimal
    bounce_rate: Decimal
    conversion_rate: Decimal


class DashboardStats(SQLModel, table=False):
    total_page_views: int
    unique_visitors: int
    total_contacts: int
    new_contacts_today: int
    newsletter_subscribers: int
    published_blog_posts: int
    active_services: int
    bounce_rate: Decimal
    conversion_rate: Decimal
