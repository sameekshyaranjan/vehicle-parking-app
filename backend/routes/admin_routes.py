from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity,verify_jwt_in_request
from sqlalchemy import and_, func
from datetime import datetime, timedelta
import json
import redis
from ..models.user import User
from ..models.parking_lot import ParkingLot
from ..models.parking_spot import ParkingSpot
from ..models.reservation import Reservation
from ..app import db
from . import admin_required, success_response, error_response
admin_bp = Blueprint('admin', __name__)
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            print("🔐 Checking JWT token...")
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            print(f"🔐 Current user ID from JWT: {current_user_id}")
            if not current_user_id:
                print("❌ No user ID in JWT")
                return jsonify({'error': 'Invalid token'}), 401
            user = User.query.get(int(current_user_id))
            print(f"🔐 User lookup result: {user}")
            if not user:
                print(f"❌ User not found with ID: {current_user_id}")
                return jsonify({'error': 'User not found'}), 401
            is_admin = getattr(user, 'is_admin', False) or user.is_admin == 1
            print(f"🔐 User admin status: is_admin={getattr(user, 'is_admin', None)},  final_is_admin={is_admin}")
            if not is_admin:
                print(f"❌ User {user.username} is not admin")
                return jsonify({'error': 'Admin access required'}), 403
            print(f"✅ Admin access granted to {user.username}")
            return f(*args, **kwargs)
        except Exception as e:
            print(f"❌ Admin check error: {e}")
            return jsonify({'error': 'Authentication error'}), 401
    return decorated_function
@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def admin_dashboard():
    try:
        cache_key = "admin_dashboard_stats"
        if current_app.redis:
            cached_data = current_app.redis.get(cache_key)
            if cached_data:
                return success_response(json.loads(cached_data), "Dashboard data retrieved from cache")
        total_lots = ParkingLot.query.count()
        total_spots = ParkingSpot.query.count()
        occupied_spots = ParkingSpot.query.filter_by(status='O').count()
        available_spots = total_spots - occupied_spots
        total_users = User.query.filter_by(is_admin=False).count()
        occupancy_rate = round((occupied_spots / total_spots * 100) if total_spots > 0 else 0, 2)
        today = datetime.now().date()
        today_reservations = Reservation.query.filter(
            func.date(Reservation.parking_timestamp) == today
        ).count()
        today_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
            func.date(Reservation.parking_timestamp) == today
        ).scalar() or 0
        week_start = today - timedelta(days=today.weekday())
        week_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
            func.date(Reservation.parking_timestamp) >= week_start
        ).scalar() or 0
        month_start = today.replace(day=1)
        month_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
            func.date(Reservation.parking_timestamp) >= month_start
        ).scalar() or 0
        active_bookings = Reservation.query.filter_by(leaving_timestamp=None).count()
        yesterday = today - timedelta(days=1)
        yesterday_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
            func.date(Reservation.parking_timestamp) == yesterday
        ).scalar() or 0
        revenue_growth = 0
        if yesterday_revenue > 0:
            revenue_growth = ((today_revenue - yesterday_revenue) / yesterday_revenue) * 100
        prev_week_start = week_start - timedelta(days=7)
        prev_week_end = week_start - timedelta(days=1)
        prev_week_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
            and_(
                func.date(Reservation.parking_timestamp) >= prev_week_start,
                func.date(Reservation.parking_timestamp) <= prev_week_end
            )
        ).scalar() or 0
        weekly_growth = 0
        if prev_week_revenue > 0:
            weekly_growth = ((week_revenue - prev_week_revenue) / prev_week_revenue) * 100
        popular_lot_query = db.session.query(
            ParkingLot.prime_location_name,
            func.count(Reservation.id).label('reservation_count')
        ).join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)\
        .join(Reservation, ParkingSpot.id == Reservation.spot_id)\
        .group_by(ParkingLot.id)\
        .order_by(func.count(Reservation.id).desc())\
        .first()
        most_popular_lot = popular_lot_query[0] if popular_lot_query else "N/A"
        recent_reservations = Reservation.query\
            .order_by(Reservation.parking_timestamp.desc())\
            .limit(5).all()
        recent_activity = []
        for reservation in recent_reservations:
            recent_activity.append({
                'id': reservation.id,
                'user_name': reservation.user.fullname,
                'lot_name': reservation.spot.parking_lot.prime_location_name,
                'spot_number': reservation.spot.spot_number,
                'vehicle_number': reservation.vehicle_number,
                'timestamp': reservation.parking_timestamp.isoformat(),
                'status': 'Active' if not reservation.leaving_timestamp else 'Completed'
            })
        system_status = {
            'overall': 'operational',
            'database': 'operational',
            'payment_system': 'operational',
            'booking_system': 'operational'
        }
        alerts = []
        if occupancy_rate > 90:
            alerts.append({
                'type': 'warning',
                'message': f'High occupancy rate: {occupancy_rate:.1f}%',
                'timestamp': datetime.now().isoformat()
            })
        if today_revenue < yesterday_revenue * 0.8:
            alerts.append({
                'type': 'info',
                'message': 'Revenue down compared to yesterday',
                'timestamp': datetime.now().isoformat()
            })
        occupancy_rate = round((occupied_spots / total_spots * 100) if total_spots > 0 else 0, 2)
        dashboard_data = {
            'total_parking_lots': total_lots,
            'total_parking_spots': total_spots,
            'occupied_spots': occupied_spots,
            'available_spots': available_spots,
            'total_users': total_users,
            'active_bookings': active_bookings,
            'occupancy_rate': occupancy_rate,
            'today_revenue': float(today_revenue),
            'week_revenue': float(week_revenue),
            'month_revenue': float(month_revenue),
            'revenue_growth': round(revenue_growth, 1),
            'weekly_growth': round(weekly_growth, 1),
            'today_reservations': today_reservations,
            'total_reservations': Reservation.query.count(),
            'most_popular_lot': most_popular_lot,
            'recent_activity': recent_activity,
            'system_status': system_status,
            'alerts': alerts,
            'daily_revenue_trend': [],
            'daily_bookings_trend': []
        }
        daily_revenue_trend = []
        daily_bookings_trend = []
        for i in range(7):
            trend_date = today - timedelta(days=i)
            daily_reservations = Reservation.query.filter(
                func.date(Reservation.parking_timestamp) == trend_date
            ).count()
            daily_revenue_val = db.session.query(func.sum(Reservation.parking_cost)).filter(
                func.date(Reservation.parking_timestamp) == trend_date
            ).scalar() or 0
            daily_revenue_trend.insert(0, {
                'date': trend_date.isoformat(),
                'revenue': float(daily_revenue_val)
            })
            daily_bookings_trend.insert(0, {
                'date': trend_date.isoformat(),
                'bookings': daily_reservations
            })
        dashboard_data['daily_revenue_trend'] = daily_revenue_trend
        dashboard_data['daily_bookings_trend'] = daily_bookings_trend
        if current_app.redis:
            current_app.redis.setex(cache_key, 300, json.dumps(dashboard_data))
        return success_response(dashboard_data, "Dashboard statistics retrieved")
    except Exception as e:
        current_app.logger.error(f"Admin dashboard error: {str(e)}")
        return error_response("Failed to retrieve dashboard data", 500)
