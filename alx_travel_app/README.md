# Travel App API Documentation

## API Endpoints

### Listings
- `GET /api/listings/` - List all listings
- `POST /api/listings/` - Create a new listing (authenticated)
- `GET /api/listings/{id}/` - Retrieve a specific listing
- `PUT /api/listings/{id}/` - Update a listing (owner only)
- `DELETE /api/listings/{id}/` - Delete a listing (owner only)

### Bookings
- `GET /api/bookings/` - List user's bookings (or all for staff)
- `POST /api/bookings/` - Create a new booking (authenticated)
- `GET /api/bookings/{id}/` - Retrieve a specific booking
- `PUT /api/bookings/{id}/` - Update a booking (owner only)
- `DELETE /api/bookings/{id}/` - Delete a booking (owner only)

## Authentication
Most endpoints require authentication. Use token authentication or session authentication.

## Swagger Documentation
Interactive API documentation is available at `/swagger/` and `/redoc/`.
