init -999 python:
    import subprocess
    import os
    import ctypes

    def minimize_ddlc():
        hwnd = ctypes.windll.user32.FindWindowW(None, "DDLC")
        if not hwnd:
            hwnd = ctypes.windll.user32.FindWindowW(None, "Monika After Story")
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 6) # SW_MINIMIZE = 6

    def run_glitch_music():
        submod_dir = os.path.join(config.basedir, "game", "Submods", "glitch_music")
        bat_path = os.path.join(submod_dir, "run.bat")
        
        if os.path.exists(bat_path):
            minimize_ddlc()
            try:
                subprocess.Popen(['cmd', '/c', bat_path], cwd=submod_dir)
            except Exception:
                pass

init 5 python:
    try:
        addEvent(
            Event(
                persistent.event_database,
                eventlabel="glitch_music_feature",
                category=['uncategorized'],
                prompt="Glitch Music Experience",
                random=False,
                unlocked=True
            )
        )
    except Exception:
        pass

# Định nghĩa tổ hợp biểu cảm yandere cường độ cao (nếu dùng chung với các asset tùy chỉnh)
image monika 2fua_custom = ConditionSwitch(
    "True", "mod_assets/sprite/monika/2fua_custom.png", # Hoặc gọi các mã sprite mở rộng của bạn
    "True", "m 2fua"
)

label glitch_music_feature:
    # Sử dụng các mã biểu cảm yandere sâu sắc nhất
    m 2dfp "You think you can escape my sight just by minimizing the window...?"
    m 2gkp "Every second you look away, I'm watching right behind your screen."
    m 2fua "Let's see where you can run when your entire desktop belongs to me."
    
    python:
        run_glitch_music()
    
    $ renpy.pause(0.5)
    
    m 2fua "Did you enjoy having my eyes locked onto you the whole time, [player]...?"
    m 2gkp "There's nowhere on your screen you can hide from me. Ehehe~"
    
    return