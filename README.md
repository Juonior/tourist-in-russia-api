# Tourist in Russia API

This is a FastAPI-based information system for tourists in Russia. The system allows users to register, login, and view tourist places. Administrators can add new places, and registered users can leave comments on places.

## Features

- User registration and authentication
- Admin and regular user roles
- Place management (admin only)
- Comments on places (authenticated users)
- Location data for places (latitude/longitude)
- User profiles with avatars
- Password management

## Setup

1. Make sure you have Docker and Docker Compose installed
2. Clone the repository
3. Run the application:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/token` - Login and get access token
- `GET /auth/me` - Get current user profile
- `PUT /auth/change-password` - Change user password
- `PUT /auth/avatar` - Update user avatar

### Places
- `GET /places/` - Get all places
- `GET /places/{place_id}` - Get a specific place
- `POST /places/` - Create a new place (admin only)

### Comments
- `POST /places/{place_id}/comments/` - Add a comment to a place
- `GET /places/{place_id}/comments/` - Get all comments for a place

## Example Usage

1. Register a new user:
```bash
curl -X POST "http://localhost:8000/auth/register" -H "Content-Type: application/json" -d '{"email":"user@example.com","username":"user","password":"password123","is_admin":false}'
```

2. Login and get token:
```bash
curl -X POST "http://localhost:8000/auth/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=user&password=password123"
```

3. Get user profile:
```bash
curl -X GET "http://localhost:8000/auth/me" -H "Authorization: Bearer YOUR_TOKEN"
```

4. Change password:
```bash
curl -X PUT "http://localhost:8000/auth/change-password" -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" -d '{"old_password":"password123","new_password":"newpassword123"}'
```

5. Update avatar:
```bash
curl -X PUT "http://localhost:8000/auth/avatar" -H "Authorization: Bearer YOUR_TOKEN" -F "file=@/path/to/your/avatar.jpg"
```

6. Create a new place (as admin):
```bash
curl -X POST "http://localhost:8000/places/" -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" -d '{"name":"Red Square","description":"Famous square in Moscow","latitude":55.7539,"longitude":37.6208}'
```

7. Add a comment:
```bash
curl -X POST "http://localhost:8000/places/1/comments/" -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" -d '{"content":"Beautiful place!"}'