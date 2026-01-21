#!/usr/bin/env python3
"""
Widget Sorting Vision System for Raspberry Pi
Detects holes in acrylic widgets using OpenCV
Communicates with Arduino via serial for automated sorting

Usage:
  python3 widget_inspector.py                    # Run with Arduino (auto mode)
  python3 widget_inspector.py --calibrate        # Calibration mode
  python3 widget_inspector.py --manual           # Manual testing mode
  python3 widget_inspector.py --port /dev/ttyUSB0  # Specify Arduino port

Vast majority of code by Claude Sonnet 4.5, with edits by Keegan Smit and Noah Grimes  
"""

import cv2
import numpy as np
import serial
import time
import sys

class WidgetInspector:
    def __init__(self, serial_port='/dev/ttyACM0', camera_id=0):
        """
        Initialize the widget inspector system
        
        Args:
            serial_port: Path to Arduino serial port (try /dev/ttyACM0, /dev/ttyUSB0, /dev/ttyACM1)
            camera_id: Camera device ID (usually 0, try 1 if camera not found)
        """
        print("="*60)
        print("WIDGET INSPECTOR INITIALIZATION")
        print("="*60)
        
        # ========== CAMERA SETUP ==========
        print("\n[1/3] Setting up camera...")
        self.camera = cv2.VideoCapture(camera_id)
        
        if not self.camera.isOpened():
            print(f"ERROR: Could not open camera {camera_id}")
            sys.exit(1)
        
        # Set resolution - 320x240 is fast and sufficient for hole detection
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize latency
        
        # Warm up camera - first few frames are often dark/corrupted
        print("   Warming up camera...")
        time.sleep(2)
        for i in range(5):
            self.camera.read()  # Discard initial frames
        
        print("   ✓ Camera ready!")
        
        # ========== SERIAL SETUP ==========
        print("\n[2/3] Connecting to Arduino...")
        self.serial = None
        try:
            self.serial = serial.Serial(serial_port, 9600, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset after connection
            print(f"   ✓ Connected to Arduino on {serial_port}")
        except (serial.SerialException, FileNotFoundError) as e:
            print(f"   ⚠️  Arduino not connected: {e}")
            print("   Running in TEST MODE - no Arduino communication")
            print("   (This is fine for calibration and testing)\n")
        
        # ========== DETECTION PARAMETERS ==========
        print("\n[3/3] Loading detection parameters...")
        
        # Hole size constraints (in pixels)
        self.HOLE_DIAMETER_MIN = 20   # Minimum hole diameter
        self.HOLE_DIAMETER_MAX = 100  # Maximum hole diameter
        
        # Expected hole position (center of frame by default)
        self.EXPECTED_X = 160  # X coordinate where hole should be
        self.EXPECTED_Y = 100  # Y coordinate where hole should be
        self.POSITION_TOLERANCE = 100  # How far off-center is acceptable
        
        # Hough Circle detection parameters
        self.BLUR_KERNEL = 5         # Gaussian blur size (must be odd)
        self.HOUGH_DP = 1            # Inverse ratio of accumulator resolution
        self.HOUGH_MIN_DIST = 50     # Minimum distance between circle centers
        self.HOUGH_PARAM1 = 30       # Edge detection threshold (higher = stricter)
        self.HOUGH_PARAM2 = 15       # Circle detection threshold (lower = more sensitive)
        
        # Widget presence detection
        self.WIDGET_THRESHOLD = 10000  # Will be auto-calibrated at startup
        self.BRIGHTNESS_CUTOFF = 120   # Brightness threshold for "dark" objects
        
        # Widget counters for tracking results
        self.goodCount = 0
        self.badCount = 0
        
        print("   ✓ Parameters loaded!")
        
        # ========== AUTO-CALIBRATION ==========
        print("\n[4/4] Auto-calibrating widget detection threshold...")
        print("   Please ensure inspection area is EMPTY")
        print("   Measuring background darkness in 3 seconds...")
        time.sleep(3)
        
        self.auto_calibrate_threshold()
        
        print("\n" + "="*60)
        print("INITIALIZATION COMPLETE")
        print("="*60 + "\n")
    
    def auto_calibrate_threshold(self):
        """
        Automatically calibrate widget detection threshold at startup
        Measures empty platform darkness and sets threshold accordingly
        """
        print("   Taking 5 calibration measurements...")
        
        measurements = []
        for i in range(5):
            # Capture frame
            frame = self.capture_image()
            if frame is None:
                print(f"   Warning: Could not capture calibration frame {i+1}")
                continue
            
            # Measure dark area
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, self.BRIGHTNESS_CUTOFF, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            max_area = 0
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
            
            measurements.append(max_area)
            print(f"   Measurement {i+1}: {max_area} pixels")
            time.sleep(0.2)
        
        if not measurements:
            print("   ⚠️  Calibration failed - using default threshold")
            return
        
        # Calculate average empty darkness
        avg_empty = sum(measurements) / len(measurements)
        
        # Set threshold = average empty darkness + 10,000 pixel buffer
        # This ensures we detect widgets while ignoring empty platform variations
        self.WIDGET_THRESHOLD = int(avg_empty + 10000)
        
        print(f"\n   ✓ Calibration complete!")
        print(f"   Empty platform darkness: {avg_empty:.0f} pixels (average)")
        print(f"   Widget detection threshold set to: {self.WIDGET_THRESHOLD} pixels")
        print(f"   (Empty + 10,000 pixel buffer)")
    
    def capture_image(self):
        """
        Capture a single frame from the camera
        
        Returns:
            frame: BGR image as numpy array, or None if capture failed
        """
        # Use grab/retrieve for minimal latency (don't use buffered frames)
        self.camera.grab()
        ret, frame = self.camera.retrieve()
        
        if not ret:
            print("ERROR: Could not capture image from camera")
            return None
        return frame
    
    def detect_widget_present(self, frame):
        """
        Detect if a widget is actually present in the frame
        Uses thresholding and contour detection to find dark objects
        
        Args:
            frame: Input BGR image
            
        Returns:
            True if widget detected, False if frame is empty
        """
        # Convert to grayscale for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Threshold to find dark objects (widgets are black on white background)
        # THRESH_BINARY_INV makes dark areas white and light areas black
        _, thresh = cv2.threshold(gray, self.BRIGHTNESS_CUTOFF, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours (outlines) of dark regions
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find the largest dark area
        max_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
        
        # Debug output to help with threshold tuning
        print(f"   [Debug] Largest dark area: {max_area} pixels (threshold: {self.WIDGET_THRESHOLD})")
        
        # Check if largest area exceeds threshold
        return max_area > self.WIDGET_THRESHOLD
    
    def detect_hole(self, image, debug=False):
        """
        Detect circular hole in widget using Hough Circle Transform
        
        Args:
            image: Input BGR image
            debug: If True, saves debug images showing detection process
            
        Returns:
            tuple: (is_good, circle_data)
                - is_good: True if hole meets all criteria (size + position)
                - circle_data: (x, y, radius) or None if no hole detected
        """
        if image is None:
            return False, None
        
        # Step 1: Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Step 2: Apply Gaussian blur to reduce noise and improve circle detection
        blurred = cv2.GaussianBlur(gray, (self.BLUR_KERNEL, self.BLUR_KERNEL), 0)
        
        # Save intermediate images for debugging if requested
        if debug:
            cv2.imwrite('debug_1_gray.jpg', gray)
            cv2.imwrite('debug_2_blurred.jpg', blurred)
        
        # Step 3: Detect circles using Hough Circle Transform
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=self.HOUGH_DP,
            minDist=self.HOUGH_MIN_DIST,
            param1=self.HOUGH_PARAM1,
            param2=self.HOUGH_PARAM2,
            minRadius=int(self.HOLE_DIAMETER_MIN / 2),
            maxRadius=int(self.HOLE_DIAMETER_MAX / 2)
        )
        
        # Debug output showing all detected circles
        print(f"   [Debug] Circles detected: {circles is not None}")
        if circles is not None:
            print(f"   [Debug] Number of circles found: {len(circles[0])}")
            for i, circle in enumerate(circles[0][:3]):  # Show first 3 circles
                cx, cy, cr = circle
                print(f"   [Debug] Circle {i}: x={cx:.1f}, y={cy:.1f}, r={cr:.1f}, diameter={cr*2:.1f}")
        
        # Process detected circles
        if circles is not None:
            # Round circle coordinates and convert to integers
            circles = np.uint16(np.around(circles))
            circle = circles[0][0]  # Take the first (strongest) circle
            
            # CRITICAL: Convert to Python int to avoid numpy uint16 overflow bugs
            x = int(circle[0])
            y = int(circle[1])
            r = int(circle[2])
            
            # Check criterion 1: Is the hole the right size?
            diameter = r * 2
            size_ok = self.HOLE_DIAMETER_MIN <= diameter <= self.HOLE_DIAMETER_MAX
            
            # Check criterion 2: Is the hole in the expected position?
            x_diff = abs(x - self.EXPECTED_X)
            y_diff = abs(y - self.EXPECTED_Y)
            position_ok = (x_diff <= self.POSITION_TOLERANCE and 
                          y_diff <= self.POSITION_TOLERANCE)
            
            # Widget is good only if BOTH criteria are met
            is_good = size_ok and position_ok
            
            # Save annotated debug image if requested
            if debug:
                debug_img = image.copy()
                
                # Draw detected circle (green if good, red if bad)
                color = (0, 255, 0) if is_good else (0, 0, 255)
                cv2.circle(debug_img, (x, y), r, color, 2)
                cv2.circle(debug_img, (x, y), 2, (0, 0, 255), 3)  # Center dot
                
                # Draw expected position rectangle
                cv2.rectangle(
                    debug_img,
                    (self.EXPECTED_X - self.POSITION_TOLERANCE, 
                     self.EXPECTED_Y - self.POSITION_TOLERANCE),
                    (self.EXPECTED_X + self.POSITION_TOLERANCE,
                     self.EXPECTED_Y + self.POSITION_TOLERANCE),
                    (255, 0, 0), 2
                )
                
                # Save debug image
                cv2.imwrite(f'debug_3_result_{"good" if is_good else "bad"}.jpg', debug_img)
                
                # Print detailed analysis
                print(f"   Circle detected: x={x}, y={y}, r={r}, diameter={diameter}")
                print(f"   Position offset: X={x_diff}px, Y={y_diff}px from expected")
                print(f"   Size check: {'PASS' if size_ok else 'FAIL'} (range: {self.HOLE_DIAMETER_MIN}-{self.HOLE_DIAMETER_MAX}px)")
                print(f"   Position check: {'PASS' if position_ok else 'FAIL'} (tolerance: {self.POSITION_TOLERANCE}px)")
            
            return is_good, (x, y, r)
        
        else:
            # No circles detected at all
            if debug:
                cv2.imwrite('debug_3_no_circle.jpg', image)
                print("   No circles detected - widget has no hole or hole not visible")
            return False, None
    
    def send_result(self, is_good, is_widget):
        """
        Send inspection result to Arduino and update counters
        
        Args:
            is_good: True if widget passed inspection
            is_widget: True if a widget was present (False if empty platform)
        """
        # Only update counters if there was actually a widget present
        if is_widget:
            if is_good:
                self.goodCount += 1
            else:
                self.badCount += 1
        
        # Cap counters at 9 each (display limitation)
        self.goodCount = min(self.goodCount, 9)
        self.badCount = min(self.badCount, 9)
        
        # Format count as two-digit number: tens=good, ones=bad
        # Example: 3 good, 2 bad = "32"
        count_number = (self.goodCount * 10) + self.badCount
        
        # Send count to Arduino if connected
        if self.serial:
            # Send count in format "45" for 4 good, 5 bad
            count_msg = f"{count_number}\n"
            self.serial.write(count_msg.encode())
            
            if is_widget:
                result_text = "GOOD" if is_good else "BAD"
                print(f"   Result: {result_text}")
            else:
                print(f"   Result: EMPTY (no widget present)")
            
            print(f"   → Sent to Arduino: {count_number} (Good: {self.goodCount}, Bad: {self.badCount})")
        else:
            # No Arduino - just print result locally
            if is_widget:
                result = "✓ GOOD" if is_good else "✗ BAD"
                print(f"   Result: {result}")
            else:
                print(f"   Result: EMPTY (no widget)")
            print(f"   Count: {count_number} (Good: {self.goodCount}, Bad: {self.badCount})")
            print(f"   (Would send to Arduino: {count_number})")
    
    def read_command(self):
        """
        Read a line from Arduino serial connection
        
        Returns:
            String command from Arduino, or None if no data available
        """
        if self.serial and self.serial.in_waiting > 0:
            try:
                line = self.serial.readline().decode('utf-8').strip()
                return line
            except UnicodeDecodeError:
                print("   Warning: Received invalid serial data")
                return None
        return None
    
    def calibrate(self):
        """
        Interactive calibration mode for tuning detection parameters
        Note: Requires display/X11 - won't work on headless Pi
        """
        print("\n" + "="*60)
        print("CALIBRATION MODE")
        print("="*60)
        print("Position a GOOD widget in the inspection area")
        print("Press 's' to capture and analyze")
        print("Press 'q' to quit calibration")
        print("="*60 + "\n")
        
        while True:
            ret, frame = self.camera.read()
            if not ret:
                continue
            
            # Show live camera feed (requires X11/display)
            cv2.imshow('Calibration - Press S to capture, Q to quit', frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s'):
                print("\n" + "-"*60)
                print("CAPTURING AND ANALYZING...")
                print("-"*60)
                
                # Check if widget is present
                hasWidget = self.detect_widget_present(frame)
                
                if hasWidget:
                    # Detect hole and save debug images
                    is_good, circle = self.detect_hole(frame, debug=True)
                    print(f"\nResult: {'✓ GOOD' if is_good else '✗ BAD'}")
                    
                    if circle:
                        x, y, r = circle
                        print(f"\nSuggested parameter updates:")
                        print(f"  self.EXPECTED_X = {x}")
                        print(f"  self.EXPECTED_Y = {y}")
                        print(f"  Hole diameter = {r*2} pixels")
                    
                    print("\nDebug images saved to current directory:")
                    print("  - debug_1_gray.jpg")
                    print("  - debug_2_blurred.jpg")
                    print("  - debug_3_result_*.jpg")
                else:
                    print("\n⚠️  NO WIDGET DETECTED")
                    print(f"   Largest dark area was below threshold ({self.WIDGET_THRESHOLD} pixels)")
                    print("   Try adjusting lighting or WIDGET_THRESHOLD")
                
                print("-"*60 + "\n")
            
            elif key == ord('q'):
                break
        
        cv2.destroyAllWindows()
        print("\nCalibration complete!\n")
    
    def run_manual(self):
        """
        Manual testing mode - press ENTER to capture and inspect
        Good for testing without Arduino connection
        """
        print("\n" + "="*60)
        print("MANUAL TESTING MODE")
        print("="*60)
        print("Press ENTER to inspect a widget")
        print("Type 'quit' to exit")
        print("="*60 + "\n")
        
        try:
            while True:
                command = input("Ready> ").strip().lower()
                
                if command == 'quit' or command == 'q':
                    break
                
                print("\n" + "-"*60)
                print("INSPECTING WIDGET...")
                print("-"*60)
                
                # Small delay for stability
                time.sleep(0.5)
                
                # Capture and analyze
                image = self.capture_image()
                
                if image is not None:
                    # Check if widget is present
                    hasWidget = self.detect_widget_present(image)
                    
                    if hasWidget:
                        # Widget present - check if it's good or bad
                        is_good, circle = self.detect_hole(image, debug=True)
                        self.send_result(is_good, True)
                    else:
                        # No widget present
                        print("   ⚠️  NO WIDGET DETECTED")
                        self.send_result(False, False)
                else:
                    print("   ERROR: Could not capture image")
                
                print("-"*60 + "\n")
                
        except KeyboardInterrupt:
            print("\n\nShutting down...")
    
    def run_auto(self):
        """
        Automatic mode - waits for Arduino signals
        Arduino sends "READY" when system is ready
        Arduino sends "CAPTURE" when it wants an inspection
        """
        print("\n" + "="*60)
        print("AUTOMATIC MODE - Waiting for Arduino signals")
        print("="*60)
        
        if not self.serial:
            print("\nERROR: Arduino not connected!")
            print("Cannot run automatic mode without Arduino.")
            print("Use --manual flag for manual testing mode.\n")
            return
        
        print("Listening for commands from Arduino...")
        print("(Arduino should send 'READY' to start, 'CAPTURE' to inspect)")
        print("Press Ctrl+C to stop\n")
        
        ready = False
        
        try:
            while True:
                # Check for commands from Arduino
                command = self.read_command()
                
                if command:
                    print(f"\n← Received from Arduino: '{command}' (length: {len(command)})")
                    
                    # Debug: show character codes
                    print(f"   Debug: Character codes: {[ord(c) for c in command]}")
                    
                    if command == "READY":
                        # Reset counters on READY signal
                        self.goodCount = 0
                        self.badCount = 0
                        ready = True
                        print("   ✓ System READY - Counters reset to 00")
                        
                        # Send READY acknowledgment back to Arduino
                        self.serial.write(b'READY\n')
                        print("   → Sent to Arduino: READY (acknowledgment)")
                        print("   Waiting for CAPTURE command...")
                    
                    elif command == "CAPTURE":
                        if not ready:
                            print("   Warning: Received CAPTURE before READY")
                        
                        print("\n" + "-"*60)
                        print("INSPECTING WIDGET...")
                        print("-"*60)
                        
                        # Small delay for mechanical stability
                        time.sleep(0.3)
                        
                        # Capture and analyze
                        image = self.capture_image()
                        
                        if image is not None:
                            # Check if widget is present
                            hasWidget = self.detect_widget_present(image)
                            
                            if hasWidget:
                                # Widget present - check if good or bad
                                is_good, circle = self.detect_hole(image, debug=False)
                                self.send_result(is_good, True)
                            else:
                                # No widget present
                                print("   ⚠️  NO WIDGET DETECTED")
                                self.send_result(False, False)
                        else:
                            # Camera error
                            self.serial.write(b'ERROR\n')
                            print("   ERROR: Could not capture image")
                        
                        print("-"*60 + "\n")
                        print("Ready for next CAPTURE command...")
                    
                    else:
                        print(f"   Unknown command: {command}")
                
                # Small delay to prevent CPU hammering
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            print("\n\nShutting down...")
    
    def cleanup(self):
        """Release all resources"""
        print("\nCleaning up...")
        self.camera.release()
        if self.serial:
            self.serial.close()
        cv2.destroyAllWindows()
        print("Cleanup complete. Goodbye!\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Widget Sorting Vision System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 widget_inspector.py                    # Automatic mode with Arduino
  python3 widget_inspector.py --manual           # Manual testing mode
  python3 widget_inspector.py --calibrate        # Calibration mode
  python3 widget_inspector.py --port /dev/ttyUSB0  # Specify serial port
  python3 widget_inspector.py --camera 1         # Use second camera
        """
    )
    
    parser.add_argument('--port', default='/dev/ttyACM0', 
                       help='Arduino serial port (default: /dev/ttyACM0)')
    parser.add_argument('--camera', type=int, default=0,
                       help='Camera device ID (default: 0)')
    parser.add_argument('--calibrate', action='store_true',
                       help='Run calibration mode (requires display)')
    parser.add_argument('--manual', action='store_true',
                       help='Run manual testing mode (no Arduino required)')
    
    args = parser.parse_args()
    
    # Create inspector instance
    try:
        inspector = WidgetInspector(serial_port=args.port, camera_id=args.camera)
    except Exception as e:
        print(f"\nFATAL ERROR during initialization: {e}")
        sys.exit(1)
    
    try:
        # Run requested mode
        if args.calibrate:
            inspector.calibrate()
        elif args.manual:
            inspector.run_manual()
        else:
            inspector.run_auto()
    finally:
        inspector.cleanup()


if __name__ == "__main__":
    main()
