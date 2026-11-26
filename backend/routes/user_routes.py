import math
from flask import Blueprint, request, jsonify, current_app, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import json
import io
import csv
from ..models.user import User
from ..models.parking_lot import ParkingLot
from ..models.parking_spot import ParkingSpot
from ..models.reservation import Reservation
from ..app import db
from . import user_required, success_response, error_response
from ..tasks.csv_export import get_task
user_bp = Blueprint('user', __name__)
def user_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            if not current_user_id:
                return error_response('Authentication required', 401)
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"User auth error: {e}")
            return error_response('Authentication error', 401)
    return decorated_function
def success_response(data, message="Success", status_code=200):
    return jsonify({
        'success': True,
        'message': message,
        'data': data
    }), status_code
def error_response(message, status_code=400):
    return jsonify({
        'success': False,
        'error': message
    }), status_code
@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@user_required
def user_dashboard():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        total_bookings = Reservation.query.filter_by(user_id=user_id).count()
        active_bookings = Reservation.query.filter_by(
            user_id=user_id,
            leaving_timestamp=None
        ).count()
        completed_bookings = Reservation.query.filter(
            Reservation.user_id == user_id,
            Reservation.leaving_timestamp.isnot(None)
        ).count()
        total_spent = db.session.query(func.sum(Reservation.parking_cost)).filter_by(
            user_id=user_id
        ).scalar() or 0
        completed_reservations = Reservation.query.filter(
            Reservation.user_id == user_id,
            Reservation.leaving_timestamp.isnot(None)
        ).all()
        total_hours = 0
        for reservation in completed_reservations:
            if reservation.leaving_timestamp and reservation.parking_timestamp:
                duration = reservation.leaving_timestamp - reservation.parking_timestamp
                total_hours += duration.total_seconds() / 3600
        avg_duration = total_hours / max(completed_bookings, 1)
        avg_cost = total_spent / max(total_bookings, 1)
        street_parking_cost = total_spent * 1.5
        total_savings = street_parking_cost - total_spent
        savings_rate = (total_savings / street_parking_cost * 100) if street_parking_cost > 0 else 0
        booking_growth = 12
        active_booking = Reservation.query.filter_by(
            user_id=user_id,
            leaving_timestamp=None
        ).first()
        active_booking_data = None
        if active_booking:
            current_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
            duration = current_time - active_booking.parking_timestamp
            hours_parked = duration.total_seconds() / 3600
            current_cost = active_booking.spot.parking_lot.price * max(1, int(hours_parked))
            active_booking_data = {
                'id': active_booking.id,
                'lot_name': active_booking.spot.parking_lot.prime_location_name,
                'spot_number': active_booking.spot.spot_number,
                'vehicle_number': active_booking.vehicle_number,
                'parking_timestamp': active_booking.parking_timestamp.isoformat(),
                'duration': hours_parked,
                'current_cost': current_cost
            }
        recent_bookings = Reservation.query.filter_by(user_id=user_id)\
            .order_by(Reservation.parking_timestamp.desc())\
            .limit(5).all()
        recent_bookings_data = []
        for booking in recent_bookings:
            recent_bookings_data.append({
                'id': booking.id,
                'lot_name': booking.spot.parking_lot.prime_location_name,
                'spot_number': booking.spot.spot_number,
                'date': booking.parking_timestamp.isoformat(),
                'cost': booking.parking_cost,
                'status': 'Active' if not booking.leaving_timestamp else 'Completed'
            })
        favorite_locations_query = db.session.query(
            ParkingLot.prime_location_name,
            func.count(Reservation.id).label('visits')
        ).join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)\
        .join(Reservation, ParkingSpot.id == Reservation.spot_id)\
        .filter(Reservation.user_id == user_id)\
        .group_by(ParkingLot.id)\
        .order_by(func.count(Reservation.id).desc())\
        .limit(3).all()
        favorite_locations_data = []
        for location, visits in favorite_locations_query:
            favorite_locations_data.append({
                'id': len(favorite_locations_data) + 1,
                'name': location,
                'visits': visits
            })
        all_lots = ParkingLot.query.all()
        nearby_lots = len(all_lots)
        total_available_spots = sum([
            ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
            for lot in all_lots
        ])
        notifications_data = [
            {
                'id': 1,
                'type': 'success',
                'message': f'Welcome back, {user.fullname}!',
                'timestamp': datetime.now().isoformat(),
                'read': False
            }
        ]
        if active_booking_data:
            notifications_data.append({
                'id': 2,
                'type': 'info',
                'message': f'Your vehicle is parked at {active_booking_data["lot_name"]}, Spot #{active_booking_data["spot_number"]}',
                'timestamp': datetime.now().isoformat(),
                'read': False
            })
        dashboard_data = {
            'userStats': {
                'totalBookings': total_bookings,
                'bookingGrowth': booking_growth,
                'totalHours': round(total_hours, 1),
                'avgDuration': round(avg_duration, 1),
                'totalSpent': round(total_spent, 2),
                'avgCost': round(avg_cost, 2),
                'totalSavings': round(total_savings, 2),
                'savingsRate': round(savings_rate, 1)
            },
            'activeReservation': active_booking_data,
            'recentBookings': recent_bookings_data,
            'favoriteLocations': favorite_locations_data,
            'nearbyLots': nearby_lots,
            'availableSpots': total_available_spots,
            'notifications': notifications_data
        }
        return success_response(dashboard_data, "Dashboard data retrieved successfully")
    except Exception as e:
        current_app.logger.error(f"User dashboard error: {str(e)}")
        return error_response("Failed to retrieve dashboard data", 500)
