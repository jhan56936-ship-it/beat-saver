# MediaPipe Data Flow: From Camera to Screen

When you play the game, here is how the magic happens behind the scenes, step by step:

1. **Camera Input (The Eyes):** Your computer's webcam captures a constant stream of video showing your body in real-time.
2. **Landmark Detection (The Brain):** The MediaPipe AI engine (`HandLandmarker` and `FaceLandmarker`) analyzes every single frame of this video. It instantly pinpoints the precise 3D coordinates (x, y, z) of 21 key points on each of your hands and the tip of your nose.
3. **Data Calculation (The Math):** The game takes these raw coordinates and calculates important information:
   - Where are your hands and head located in the game's 3D world?
   - How fast are your hands moving (Velocity)?
   - At what angle are your hands pointing (3D Quaternion Direction)?
4. **Hit Detection (The Judge):** Every fraction of a second, the game checks if your calculated hand positions overlap with any incoming 3D blocks. If there's a collision, it compares your swing's speed and angle against the block's required direction to determine your score (Perfect, Great, Miss). It also checks if your head position overlaps with a red wall to apply damage.
5. **State Update (The Rules):** Based on the judge's decision, the game updates your current state: increasing your score and combo on a hit, or slashing your health and resetting your combo if you hit a bomb or a wall.
6. **Screen Rendering (The Show):** Finally, the Three.js graphics engine takes all this updated information and draws the next frame on your monitor. You see the sabers perfectly mimicking your real hands, slicing blocks in half, triggering neon explosions, and making the screen shake—all happening 60 times every single second!

---

# 🎙️ Q&A 예상 트러블슈팅 가이드

발표 후 나오기 쉬운 질문 3가지와 핵심 답변입니다.

**Q1. 카메라(웹캠) 인식 속도가 느리거나 버벅일 때는 어떻게 헸나요?**
> A. MediaPipe 초기화 시 기본적으로 GPU(그래픽 카드) 가속을 사용하도록 설정했습니다. 만약 사용자 환경에서 GPU 지원이 안 되면 자동으로 CPU 모드로 전환되는 예외 처리(Fallback) 코드를 작성하여 튕기지 않고 안정적으로 돌아가도록 해결했습니다.

**Q2. 음악에 맞춰 맵을 생성할 때 빡빡하거나 너무 쉽지는 않나요? (난이도)**
> A. Web Audio API로 비트를 추출한 뒤, 선택한 난이도(EASY/NORMAL/HARD)에 따라 생성된 노트들을 무작위로 솎아내는(Skip chance) 확률 모델을 적용했습니다. 하드 모드에서는 추출된 비트에 거의 다 노트가 배치되지만, 이지 모드에서는 65% 이상을 솎아내어 여유롭게 즐길 수 있도록 밸런스를 맞췄습니다.

**Q3. '내려치기' 같은 타격 판정은 정확하게 어떻게 계산하나요? 진짜 칼싸움 같나요?**
> A. 처음에는 단순히 '손목의 기울어진 각도'만 체크했더니 타격감이 답답했습니다. 그래서 이를 개선하여 현재는 '손바닥의 순간 이동 방향 벡터(Velocity)'와 '손목-손끝의 3D 쿼터니언 회전 각도', 그리고 '날아오는 블록과의 Z축 타이밍 거리' 이 3가지를 가중치를 두어 종합 평가(calcScore)하도록 로직을 설계했습니다. 덕분에 궤적에 맞춰 시원하게 휘두르기만 해도 부드럽게 타격이 인정됩니다.

---

# 📸 발표 화면 및 코드 근거 자료 준비 가이드

각 질문과 기술 어필 포인트에 맞춰 아래의 화면과 코드 위치를 캡처하여 발표 자료(PPT 등)에 추가하세요.

**1. AI 모션 인식 엔진 (MediaPipe Tracking)**
- **화면 캡처:** 웹캠 권한 허용 후 얼굴(코)과 손에 랜드마크 점이 인식되어 있는 실제 플레이 화면
- **코드 위치 (`index.html`):** 
  - `initMediaPipe()` 함수 (약 880번 줄): `HandLandmarker`와 `FaceLandmarker`를 비전 모델로 가져오고 GPU/CPU Fallback을 처리하는 부분
  - `detectLoop()` 내의 얼굴 추적 로직 (약 940번 줄): `f.faceLandmarks[0][1]`(코)의 좌표를 가져와 `headPos`를 계산하는 부분

**2. 자동 맵 생성기 (Procedural Beatmap Generator)**
- **화면 캡처:** "PLAY CUSTOM MAP" 버튼이 눌리기 전, 오디오 파일을 업로드하고 맵이 즉시 생성되는 'Setup Panel' 화면
- **코드 위치 (`index.html`):**
  - `extractBeatsAsync` 함수 (약 1500번 줄 후반): Web Audio API로 AudioBuffer를 순회하며 진폭(Amplitude) 피크점을 찾아 비트를 배열에 담는 핵심 수학 로직
  - `beats.forEach` 안의 맵 생성 로직 (약 1600번 줄 후반): `Math.random()`과 `diffConfig.skipChance`를 사용해 함정(Wall/Bomb)과 일반 노트를 확률적으로 섞는 부분

**3. '내려치기' 등 3D 타격 판정 및 회피 시스템**
- **화면 캡처:** 
  - 양옆의 빨간 벽(Wall)을 피해 몸을 숙이는 게임 화면 (시각적 임팩트)
  - 칼을 크게 휘둘러 "PERFECT"와 거대한 노란 점수가 뜬 찰나의 화면 (타격감 어필)
- **코드 위치 (`index.html`):**
  - `checkHit(block)` 내의 벽/폭탄 충돌 로직: 헤드 포지션(`hx`)이 벽 안에 들어갔는지 계산하고 `health`를 깎는 부분
  - `calcScore(block)` 함수 (약 1150번 줄): `speed > 0.005`일 때 속도 벡터(Velocity)와 손목 회전(Angle)을 종합(Combined)하여 등급과 색상을 반환하는 하이브리드 수식

**4. 3D 그래픽 및 구조물 렌더링 (Three.js)**
- **화면 캡처:** 폭탄을 잘못 베었을 때 폭발하는 파티클(Particle) 효과나, 블록이 산산조각 나는 화면
- **코드 위치 (`index.html`):** 
  - `makeBlock(block)` 내 `bomb` 타입 렌더링 (약 820번 줄): 기본 입방체(Icosahedron)에 `ConeGeometry` 가시를 덧붙이는 3D 수학적 공간 배치 부분
