#!/bin/bash

# Colors for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_DIR="$PWD"
VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"
DJANGO_PROJECT_DIR="Dramoir"
DJANGO_SETTINGS_MODULE="MovieSeries.settings.dev"

# Check Redis service
check_redis() {
    echo -e "${BLUE}Checking Redis service...${NC}"
    if command -v redis-cli &> /dev/null; then
        if redis-cli ping &> /dev/null; then
            echo -e "${GREEN}Redis is running.${NC}"
            return 0
        else
            echo -e "${YELLOW}Redis is installed but not running. Attempting to start it...${NC}"
            if command -v systemctl &> /dev/null; then
                sudo systemctl start redis || redis-server &
            else
                redis-server &
            fi
            sleep 2
            if redis-cli ping &> /dev/null; then
                echo -e "${GREEN}Redis started successfully.${NC}"
                return 0
            else
                echo -e "${RED}Error starting Redis.${NC}"
                return 1
            fi
        fi
    else
        echo -e "${RED}Redis is not installed. Please install it:${NC}"
        echo -e "For Ubuntu/Debian: ${YELLOW}sudo apt install redis-server${NC}"
        echo -e "For Arch Linux: ${YELLOW}sudo pacman -S redis${NC}"
        echo -e "For macOS: ${YELLOW}brew install redis${NC}"
        return 1
    fi
}

# Check for virtual environment
check_venv() {
    echo -e "${BLUE}Checking virtual environment...${NC}"
    if [ -d "$VENV_DIR" ]; then
        echo -e "${GREEN}Virtual environment found.${NC}"
        return 0
    else
        echo -e "${YELLOW}Virtual environment not found. Creating a new one...${NC}"
        python -m venv $VENV_DIR
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Virtual environment created successfully.${NC}"
            return 0
        else
            echo -e "${RED}Error creating virtual environment.${NC}"
            return 1
        fi
    fi
}

# Activate virtual environment
activate_venv() {
    echo -e "${BLUE}Activating virtual environment...${NC}"
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
    elif [ -f "$VENV_DIR/Scripts/activate" ]; then
        source "$VENV_DIR/Scripts/activate"
    else
        echo -e "${RED}Virtual environment activation file not found.${NC}"
        return 1
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Virtual environment activated successfully.${NC}"
        echo -e "${YELLOW}Virtual environment info:${NC}"
        python --version
        pip --version
        return 0
    else
        echo -e "${RED}Error activating virtual environment.${NC}"
        return 1
    fi
}

# Install dependencies
install_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo -e "${YELLOW}Upgrading pip...${NC}"
        pip install --upgrade pip
        
        echo -e "${YELLOW}Installing dependencies from $REQUIREMENTS_FILE...${NC}"
        pip install -r "$REQUIREMENTS_FILE"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Dependencies installed successfully.${NC}"
            return 0
        else
            echo -e "${RED}Error installing dependencies.${NC}"
            echo -e "${YELLOW}Attempting to install core dependencies individually...${NC}"
            pip install Django djangorestframework djangorestframework-simplejwt drf-yasg django-environ django-cors-headers whitenoise itsdangerous celery redis django-celery-results python-dotenv django-extensions Pillow
            return $?
        fi
    else
        echo -e "${YELLOW}$REQUIREMENTS_FILE not found. Installing core packages...${NC}"
        pip install Django djangorestframework djangorestframework-simplejwt drf-yasg django-environ django-cors-headers whitenoise itsdangerous celery redis django-celery-results python-dotenv django-extensions Pillow
        return $?
    fi
}

# Check Django project
check_django_project() {
    echo -e "${BLUE}Checking Django project...${NC}"
    if [ -d "$DJANGO_PROJECT_DIR" ]; then
        echo -e "${GREEN}Django project found at $DJANGO_PROJECT_DIR.${NC}"
        
        # Check manage.py
        if [ -f "$DJANGO_PROJECT_DIR/manage.py" ]; then
            echo -e "${GREEN}manage.py found.${NC}"
        else
            echo -e "${RED}manage.py not found in $DJANGO_PROJECT_DIR.${NC}"
            return 1
        fi
        
        # Check settings module
        if [ -d "$DJANGO_PROJECT_DIR/MovieSeries/settings" ]; then
            echo -e "${GREEN}Settings directory found.${NC}"
            
            # Check development settings
            if [ -f "$DJANGO_PROJECT_DIR/MovieSeries/settings/dev.py" ]; then
                echo -e "${GREEN}Development settings found.${NC}"
            else
                echo -e "${RED}Development settings not found.${NC}"
                return 1
            fi
        else
            echo -e "${RED}Settings directory not found.${NC}"
            return 1
        fi
        
        return 0
    else
        echo -e "${RED}Django project not found at $DJANGO_PROJECT_DIR.${NC}"
        return 1
    fi
}

# Run database migrations
run_migrations() {
    echo -e "${BLUE}Running database migrations...${NC}"
    cd $DJANGO_PROJECT_DIR
    
    echo -e "${YELLOW}Making migrations...${NC}"
    python manage.py makemigrations
    
    echo -e "${YELLOW}Applying migrations...${NC}"
    python manage.py migrate
    
    cd ..
    echo -e "${GREEN}Migrations completed.${NC}"
    return 0
}