def success_response(data, message="Success", status_code=200):
    return jsonify({
        'success': True,
        'message': message,
        'data': data
    }), status_code
def error_response(message, status_code=400):
    """Return standardized error response"""
    return jsonify({
        'success': False,
        'error': message
    }), status_code

@admin_bp.route('/parking-lots', methods=['GET'])
@jwt_required()
@admin_required
def get_parking_lots():
   
    try:
        lots = ParkingLot.query.all()
        lots_data = []
        
        for lot in lots:
            occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
            lots_data.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'price': lot.price,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'number_of_spots': lot.number_of_spots,
                'occupied_spots': occupied_spots,
                'available_spots': lot.number_of_spots - occupied_spots,
                'occupancy_rate': round((occupied_spots / lot.number_of_spots * 100) if lot.number_of_spots > 0 else 0, 2)
            })
        
        return success_response(lots_data, "Parking lots retrieved successfully")
        
    except Exception as e:
        current_app.logger.error(f"Get parking lots error: {str(e)}")
        return error_response("Failed to retrieve parking lots", 500)

@admin_bp.route('/parking-lots', methods=['POST'])
@jwt_required()
@admin_required
def create_parking_lot():
  
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['prime_location_name', 'price', 'address', 'pin_code', 'number_of_spots']
        for field in required_fields:
            if field not in data or not data[field]:
                return error_response(f"Missing required field: {field}", 400)
        
        # Validate number of spots
        if data['number_of_spots'] <= 0 or data['number_of_spots'] > current_app.config['MAX_PARKING_SPOTS_PER_LOT']:
            return error_response(f"Number of spots must be between 1 and {current_app.config['MAX_PARKING_SPOTS_PER_LOT']}", 400)
        
        # Create parking lot
        parking_lot = ParkingLot(
            prime_location_name=data['prime_location_name'],
            price=float(data['price']),
            address=data['address'],
            pin_code=data['pin_code'],
            number_of_spots=int(data['number_of_spots'])
        )
        
        db.session.add(parking_lot)
        db.session.flush()  # Get the lot ID
        
        # Create parking spots automatically
        spots = []
        for i in range(1, parking_lot.number_of_spots + 1):
            spot = ParkingSpot(
                lot_id=parking_lot.id,
                spot_number=i,
                status='A'  # Available
            )
            spots.append(spot)
        
        db.session.add_all(spots)
        db.session.commit()
        
        # Invalidate cache
        if current_app.redis:
            current_app.redis.delete("admin_dashboard_stats")
            current_app.redis.delete("available_parking_lots")
        
        return success_response({
            'id': parking_lot.id,
            'message': f"Parking lot created with {parking_lot.number_of_spots} spots"
        }, "Parking lot created successfully", 201)
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create parking lot error: {str(e)}")
        return error_response("Failed to create parking lot", 500)

