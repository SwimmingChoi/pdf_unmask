# PDF 마스킹 제거

PDF의 강조, 사각형 주석, 적용 전 교정(Redact) 표시를 제거한 사본을 만듭니다.
원본은 유지되며 같은 폴더에 `<원래이름>_마스킹제거.pdf`로 저장됩니다.
이미 적용된 교정으로 삭제된 내용은 복원할 수 없습니다.

## Windows 실행파일 다운로드

GitHub에 푸시할 때마다 Windows x64 실행파일을 자동 빌드합니다.

1. [Actions → Build Windows EXE](https://github.com/SwimmingChoi/pdf_unmask/actions/workflows/build-windows.yml)로 이동합니다.
2. 초록색 체크 표시로 완료된 실행을 엽니다.
3. 페이지 아래 **Artifacts**에서 **PDF-unmask-Windows-x64**를 다운로드합니다. GitHub 로그인이 필요합니다.
4. ZIP 파일을 풀고 `PDF마스킹제거.exe`를 실행합니다. Python 설치는 필요하지 않습니다.

빌드 결과는 30일간 보관합니다. Actions의 **Run workflow**로 수동 빌드도 가능합니다.

## 사용법

- PDF 파일 또는 폴더를 exe 위로 끌어다 놓습니다. 여러 개도 가능합니다.
- exe를 직접 실행하면 처리할 폴더를 선택할 수 있습니다.
- 폴더의 PDF만 처리하며 하위 폴더와 이미 생성된 결과 파일은 건너뜁니다.

## 직접 빌드

Windows에 Python 3.12를 설치한 뒤 `build.bat`를 실행합니다.
완성된 파일은 `dist/PDF마스킹제거.exe` 경로에 생성됩니다.
