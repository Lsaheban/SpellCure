"""
spellcure.corrector
-------------------
Saheban Khan's original spelling correction engine — refactored into a class.
Retains ratio-based probability logic and recursive refinement system.
"""
import nltk
from nltk.data import find

# Auto-download 'words' corpus if missing
try:
    find("corpora/words")
except LookupError:
    print("[INFO] Downloading NLTK 'words' corpus...")
    nltk.download("words", quiet=True)

from nltk.corpus import words


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

        if custom_vocab:
            self.lis = list(set(custom_vocab))
        elif mode == "large":
            print("[INFO] Using NLTK large vocabulary...")
            self.lis = list(set(words.words()))
        else:
            # Saheban’s default mini vocab list
            self.lis = list(
                set(
                    [
"a", "about", "above", "above", "across","after""afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by","bull", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon","hello","hell", "hers", "him", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itavl_wf", "keep","kill", "last", "latter", "latterly", "least", "less","loose", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myavl_wf", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ouravl_wves", "out", "over", "own","part", "per", "perhaps","place","please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themavl_wves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "shall", "the","hi","like","lie","one","two","three","moon","doing","good","think","looking","day","bought","bag","visiting","shop","I","i","today","friend","going","able", "absent", "accept", "action", "active", "actual", "advice", "affair", "afraid", "again", "age", "agree", "ahead", "aid", "aim", "air", "alert", "alive", "allow", "almost", "alone", "alongside", "already", "also", "alter", "always", "amazed", "ancient", "anger", "angle", "angry", "animal", "annual", "another", "answer", "anybody", "anyway", "apart", "appear", "apply", "approve", "area", "argue", "arise", "around", "arrange", "arrive", "article", "artist", "aside", "asked", "aspect", "assist", "assume", "assure", "attract", "audience", "author", "auto", "available", "average", "avoid", "aware", "awkward", "baby", "backed", "background", "badly", "bake", "balance", "ball", "bank", "bar", "base", "basic", "basis", "beauty", "become", "bed", "beforehand", "began", "begin", "being", "believe", "below", "belt", "bend", "beneath", "benefit", "besides", "best", "bet", "better", "between", "beyond", "bias", "big", "bill", "bind", "birth", "bit", "bite", "black", "blade", "blame", "blank", "blast", "blind", "block", "blood", "blow", "blue", "board", "boat", "body", "boil", "bold", "bomb", "bone", "book", "boot", "border", "born", "borrow", "boss", "both", "bother", "bottle", "bottom", "bound", "bow", "box", "boy", "brain", "branch", "brand", "brave", "bread", "break", "breath", "breathe", "brief", "bright", "bring", "broad", "broken", "brother", "brought", "brown", "brush", "build", "burn", "burst", "business", "busy", "but", "buy", "by", "cable", "cake", "call", "calm", "camera", "camp", "canal", "cap", "capable", "capital", "captain", "capture", "care", "careful", "cargo", "carpet", "carry", "case", "cast", "catch", "cause", "cell", "center", "central", "century", "certain", "chain", "chair", "challenge", "chance", "change", "chapter", "character", "charge", "chart", "chat", "check", "cheer", "chemical", "chest", "chief", "child", "children", "chill", "choice", "choose", "chronic", "church", "circle", "circuit", "circumstance", "city", "civil", "claim", "class", "clean", "clear", "climb", "clock", "close", "closer", "clothes", "cloud", "cluster", "coach", "coal", "coast", "coat", "code", "coffee", "cold", "collapse", "colleague", "collect", "college", "color", "column", "combine", "come", "comfort", "command", "comment", "commercial", "common", "community", "company", "compare", "compete", "complete", "complex", "compose", "concern", "conclude", "condition", "conduct", "confident", "confirm", "confuse", "connect", "consider", "consist", "constant", "construct", "consult", "consume", "contact", "contain", "content", "continue", "control", "converse", "convert", "convince", "cook", "cool", "cooperate", "cope", "copy", "core", "corner", "corporate", "correct", "cost", "cotton", "couch", "cough", "could", "council", "counsel", "count", "country", "couple", "course", "court", "cover", "cow", "crack", "craft", "cram", "crash", "crawl", "cream", "create", "credit", "crime", "crisis", "critical", "crop", "cross", "crow","crowd", "crown", "crucial", "cry", "culture", "cup", "current", "curve", "custom", "cut", "cycle", "dad", "danger", "dare", "dark", "date", "daughter", "daylight", "deal", "debate", "decade", "decide", "decision", "declare", "decline", "decorate", "dedicate", "deep", "default", "defeat", "defend", "define", "degree", "delay", "deliver", "demand", "democratic", "demonstrate", "deny", "department", "depend", "deploy", "deposit", "describe", "deserve", "design", "desire", "destroy", "detail", "determine", "develop", "device", "devote", "diagnose", "dictate", "die", "differ", "different", "difficult", "digest", "digital", "dignity", "dimension", "direct", "directory", "dirt", "disagree", "disappear", "disclose", "discuss", "disease", "dish", "dismiss", "display", "distance", "distinguish", "distribute", "district", "disturb", "diverse", "divide", "division", "dozen", "draft", "drag", "dramatic", "draw", "dream", "dress", "drink", "drive", "drop", "drought", "drug", "dry", "due", "dull", "dump", "during", "dust", "duty", "each", "eager", "ear", "early", "earn", "earth", "ease", "east", "easy", "eat", "economic", "edge", "edit", "educate", "effort", "egg", "eight", "either", "elder", "elect", "electric", "electronic", "element", "eliminate", "else", "elsewhere", "embark", "embody", "emerge", "emotion", "emphasize", "employ", "empty", "enable", "enclose", "encounter", "end", "endorse", "enemy", "energetic", "energy", "enforce", "engage", "engine", "enhance", "enjoy", "enlarge", "enough", "ensure", "enter", "entertain", "entire", "entry", "envelope", "environment", "episode", "equal", "equip", "equity", "era", "escape", "essay", "essence", "establish", "estimate", "ethics", "evaluate", "even", "event", "ever", "every", "evidence", "evil", "evolve", "examine", "example", "exceed", "excellent", "except", "exchange", "excite", "exclude", "executive", "exercise", "exhaust", "exhibit", "exist", "expand", "expect", "expense", "experience", "expert", "explain", "exploit", "explore", "export", "expose", "express", "extend", "extra", "extreme", "eye", "face", "fact", "factor", "factory", "faculty", "fade", "fail", "fair", "faith", "fall", "false", "fame", "family", "famous", "fan", "fantasy", "far", "farm", "fast", "fat", "father", "fault", "favor", "fear", "feature", "fed", "fee", "feed", "feel", "female", "fence", "few", "field", "figure", "file", "fill", "film", "final", "finance", "find", "fine", "finger", "finish", "fire", "firm", "first", "fish", "fit", "five", "fix", "flag", "flame", "flash", "flat", "flavor", "flesh", "flight", "float", "floor", "flow", "flower", "fly", "focus", "fold", "follow", "food", "foot", "football", "for", "force", "foreign", "forest", "forget", "forgive", "form", "formal", "format", "former", "formula", "forth", "fortune", "forward", "found", "four", "fox", "frame", "free", "freedom", "freeze", "French", "frequent", "fresh", "friend", "friendly", "friendship", "from", "front", "frost","frown", "fruit", "fuel", "full", "fun", "function", "fund", "funny", "furniture", "further", "future", "gain", "game", "gap", "garage", "garden", "gas", "gate", "gather", "gay", "gaze", "general", "generate", "gentle", "genuine", "geography", "get", "ghost", "giant", "gift", "girl", "give", "glad", "glass", "global", "glove", "glow", "go", "goal", "god", "gold", "golf", "good", "government", "governor", "grab", "grade", "grain", "grand", "grant", "graph", "grass", "grave", "great", "green", "groan", "ground", "group", "grow", "guarantee", "guess", "guest", "guide", "guilt", "gun", "guy", "habit", "hair", "half", "hall", "hand", "handle", "hang", "happen", "happy", "hard", "hat", "hate", "have", "he", "head", "health", "hear", "heart", "heat", "heavy", "help", "hence", "her", "here", "hero", "hides", "high", "highlight", "highway", "hill", "him", "hip", "hire", "history", "hit", "hold", "hole", "holiday", "home", "honest", "honey", "hood", "hook", "hope", "horizon", "horse", "hospital", "host", "hot", "hotel", "hour", "house", "how", "however", "huge", "human", "humble", "humor", "hundred", "hungry", "hunt", "hurry", "hurt", "husband", "hypothetical","is", "idea", "ideal", "identify", "ignore", "ill", "image", "imagine", "immediate", "imply", "import", "impose", "impossible", "impress", "improve", "in", "inch", "incident", "include", "income", "increase", "indeed", "independent", "indicate", "individual", "industry", "inevitable", "influence", "inform", "initial", "initiate", "injure", "injustice", "ink", "inner", "innocent", "input", "inquire", "insane", "inside", "insist", "inspect", "inspire", "install", "instead", "institution", "instruction", "instrument", "insult", "insurance", "intact", "intend", "intense", "interest", "interfere", "internal", "international", "interpret", "interrupt", "interview", "into", "introduce", "invent", "invest", "invite", "involve", "iron", "is", "island", "issue", "it", "item", "its", "jacket", "job", "join", "joint", "joke", "journal", "journey", "joy", "judge", "judgment", "juice", "jump", "junior", "jury", "just", "justice", "keen", "keep", "key", "kick", "kid", "kill", "kind", "king", "kiss", "kitchen", "knee", "knife", "knock", "know", "knowledge", "lab", "label", "labor", "lack", "lady", "lake", "lamp", "land", "language", "lap", "large", "last", "late", "laugh", "law", "lawyer", "lay", "layer", "lead", "leader", "leaf", "learn", "leave", "lecture", "left", "leg", "legal", "legislature", "length", "lend", "less", "lesson", "let", "letter", "level", "lie", "life", "lift", "light", "like", "likely", "limit", "line", "link", "lip", "liquid", "list", "listen", "literature", "little", "live", "load", "loan", "local", "locate", "lock", "log", "logic", "logical", "lonely", "long", "look", "loop", "lose", "loss", "lost", "lot", "loud", "love", "low", "lower", "luck","lucky", "lunch", "machine", "mad", "magazine", "magic", "maid", "mail", "main", "major", "make", "male", "mall", "man", "manage", "manner", "many", "map", "mark", "market", "marriage", "marry", "mask", "mass", "master", "match", "material", "math", "matter", "max", "maybe", "mayor", "meal", "mean", "measure", "meat", "media", "medical", "meet", "member", "memory", "mental", "menu", "mercy", "message", "metal", "method", "middle", "midnight", "milk", "mind", "mine", "minister", "minor", "minute", "miracle", "mirror", "miss", "mistake", "mix", "model", "mom", "moment", "money", "monitor", "month", "mood", "moon", "more", "morning", "mortgage", "most", "mother", "motion", "motor", "mount", "mountain", "mouse", "mouth", "move", "movie", "much", "mud", "music", "must", "mutual", "my", "mystery", "myth", "nail", "name", "nation", "native", "natural", "nature", "near", "neat", "necessary", "neck", "need", "negative", "neighbor", "neither", "nervous", "nest", "net", "network", "never", "new", "news", "next", "nice", "night", "nine", "no", "nobody", "nod", "noise", "none", "noon", "nor", "normal", "north", "nose", "not", "note", "nothing", "notice", "noun", "novel", "now", "number", "numerous", "nurse", "nut", "object", "obvious", "occur", "ocean", "odd", "offer", "office", "officer", "official", "often", "oil", "old", "olive", "on", "once", "one", "only", "open", "operate", "opinion", "opportunity", "oppose", "option", "or", "orange", "order", "ordinary", "organ", "organization", "orient", "original", "other", "others", "our", "out", "outcome", "outside", "over", "own", "owner", "pace", "pack", "page", "pain", "paint", "pair", "pal", "park", "part", "participant", "particular", "partner", "pass", "passage", "passenger", "passion", "past", "path", "patient", "pattern", "pause", "pay", "peace", "pen", "people", "pepper", "per", "perform", "perhaps", "period", "permanent", "permit", "person", "personal", "phone", "photo", "phrase", "physical", "piano", "pick", "picture", "piece", "pig", "pill", "pilot", "pine", "pink", "place", "plan", "plane", "plant", "plastic", "plate", "play", "player", "please", "pleasure", "plot", "plus", "pocket", "poem", "poet", "point", "police", "policy", "polite", "political", "pond", "pool", "pop", "popular", "population", "port", "position", "positive", "possess", "possible", "post", "pot", "potato", "potential", "pound", "power", "practical", "practice", "pray", "preach", "precise", "predict", "prefer", "prepare", "present", "president", "press", "pretty", "prevent", "price", "pride", "priest", "primary", "prime", "principle", "print", "prior", "priority", "prison", "private", "prize", "problem", "procedure", "process", "produce", "product", "profess", "professional", "professor", "profile", "profit", "program", "progress", "project", "promote", "prompt", "proof", "proper", "property", "prospect", "protect", "proud", "prove", "provide", "public", "publish", "pull", "pulse", "pump", "punish","pure", "purpose", "push", "put", "quality", "quarter", "question", "quiet", "quit", "quite", "quote", "race", "radio", "rail", "rain", "raise", "range", "rate", "rather", "raw", "reach", "read", "ready", "real", "realize", "reason", "recall", "receive", "recent", "recognize", "recommend", "record", "recover", "red", "reduce", "reflect", "reform", "refresh", "refuse", "regard", "region", "register", "regret", "regular", "relate", "relation", "release", "relief", "relieve", "rely", "remain", "remark", "remember", "remind", "remove", "rent", "repair", "repeat", "replace", "reply", "report", "represent", "request", "require", "rescue", "research", "resist", "resolve", "respect", "respond", "rest", "result", "retain", "return", "reveal", "review", "reward", "rhythm", "rice", "rich", "ride", "right", "ring", "rise", "risk", "river", "road", "rob", "rock", "role", "roll", "roof", "room", "root", "rosy", "round", "route", "routine", "row", "rub", "ruin", "rule", "run", "rush", "sad", "safe", "sail", "sale", "salt", "same", "sample", "sand", "satellite", "satisfy", "save", "say", "scale", "scan", "scene", "schedule", "scheme", "school", "science", "scope", "score", "search", "season", "seat", "second", "secret", "section", "see", "seek", "seem", "select", "self", "sell", "send", "senior", "sense", "series", "serious", "servant", "serve", "service", "session", "set", "settle", "seven", "several", "sew", "sex", "shadow", "shake", "shall", "shape", "share", "sharp", "shave", "she", "shed", "shell", "shift", "shine", "ship", "shirt", "shoe", "shoot", "shop", "short", "shot", "should", "shoulder", "shout", "show", "shut", "side", "sight", "sign", "signal", "silent", "silver", "similar", "simple", "since", "sing", "sister", "sit", "site", "situate", "six", "size", "sketch", "skill", "skin", "skirt", "sky", "slate", "sleep", "slide", "slip", "slow", "small", "smart", "smell", "smile", "smoke", "smooth", "snake", "society", "soft", "software", "soil", "soldier", "solid", "solution", "solve", "some", "someone", "something", "sometimes", "son", "song", "soon", "sort", "soul", "sound", "source", "south", "space", "speak", "special", "specify", "speed", "spell", "spend", "sphere", "spirit", "spite", "split", "sport", "spot", "spread", "spring", "square", "stage", "stair", "stake", "stand", "standard", "star", "start", "state", "statement", "station", "stay", "steal", "steel", "step", "stick", "still", "stitch", "stock", "stomach", "stone", "stop", "store", "storm", "story", "straight", "strange", "strategy", "stream", "street", "strength", "stress", "stretch", "strike", "string", "strip", "stroke", "strong", "structure", "struggle", "student", "study", "stuff", "style", "subject", "submit", "substance", "success", "such", "sudden", "suffer", "sugar", "suggest", "summer", "summit", "sun", "super", "supply", "support", "suppose", "sure", "surface", "surprise", "surround", "survey", "suspect", "sustain", "swear", "sweet","swim", "swing", "switch", "sympathetic", "system", "table", "tackle", "tail", "take", "talent", "talk", "tank", "tape", "target", "task", "taste", "tax", "tea", "teach", "team", "tell", "ten", "tenant", "tend", "tennis", "tent", "term", "test", "text", "than", "thank", "that", "the", "theme", "then", "there", "therefore", "these", "they", "thing", "think", "third", "this", "thought", "thousand", "thread", "three", "throat", "through", "throw", "thumb", "thus", "ticket", "tide", "tie", "tiger", "tight", "time", "tin", "tiny", "tip", "tire", "title", "to", "tobacco", "today", "toe", "together", "tomorrow", "tone", "tongue", "tonight", "tool", "tooth", "top", "topic", "total", "touch", "tough", "tour", "tower", "town", "track", "trade", "traffic", "trail", "train", "transfer", "transform", "translate", "transmit", "travel", "treat", "tree", "tremble", "trial", "tribe", "trick", "trip", "trouble", "truck", "true", "trust", "truth", "try", "tube", "tune", "turkey", "turn", "twelve", "twenty", "twice", "two", "type", "typical", "ugly", "uncle", "under", "understand", "undertake", "unhappy", "union", "unit", "unite", "university", "unknown", "unless", "until", "unusual", "up", "upon", "upper", "upset", "use", "used", "user", "usual", "vacant", "vague", "valiant", "value", "valve", "van", "variable", "variation", "various", "vast", "vegetable", "vehicle", "venture", "verbal", "verify", "very", "vessel", "veteran", "vex", "via", "vice", "victim", "victory", "view", "village", "violence", "violent", "violet", "virtual", "virtue", "visible", "vision", "visit", "visual", "vital", "vivid", "voice", "void", "volcanic", "volume", "volunteer", "vote", "vouch", "vowel", "wage", "walk", "wall", "wander", "want", "war", "warm", "warn", "wash", "waste", "watch", "water", "wave", "way", "we", "weak", "wealth", "weapon", "wear", "weather", "web", "week", "weekend", "weird", "welcome", "weld", "well", "west", "wet", "what", "wheel", "when", "where", "which", "while", "white", "who", "whole", "why", "wide", "wife", "wild", "will", "win", "wind", "window", "wine", "wing", "winner", "winter", "wire", "wise", "wish", "with", "within", "without", "witness", "woman", "wonder", "wood", "wooden", "word", "work", "worker", "world", "worship", "worst", "worth", "would", "wound", "wrap", "write", "wrong", "yard", "year", "yell", "yellow", "yes", "yesterday", "yet", "yield", "you", "young", "your", "youth", "zeal", "zero", "zone","account","twenty","rupee","magnet","your"
                    ]
                )
            )

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
        words_input = text.strip().split()
        results = []
        for w in words_input:
            pul, len_in, lez, w_len = self._tor(w)
            avl_w = self._mon(len_in, lez, w_len)
            tel = self._don(pul, len_in, avl_w)
            matches = self._race(tel)
            results.append("/".join(matches))
        return " ".join(results)