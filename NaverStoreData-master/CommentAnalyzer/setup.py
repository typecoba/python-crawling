from cx_Freeze import setup, Executable
import sys

# 패키지 추가 및 제외
buildOptions = dict(packages = ["wordcloud", "idna","re","sys","os", "jpype", "konlpy", "matplotlib", "macholib", "numpy", "pandas", "requests", "simplejson", "urllib3", "sqlite3", "wx"],
                    excludes = ["tkinter", "PyQt4.QtSql"],
                    # 워드클라우드 관련 파일 추가
                    zip_includes = [(r'C:\CommentAnalysis\venv\Lib\site-packages\wordcloud\stopwords', 'wordcloud/stopwords'),
                                    (r'C:\CommentAnalysis\venv\Lib\site-packages\wordcloud\DroidSansMono.ttf', 'wordcloud/DroidSansMono.ttf')]

)

# 개발 환경 정의
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# exe 실행시 동작될 py파일
exe = [Executable("mainGUI.py", base=base)]

# build 관련 설정
setup(
    name='CommentAnalyzer',
    version = '0.1',
    author = "IML",
    description = "I'M IML!",
    options = dict(build_exe = buildOptions),
    executables = exe
)