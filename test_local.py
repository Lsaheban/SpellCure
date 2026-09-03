import sys
import os

# Ensure we can import SpellCure from the current directory
sys.path.append(os.path.join(os.path.dirname(__file__), "SpellCure"))

try:
    from SpellCure import SpellCure
except ImportError:
    # If running from inside SpellCure dir or if package is installed differently
    try:
        from .corrector import SpellCure
    except ImportError:
        # Fallback for direct execution
        sys.path.append(os.getcwd())
        from SpellCure import SpellCure

def test_spellcure():
    print("Testing SpellCure Library...")
    
    # Test 1: Small Mode (Default)
    print("\n[Test 1] Testing 'small' mode (built-in vocabulary)...")
    try:
        corrector = SpellCure(mode="small")
        # Test a simple sentence
        input_text = "ths si a tset strng"
        expected_output = "this is a test strong" # 'strong' or string? 'strng' -> 'strong' likely
        corrected = corrector.correct(input_text)
        print(f"Input:    '{input_text}'")
        print(f"Output:   '{corrected}'")
    except Exception as e:
        print(f"FAILED: {e}")

    # Test 2: Large Mode (NLTK)
    print("\n[Test 2] Testing 'large' mode (NLTK vocabulary)...")
    try:
        # Note: This might download NLTK data if not present
        corrector_large = SpellCure(mode="large")
        input_word = "aplpes balouns"
        corrected_word = corrector_large.correct(input_word)
        print(f"Input:    '{input_word}'")
        print(f"Output:   '{corrected_word}'")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_spellcure()