@user_bp.route('/extend-booking/<int:booking_id>', methods=['POST'])
@jwt_required()
@user_required
def extend_booking(booking_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        additional_hours = data.get('additional_hours', 1)
        reservation = Reservation.query.filter_by(
            id=booking_id,
            user_id=user_id,
            leaving_timestamp=None
        ).first()
        if not reservation:
            return error_response("Active reservation not found", 404)
        hourly_rate = reservation.spot.parking_lot.price
        additional_cost = hourly_rate * additional_hours
        reservation.parking_cost = (reservation.parking_cost or 0) + additional_cost
        current_remarks = reservation.remarks or ""
        new_remarks = f"{current_remarks} Extended by {additional_hours}h (+₹{additional_cost})"
        reservation.remarks = new_remarks
        db.session.commit()
        return success_response({
            'booking_id': booking_id,
            'additional_hours': additional_hours,
            'additional_cost': additional_cost,
            'new_total_cost': reservation.parking_cost
        }, f"Booking extended by {additional_hours} hours")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Extend booking error: {str(e)}")
        return error_response("Failed to extend booking", 500)
@user_bp.route('/parking-lots', methods=['GET'])
@jwt_required()
@user_required
def get_available_parking_lots():
    try:
        cache_key = "available_parking_lots"
        if current_app.redis:
            cached_data = current_app.redis.get(cache_key)
            if cached_data:
                return success_response(json.loads(cached_data), "Parking lots retrieved from cache")
        lots = ParkingLot.query.all()
        lots_data = []
        for lot in lots:
            available_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
            lots_data.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'price': lot.price,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'total_spots': lot.number_of_spots,
                'available_spots': available_spots,
                'is_available': available_spots > 0
            })
        if current_app.redis:
            current_app.redis.setex(cache_key, 300, json.dumps(lots_data))
        return success_response(lots_data, "Available parking lots retrieved successfully")
    except Exception as e:
        current_app.logger.error(f"Get parking lots error: {str(e)}")
        return error_response("Failed to retrieve parking lots", 500)
