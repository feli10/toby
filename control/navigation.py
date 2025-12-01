import time
import math
import config
from motor import MotorDriver
from sensors import UltrasonicSensor

class Navigator:
    """
    Navigation system for Toby with destination tracking and obstacle avoidance.
    Estimates position based on speed and time.
    """
    
    def __init__(self, motor_driver, sensor_left, sensor_right):
        self.motor = motor_driver
        self.sensor_left = sensor_left
        self.sensor_right = sensor_right
        
        # Position tracking (in cm)
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0  # degrees, 0 = forward (positive y-axis)
        
        # Destination
        self.dest_x = None
        self.dest_y = None
        self.has_destination = False
        
        # Movement calibration
        self.cm_per_second = 10.0  
        self.degrees_per_second = 90.0  
        
        # State tracking
        self.last_update_time = time.time()
        
    def set_destination(self, x, y):
        """Set a destination point in cm relative to starting position."""
        self.dest_x = x
        self.dest_y = y
        self.has_destination = True
        print(f"Destination set to: ({x:.1f}, {y:.1f}) cm")
        
    def clear_destination(self):
        """Clear the current destination."""
        self.has_destination = False
        self.dest_x = None
        self.dest_y = None
        print("Destination cleared")
        
    def get_position(self):
        """Return current estimated position."""
        return (self.x, self.y, self.heading)
    
    def get_distance_to_destination(self):
        """Calculate distance to destination in cm."""
        if not self.has_destination:
            return None
        dx = self.dest_x - self.x
        dy = self.dest_y - self.y
        return math.sqrt(dx*dx + dy*dy)
    
    def get_bearing_to_destination(self):
        """Calculate bearing to destination in degrees."""
        if not self.has_destination:
            return None
        dx = self.dest_x - self.x
        dy = self.dest_y - self.y
        bearing = math.degrees(math.atan2(dx, dy))
        return bearing
    
    def get_heading_error(self):
        """Calculate difference between current heading and desired bearing."""
        if not self.has_destination:
            return 0
        bearing = self.get_bearing_to_destination()
        error = bearing - self.heading
        while error > 180:
            error -= 360
        while error < -180:
            error += 360
        return error
    
    def update_position(self, distance_moved, angle_turned):
        """
        Update estimated position based on movement.
        distance_moved: in cm
        angle_turned: in degrees (positive = left turn)
        """
        # Update heading
        self.heading += angle_turned
        self.heading = self.heading % 360
        
        # Update position based on distance moved in current heading
        heading_rad = math.radians(self.heading)
        self.x += distance_moved * math.sin(heading_rad)
        self.y += distance_moved * math.cos(heading_rad)
        
    def check_obstacles(self):
        """Check both ultrasonic sensors and return obstacle status."""
        dist_left = self.sensor_left.get_distance()
        dist_right = self.sensor_right.get_distance()
        
        obstacle_left = dist_left and dist_left < config.SAFE_FRONT_DISTANCE
        obstacle_right = dist_right and dist_right < config.SAFE_BACK_DISTANCE
        
        return dist_left, dist_right, obstacle_left, obstacle_right
    
    def turn_by_angle(self, angle_degrees):
        """Turn by specified angle (positive = left, negative = right)."""
        direction = 1 if angle_degrees > 0 else -1
        turn_time = abs(angle_degrees) / self.degrees_per_second
        
        print(f"Turning {'left' if direction > 0 else 'right'} by {abs(angle_degrees):.1f} degrees...")
        
        self.motor.set_speed('A', 0)
        self.motor.set_speed('B', direction * config.TURN_SPEED)
        time.sleep(turn_time)
        self.motor.stop_all()
        time.sleep(0.1)
        
        # Update position tracking
        self.update_position(0, angle_degrees)
        
        return turn_time
    
    def move_forward(self, duration):
        """Move forward for specified duration in seconds."""
        print(f"Moving forward for {duration:.2f}s...")
        
        self.motor.set_speed('A', config.DRIVE_SPEED)
        self.motor.set_speed('B', 0)
        time.sleep(duration)
        self.motor.stop_all()
        time.sleep(0.1)
        
        # Update position tracking
        distance = self.cm_per_second * duration
        self.update_position(distance, 0)
        
        return distance
    
    def avoid_obstacle(self):
        """
        Execute obstacle avoidance maneuver.
        Turns away from obstacle, moves forward a bit, then turns back to check.
        """
        dist_left, dist_right, obs_left, obs_right = self.check_obstacles()
        
        print(f"Obstacle detected - Left: {dist_left}, Right: {dist_right}")
        
        # Determine turn direction based on which sensor detected obstacle
        if obs_left and obs_right:
            # Both sides blocked, turn around
            print("Both sides blocked! Turning around...")
            self.turn_by_angle(-90)
            return True
        elif obs_left:
            # Turn right to avoid
            print("Obstacle on left, avoiding right...")
            self.turn_by_angle(-45)
            self.move_forward(1.0)
            self.turn_by_angle(45)
            return True
        elif obs_right:
            # Turn left to avoid
            print("Obstacle on right, avoiding left...")
            self.turn_by_angle(45)
            self.move_forward(1.0)
            self.turn_by_angle(-45)
            return True
        
        return False
    
    def navigate_step(self):
        """
        Execute one navigation step: check for obstacles, 
        avoid if needed, otherwise move toward destination.
        """
        # Check if we've reached destination
        if self.has_destination:
            dist_to_dest = self.get_distance_to_destination()
            if dist_to_dest < 10:  
                print(f"Destination reached! Position: ({self.x:.1f}, {self.y:.1f})")
                self.motor.stop_all()
                self.clear_destination()
                return False
            
            print(f"Position: ({self.x:.1f}, {self.y:.1f}), "
                  f"Heading: {self.heading:.1f}°, "
                  f"Distance to dest: {dist_to_dest:.1f}cm")
        
        # Check for obstacles
        dist_left, dist_right, obs_left, obs_right = self.check_obstacles()
        
        print(f"Sensors - Left: {dist_left}cm, Right: {dist_right}cm")
        
        # If obstacle detected, avoid it
        if obs_left or obs_right:
            self.avoid_obstacle()
            return True
        
        # No obstacles - navigate toward destination if we have one
        if self.has_destination:
            heading_error = self.get_heading_error()
            
            # If heading error is large, turn to face destination
            if abs(heading_error) > 15:
                print(f"Adjusting heading by {heading_error:.1f}°")
                turn_angle = max(-45, min(45, heading_error))  # Limit to 45 degree turns
                self.turn_by_angle(turn_angle)
            else:
                # Heading is good, move forward
                print("Path clear, moving toward destination...")
                self.move_forward(0.5)
        else:
            # No destination, just move forward
            print("No destination set, moving forward...")
            self.move_forward(0.5)
        
        time.sleep(0.1)
        return True
    
    def navigate_to_destination(self, timeout=60):
        """Navigate to destination with obstacle avoidance."""
        if not self.has_destination:
            print("No destination set!")
            return False
        
        start_time = time.time()
        
        while self.has_destination:
            if time.time() - start_time > timeout:
                print("Navigation timeout!")
                self.motor.stop_all()
                return False
            
            if not self.navigate_step():
                return True
        
        return True