# Start Celery server
start_celery() {
    echo -e "${BLUE}Starting Celery server...${NC}"
    cd $DJANGO_PROJECT_DIR
    
    # Check for celery.py file
    if [ -f "MovieSeries/celery.py" ]; then
        echo -e "${GREEN}celery.py file found.${NC}"
        
        # Set environment variables
        export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
        echo -e "${YELLOW}Django settings: $DJANGO_SETTINGS_MODULE${NC}"
        
        # Kill any running Celery processes
        pkill -f 'celery worker' || true
        
        # Run Celery with debug
        celery -A MovieSeries worker -l info &
        CELERY_PID=$!
        echo -e "${GREEN}Celery server started with PID $CELERY_PID.${NC}"
    else
        echo -e "${RED}celery.py file not found.${NC}"
        cd ..
        return 1
    fi
    
    cd ..
    return 0
}

# Start Django server
start_django() {
    echo -e "${BLUE}Starting Django server...${NC}"
    cd $DJANGO_PROJECT_DIR
    
    # Set environment variables
    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    echo -e "${YELLOW}Django settings: $DJANGO_SETTINGS_MODULE${NC}"
    
    # Run collectstatic
    echo -e "${YELLOW}Collecting static files...${NC}"
    python manage.py collectstatic --noinput || true
    
    # Run Django development server
    echo -e "${YELLOW}Starting Django development server...${NC}"
    python manage.py runserver
    
    cd ..
    return 0
}

# Cleanup function
cleanup() {
    echo -e "${YELLOW}Cleaning up...${NC}"
    if [ ! -z "$CELERY_PID" ]; then
        echo -e "${BLUE}Stopping Celery server (PID: $CELERY_PID)...${NC}"
        kill $CELERY_PID 2>/dev/null || true
    fi
    
    # Kill any remaining Celery processes
    pkill -f 'celery worker' 2>/dev/null || true
    
    echo -e "${GREEN}Cleanup completed successfully.${NC}"
}

# Show help
show_help() {
    echo -e "${BLUE}=== Movie Series API Project Runner ===${NC}"
    echo -e "This script sets up and runs the Movie Series API project."
    echo -e ""
    echo -e "Usage:"
    echo -e "  ${YELLOW}./run_project.sh${NC}             - Set up environment and run the project"
    echo -e "  ${YELLOW}./run_project.sh help${NC}        - Show this help message"
    echo -e "  ${YELLOW}./run_project.sh setup${NC}       - Only set up the environment"
    echo -e "  ${YELLOW}./run_project.sh django${NC}      - Only start the Django server"
    echo -e "  ${YELLOW}./run_project.sh celery${NC}      - Only start the Celery worker"
    echo -e "  ${YELLOW}./run_project.sh migrate${NC}     - Only run database migrations"
    echo -e "  ${YELLOW}./run_project.sh test${NC}        - Only test email sending"
    echo -e ""
    echo -e "Environment:"
    echo -e "  ${YELLOW}DJANGO_SETTINGS_MODULE${NC}       - Django settings module (default: $DJANGO_SETTINGS_MODULE)"
    echo -e ""
}

# Test direct email sending
test_email() {
    echo -e "${BLUE}Testing direct email sending...${NC}"
    cd $DJANGO_PROJECT_DIR
    
    # Set environment variables
    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    echo -e "${YELLOW}Django settings: $DJANGO_SETTINGS_MODULE${NC}"
    
    # Run Django shell with a test script
    echo -e "${YELLOW}Running email test script...${NC}"
    python -c "
from django.core.mail import send_mail
from django.conf import settings

print('Email settings:')
print(f'EMAIL_HOST: {settings.EMAIL_HOST}')
print(f'EMAIL_PORT: {settings.EMAIL_PORT}')
print(f'EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
print(f'EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}')
print(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
print(f'EMAIL_BACKEND: {settings.EMAIL_BACKEND}')

try:
    print('Sending test email...')
    success = send_mail(
        'Test Email from Django',
        'This is a test email from your Django application.',
        settings.EMAIL_HOST_USER,
        ['${TEST_EMAIL:-tkiew32@gmail.com}'],  # Use provided email or default
        fail_silently=False,
    )
    if success:
        print('Email sent successfully!')
    else:
        print('Email sending failed.')
except Exception as e:
    print(f'Error: {str(e)}')
"
    
    cd ..
    return 0
}

# Main function
main() {
    # Handle command line arguments
    case "$1" in
        help)
            show_help
            return 0
            ;;
        setup)
            # Only set up environment
            check_venv || exit 1
            activate_venv || exit 1
            install_dependencies || exit 1
            check_django_project || exit 1
            check_redis || exit 1
            echo -e "${GREEN}Setup completed successfully.${NC}"
            return 0
            ;;
        django)
            # Only start Django server
            activate_venv || exit 1
            check_django_project || exit 1
            start_django
            return 0
            ;;
        celery)
            # Only start Celery worker
            activate_venv || exit 1
            check_django_project || exit 1
            check_redis || exit 1
            start_celery
            return 0
            ;;
        migrate)
            # Only run migrations
            activate_venv || exit 1
            check_django_project || exit 1
            run_migrations
            return 0
            ;;
        test)
            # Only test email 
            activate_venv || exit 1
            check_django_project || exit 1
            TEST_EMAIL="$2"  # Get optional email argument
            test_email
            return 0
            ;;
        *)
            # Full setup and run
            echo -e "${BLUE}=== Starting Movie Series API Project ===${NC}"
            
            # Register cleanup function to run on exit
            trap cleanup EXIT
            
            # Set up environment
            check_venv || exit 1
            activate_venv || exit 1
            install_dependencies || exit 1
            check_django_project || exit 1
            check_redis || exit 1
            
            # Run migrations
            run_migrations || exit 1
            
            # Start Celery
            start_celery || exit 1
            
            # Start Django server
            start_django
            ;;
    esac
}

# Run main function with all arguments passed to the script
main "$@"