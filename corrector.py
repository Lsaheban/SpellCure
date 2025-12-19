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


class corrector:
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

        if custom_vocab:
            self.lis = list(set(custom_vocab))
        elif mode == "large":
            print("[INFO] Using NLTK large vocabulary...")
            self.lis = list(set(words.words()))
        else:
            # Saheban’s default mini vocab list
            self.lis = list(mylib)

        print(f"[INFO] Vocabulary loaded with {len(self.lis)} words.")

    # ========================
    # INTERNAL HELPER METHODS
    # ========================
    def _tor(self, x):
        len_in = len(x)
        lez = list(x)
        w_len = len(self.lis)
        sol = []
        pul = []
        for it in range(w_len):
            kup = list(self.lis[it])
            for i in range(len_in):
                if lez[i] in kup:
                    cal = kup.index(lez[i]) + 1
                    rc = i + 1
                    sol.append(rc / cal if rc < cal else cal / rc)
            if sol:
                pul.append(sum(sol) / len_in)
                sol.clear()
            else:
                pul.append(0)
        return pul, len_in, lez, w_len

    def _mon(self, len_in, lez, w_len):
        avl_w = []
        for it in range(w_len):
            sup = list(self.lis[it])
            lol = 0
            for i in range(len_in):
                if lez[i] in sup:
                    sup.remove(lez[i])
                    lol += 1
            avl_w.append(lol)
        return avl_w

    def _don(self, pul, len_in, avl_w):
        tel = []
        w_len = len(self.lis)
        for l in range(w_len):
            jen = len(self.lis[l])
            my = pul[l] + 0.02
            sk = (avl_w[l] / len_in) + 0.02
            dx = (len_in / jen - 0.01) if len_in < jen else (jen / len_in - 0.02)
            resl = (dx + sk + my) / 3
            tel.append(resl)
        return tel

    def _race(self, tel, min_val=0.0):
        result = []
        for j, score in enumerate(tel):
            if score > (0.95 - min_val):
                result.append(self.lis[j])
        if not result and min_val < 0.3:
            return self._race(tel, min_val + 0.01)
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
            pul, len_in, lez, w_len = self._tor(w)
            avl_w = self._mon(len_in, lez, w_len)
            tel = self._don(pul, len_in, avl_w)
            matches = self._race(tel)
            results.append("/".join(matches))
        return " ".join(results)
