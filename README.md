# NOVA

NOVA is an adaptive assistive platform designed for children with neurodevelopmental disorders such as Autism Spectrum Disorder (ASD), ADHD and Down Syndrome.

The objective of the project is to create an intelligent system capable of adapting both communication style and interactive activities according to the child's emotional state and long-term progress.

## Features

- 🎥 Real-time face detection
- 😊 Real-time emotion recognition using TensorFlow Lite
- 🧠 Adaptive communication difficulty system
- 🎮 Adaptive mini-games
- 📈 Dynamic score management
- 🔄 Automatic game difficulty adjustment
- 🖥️ Modular software architecture

## Current Architecture

```
NOVA
│
├── vision/
│   ├── Camera
│   ├── FaceDetector
│   ├── EmotionDetector
│   └── VisionModule
│
├── difficulty/
│   └── DifficultyManager
│
├── games/
│   ├── GameManager
│   └── DinoGame
│
└── app.py
```

## Difficulty System

The project uses two independent adaptive systems.

### Communication Difficulty

Communication complexity is adjusted according to the user's emotional state.

- Happy for a sustained period → increase communication complexity.
- Sad or Angry for a sustained period → reduce communication complexity.

The final version will support multiple communication levels, ranging from image-assisted communication to fully verbal interaction.

### Game Difficulty

Game difficulty is independent from communication difficulty.

Difficulty changes are based on the player's performance score.

Current implementation contains three levels:

- Level 1
    - Slow speed
    - One obstacle

- Level 2
    - Medium speed
    - Two obstacles

- Level 3
    - High speed
    - Three simultaneous obstacles

## Vision Module

The emotion recognition pipeline consists of:

- Camera capture
- Face detection (OpenCV Haar Cascade)
- Face preprocessing
- TensorFlow Lite CNN inference
- Emotion classification

Current emotions:

- Happy
- Sad
- Angry
- Neutral
- Fear
- Surprise
- Disgust

## Games

The first implemented game is a simple endless runner inspired by the Chrome Dino Game.

The purpose of this game is not therapeutic by itself. It serves as a sandbox for validating:

- score management
- adaptive difficulty
- emotion integration
- future communication adaptation

## Technologies

- Python
- OpenCV
- TensorFlow Lite
- Pygame
- NumPy

## Future Work

- Emotion-aware communication assistant
- Image-assisted communication levels
- Multiple therapeutic games
- User profiles
- Progress tracking
- Achievement system
- Data logging
- Custom emotion recognition model
- Raspberry Pi deployment
- ESP32 companion device
- Voice interaction
- AI conversational assistant

## Status

🚧 Work in Progress

This repository is under active development as part of the NOVA adaptive assistive platform.