@admin_bp.route('/parking-lots/<int:lot_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_parking_lot(lot_id):
 
    try:
        lot = ParkingLot.query.get_or_404(lot_id)
        data = request.get_json()
        
        # Update basic information
        if 'prime_location_name' in data:
            lot.prime_location_name = data['prime_location_name']
        if 'price' in data:
            lot.price = float(data['price'])
        if 'address' in data:
            lot.address = data['address']
        if 'pin_code' in data:
            lot.pin_code = data['pin_code']
        
        # Handle spot number changes
        if 'number_of_spots' in data:
            new_spots_count = int(data['number_of_spots'])
            current_spots_count = lot.number_of_spots
            
            if new_spots_count != current_spots_count:
                # Check if we can reduce spots (no occupied spots beyond new count)
                if new_spots_count < current_spots_count:
                    occupied_spots_beyond = ParkingSpot.query.filter(
                        ParkingSpot.lot_id == lot_id,
                        ParkingSpot.spot_number > new_spots_count,
                        ParkingSpot.status == 'O'
                    ).count()
                    
                    if occupied_spots_beyond > 0:
                        return error_response("Cannot reduce spots: some spots beyond the new limit are occupied", 400)
                    
                    # Remove excess spots
                    ParkingSpot.query.filter(
                        ParkingSpot.lot_id == lot_id,
                        ParkingSpot.spot_number > new_spots_count
                    ).delete()
                
                elif new_spots_count > current_spots_count:
                    # Add new spots
                    new_spots = []
                    for i in range(current_spots_count + 1, new_spots_count + 1):
                        spot = ParkingSpot(
                            lot_id=lot_id,
                            spot_number=i,
                            status='A'
                        )
                        new_spots.append(spot)
                    db.session.add_all(new_spots)
                
                lot.number_of_spots = new_spots_count
        
        db.session.commit()
        
        # Invalidate cache
        if current_app.redis:
            current_app.redis.delete("admin_dashboard_stats")
            current_app.redis.delete("available_parking_lots")
        
        return success_response({'id': lot.id}, "Parking lot updated successfully")
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update parking lot error: {str(e)}")
        return error_response("Failed to update parking lot", 500)


@admin_bp.route('/parking-lots/<int:lot_id>', methods=['DELETE'])  
@jwt_required()
@admin_required
def delete_parking_lot(lot_id): 
    
    try:
        lot = ParkingLot.query.get_or_404(lot_id) 
        
        # Check if any spots are occupied
        occupied_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count()  
        if occupied_spots > 0:
            return error_response("Cannot delete parking lot: some spots are currently occupied", 400)

        # Delete all reservations history for this lot
        spot_ids = [spot.id for spot in lot.spots]
        if spot_ids:
            Reservation.query.filter(Reservation.spot_id.in_(spot_ids)).delete(synchronize_session=False)

        # Delete the lot (cascade will delete spots)
        db.session.delete(lot)
        db.session.commit()

        # Invalidate cache
        if current_app.redis:
            current_app.redis.delete("admin_dashboard_stats")
            current_app.redis.delete("available_parking_lots")

        return success_response(None, "Parking lot deleted successfully")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Delete parking lot error: {str(e)}")
        return error_response("Failed to delete parking lot", 500)

@admin_bp.route('/parking-spots/<int:lot_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_parking_spots(lot_id):
   
    try:
        lot = ParkingLot.query.get_or_404(lot_id)
        spots = ParkingSpot.query.filter_by(lot_id=lot_id).order_by(ParkingSpot.spot_number).all()
        
        spots_data = []
        for spot in spots:
            spot_info = {
                'id': spot.id,
                'spot_number': spot.spot_number,
                'status': spot.status,
                'status_text': 'Occupied' if spot.status == 'O' else 'Available'
            }
            
            # If occupied, get vehicle details
            if spot.status == 'O':
                current_reservation = Reservation.query.filter_by(
                    spot_id=spot.id,
                    leaving_timestamp=None
                ).first()
                
                if current_reservation:
                    spot_info['vehicle_number'] = current_reservation.vehicle_number
                    spot_info['user_name'] = current_reservation.user.fullname
                    spot_info['parking_since'] = current_reservation.parking_timestamp.isoformat()
            
            spots_data.append(spot_info)
        
        return success_response({
            'lot_name': lot.prime_location_name,
            'total_spots': len(spots_data),
            'spots': spots_data
        }, "Parking spots retrieved successfully")
        
    except Exception as e:
        current_app.logger.error(f"Get parking spots error: {str(e)}")
        return error_response("Failed to retrieve parking spots", 500)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    
    try:
        users = User.query.filter_by(is_admin=False).all()
        
        users_data = []
        for user in users:
            # Get user's reservation statistics
            total_reservations = Reservation.query.filter_by(user_id=user.id).count()
            active_reservations = Reservation.query.filter_by(
                user_id=user.id,
                leaving_timestamp=None
            ).count()
            
            users_data.append({
                'id': user.id,
                'username': user.username,
                'fullname': user.fullname,
                'email': user.email,
                'address': user.address,
                'pin_code': user.pin_code,
                'total_reservations': total_reservations,
                'active_reservations': active_reservations
            })
        
        return success_response(users_data, "Users retrieved successfully")
        
    except Exception as e:
        current_app.logger.error(f"Get users error: {str(e)}")
        return error_response("Failed to retrieve users", 500)

@admin_bp.route('/statistics', methods=['GET'])
@jwt_required()
@admin_required
def get_statistics():
    
    try:
        # Daily reservations for the last 7 days
        daily_stats = []
        for i in range(7):
            date = datetime.now().date() - timedelta(days=i)
            reservations_count = Reservation.query.filter(
                func.date(Reservation.parking_timestamp) == date
            ).count()
            
            revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
                func.date(Reservation.parking_timestamp) == date
            ).scalar() or 0
            
            daily_stats.append({
                'date': date.isoformat(),
                'reservations': reservations_count,
                'revenue': float(revenue)
            })
        
        # Parking lot usage statistics
        lot_stats = []
        lots = ParkingLot.query.all()
        for lot in lots:
            total_reservations = db.session.query(func.count(Reservation.id)).join(
                ParkingSpot, Reservation.spot_id == ParkingSpot.id
            ).filter(ParkingSpot.lot_id == lot.id).scalar()
            
            lot_stats.append({
                'lot_name': lot.prime_location_name,
                'total_spots': lot.number_of_spots,
                'total_reservations': total_reservations,
                'current_occupied': ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
            })
        
        return success_response({
            'daily_stats': daily_stats,
            'lot_stats': lot_stats
        }, "Statistics retrieved successfully")
        
    except Exception as e:
        current_app.logger.error(f"Get statistics error: {str(e)}")
        return error_response("Failed to retrieve statistics", 500)


# Add these new routes to admin_routes.py

@admin_bp.route('/statistics/comprehensive', methods=['GET'])
@jwt_required()
@admin_required
def get_comprehensive_statistics():
    
    try:
        time_range = request.args.get('time_range', '30d')
        
        # Calculate date range
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

        # Total Revenue
        total_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
            and_(
                Reservation.parking_timestamp >= start_date,
                Reservation.parking_timestamp <= end_date
            )
        ).scalar() or 0

        # Total Bookings
        total_bookings = Reservation.query.filter(
            and_(
                Reservation.parking_timestamp >= start_date,
                Reservation.parking_timestamp <= end_date
            )
        ).count()

        # Active Users (users who made bookings in the period)
        active_users = db.session.query(func.count(func.distinct(Reservation.user_id))).filter(
            and_(
                Reservation.parking_timestamp >= start_date,
                Reservation.parking_timestamp <= end_date
            )
        ).scalar() or 0


        total_spots = ParkingSpot.query.count()
        
        if total_spots > 0:
            # Get current occupied spots
            current_occupied = ParkingSpot.query.filter_by(status='O').count()
            
            # Calculate simple occupancy rate based on current state
            avg_occupancy = (current_occupied / total_spots) * 100
            
            # Alternative: Calculate based on active reservations in period
            active_reservations_in_period = Reservation.query.filter(
                and_(
                    Reservation.parking_timestamp >= start_date,
                    Reservation.parking_timestamp <= end_date,
                    Reservation.leaving_timestamp.is_(None)
                )
            ).count()
            
            # Use the higher of current occupancy or active reservations rate
            reservation_based_occupancy = (active_reservations_in_period / total_spots) * 100
            avg_occupancy = max(avg_occupancy, reservation_based_occupancy)
        else:
            avg_occupancy = 0

        # Mock satisfaction and efficiency (you can implement real calculations)
        satisfaction_rate = 94.2  # Based on ratings if you have them
        efficiency_rate = 87.5   # Based on utilization metrics

        # Revenue growth (compare with previous period)
        prev_start_date = start_date - (end_date - start_date)
        prev_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
            and_(
                Reservation.parking_timestamp >= prev_start_date,
                Reservation.parking_timestamp < start_date
            )
        ).scalar() or 0

        revenue_growth = 0
        if prev_revenue > 0:
            revenue_growth = ((total_revenue - prev_revenue) / prev_revenue) * 100

        # Geographic Distribution (by pin code)
        geographic_data = db.session.query(
            ParkingLot.pin_code,
            func.count(func.distinct(ParkingLot.id)).label('lots_count'),
            func.count(Reservation.id).label('bookings_count'),
            func.sum(Reservation.parking_cost).label('total_revenue')
        ).join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)\
        .join(Reservation, ParkingSpot.id == Reservation.spot_id)\
        .filter(
            and_(
                Reservation.parking_timestamp >= start_date,
                Reservation.parking_timestamp <= end_date
            )
        ).group_by(ParkingLot.pin_code).all()

        areas = []
        for pin_code, lots_count, bookings_count, revenue in geographic_data:
            # Generate area name based on pin code (you can enhance this)
            area_name = f"Area {pin_code[:3]}"
            areas.append({
                'name': area_name,
                'pinCode': pin_code,
                'lots': lots_count,
                'bookings': bookings_count,
                'revenue': float(revenue or 0)
            })

        # Revenue and Bookings Trend (daily data for charts)
        daily_trend = []
        for i in range(30):  # Last 30 days
            trend_date = end_date - timedelta(days=i)
            daily_bookings = Reservation.query.filter(
                func.date(Reservation.parking_timestamp) == trend_date.date()
            ).count()
            
            daily_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
                func.date(Reservation.parking_timestamp) == trend_date.date()
            ).scalar() or 0
            
            daily_trend.insert(0, {
                'date': trend_date.date().isoformat(),
                'bookings': daily_bookings,
                'revenue': float(daily_revenue)
            })

        # Top performing locations
        top_locations = db.session.query(
            ParkingLot.prime_location_name,
            func.count(Reservation.id).label('bookings'),
            func.sum(Reservation.parking_cost).label('revenue')
        ).join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)\
        .join(Reservation, ParkingSpot.id == Reservation.spot_id)\
        .filter(
            and_(
                Reservation.parking_timestamp >= start_date,
                Reservation.parking_timestamp <= end_date
            )
        ).group_by(ParkingLot.id)\
        .order_by(func.sum(Reservation.parking_cost).desc())\
        .limit(5).all()

        top_locations_data = []
        for location, bookings, revenue in top_locations:
            top_locations_data.append({
                'name': location,
                'bookings': bookings,
                'revenue': float(revenue or 0)
            })

        statistics_data = {
            'overview': {
                'totalRevenue': float(total_revenue),
                'totalBookings': total_bookings,
                'activeUsers': active_users,
                'avgOccupancy': round(avg_occupancy, 1),
                'satisfaction': satisfaction_rate,
                'efficiency': efficiency_rate,
                'revenueGrowth': round(revenue_growth, 1)
            },
            'geographicData': areas,
            'trendData': daily_trend,
            'topLocations': top_locations_data,
            'timeRange': time_range
        }

        return success_response(statistics_data, "Comprehensive statistics retrieved successfully")

    except Exception as e:
        current_app.logger.error(f"Get comprehensive statistics error: {str(e)}")
        return error_response("Failed to retrieve comprehensive statistics", 500)



