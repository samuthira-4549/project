import streamlit as st
import random
import math

# Function to calculate optimal attempts based on binary search concept
def calculate_optimal_attempts(lower, upper):
    return math.ceil(math.log2(upper - lower + 1))

# User Guesses the Number
def user_guesses_game(lower, upper ):
    st.title("Optimal Number Guessing Game")
    st.write("Try to guess the number I'm thinking of in as few attempts as possible!")
    # Validate the range
    if lower >= upper:
        st.error("Invalid range! Ensure the upper bound is greater than the lower bound.")
        return

    # Step 2: Initialize session state variables
    if "target_number" not in st.session_state:
        st.session_state.target_number = random.randint(int(lower), int(upper))
        st.session_state.attempts = 0
        st.session_state.current_lower = int(lower)
        st.session_state.current_upper = int(upper)
        st.session_state.game_over = False

    # Calculate the optimal number of attempts using binary search
    max_attempts = math.ceil(math.log2(st.session_state.current_upper - st.session_state.current_lower + 1))
    st.write(f"Try to guess the number within {max_attempts} attempts!")

    # Step 3: User's guess input
    user_guess = st.number_input("Enter your guess:",
        min_value=st.session_state.current_lower,
        max_value=st.session_state.current_upper
    )

    # Step 4: Button to submit the guess
    if st.button("Submit Guess") and not st.session_state.game_over:
        st.session_state.attempts += 1

        # Check if the guess is correct, too high, or too low
        if user_guess < st.session_state.target_number:
            st.warning("Too low! Try a higher number.")
            st.session_state.current_lower = user_guess + 1  # Narrow down the lower bound
        elif user_guess > st.session_state.target_number:
            st.warning("Too high! Try a lower number.")
            st.session_state.current_upper = user_guess - 1  # Narrow down the upper bound
        else:
            st.success(f"Congratulations! You guessed the number {st.session_state.target_number} in {st.session_state.attempts} attempts.")
            st.balloons()
            st.session_state.game_over = True

    # Display a "Play Again" button once the game is over
    if st.session_state.game_over:
        if st.button("Play Again"):
            del st.session_state.target_number
            del st.session_state.attempts
            del st.session_state.current_lower
            del st.session_state.current_upper
            st.session_state.game_over = False

# Machine Guesses the Number
def machine_guesses_game(lower, upper):
    if "machine_lower" not in st.session_state:
        st.session_state.machine_lower = lower
        st.session_state.machine_upper = upper
        st.session_state.machine_attempts = 0
        st.session_state.optimal_attempts = calculate_optimal_attempts(lower, upper)

    st.write("Think of a number and let me guess it!")
    mid = (st.session_state.machine_lower + st.session_state.machine_upper) // 2
    st.write(f"My guess is: {mid}")

    feedback = st.radio("Is my guess correct?", ("Too low", "Too high", "Correct"))
    if st.button("Submit Feedback"):
        st.session_state.machine_attempts += 1
        if feedback == "Too low":
            st.session_state.machine_lower = mid + 1
        elif feedback == "Too high":
            st.session_state.machine_upper = mid - 1
        else:
            st.write(f"I guessed your number in {st.session_state.machine_attempts} attempts!")
            st.balloons()  # Celebration effect for correct guess
            if st.session_state.machine_attempts <= st.session_state.optimal_attempts:
                st.write("I guessed it within the optimal number of attempts!")
            else:
                st.write(f"Optimal attempts were {st.session_state.optimal_attempts}.")
            st.session_state.machine_lower, st.session_state.machine_upper, st.session_state.machine_attempts = lower, upper, 0  # Reset for next game

# Main Streamlit app
st.title("Guessing Game")
st.write("Choose a mode:")

mode = st.selectbox("Mode", ["User Guesses the Number", "Machine Guesses the Number"])
lower = st.number_input("Choose the lower bound:", value=1)
upper = st.number_input("Choose the upper bound:", value=100)

if mode == "User Guesses the Number":
    user_guesses_game(lower, upper )
else:
    machine_guesses_game(lower,upper)
