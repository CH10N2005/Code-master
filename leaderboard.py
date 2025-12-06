import json
import os
from datetime import datetime

LEADERBOARD_FILE = "leaderboard.json"

def save_score(player_name, score, total_questions):
    """
    Save player score to leaderboard file
    Uses JSON file storage (File I/O)
    """
    # Calculate percentage
    percentage = (score / total_questions) * 100
    
    # score entry dictionary
    score_entry = {
        "name": player_name,
        "score": score,
        "total": total_questions,
        "percentage": round(percentage, 2),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Load existing scores
    scores = load_scores()
    
    # Add new score
    scores.append(score_entry)
    
    # Sort by score (highest first) - SORTING ALGORITHM
    scores.sort(key=lambda x: x["percentage"], reverse=True)
    
    # Keep only top 10 - LIST SLICING
    scores = scores[:10]
    
    # Save to file
    try:
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(scores, f, indent=4)
        print(f"Score saved for {player_name}")
        return True
    except Exception as e:
        print(f"Error saving score: {e}")
        return False

def load_scores():
    """
    Load scores from leaderboard file
    Returns empty list if file doesn't exist
    """
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            scores = json.load(f)
        return scores
    except Exception as e:
        print(f"Error loading scores: {e}")
        return []

def get_leaderboard_text():
    """
    Get formatted leaderboard text for display
    """
    scores = load_scores()
    
    if not scores:
        return "No scores yet!\nBe the first to play!"
    
    leaderboard_text = "🏆 TOP 10 LEADERBOARD 🏆\n\n"
    
    for i, score in enumerate(scores, 1):
        leaderboard_text += f"{i}. {score['name']} - "
        leaderboard_text += f"{score['score']}/{score['total']} "
        leaderboard_text += f"({score['percentage']}%)\n"
        leaderboard_text += f"   {score['date']}\n\n"
    
    return leaderboard_text

def clear_leaderboard():
    """
    Clear all scores (for testing purposes)
    """
    try:
        if os.path.exists(LEADERBOARD_FILE):
            os.remove(LEADERBOARD_FILE)
        print("Leaderboard cleared")
        return True
    except Exception as e:
        print(f"Error clearing leaderboard: {e}")
        return False