@admin_bp.route('/statistics/revenue-trends', methods=['GET'])
@jwt_required()
@admin_required
def get_revenue_trends():
  
    try:
        period = request.args.get('period', 'daily')  # daily, weekly, monthly
        days = int(request.args.get('days', 30))
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        trends = []
        
        if period == 'daily':
            for i in range(days):
                date = start_date + timedelta(days=i)
                revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
                    func.date(Reservation.parking_timestamp) == date.date()
                ).scalar() or 0
                
                bookings = Reservation.query.filter(
                    func.date(Reservation.parking_timestamp) == date.date()
                ).count()
                
                trends.append({
                    'date': date.date().isoformat(),
                    'revenue': float(revenue),
                    'bookings': bookings
                })
        
        elif period == 'weekly':
            weeks = days // 7
            for i in range(weeks):
                week_start = start_date + timedelta(weeks=i)
                week_end = week_start + timedelta(days=6)
                
                revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
                    and_(
                        Reservation.parking_timestamp >= week_start,
                        Reservation.parking_timestamp <= week_end
                    )
                ).scalar() or 0
                
                bookings = Reservation.query.filter(
                    and_(
                        Reservation.parking_timestamp >= week_start,
                        Reservation.parking_timestamp <= week_end
                    )
                ).count()
                
                trends.append({
                    'date': week_start.date().isoformat(),
                    'revenue': float(revenue),
                    'bookings': bookings,
                    'period': f"Week {i+1}"
                })

        return success_response({
            'trends': trends,
            'period': period,
            'totalDays': days
        }, "Revenue trends retrieved successfully")

    except Exception as e:
        current_app.logger.error(f"Get revenue trends error: {str(e)}")
        return error_response("Failed to retrieve revenue trends", 500)

