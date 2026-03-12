from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

class RoastBot:
    def __init__(self):
        # Context-based roasts for different scenarios
        self.context_dict = {
            "programmer|developer|coder|code": {
                "roasts": [
                    "Your code has more bugs than features.",
                    "You copy-paste from Stack Overflow, that's not programming, that's plagiarism.",
                    "Your debugging method is just praying it works.",
                    "Even AI won't help you write clean code.",
                    "You're the reason 'it works on my machine' exists.",
                    "Your Git history is more tragic than a Shakespearean play.",
                    "You write code like you're being paid by the line—badly.",
                ],
                "keywords": ["program", "code", "debug", "bug", "git", "python", "java", "javascript", "database"]
            },
            "student|lazy|procrastinate": {
                "roasts": [
                    "You're so lazy, sloths file complaints against you.",
                    "Your motivation is lower than your GPA.",
                    "You don't do assignments, you do 'creative interpretations of deadlines.'",
                    "Your productivity graph looks like a dying iPhone battery.",
                    "All-nighters aren't a study method, they're a cry for help.",
                    "You're proof that not everyone deserves a diploma.",
                ],
                "keywords": ["lazy", "procrastinate", "student", "assignment", "homework", "studying", "sleep"]
            },
            "gym|fitness|workout|athlete": {
                "roasts": [
                    "Your gym routine: walk in, check Instagram, walk out.",
                    "You're more committed to excuses than to exercise.",
                    "Your mirror selfies don't count as cardio.",
                    "You talk about gym more than you actually go to the gym.",
                    "Protein shakes aren't a substitute for actually working out.",
                    "Your workout routine is me walking to the fridge.",
                ],
                "keywords": ["gym", "fit", "workout", "exercise", "athlete", "protein", "weight"]
            },
            "relationship|dating|girlfriend|boyfriend|single": {
                "roasts": [
                    "Your relationship status matches your life status: complicated.",
                    "You're single because even your Wi-Fi has better connection than you.",
                    "Your love life: a tragedy in multiple acts.",
                    "You're not single by choice—you're single out of necessity.",
                    "Your dating profile has more red flags than a communist rally.",
                    "Swiping left or right won't fix your personality.",
                ],
                "keywords": ["relationship", "dating", "single", "girlfriend", "boyfriend", "crush", "love"]
            },
            "job|work|career|office|boss": {
                "roasts": [
                    "Your job performance is like your coffee—bitter and disappointing.",
                    "You're the reason HR exists.",
                    "Your career path: sideways and downward.",
                    "You don't work to live, you live to avoid working.",
                    "Your boss hired you out of pity, not competence.",
                    "Your resume is more fiction than your dating profile.",
                    "Even your computer dreads Mondays when you're working.",
                ],
                "keywords": ["job", "work", "boss", "career", "office", "lazy", "fired", "resignation"]
            },
            "money|poor|broke|rich|expensive": {
                "roasts": [
                    "Your bank account is flatter than the Earth according to some people.",
                    "You're not poor, you're 'financially creative.'",
                    "You can't even afford to pay attention.",
                    "Your salary is inversely proportional to your ego.",
                    "You've got champagne taste on a beer budget—actually, water budget.",
                    "Your wallet is like your selfies—empty and sad.",
                ],
                "keywords": ["money", "poor", "broke", "rich", "salary", "credit", "debt"]
            },
            "appearance|ugly|fat|thin|height|bald": {
                "roasts": [
                    "Your appearance is what happens when creation takes a sick day.",
                    "You didn't lose the genetic lottery, you never had a ticket.",
                    "Your face is a cautionary tale for procreation.",
                    "Mirror, mirror on the wall—I'm not telling you anything.",
                    "You're not unattractive, you're just 'uniquely unfortunate.'",
                    "Your selfies need filters, lighting, angles—basically Photoshop 2.0.",
                ],
                "keywords": ["ugly", "fat", "thin", "height", "bald", "appearance", "look", "face"]
            },
            "stupid|dumb|smart|intelligence": {
                "roasts": [
                    "Your IQ and your age have a lot in common—both disappointingly low.",
                    "You're not dumb, you're just 'creatively unintelligent.'",
                    "If brains were dynamite, you couldn't blow your nose.",
                    "You're proof that evolution can go in reverse.",
                    "Your intelligence level is a mystery wrapped in an enigma wrapped in stupidity.",
                ],
                "keywords": ["dumb", "stupid", "smart", "intelligence", "idiot", "genius"]
            },
        }
    
    def get_context(self, prompt: str) -> list:
        """Extract context from the prompt to generate relevant roasts."""
        prompt_lower = prompt.lower()
        matched_roasts = []
        
        # Check for context matches
        for context, data in self.context_dict.items():
            context_words = context.split("|")
            if any(word in prompt_lower for word in context_words):
                matched_roasts.extend(data["roasts"])
        
        return matched_roasts
    
    def generate_roast(self, prompt: str) -> str:
        """Generate a roast based on user prompt."""
        if not prompt.strip():
            return "Even your prompt was too lazy to be complete."
        
        # Get context-based roasts
        context_roasts = self.get_context(prompt)
        
        if context_roasts:
            roast = random.choice(context_roasts)
        else:
            # Generic roasts for general prompts
            generic = [
                "Your prompt description is vaguer than your life direction.",
                "You're asking me to roast someone, but I'm already roasting you for this effort.",
                "That description is so vague, even a psychic would give up.",
                "Your request is about as clear as your future looks.",
                "I've seen better descriptions on a dating app for bots.",
                "Your prompt is like your plans—absolutely nowhere.",
            ]
            roast = random.choice(generic)
        
        return f"🔥 {roast}"
    
    def roast_user(self, prompt: str) -> str:
        """Generate a roast about the user themselves."""
        user_roasts = [
            "You're the type of person who needs a roast bot. Think about that.",
            "You came here to roast others, but honey, you should be worried about yourself.",
            "At least you're self-aware enough to know others need roasting. Still says a lot about you.",
            "You're so bored you're using a roast bot. Your life must be fascinating.",
            "The fact that you're here means you've got a LOT of free time.",
            "You care about roasting others more than your own life? That's actually concerning.",
            "You're using a roast bot instead of improving yourself. Make better choices.",
            "I can't decide what's sadder—that you use this, or that you'll probably use it again.",
            "Your typing speed is the only impressive thing about this interaction.",
            "You came here for entertainment? Your life must be a real bore.",
            "At least you have the courage to admit people deserve roasting. Growth!",
            "Using a roast bot makes you either hilarious or friendless. I'll let you figure out which.",
            "You're spending your time on this instead of doing literally anything productive.",
            "The irony is that you came here to roast others, but you're the real comedy.",
            "Your dedication to roasting strangers is honestly kind of commitment. Weird, but impressive.",
        ]
        return f"🔥 {random.choice(user_roasts)}"

# Initialize roast bot
bot = RoastBot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/roast', methods=['POST'])
def roast():
    data = request.json
    prompt = data.get('prompt', '').strip()
    
    if not prompt:
        return jsonify({'error': 'Please enter a description!'}), 400
    
    roast_target = bot.generate_roast(prompt)
    roast_user = bot.roast_user(prompt)
    
    return jsonify({
        'roast_target': roast_target,
        'roast_user': roast_user
    })

if __name__ == '__main__':
    app.run(debug=True)
