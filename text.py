# --- 1. THE "OLD WAY" (STANDARD CLASS) ---
# This requires "Boilerplate": manual work to set up the object's brain and voice.
class ChessGame_Original:
    # The __init__ method is the "Constructor." 
    # Without @dataclass, you must manually map every input to 'self'.
    def __init__(self, player_white, player_black, rating_diff, is_rated=True):
        self.player_white = player_white
        self.player_black = player_black
        self.rating_diff = rating_diff
        self.is_rated = is_rated

    # The __repr__ (Representation) tells Python how to print the object.
    # Without this, printing game1 would just show a memory address like <__main__.Object at 0x123>.
    def __repr__(self):
        return (f"ChessGame(player_white={self.player_white!r}, "
                f"player_black={self.player_black!r}, "
                f"rating_diff={self.rating_diff}, "
                f"is_rated={self.is_rated})")

game1 = ChessGame_Original("Kian", "Magnus", 400)
print(game1)

print("="*50)

# --- 2. THE "CLEAN WAY" (DATACLASS) ---
from dataclasses import dataclass

# The @dataclass decorator automatically writes __init__ and __repr__ for us.
@dataclass
class ChessGame:
    # We use Type Hints here, but they are "suggestions," not enforced laws.
    player_white: str
    player_black: str
    rating_diff: int
    is_rated: bool = True  # Default value

game2 = ChessGame("Kian", "Hikaru", 350)
print(game2)

print("="*50)

# --- 3. THE "LOOSE TYPING" CAVEAT ---
@dataclass
class myTest:
    breakfast : str
    lunch : str
    calories : int

# WARNING: Standard Python is "Dynamically Typed." 
# Even though we hinted 'int' for calories, passing the string 'f' works 
# because Python doesn't check types at runtime. This can lead to bugs in math!
myOutout = myTest('a','b','f')
print(myOutout)

print("="*50)

# --- 4. THE "SAFE WAY" (PYDANTIC BASEMODEL) ---
from pydantic import BaseModel, ValidationError

# Pydantic is for "Data Validation." It treats Type Hints as "Enforced Rules."
class MyTestBase(BaseModel):
    breakfast: str
    lunch: str
    calories: int

# In 2026/Pydantic v2+, passing positional arguments ('a', 'b', 'f') is allowed,
# but Pydantic will now trigger a ValidationError because 'f' cannot be an integer.
try:
    # This will try to convert 'f' to an int, fail, and throw an error.
    myOutoutBase = MyTestBase(breakfast='a', lunch='b', calories='f')
    print(myOutoutBase)
except ValidationError as e:
    print("Pydantic stopped the 'bad' data from entering the system!")
    # print(e) # Uncomment to see the detailed error report