@user_bp.route('/book-parking', methods=['POST'])
@jwt_required()
@user_required
def book_parking_spot():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        if 'lot_id' not in data or 'vehicle_number' not in data:
            return error_response("Lot ID and vehicle number are required", 400)
        lot_id = data['lot_id']
        vehicle_number = data['vehicle_number'].strip().upper()
        active_booking = Reservation.query.filter_by(
            user_id=user_id,
            leaving_timestamp=None
        ).first()
        if active_booking:
            return error_response("You already have an active parking reservation", 400)
        lot = ParkingLot.query.get_or_404(lot_id)
        available_spot = ParkingSpot.query.filter_by(
            lot_id=lot_id,
            status='A'
        ).order_by(ParkingSpot.spot_number).first()
        if not available_spot:
            return error_response("No available parking spots in this lot", 400)
        reservation = Reservation(
            user_id=user_id,
            spot_id=available_spot.id,
            vehicle_number=vehicle_number,
            parking_timestamp=datetime.utcnow() + timedelta(hours=5, minutes=30),
            parking_cost=lot.price
        )
        available_spot.status = 'O'
        db.session.add(reservation)
        db.session.commit()
        if current_app.redis:
            current_app.redis.delete("available_parking_lots")
            current_app.redis.delete("admin_dashboard_stats")
        return success_response({
            'reservation_id': reservation.id,
            'spot_number': available_spot.spot_number,
            'lot_name': lot.prime_location_name,
            'parking_cost': lot.price,
            'message': f"Parking spot {available_spot.spot_number} booked successfully"
        }, "Parking spot booked successfully", 201)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Book parking error: {str(e)}")
        return error_response("Failed to book parking spot", 500)
