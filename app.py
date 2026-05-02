import streamlit as st
import swisseph as swe
from datetime import datetime, date
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- 1. THE TEACHER'S GUIDED PRACTICE ---
TEACHER_GUIDE = {
    "Downward-Facing Dog": {
        "sanskrit": "Adho Mukha Svanasana",
        "focus": "Psoas Release (Deep Hip & Lower Back Connection)",
        "steps": [
            "Start on your hands and knees.",
            "Tuck your toes and lift your hips high.",
            "Press through your palms.",
            "Pedal your feet to stretch the calves.",
            "Let your head hang heavy.",
        ],
    },
    "Mountain Pose": {
        "sanskrit": "Tadasana",
        "focus": "Heart Center & Posture",
        "steps": [
            "Stand tall with feet rooted.",
            "Roll your shoulders back and down.",
            "Palms face forward.",
            "Reach the crown of your head to the sky.",
        ],
    },
    "Bridge Pose": {
        "sanskrit": "Setu Bandhasana",
        "focus": "Nervous System & Digestion",
        "steps": [
            "Lie on your back, knees bent.",
            "Press feet down and lift your hips.",
            "Interlace hands beneath you if possible.",
            "Breathe into the belly.",
        ],
    },
    "Crow Pose": {
        "sanskrit": "Bakasana",
        "focus": "Mental Focus & Wrist Strength",
        "steps": [
            "Squat low, hands flat on the mat.",
            "Place knees against your upper arms.",
            "Lean forward, shifting weight into your hands.",
            "Lift feet one at a time.",
        ],
    },
    "Forearm Stand": {
        "sanskrit": "Pincha Mayurasana",
        "focus": "Perspective Shift & Blood Flow",
        "steps": [
            "Forearms down, elbows shoulder-width apart.",
            "Lift hips and walk feet in toward your face.",
            "Lift one leg, then the other.",
            "Gaze softly between your arms.",
        ],
    },
    "Bound Angle Pose":
