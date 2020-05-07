# Linux

## 설치

### Ubuntu on Windows 10

1. Microsoft store에서 ubuntu를 검색하여 설치

   ```
   C:\Users\사용자명\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu20.04onWindows_79rhkp1fndgsc\LocalState\rootfs
   ```

2. 0X8007019e 에러 발생 시 windows powershell 관리자권한으로 다음 실행 및 재부팅

   ```
   Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
   ```

3. 계정설정 후 패키지 업데이트

   ```
   sudo apt-get update
   ```

   