@user_bp.route('/release-parking/<int:reservation_id>', methods=['POST'])
@jwt_required()
@user_required
def release_parking_spot(reservation_id):
    current_app.logger.info("--- Release Parking Request Start ---")
    current_app.logger.info(f"Attempting to release reservation ID: {reservation_id}")
    current_app.logger.info(f"Request Headers: {request.headers}")
    current_app.logger.info(f"Request Body (raw): {request.data}")
    if not request.is_json:
        return error_response("Content-Type must be application/json", 415)
    data = request.get_json()
    if not data:
        return error_response("Request body cannot be empty", 400)
    rating = data.get('rating')
    if rating is None:
        return error_response("A 'rating' is required in the request body", 400)
    try:
        user_id = get_jwt_identity()
        reservation = Reservation.query.filter_by(
            id=reservation_id,
            user_id=user_id,
            leaving_timestamp=None
        ).first()
        if not reservation:
            return error_response(f"No active reservation found with ID {reservation_id}", 404)
        leaving_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
        duration_seconds = (leaving_time - reservation.parking_timestamp).total_seconds()
        hours_parked = math.ceil(duration_seconds / 3600)
        if hours_parked < 1:
            hours_parked = 1
        final_cost = reservation.spot.parking_lot.price * hours_parked
        reservation.leaving_timestamp = leaving_time
        reservation.parking_cost = final_cost
        reservation.remarks = f"User Rating: {rating}/5"
        reservation.spot.status = 'A'
        db.session.commit()
        current_app.logger.info("--- Release Parking Request Success ---")
        return success_response({
            'message': 'Parking spot released successfully!',
            'reservation_id': reservation.id,
            'final_cost': final_cost,
            'duration_hours': hours_parked,
            'spot_number': reservation.spot.spot_number,
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Internal server error during release: {str(e)}")
        return error_response("An internal server error occurred.", 500)
@user_bp.route('/my-bookings', methods=['GET'])
@jwt_required()
@user_required
def get_user_bookings():
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        bookings = Reservation.query.filter_by(user_id=user_id)\
            .order_by(Reservation.parking_timestamp.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        bookings_data = []
        for booking in bookings.items:
            duration_hours = 0
            if booking.leaving_timestamp:
                duration = booking.leaving_timestamp - booking.parking_timestamp
                duration_hours = round(duration.total_seconds() / 3600, 1)
            elif booking.parking_timestamp:
                duration = (datetime.utcnow() + timedelta(hours=5, minutes=30)) - booking.parking_timestamp
                duration_hours = round(duration.total_seconds() / 3600, 1)
            bookings_data.append({
                'id': booking.id,
                'lot_name': booking.spot.parking_lot.prime_location_name,
                'lot_address': booking.spot.parking_lot.address,
                'spot_number': booking.spot.spot_number,
                'vehicle_number': booking.vehicle_number,
                'parking_timestamp': booking.parking_timestamp.isoformat(),
                'leaving_timestamp': booking.leaving_timestamp.isoformat() if booking.leaving_timestamp else None,
                'duration_hours': duration_hours,
                'parking_cost': booking.parking_cost,
                'status': 'Active' if not booking.leaving_timestamp else 'Completed',
                'remarks': booking.remarks
            })
        return success_response({
            'bookings': bookings_data,
            'pagination': {
                'page': bookings.page,
                'pages': bookings.pages,
                'per_page': bookings.per_page,
                'total': bookings.total,
                'has_next': bookings.has_next,
                'has_prev': bookings.has_prev
            }
        }, "Booking history retrieved successfully")
    except Exception as e:
        current_app.logger.error(f"Get user bookings error: {str(e)}")
        return error_response("Failed to retrieve booking history", 500)
@user_bp.route('/export-history', methods=['POST'])
@jwt_required()
@user_required
def export_parking_history():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return error_response("User not found", 404)
        reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.parking_timestamp.desc()).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Slot ID', 'Spot ID', 'Vehicle Number', 'Parking In', 'Parking Out', 'Cost', 'Remarks'])
        for r in reservations:
            writer.writerow([
                r.id,
                r.spot_id,
                r.vehicle_number,
                r.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S') if r.parking_timestamp else '',
                r.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if r.leaving_timestamp else 'N/A',
                r.parking_cost,
                r.remarks
            ])
        csv_content = output.getvalue()
        output.close()
        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=parking_history.csv"})
    except Exception as e:
        current_app.logger.error(f"Export history error: {str(e)}")
        return error_response("Failed to generate export", 500)
@user_bp.route('/statistics', methods=['GET'])
@jwt_required()
@user_required
def get_user_statistics():
    try:
        user_id = get_jwt_identity()
        monthly_stats = []
        for i in range(6):
            current_date = datetime.now().replace(day=1) - timedelta(days=i*30)
            start_of_month = current_date.replace(day=1)
            if current_date.month == 12:
                end_of_month = current_date.replace(year=current_date.year+1, month=1, day=1) - timedelta(days=1)
            else:
                end_of_month = current_date.replace(month=current_date.month+1, day=1) - timedelta(days=1)
            monthly_bookings = Reservation.query.filter(
                and_(
                    Reservation.user_id == user_id,
                    Reservation.parking_timestamp >= start_of_month,
                    Reservation.parking_timestamp <= end_of_month
                )
            ).count()
            monthly_spending = db.session.query(func.sum(Reservation.parking_cost)).filter(
                and_(
                    Reservation.user_id == user_id,
                    Reservation.parking_timestamp >= start_of_month,
                    Reservation.parking_timestamp <= end_of_month
                )
            ).scalar() or 0
            monthly_stats.append({
                'month': start_of_month.strftime('%Y-%m'),
                'bookings': monthly_bookings,
                'spending': float(monthly_spending)
            })
        lot_usage = db.session.query(
            ParkingLot.prime_location_name,
            func.count(Reservation.id).label('usage_count')
        ).join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)\
         .join(Reservation, ParkingSpot.id == Reservation.spot_id)\
         .filter(Reservation.user_id == user_id)\
         .group_by(ParkingLot.id)\
         .order_by(func.count(Reservation.id).desc())\
         .limit(5).all()
        lot_usage_data = [{'lot_name': lot[0], 'usage_count': lot[1]} for lot in lot_usage]
        return success_response({
            'monthly_stats': monthly_stats,
            'lot_usage': lot_usage_data
        }, "User statistics retrieved successfully")
    except Exception as e:
        current_app.logger.error(f"Get user statistics error: {str(e)}")
        return error_response("Failed to retrieve user statistics", 500)
@user_bp.route('/active-reservation', methods=['GET'])
@jwt_required()
@user_required
def get_active_reservation():
    try:
        user_id = get_jwt_identity()
        active_reservation = Reservation.query.filter_by(
            user_id=user_id,
            leaving_timestamp=None
        ).first()
        if not active_reservation:
            return success_response(None, "No active reservation found")
        current_time = datetime.now()
        duration = current_time - active_reservation.parking_timestamp
        hours_parked = max(1, int(duration.total_seconds() / 3600))
        estimated_cost = active_reservation.spot.parking_lot.price * hours_parked
        reservation_data = {
            'id': active_reservation.id,
            'lot_name': active_reservation.spot.parking_lot.prime_location_name,
            'lot_address': active_reservation.spot.parking_lot.address,
            'spot_number': active_reservation.spot.spot_number,
            'vehicle_number': active_reservation.vehicle_number,
            'parking_timestamp': active_reservation.parking_timestamp.isoformat(),
            'duration_hours': hours_parked,
            'estimated_cost': estimated_cost,
            'hourly_rate': active_reservation.spot.parking_lot.price
        }
        return success_response(reservation_data, "Active reservation retrieved successfully")
    except Exception as e:
        current_app.logger.error(f"Get active reservation error: {str(e)}")
        return error_response("Failed to retrieve active reservation", 500)
@user_bp.route('/quick-search', methods=['POST'])
@jwt_required()
@user_required
def quick_search():
    try:
        data = request.get_json()
        location = data.get('location', '').strip()
        date = data.get('date')
        time = data.get('time')
        lots = ParkingLot.query.filter(
            db.or_(
                ParkingLot.prime_location_name.ilike(f'%{location}%'),
                ParkingLot.address.ilike(f'%{location}%')
            )
        ).all()
        search_results = []
        for lot in lots:
            available_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
            if available_spots > 0:
                search_results.append({
                    'id': lot.id,
                    'prime_location_name': lot.prime_location_name,
                    'address': lot.address,
                    'price': lot.price,
                    'available_spots': available_spots
                })
        return success_response(search_results, "Search results retrieved successfully")
    except Exception as e:
        current_app.logger.error(f"Quick search error: {str(e)}")
        return error_response("Failed to search locations", 500)
@user_bp.route('/statistics/detailed', methods=['GET'])
@jwt_required()
@user_required
def get_detailed_statistics():
    try:
        user_id = get_jwt_identity()
        time_range = request.args.get('time_range', '30d')
        end_date = datetime.now()
        if time_range == '7d':
            start_date = end_date - timedelta(days=7)
        elif time_range == '30d':
            start_date = end_date - timedelta(days=30)
        elif time_range == '90d':
            start_date = end_date - timedelta(days=90)
        elif time_range == '6m':
            start_date = end_date - timedelta(days=180)
        elif time_range == '1y':
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=30)
        reservations = Reservation.query.filter(
            and_(
                Reservation.user_id == user_id,
                Reservation.parking_timestamp >= start_date,
                Reservation.parking_timestamp <= end_date
            )
        ).all()
        total_sessions = len(reservations)
        total_spending = sum([r.parking_cost or 0 for r in reservations])
        total_hours = 0
        for reservation in reservations:
            if reservation.leaving_timestamp and reservation.parking_timestamp:
                duration = reservation.leaving_timestamp - reservation.parking_timestamp
                total_hours += duration.total_seconds() / 3600
        prev_start_date = start_date - (end_date - start_date)
        prev_reservations = Reservation.query.filter(
            and_(
                Reservation.user_id == user_id,
                Reservation.parking_timestamp >= prev_start_date,
                Reservation.parking_timestamp < start_date
            )
        ).count()
        session_growth = 0
        if prev_reservations > 0:
            session_growth = ((total_sessions - prev_reservations) / prev_reservations) * 100
        street_parking_cost = total_spending * 1.5
        total_savings = street_parking_cost - total_spending
        savings_rate = (total_savings / street_parking_cost * 100) if street_parking_cost > 0 else 0
        cost_breakdown_query = db.session.query(
            ParkingLot.prime_location_name,
            func.sum(Reservation.parking_cost).label('total_cost'),
            func.count(Reservation.id).label('booking_count')
        ).join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)\
        .join(Reservation, ParkingSpot.id == Reservation.spot_id)\
        .filter(
            and_(
                Reservation.user_id == user_id,
                Reservation.parking_timestamp >= start_date,
                Reservation.parking_timestamp <= end_date
            )
        ).group_by(ParkingLot.id).all()
        cost_breakdown = []
        colors = ['#000133', '#4B006E', '#8AB8FE', '#6c757d', '#28a745']
        for i, (location, cost, count) in enumerate(cost_breakdown_query):
            percentage = (cost / total_spending * 100) if total_spending > 0 else 0
            cost_breakdown.append({
                'category': location,
                'amount': float(cost or 0),
                'percent': round(percentage, 1),
                'color': colors[i % len(colors)],
                'bookings': count
            })
        top_locations_query = db.session.query(
            ParkingLot.prime_location_name,
            func.count(Reservation.id).label('visits'),
            func.sum(Reservation.parking_cost).label('total_spent')
        ).join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)\
        .join(Reservation, ParkingSpot.id == Reservation.spot_id)\
        .filter(
            and_(
                Reservation.user_id == user_id,
                Reservation.parking_timestamp >= start_date
            )
        ).group_by(ParkingLot.id)\
        .order_by(func.count(Reservation.id).desc())\
        .limit(5).all()
        top_locations = []
        for i, (location, visits, spent) in enumerate(top_locations_query):
            growth = 15 - (i * 3)
            top_locations.append({
                'id': i + 1,
                'name': location,
                'visits': visits,
                'revenue': float(spent or 0),
                'growth': growth,
                'percentage': round((visits / total_sessions * 100) if total_sessions > 0 else 0, 1)
            })
        insights = []
        if reservations:
            hourly_usage = {}
            for reservation in reservations:
                hour = reservation.parking_timestamp.hour
                hourly_usage[hour] = hourly_usage.get(hour, 0) + 1
            peak_hour = max(hourly_usage, key=hourly_usage.get)
            if 9 <= peak_hour <= 17:
                insights.append({
                    'id': 1,
                    'type': 'info',
                    'icon': 'fa-clock',
                    'title': 'Peak Usage Pattern',
                    'description': f'You park most frequently at {peak_hour}:00. Consider booking in advance during peak hours.'
                })
        avg_cost_per_hour = (total_spending / total_hours) if total_hours > 0 else 0
        if avg_cost_per_hour < 50:
            insights.append({
                'id': 2,
                'type': 'positive',
                'icon': 'fa-thumbs-up',
                'title': 'Cost Efficient Parker!',
                'description': f'Your average parking cost is ₹{avg_cost_per_hour:.0f}/hour, which is below market average.'
            })
        if total_sessions >= 10:
            insights.append({
                'id': 3,
                'type': 'positive',
                'icon': 'fa-star',
                'title': 'Frequent Parker',
                'description': f'You\'ve completed {total_sessions} parking sessions. You\'re saving ₹{total_savings:.0f} vs street parking!'
            })
        weekly_data = []
        monthly_data = []
        for week in range(4):
            week_start = end_date - timedelta(weeks=week+1)
            week_end = end_date - timedelta(weeks=week)
            week_reservations = [r for r in reservations
                               if week_start <= r.parking_timestamp < week_end]
            week_sessions = len(week_reservations)
            week_hours = sum([(r.leaving_timestamp - r.parking_timestamp).total_seconds() / 3600
                            for r in week_reservations
                            if r.leaving_timestamp and r.parking_timestamp], 0)
            week_amount = sum([r.parking_cost or 0 for r in week_reservations])
            week_avg_cost = (week_amount / week_sessions) if week_sessions > 0 else 0
            weekly_data.insert(0, {
                'week': f'Week {4-week}',
                'sessions': week_sessions,
                'hours': round(week_hours, 1),
                'amount': round(week_amount, 2),
                'avgCost': round(week_avg_cost, 2)
            })
        for month in range(6):
            month_start = (end_date.replace(day=1) - timedelta(days=month*30)).replace(day=1)
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year+1, month=1)
            else:
                month_end = month_start.replace(month=month_start.month+1)
            month_reservations = [r for r in reservations
                                if month_start <= r.parking_timestamp < month_end]
            month_sessions = len(month_reservations)
            month_hours = sum([(r.leaving_timestamp - r.parking_timestamp).total_seconds() / 3600
                             for r in month_reservations
                             if r.leaving_timestamp and r.parking_timestamp], 0)
            month_amount = sum([r.parking_cost or 0 for r in month_reservations])
            prev_month_start = month_start - timedelta(days=30)
            prev_month_end = month_start
            prev_month_sessions = len([r for r in reservations
                                     if prev_month_start <= r.parking_timestamp < prev_month_end])
            growth = 0
            if prev_month_sessions > 0:
                growth = round(((month_sessions - prev_month_sessions) / prev_month_sessions) * 100, 1)
            monthly_data.insert(0, {
                'month': month_start.strftime('%B'),
                'sessions': month_sessions,
                'hours': round(month_hours, 1),
                'amount': round(month_amount, 2),
                'growth': growth
            })
        location_data = []
        for location, visits, spent in top_locations_query:
            avg_duration = 0
            location_reservations = [r for r in reservations
                                   if r.spot.parking_lot.prime_location_name == location]
            if location_reservations:
                total_duration = sum([(r.leaving_timestamp - r.parking_timestamp).total_seconds() / 3600
                                    for r in location_reservations
                                    if r.leaving_timestamp and r.parking_timestamp], 0)
                avg_duration = total_duration / len(location_reservations)
            location_data.append({
                'name': location,
                'visits': visits,
                'hours': round(sum([(r.leaving_timestamp - r.parking_timestamp).total_seconds() / 3600
                                  for r in location_reservations
                                  if r.leaving_timestamp and r.parking_timestamp], 0), 1),
                'amount': round(float(spent or 0), 2),
                'avgDuration': round(avg_duration, 1)
            })
        statistics_data = {
            'reportData': {
                'totalSpending': round(total_spending, 2),
                'revenueGrowth': round(session_growth, 1),
                'totalSessions': total_sessions,
                'sessionGrowth': round(session_growth, 1),
                'avgDuration': round(total_hours / max(total_sessions, 1), 1),
                'durationChange': -5,
                'totalSavings': round(total_savings, 2),
                'satisfactionRate': 94,
                'satisfactionGrowth': 2.1,
                'efficiencyRate': 89,
                'efficiencyGrowth': 4.5
            },
            'costBreakdown': cost_breakdown,
            'favoriteLocations': top_locations,
            'parkingInsights': insights,
            'weeklyData': weekly_data,
            'monthlyData': monthly_data,
            'locationData': location_data
        }
        return success_response(statistics_data, "Detailed statistics retrieved successfully")
    except Exception as e:
        current_app.logger.error(f"Get detailed statistics error: {str(e)}")
        return error_response("Failed to retrieve detailed statistics", 500)
@user_bp.route('/export-report', methods=['POST'])
@jwt_required()
@user_required
def export_user_report():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        time_range = data.get('time_range', '30d')
        return success_response({
            'export_id': f'export_{user_id}_{int(datetime.now().timestamp())}',
            'status': 'processing',
            'message': 'Report export initiated. You will receive an email when ready.'
        }, "Report export started successfully")
    except Exception as e:
        current_app.logger.error(f"Export user report error: {str(e)}")
        return error_response("Failed to export report", 500)