from cx_Freeze import setup, Executable

# Define your script and options
setup(
    name="MyApplication",
    version="1.0",
    description="My Python Application",
    executables=[
        Executable(
            "scratch.py",
            base="Win32GUI",  # This prevents a console window from appearing
            icon="icon.ico"  # Specify the path to your .ico file
        )
    ]
)