@admin_bp.route('/statistics/performance-metrics', methods=['GET'])
@jwt_required()
@admin_required
def get_performance_metrics():
    
    try:
        # Peak hours analysis
        hourly_usage = db.session.query(
            func.extract('hour', Reservation.parking_timestamp).label('hour'),
            func.count(Reservation.id).label('bookings')
        ).group_by(func.extract('hour', Reservation.parking_timestamp)).all()

        peak_hours = []
        for hour, bookings in hourly_usage:
            peak_hours.append({
                'hour': int(hour),
                'bookings': bookings,
                'label': f"{int(hour):02d}:00"
            })

        # Average session duration
        completed_reservations = Reservation.query.filter(
            Reservation.leaving_timestamp.isnot(None)
        ).all()

        total_duration = 0
        session_count = 0
        for reservation in completed_reservations:
            if reservation.leaving_timestamp and reservation.parking_timestamp:
                duration = reservation.leaving_timestamp - reservation.parking_timestamp
                total_duration += duration.total_seconds() / 3600  # Convert to hours
                session_count += 1

        avg_session_duration = total_duration / max(session_count, 1)

        # Utilization rate by location
        location_utilization = []
        lots = ParkingLot.query.all()
        
        for lot in lots:
            total_bookings = db.session.query(func.count(Reservation.id)).join(
                ParkingSpot, Reservation.spot_id == ParkingSpot.id
            ).filter(ParkingSpot.lot_id == lot.id).scalar()
            
            max_possible_bookings = lot.number_of_spots * 24 * 30  # Rough calculation
            utilization_rate = (total_bookings / max_possible_bookings) * 100 if max_possible_bookings > 0 else 0
            
            location_utilization.append({
                'location': lot.prime_location_name,
                'utilization': round(min(100, utilization_rate), 1),
                'totalSpots': lot.number_of_spots,
                'totalBookings': total_bookings
            })

        metrics_data = {
            'peakHours': peak_hours,
            'avgSessionDuration': round(avg_session_duration, 1),
            'locationUtilization': location_utilization,
            'systemEfficiency': 87.5,  # Mock value - you can calculate based on real metrics
            'customerSatisfaction': 94.2  # Mock value - you can calculate from ratings
        }

        return success_response(metrics_data, "Performance metrics retrieved successfully")

    except Exception as e:
        current_app.logger.error(f"Get performance metrics error: {str(e)}")
        return error_response("Failed to retrieve performance metrics", 500)

