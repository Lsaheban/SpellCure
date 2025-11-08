<<<<<<< HEAD
# spellcure

SpellCure — a correction engine for highly scrambled text (by Saheban Khan).  
It matches distorted or jumbled words to their most likely real forms using ratio-based scoring and NLTK word datasets.

---

## 🧠 How it Works
SpellCure compares each input token to words in its vocabulary using a position-based ratio algorithm.  
The algorithm calculates similarity between character positions and recursively refines results until a confident match is found.
## EXAMPLE
from spellcure import SpellCure

# Use small built-in vocabulary
model = SpellCure(mode="small")
print(model.correct("ths si a tset"))
# Output: this is a test

# Use NLTK's large vocabulary
model = SpellCure(mode="large")
print(model.correct("aplpe"))
# Output: apple

---

## ⚙️ Installation
```bash
pip install spellcure


Install
=======
# SpellCure
its spelling correction engine works only with mathematical algorithm to identify the correct word or possible words for  highly scrambled text 
>>>>>>> fd15c3e21c8c55f84a6258331221fb9bdf762083

