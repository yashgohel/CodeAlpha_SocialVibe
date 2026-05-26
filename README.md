# Social Vibe

Social Vibe is a feature-rich, full-stack social media web application built with Python and Django. It provides a modern, interactive platform for users to connect, share content, and communicate in real-time within a stunning "glassmorphism" themed environment.

## About The Project

Social Vibe is designed to offer a premium social networking experience. The application features a sleek, dark-themed UI with elegant glassmorphism effects, ensuring a high-end feel. It covers the core functionalities of a modern social platform, including content sharing, social networking, and direct communication, all while maintaining a responsive and fluid user experience.

## Key Features

- **User Authentication**: Secure Sign-up, Login, and Password Reset functionality.
- **Dynamic Profiles**: Personalized user profiles with customizable profile pictures, cover images, and bios.
- **Content Sharing**: 
  - Create posts with text, images, and videos.
  - Express moods using the "Feelings" feature.
  - Share temporary "Stories" with friends.
- **Social Interactions**:
  - Like and comment on posts.
  - Manage comments with deletion options.
  - Follow and unfollow other users to build your network.
- **Direct Messaging**:
  - Integrated chat system for one-on-one communication.
  - Support for media attachments in messages.
  - Edit and track message status (read/unread).
- **Notification System**: Real-time notifications for new followers, likes, comments, and messages.
- **User Search**: Easily find other users using the search functionality (supports `@` mentions).
- **Responsive Design**: Fully optimized for both desktop and mobile devices.

## Getting Started

Follow these steps to set up and run Social Vibe on your local machine.

### Prerequisites

- Python 3.x
- Django

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yashgohel/CodeAlpha_SocialVibe.git
   cd CodeAlpha_SocialVibe
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**:
   ```bash
   cd socialvibe
   python manage.py migrate
   ```

5. **Create a superuser (for Admin access)**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

Now, open your browser and navigate to `http://127.0.0.1:8000/` to explore Social Vibe!

## How to Use the Website

1. **Sign Up / Log In**: Create a new account or log in with your credentials to access the platform.
2. **Update Profile**: Head to the settings or your profile page to upload a profile picture and cover image.
3. **Connect with Others**: Use the search bar to find friends and follow them to see their posts on your home feed.
4. **Share Content**: Post updates, feelings, or stories from the home page.
5. **Interact**: Like and comment on your friends' posts to stay engaged.
6. **Chat**: Use the Messages tab to send direct messages and media to your followers along with edit and delete features.
7. **Manage Account**: Use the Settings page to update your information or change your password.
8. **Delete Account**: Delete the account permanently through Settings page.
