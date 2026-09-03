
import sys
import os
import traceback

# Increase recursion depth
sys.setrecursionlimit(20000)

def generate_verbs():
    print("Starting verb generation process...")
    results = {}
    
    # Setup NLTK paths
    import nltk
    nltk.data.path.append(os.path.join(os.path.expanduser('~'), 'nltk_data'))
    nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))
    
    candidate_words = set()

    # 1. Load from WordNet
    try:
        from nltk.corpus import wordnet as wn
        print("Loading from WordNet...")
        try:
            wn_verbs = set(l.name() for s in wn.all_synsets('v') for l in s.lemmas())
            single_word_verbs = {v for v in wn_verbs if '_' not in v}
            candidate_words.update(single_word_verbs)
            print(f"Added {len(single_word_verbs)} verbs from WordNet.")
        except Exception:
            print("WordNet lookup failed (possibly data missing).")
            # Try downloading if missing
            try:
                nltk.download('wordnet', quiet=True)
                nltk.download('omw-1.4', quiet=True)
                wn_verbs = set(l.name() for s in wn.all_synsets('v') for l in s.lemmas())
                candidate_words.update({v for v in wn_verbs if '_' not in v})
                print(f"Added {len(candidate_words)} verbs after download.")
            except:
                pass
    except Exception as e:
        print(f"NLTK WordNet error: {e}")

    # 2. Load from sklib
    try:
        sys.path.append(os.path.dirname(__file__))
        from sklib import mylib
        print(f"Loading {len(mylib)} words from sklib...")
        candidate_words.update(mylib)
    except Exception as e:
        print(f"Could not load sklib: {e}")

    # 3. Load from NLTK Words (if available)
    try:
        from nltk.corpus import words
        print("Loading from NLTK Words...")
        try:
             w_list = set(words.words())
             candidate_words.update(w_list)
             print(f"Total candidates now: {len(candidate_words)}")
        except LookupError:
             print("Downloading words corpus...")
             nltk.download('words', quiet=True)
             w_list = set(words.words())
             candidate_words.update(w_list)
             print(f"Total candidates after download: {len(candidate_words)}")
    except Exception as e:
        print(f"NLTK Words error: {e}")

    print(f"Total unique candidate words to process: {len(candidate_words)}")
    
    # Filter for Verbs using lemminflect or heuristics
    # Since we can't easily check IS_VERB without context, we will try to get VBD/VBN. 
    # If lemminflect returns None or same as noun input, it might not be a verb.
    # Actually lemminflect returns tuples.
    
    try:
        import lemminflect
        from lemminflect import getInflection
        HAS_LEMMINFLECT = True
        print("Using lemminflect to filter and conjugate...")
    except ImportError:
        HAS_LEMMINFLECT = False
        print("lemminflect missing. Cannot filter accurately. Will conjugate all candidates (heuristic).")

    final_verbs = {}
    
    count = 0
    for word in candidate_words:
        if not word.isalpha(): continue # Skip numbers, punctuation
        word = word.lower()
        
        past = ""
        pp = ""
        
        if HAS_LEMMINFLECT:
            # Check if it has a verb form
            vbd = getInflection(word, tag='VBD')
            vbn = getInflection(word, tag='VBN')
            
            if vbd: past = vbd[0]
            if vbn: pp = vbn[0]
            
            # Heuristic: If lemminflect returns something valid, we assume it can be a verb.
            # However, lemminflect might return forms for nouns if forced? 
            # getInflection usually returns () if not found for that POS? 
            # Actually getInflection returns a tuple, empty if unknown.
            
            if past and pp:
                final_verbs[word] = [past, pp]
        else:
            # Fallback simple rules
            if word.endswith('e'):
                final_verbs[word] = [word + 'd', word + 'd']
            else:
                final_verbs[word] = [word + 'ed', word + 'ed']

        count += 1
        if count % 10000 == 0:
            print(f"Processed {count} words...")

    print(f"Final verb count: {len(final_verbs)}")

    # Write to file
    output_path = os.path.join(os.path.dirname(__file__), 'verbs_data.py')
    print(f"Writing to {output_path}...")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Auto-generated verb forms\n")
        f.write("# Format: verb: [past, past_participle]\n\n")
        f.write(f"# Total verbs: {len(final_verbs)}\n")
        f.write("VERB_FORMS = {\n")
        for v in sorted(final_verbs.keys()):
            forms = final_verbs[v]
            f.write(f'    "{v}": ["{forms[0]}", "{forms[1]}"],\n')
        f.write("}\n")
    print("Done.")

if __name__ == "__main__":
    generate_verbs()
