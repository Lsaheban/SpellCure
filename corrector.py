import nltk
from nltk.data import find

# Auto-download 'words' corpus if missing
try:
    find("corpora/words")
except LookupError:
    print("[INFO] Downloading NLTK 'words' corpus...")
    nltk.download("words", quiet=True)

from nltk.corpus import words
from .sklib import mylib


class SpellCure:
    def __init__(self, mode="small", custom_vocab=None):
        """
        Initialize the SpellCure engine.

        Parameters
        ----------
        mode : str
            "small" (default) for built-in word list, or "large" for nltk words corpus.
        custom_vocab : list[str] or None
            If provided, uses your own vocabulary list instead of built-in ones.
        """

        # Store common words set for scoring boost later
        self.common_set = set(mylib)

        if custom_vocab:
            self.lis = list(set(custom_vocab))
        elif mode == "large":
            print("[INFO] Using NLTK large vocabulary...")
            # MERGE: Combine NLTK words + sklib common words to ensure common words are present
            # Filtering NLTK to unique set first
            nltk_words = set(words.words())
            self.lis = list(nltk_words.union(self.common_set))
        else:
            # Saheban’s default mini vocab list
            self.lis = list(mylib)

        print(f"[INFO] Vocabulary loaded with {len(self.lis)} words.")

    # ========================
    # INTERNAL HELPER METHODS
    # ========================
    def _tor(self, x, candidates):
        len_in = len(x)
        lez = list(x)
        w_len = len(candidates)
        pul = []
        
        for it in range(w_len):
            kup = list(candidates[it])
            len_kup = len(kup)
            sol = []
            
            # Map of char -> list of indices in candidate for O(1) lookup
            target_indices = {}
            for idx, char in enumerate(kup):
                if char not in target_indices:
                    target_indices[char] = []
                target_indices[char].append(idx)
            
            max_len = max(len_in, len_kup)
            
            for i in range(len_in):
                char = lez[i]
                if char in target_indices:
                    # Find the index in candidate closest to i
                    best_j = min(target_indices[char], key=lambda k: abs(k - i))
                    
                    # New Math: Linear Distance Penalty
                    dist_score = 1.0 - (abs(best_j - i) / max_len)
                    sol.append(dist_score)
            
            if sol:
                # Average score of matched characters
                pul.append(sum(sol) / len_in)
            else:
                pul.append(0)
        return pul, len_in, lez, w_len

    def _mon(self, len_in, lez, w_len, candidates):
        avl_w = []
        for it in range(w_len):
            sup = list(candidates[it])
            lol = 0
            for i in range(len_in):
                if lez[i] in sup:
                    sup.remove(lez[i])
                    lol += 1
            avl_w.append(lol)
        return avl_w

    def _don(self, pul, len_in, avl_w, candidates):
        tel = []
        w_len = len(candidates)
        for l in range(w_len):
            cand_word = candidates[l]
            jen = len(cand_word)
            
            # Component 1: Position Score
            my = pul[l] 
            
            # Component 2: Presence Score
            sk = (avl_w[l] / len_in) 
            
            # Component 3: Length Similarity
            dx = min(len_in, jen) / max(len_in, jen)
            
            # WEIGHTED AVERAGE
            # Prioritize character presence (sk) and position (my)
            raw_score = (my * 1.0 + sk * 1.2 + dx * 0.8) / 3.0
            
            # BONUS: Common Word Boost (+0.1)
            if cand_word in self.common_set:
                raw_score += 0.1
                
            tel.append(raw_score)
        return tel

    def _race(self, tel, candidates, min_val=0.0):
        # Return top matches sorted by score
        scored_candidates = []
        for j, score in enumerate(tel):
            if score > 0.6: # Filter low quality matches
                scored_candidates.append((score, candidates[j]))
        
        # Sort descending by score
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        
        # Return top 3 unique words
        seen = set()
        result = []
        for score, word in scored_candidates:
            if word not in seen:
                result.append(word)
                seen.add(word)
            if len(result) >= 3:
                break
                
        return result or ["<no match>"]

    # ========================
    # PUBLIC METHOD
    # ========================
    def correct(self, text):
        """
        Correct a single word or full sentence.
        Returns the best guesses for each token.
        """
        words_input = text.strip().lower().split()
        results = []
        for w in words_input:
            # OPTIMIZATION: Filter candidates by length (length +/- 2)
            w_len_val = len(w)
            candidates = [word for word in self.lis if abs(len(word) - w_len_val) <= 2]
            
            if not candidates:
                candidates = self.lis

            pul, len_in, lez, w_len = self._tor(w, candidates)
            avl_w = self._mon(len_in, lez, w_len, candidates)
            tel = self._don(pul, len_in, avl_w, candidates)
            matches = self._race(tel, candidates)
            results.append("/".join(matches))
        return " ".join(results)
