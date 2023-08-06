import sys
import platform
sys_str = platform.uname().system
if sys_str == "Window":
    print(999)
else:
    raise SystemError(f"The current operating system is {sys_str}, Please contact the developer.")