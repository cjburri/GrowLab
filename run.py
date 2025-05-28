from app import create_app
import RPi.GPIO as GPIO
app = create_app()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()
        print("Server stopped")